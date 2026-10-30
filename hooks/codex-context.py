#!/usr/bin/env python3
"""Codex 훅 — Claude Code 세션이 받는 프로젝트 맥락을 Codex 세션에도 똑같이 넣는다(export.py가 ~/.codex/hooks.json에 건다).

SessionStart: 프로젝트 NEXT.md의 NEXT-ACTION 블록(Claude 쪽 session-start.sh와 같은 블록).
UserPromptSubmit: 프로젝트 `.claude/settings.json`의 UserPromptSubmit 명령(볼트·그래프 질의 훅 등)을 같은 입력으로 돌린 출력.
Codex 훅 입력은 Claude와 같은 이름(prompt·cwd·hook_event_name)이라 프로젝트 훅을 고치지 않고 그대로 쓴다.
훅이 실패해도 Codex 작업은 막지 않는다 — 맥락만 빠진다(stderr에 한 줄)."""
import json
import os
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


def main() -> None:
    payload = json.load(sys.stdin)
    root = project_root(Path(payload.get("cwd") or os.getcwd()).resolve())
    event = payload.get("hook_event_name", "")
    text = next_block(root) if event == "SessionStart" else prompt_hooks(root, payload) if event == "UserPromptSubmit" else ""
    if text:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
