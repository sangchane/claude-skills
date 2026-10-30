#!/usr/bin/env python3
"""Claude가 일을 Codex에 나눠 맡길 때 쓰는 실행기 — 일 종류로 모델·reasoning effort를 고르고 `codex exec`로 넘긴다.

  python3 <dev>/tools/codex_run.py --kind build -C <저장소> -o <결과.md> <지시문 파일>
  종류(서브에이전트 모델 고르기와 같은 기준, rules.md 「모델·effort·위임」):
    bulk     기계적 대량(이름 바꾸기·문구 일괄)      → 빠른 모델 · low
    survey   패턴 반복·조사·문서 정리              → 주력 모델 · medium
    build    기능 하나 구현(M)                    → 주력 모델 · high
    judge    판단 집약(역분석·불변식·보안·설계, L)  → 최상위 모델 · high
    research 원인 불명·장기 조사                   → 최상위 모델 · xhigh
모델 이름은 Codex가 받아 둔 목록(~/.codex/models_cache.json)의 설명으로 고른다 — 새 모델이 나와도 이 파일을 안 고쳐도 된다.
--model·--effort로 직접 줄 수 있다. 맥락(NEXT 블록 + Claude 메모리 목록 + 지시문으로 돌린 프로젝트 질문 훅 + --query로 찾은 그래프 노드)은 이 실행기가
지시문 앞에 직접 붙인다 — Codex 훅(hooks/codex-context.py)은 사용자가 /hooks로 승인해야 돌아서(명령 해시 신뢰), 승인 전에도 같은 맥락이 가게.
지시문은 표준 입력(-)으로 주고 닫는다 — 열어 두면 「Reading additional input from stdin」에서 멈추고(2026-10-26), 윈도우 codex.cmd는 인자의 |·줄바꿈을 깬다(2026-10-30)."""
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

KINDS = {  # 종류 → (모델 설명에서 찾을 말, effort)
    "bulk": ("Fast and affordable", "low"),
    "survey": ("Latest workhorse", "medium"),
    "build": ("Latest workhorse", "high"),
    "judge": ("Frontier", "high"),
    "research": ("Frontier", "xhigh"),
}
ORDER = ["low", "medium", "high", "xhigh", "max", "ultra"]
CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
PREAMBLE = """[Claude가 나눠 맡긴 일 — Claude Code 세션과 같은 조건으로 한다]
- 이 저장소의 AGENTS.md(네비게이션·규약·검증 게이트)를 먼저 따른다. 근거·구조는 grep으로 헤매기 전에 AGENTS.md에 적힌 볼트 인덱스·질의 도구·그래프부터 본다.
- 아래 「맥락」은 Claude 세션이 받는 것과 같은 NEXT 블록과 이 요청에 걸린 볼트·그래프 노트다. 그 노트부터 본다.
- 끝나면 한국어로 보고한다: 한 일 · 바꾼 파일 · 검증 명령과 결과 줄 · 못 한 것.

"""


def context(cd: str, text: str, query: str) -> str:
    """Codex 훅과 같은 함수로 NEXT 블록 + Claude 메모리 목록 + 프로젝트 질문 훅 출력 + 그래프 질의(query)"""
    spec = importlib.util.spec_from_file_location("codex_context", Path(__file__).resolve().parent.parent / "hooks" / "codex-context.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    root = mod.project_root(Path(cd).resolve())
    parts = [mod.next_block(root), mod.memory_index(root),
             mod.prompt_hooks(root, {"prompt": text, "cwd": str(root), "hook_event_name": "UserPromptSubmit"}), mod.graph_hits(root, query)]
    return "## 맥락\n" + "\n\n".join(p for p in parts if p) + "\n\n## 할 일\n" if any(parts) else ""


def pick_model(kind: str) -> tuple[str | None, list[str]]:
    """(모델 이름, 그 모델이 받는 effort 목록) — 목록 파일이 없거나 맞는 설명이 없으면 (None, []) = Codex 기본 모델"""
    try:
        models = json.loads((CODEX_HOME / "models_cache.json").read_text(encoding="utf-8"))["models"]
    except (OSError, ValueError, KeyError):
        return None, []
    want = KINDS[kind][0]
    for m in models:
        desc = m.get("description") or ""
        if want in desc and "Older" not in desc:
            return m["slug"], [lv["effort"] for lv in m.get("supported_reasoning_levels", [])]
    return None, []


def fit_effort(effort: str, supported: list[str]) -> str:
    """모델이 못 받는 단계면 받는 것 중 가장 가까운 아래 단계(없으면 가장 낮은 것)"""
    if not supported or effort in supported:
        return effort
    lower = [e for e in supported if e in ORDER and ORDER.index(e) <= ORDER.index(effort)]
    return max(lower, key=ORDER.index) if lower else supported[0]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--kind", choices=KINDS, required=True)
    ap.add_argument("--model")
    ap.add_argument("--effort", choices=ORDER)
    ap.add_argument("-C", "--cd", required=True, help="Codex가 일할 저장소")
    ap.add_argument("-o", "--out", required=True, help="Codex 마지막 답을 쓸 파일")
    ap.add_argument("prompt", help="지시문 파일(- 이면 표준 입력)")
    ap.add_argument("--query", help="그래프에서 먼저 찾을 질문(없으면 지시문 첫 줄)")
    ap.add_argument("--dry-run", action="store_true", help="고른 모델·명령과 붙일 맥락을 보이고 돌리지 않음")
    a = ap.parse_args()
    text = sys.stdin.read() if a.prompt == "-" else Path(a.prompt).read_text(encoding="utf-8")
    ctx = context(a.cd, text, a.query or next((l.strip("#- ") for l in text.splitlines() if l.strip("#- ")), ""))
    model, supported = (a.model, []) if a.model else pick_model(a.kind)
    effort = fit_effort(a.effort or KINDS[a.kind][1], supported)
    # 윈도우는 codex가 npm 껍데기 codex.cmd라 이름만으론 못 찾고(WinError 2), cmd.exe가 인자의 |·줄바꿈을 깬다 — 실행 파일은 which로, 지시문은 표준 입력(-)으로(2026-10-30)
    cmd = [shutil.which("codex") or "codex", "exec", "-C", a.cd, "-o", a.out, "-c", f'model_reasoning_effort="{effort}"', *(["-m", model] if model else []), "-"]
    print(json.dumps({"kind": a.kind, "model": model or "(Codex 기본)", "effort": effort, "cd": a.cd, "out": a.out}, ensure_ascii=False), flush=True)
    if a.dry_run:
        print(ctx)
        return 0
    return subprocess.run(cmd, input=PREAMBLE + ctx + text, text=True, encoding="utf-8", env={**os.environ, "DEV_CONTEXT_INLINE": "1"}).returncode   # 입력을 다 주고 닫으니 「Reading additional input from stdin」에서 멈추지 않는다


if __name__ == "__main__":
    assert fit_effort("xhigh", ["low", "medium", "high"]) == "high" and fit_effort("low", ["medium", "high"]) == "medium"
    sys.exit(main())
