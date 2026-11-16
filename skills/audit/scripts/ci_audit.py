#!/usr/bin/env python3
"""CI 감사 — 최근 실행 N번의 작업(job)마다 시간을 대기·셋업·실행으로 나눠 가장 느린 작업을 보고한다. 읽기만 한다.

  python3 -I ci_audit.py [--repo owner/name] [--limit 150] [--top 5]

나누는 법 (GitHub Actions jobs API 의 시각으로 셈, 초)
  대기 = job.started_at - job.created_at          (기계 할당을 기다린 시간)
  셋업 = 이름이 SETUP 에 맞는 단계들의 합         (체크아웃·도구 설치·의존성 설치·캐시 복원, 끝 정리 Post·Complete job 포함)
  실행 = (job.completed_at - job.started_at) - 셋업
"""
import argparse
import json
import re
import statistics
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# shortcut: 단계 이름으로 셋업을 가른다 — 이름이 특이한 준비 단계는 실행으로 잡힌다. 틀리면 이 식에 이름을 더한다.
SETUP = re.compile(
    r"(?i)^(set up job|complete job|post |run actions/(checkout|setup-|cache|download-artifact)|checkout|"
    r"(set ?up|install|restore|cache|download|clone)\b|.*\b(npm ci|pnpm install|yarn install|pip install|uv sync|poetry install|"
    r"bundle install|go mod download|cargo fetch|deno install|apt-get install)\b)"
)


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def secs(a, b):
    return max(0.0, (ts(b) - ts(a)).total_seconds()) if a and b else 0.0


def breakdown(job):
    """job 하나 → {대기, 셋업, 실행, 합계} 초. 끝나지 않았거나 건너뛴 job 은 None."""
    if not job.get("started_at") or not job.get("completed_at") or job.get("conclusion") == "skipped":
        return None
    queue = secs(job.get("created_at") or job["started_at"], job["started_at"])
    run = secs(job["started_at"], job["completed_at"])
    setup = sum(secs(s.get("started_at"), s.get("completed_at")) for s in job.get("steps") or [] if SETUP.match(s.get("name", "")))
    setup = min(setup, run)
    return {"queue": queue, "setup": setup, "exec": run - setup, "total": queue + run}


def summarize(jobs, top):
    """[(작업 이름, job)] → 합계 중앙값이 큰 순 top 개 행."""
    groups = {}
    for name, job in jobs:
        b = breakdown(job)
        if b:
            groups.setdefault(name, []).append(b)
    rows = []
    for name, bs in groups.items():
        med = {k: statistics.median(b[k] for b in bs) for k in ("queue", "setup", "exec", "total")}
        rows.append({"name": name, "n": len(bs), **med, "max_total": max(b["total"] for b in bs)})
    return sorted(rows, key=lambda r: r["total"], reverse=True)[:top]


def gh(*args):
    out = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=120)
    if out.returncode:
        sys.exit(f"gh {' '.join(args[:3])} 실패: {out.stderr.strip()[:300]}")
    return out.stdout


def fetch(repo, limit):
    runs = json.loads(gh("run", "list", "-R", repo, "-L", str(limit), "--json", "databaseId,workflowName,status"))
    runs = [r for r in runs if r["status"] == "completed"]

    def jobs_of(r):
        pages = gh("api", "--paginate", f"repos/{repo}/actions/runs/{r['databaseId']}/jobs?per_page=100", "--jq", ".jobs[]")
        return [(f"{r['workflowName']} / {j['name']}", j) for j in map(json.loads, filter(None, pages.splitlines()))]

    with ThreadPoolExecutor(8) as pool:
        return len(runs), [j for js in pool.map(jobs_of, runs) for j in js]


def table(rows):
    lines = ["| 작업 | 횟수 | 대기 | 셋업 | 실행 | 합계 | 가장 느린 한 번 |", "|---|---:|---:|---:|---:|---:|---:|"]
    lines += [f"| {r['name']} | {r['n']} | {r['queue']:.0f} | {r['setup']:.0f} | {r['exec']:.0f} | {r['total']:.0f} | {r['max_total']:.0f} |" for r in rows]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", help="owner/name (없으면 지금 폴더의 gh 저장소)")
    ap.add_argument("--limit", type=int, default=150)
    ap.add_argument("--top", type=int, default=5)
    a = ap.parse_args()
    repo = a.repo or gh("repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner").strip()
    n_runs, jobs = fetch(repo, a.limit)
    rows = summarize(jobs, a.top)
    print(f"# CI 감사 — {repo}\n\n끝난 실행 {n_runs}번 · job {len(jobs)}개. 값은 작업마다 중앙값(초).\n")
    print(table(rows) if rows else "끝난 job 이 없습니다.")


if __name__ == "__main__":
    main()
