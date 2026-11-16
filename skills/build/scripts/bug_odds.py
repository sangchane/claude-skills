#!/usr/bin/env python3
"""버그 유입 확률 재기 — 코드에 작은 실수(변이)를 하나씩 넣고 시험이 잡는지 센다. 놓친 비율 = 이 코드에 실수가 들어와도 시험이 통과시킬 확률의 대리값.

  python3 -I bug_odds.py --file src/x.ts --test "deno test src/" [--lines 10-80] [--max 60] [--target 10]

- 시험 명령은 원본에서 먼저 통과해야 한다(아니면 멈춤).
- 파일은 끝나면 원래 바이트로 되돌린다(중단·오류에도). 놓친 변이는 줄 번호와 함께 찍는다.
- 종료 코드: 놓친 비율 <= --target % 면 0, 넘으면 1, 준비 실패 2.
"""
import argparse
import atexit
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

# (찾을 식, 바꿀 글) — 공백으로 둘러싼 이항 연산만 바꿔 제네릭·화살표·증감을 피한다.
# shortcut: 글자 단위 변이라 형 검사에서 깨지는 변이도 「잡음」으로 센다. 점수가 의심스러우면 Stryker·mutmut 같은 도구로 올린다.
OPS = [
    (r" === ", " !== "), (r" !== ", " === "), (r" == ", " != "), (r" != ", " == "),
    (r" <= ", " > "), (r" >= ", " < "), (r" < ", " >= "), (r" > ", " <= "),
    (r" && ", " || "), (r" \|\| ", " && "), (r" and ", " or "), (r" or ", " and "),
    (r" \+ ", " - "), (r" - ", " + "), (r" \* ", " / "),
    (r"\btrue\b", "false"), (r"\bfalse\b", "true"), (r"\bTrue\b", "False"), (r"\bFalse\b", "True"),
    (r"(?<![\w.])(\d+)(?![\w.])", None),  # 정수 n → n+1
]
COMMENT = re.compile(r"^\s*(#|//|/\*|\*)")


def in_string(line, i):
    return any(line[:i].count(q) % 2 for q in "\"'`")


def mutants(text, lines=None):
    """[(줄 번호, 원래 줄, 바꾼 줄)] — 한 변이에 한 곳만 바꾼다."""
    out = []
    for n, line in enumerate(text.split("\n"), 1):
        if (lines and not lines[0] <= n <= lines[1]) or COMMENT.match(line):
            continue
        for pat, rep in OPS:
            for m in re.finditer(pat, line):
                if in_string(line, m.start()):
                    continue
                new = str(int(m.group(1)) + 1) if rep is None else rep
                out.append((n, line, line[:m.start()] + new + line[m.end():]))
    return out


def sample(items, k):
    if len(items) <= k:
        return items
    step = len(items) / k
    return [items[int(i * step)] for i in range(k)]


def passes(cmd, timeout):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, timeout=timeout).returncode == 0
    except subprocess.TimeoutExpired:
        return False  # 무한 반복 변이는 잡은 것으로 본다


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--test", required=True, help="시험 명령 (셸로 돈다)")
    ap.add_argument("--lines", help="시작-끝 줄 (바꿀 코드만 잴 때)")
    ap.add_argument("--max", type=int, default=60, help="변이 수 상한 (고르게 뽑음)")
    ap.add_argument("--target", type=float, default=10.0, help="놓친 비율 목표 %%")
    a = ap.parse_args()

    path = Path(a.file)
    original = path.read_bytes()
    restore = lambda *_: path.write_bytes(original)  # noqa: E731
    atexit.register(restore)
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: sys.exit(130))

    t0 = time.monotonic()
    if not passes(a.test, None):
        print("원본에서 시험이 실패합니다 — 먼저 시험을 통과시키세요.")
        return 2
    timeout = max(10.0, (time.monotonic() - t0) * 3)

    rng = tuple(map(int, a.lines.split("-"))) if a.lines else None
    text = original.decode("utf-8")
    picked = sample(mutants(text, rng), a.max)
    if not picked:
        print("바꿀 곳이 없습니다.")
        return 2
    rows = text.split("\n")
    survived = []
    for n, old, new in picked:
        path.write_text("\n".join(rows[: n - 1] + [new] + rows[n:]), encoding="utf-8")
        if passes(a.test, timeout):
            survived.append((n, old.strip(), new.strip()))
        restore()

    pct = 100 * len(survived) / len(picked)
    print(f"변이 {len(picked)}개 · 잡음 {len(picked) - len(survived)} · 놓침 {len(survived)} → 놓친 비율 {pct:.1f}% (목표 {a.target:g}% 이하)")
    for n, old, new in survived:
        print(f"  놓침 {path}:{n}  {old}  →  {new}")
    return 0 if pct <= a.target else 1


if __name__ == "__main__":
    sys.exit(main())
