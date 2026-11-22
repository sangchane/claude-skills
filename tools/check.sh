#!/usr/bin/env bash
# 이 저장소의 자체 시험 한 묶음 — 커밋 훅(tools/git-hooks/pre-commit)과 GitHub CI(.github/workflows/check.yml)가 같은 것을 돈다.
set -e
cd "$(dirname "$0")/.."
bash hooks/test-session-start.sh </dev/null
bash hooks/test-verify-gate.sh </dev/null
bash hooks/test-rtk.sh </dev/null
python3 -I skills/audit/scripts/test_ci_audit.py
python3 -I skills/build/scripts/test_bug_odds.py
python3 -I tools/test_leftovers.py
echo "check ok"
