#!/usr/bin/env python3
"""정비 문체 준수율 재기 — 이 PC 의 Claude Code 대화 기록(~/.claude/projects/*/*.jsonl)에서 턴마다 끝 보고를 뽑아
hooks/ste_check.py 와 같은 검사로 주마다 센다. 기록은 읽기만 하고 밖으로 보내지 않는다.
  python3 -I tools/ste_measure.py [--since 2026-10-26]
2026-11-22 기준선(10-26~11-22, 300자 넘는 끝 보고 805개): 1항 지킴 32% · 모든 항목 통과 23%."""
import argparse
import collections
import glob
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hooks"))
from ste_check import MIN_CHARS, plain, problems  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    _s.reconfigure(encoding="utf-8", errors="replace")


def text_of(m):
    c = m.get("message", {}).get("content")
    if isinstance(c, str):
        return c
    return "\n".join(b.get("text", "") for b in c or [] if isinstance(b, dict) and b.get("type") == "text")


def user_turn(m):
    """사용자가 친 말(도구 결과·명령 출력·메타 줄은 뺀다)."""
    if m.get("type") != "user" or m.get("isMeta"):
        return False
    c = m.get("message", {}).get("content")
    if isinstance(c, str):
        return not c.startswith("<")
    return any(isinstance(b, dict) and b.get("type") == "text" and not b.get("text", "").startswith("<") for b in c or [])


def finals(since):
    """턴마다 마지막 답 (날짜, 글)."""
    out = []
    for f in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
        last = None
        try:
            lines = [json.loads(l) for l in open(f, encoding="utf-8") if l.strip()]
        except (OSError, ValueError):
            continue
        for m in lines:
            if m.get("isSidechain"):
                continue
            if user_turn(m):
                if last:
                    out.append(last)
                last = None
            elif m.get("type") == "assistant" and text_of(m).strip():
                last = (m.get("timestamp", "")[:10], text_of(m))
        if last:
            out.append(last)
    return [x for x in out if x[0] >= since and len(plain(x[1]).strip()) >= MIN_CHARS]


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--since", default="2026-10-26")
    o = a.parse_args()
    weeks = collections.defaultdict(lambda: collections.Counter())
    for day, text in finals(o.since):
        wk = weeks[day[:8] + ("1" if day[8:] < "08" else "2" if day[8:] < "15" else "3" if day[8:] < "22" else "4")]
        found = {p.split(":")[0].split(" ")[0] for p in problems(text)}
        wk["답"] += 1
        wk["통과"] += not found
        for k in ("1항", "3항", "8항", "9항", "화살표"):
            wk[k] += k in found
    print("주(월-n째)   끝 보고  모두 통과  1항 지킴  화살표  8항 약어  9항 문단  3항 긴 문장")
    for w in sorted(weeks):
        c = weeks[w]
        n = c["답"]
        pct = lambda k: f"{100 * c[k] // n:3d}%"  # noqa: E731
        print(f"{w:10s} {n:7d}  {100 * c['통과'] // n:7d}%  {100 * (n - c['1항']) // n:6d}%  {pct('화살표'):>6s}  {pct('8항'):>7s}  {pct('9항'):>7s}  {pct('3항'):>9s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
