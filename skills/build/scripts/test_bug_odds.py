#!/usr/bin/env python3
"""bug_odds.py 자체 시험 — 약한 시험은 놓침이 나오고 목표를 넘어 1, 강한 시험은 0, 파일은 원래대로.  python3 -I scripts/test_bug_odds.py"""
import subprocess
import sys
import tempfile
from pathlib import Path

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
from bug_odds import mutants  # noqa: E402

# 문자열·주석 안은 바꾸지 않는다
assert mutants('# a == b\ns = "x == y"\n') == []
assert [m[2] for m in mutants("if a == b and c < 2:")] == ["if a != b and c < 2:", "if a == b and c >= 2:", "if a == b or c < 2:", "if a == b and c < 3:"]

d = Path(tempfile.mkdtemp())
src = "def f(a, b):\n    if a > 0:\n        return a + b\n    return 0\n"
(d / "m.py").write_text(src)
(d / "weak.py").write_text("import m\nassert m.f(1, 2) == 3\n")
(d / "strong.py").write_text("import m\nassert m.f(1, 2) == 3\nassert m.f(0, 5) == 0\nassert m.f(-1, 5) == 0\nassert m.f(1, 0) == 1\n")


def run(test):
    return subprocess.run([sys.executable, "-I", str(here / "bug_odds.py"), "--file", str(d / "m.py"),
                           # cd 없이 시험 파일 경로로 — Windows cmd 의 cd 는 다른 드라이브(임시 폴더 C:, 저장소 D:)로 옮기지 못한다.
                           "--test", f'"{sys.executable}" -B "{d / test}"', "--target", "0"], capture_output=True, text=True, encoding="utf-8")


weak = run("weak.py")
assert weak.returncode == 1 and "놓침" in weak.stdout, weak.stdout + weak.stderr
assert (d / "m.py").read_text() == src
strong = run("strong.py")
assert strong.returncode == 0 and "놓친 비율 0.0%" in strong.stdout, strong.stdout + strong.stderr
assert (d / "m.py").read_text() == src
print("ok bug_odds")
