#!/usr/bin/env python3
"""ci_audit.py 자체 시험 — gh 없이 가짜 job 으로 나누기·정렬을 본다.  python3 -I scripts/test_ci_audit.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ci_audit import SETUP, breakdown, summarize  # noqa: E402


def step(name, a, b):
    return {"name": name, "started_at": f"2026-01-01T00:{a}Z", "completed_at": f"2026-01-01T00:{b}Z"}


job = {
    "created_at": "2026-01-01T00:00:00Z", "started_at": "2026-01-01T00:00:30Z", "completed_at": "2026-01-01T00:05:30Z",
    "conclusion": "success",
    "steps": [step("Set up job", "00:30", "00:35"), step("Run actions/checkout@v4", "00:35", "00:45"),
              step("Install deps", "00:45", "01:45"), step("Run tests", "01:45", "05:25"), step("Post Run actions/checkout@v4", "05:25", "05:30")],
}
b = breakdown(job)
assert b == {"queue": 30, "setup": 80, "exec": 220, "total": 330}, b
assert all(SETUP.match(n) for n in ["Clone repository", "Set up Deno", "Post Set up Deno", "Complete job", "Run npm ci"])
assert not any(SETUP.match(n) for n in ["Run tests", "Lint", "Build"])
assert breakdown({**job, "conclusion": "skipped"}) is None
assert breakdown({**job, "completed_at": None}) is None

fast = {**job, "completed_at": "2026-01-01T00:01:30Z", "steps": []}
rows = summarize([("ci / test", job), ("ci / test", job), ("ci / lint", fast)], top=5)
assert [r["name"] for r in rows] == ["ci / test", "ci / lint"], rows
assert rows[0]["n"] == 2 and rows[1]["setup"] == 0 and rows[1]["exec"] == 60, rows
assert len(summarize([("a", job), ("b", fast)], top=1)) == 1
print("ok ci_audit")
