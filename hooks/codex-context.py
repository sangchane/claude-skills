#!/usr/bin/env python3
"""Codex 훅 — Claude Code 세션이 받는 프로젝트 맥락을 Codex 세션에도 똑같이 넣는다(export.py가 ~/.codex/hooks.json에 건다).

SessionStart: 프로젝트 NEXT.md의 NEXT-ACTION 블록(Claude 쪽 session-start.sh와 같은 블록) + Claude 자동 메모리 목록(MEMORY.md).
UserPromptSubmit 끝에 graphify-out/graph.json이 있으면 질문으로 graphify query 결과도(Claude가 근거를 찾을 때 처음 하는 일).
UserPromptSubmit: 프로젝트 `.claude/settings.json`의 UserPromptSubmit 명령(볼트·그래프 질의 훅 등)을 같은 입력으로 돌린 출력.
Codex 훅 입력은 Claude와 같은 이름(prompt·cwd·hook_event_name)이라 프로젝트 훅을 고치지 않고 그대로 쓴다.
훅이 실패해도 Codex 작업은 막지 않는다 — 맥락만 빠진다(stderr에 한 줄)."""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

LIMIT = 9000  # Claude 훅 출력 한도(10,000자) 안 — 두 도구가 같은 양을 받게


def project_root(cwd: Path) -> Path:
    for d in (cwd, *cwd.parents):
        if (d / ".git").exists():
            return d
    return cwd


def next_block(root: Path) -> str:
    for rel in ("NEXT.md", "coordination/NEXT.md"):
        f = root / rel
        if f.is_file():
            t = f.read_text(encoding="utf-8")
            a, b = t.find("<!-- NEXT-ACTION:START -->"), t.find("<!-- NEXT-ACTION:END -->")
            if a >= 0 and b > a:
                block = t[a:b]
                return f"## 현재 작업 ({rel})\n" + (block if len(block) <= LIMIT else block[:LIMIT] + f"\n> 잘림 — 나머지는 {rel}을 읽는다.")
    return ""


def prompt_hooks(root: Path, payload: dict) -> str:
    try:
        cfg = json.loads((root / ".claude" / "settings.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    out = []
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(root)}
    for group in cfg.get("hooks", {}).get("UserPromptSubmit", []):
        for h in group.get("hooks", []):
            if h.get("type") != "command":
                continue
            try:
                p = subprocess.run(h["command"], shell=True, input=json.dumps(payload, ensure_ascii=False), capture_output=True,
                                   text=True, timeout=h.get("timeout", 10), cwd=root, env=env)
            except subprocess.TimeoutExpired:
                print(f"codex-context: 프로젝트 훅 시간 초과 {h['command']}", file=sys.stderr)
                continue
            if p.returncode == 0 and p.stdout.strip():
                out.append(p.stdout.strip())
            elif p.returncode:
                print(f"codex-context: 프로젝트 훅 실패 {p.returncode} {p.stderr.strip()[-200:]}", file=sys.stderr)
    return "\n".join(out)[:LIMIT]


def memory_index(root: Path) -> str:
    """Claude 자동 메모리 목록(사용자 지적·선호) — Claude는 세션마다 이걸 받는다. 폴더 이름 = 프로젝트 경로의 영숫자 아닌 글자를 '-'로"""
    d = Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(root)) / "memory"
    f = d / "MEMORY.md"
    if not f.is_file():
        return ""
    return f"## 사용자 메모리 (Claude와 같은 목록 — 각 줄의 파일은 {d} 에 있다, 해당하면 읽는다)\n" + f.read_text(encoding="utf-8")[:LIMIT]


def graph_hits(root: Path, question: str) -> str:
    """볼트를 그래프로 정리한 프로젝트면 할 일 문장으로 그래프를 먼저 찾아 붙인다 — Claude가 근거를 찾을 때 처음 하는 일(rules.md 「문서 지도」)"""
    exe, q = shutil.which("graphify"), " ".join(question.split())[:200]
    if not exe or not q or not (root / "graphify-out" / "graph.json").is_file():
        return ""
    try:
        p = subprocess.run([exe, "query", q, "--budget", "1500"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=45, cwd=root,
                           env={**os.environ, "PYTHONUTF8": "1"})   # 훅 시간 제한(60초) 안 · 윈도우 cp949 출력이 깨지지 않게
    except subprocess.TimeoutExpired:
        print("codex-context: graphify query 시간 초과", file=sys.stderr)
        return ""
    return f"## 그래프에서 먼저 찾은 노드 (graphify query \"{q[:80]}\")\n" + p.stdout.strip()[:LIMIT] if p.returncode == 0 and p.stdout.strip() else ""


def main() -> None:
    sys.stdin.reconfigure(encoding="utf-8"); sys.stdout.reconfigure(encoding="utf-8")   # 윈도우 파이프 기본은 cp949 — Codex가 주는 UTF-8 질문·한글 맥락이 깨진다
    if os.environ.get("DEV_CONTEXT_INLINE"):   # codex_run.py가 같은 맥락을 지시문 앞에 이미 붙였다 — 훅이 또 붙이면 두 벌
        return
    payload = json.load(sys.stdin)
    root = project_root(Path(payload.get("cwd") or os.getcwd()).resolve())
    event = payload.get("hook_event_name", "")
    parts = [next_block(root), memory_index(root)] if event == "SessionStart" else \
        [prompt_hooks(root, payload), graph_hits(root, payload.get("prompt", ""))] if event == "UserPromptSubmit" else []
    text = "\n\n".join(p for p in parts if p)
    if text:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
