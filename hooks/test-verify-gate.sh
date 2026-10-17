#!/usr/bin/env bash
# verify-gate.sh 자체 시험 — 임시 git 저장소에서 다섯 경우.  bash hooks/test-verify-gate.sh
set -u
here="$(cd "$(dirname "$0")" && pwd)"
t="$(mktemp -d)"; cd "$t" && git init -q && touch x && git add x && git -c user.name=t -c user.email=t@t commit -qm init
next() { printf '<!-- NEXT-ACTION:START -->\n- 등급: %s · 단계: ④ BUILD\n<!-- NEXT-ACTION:END -->\n' "$1" > NEXT.md; }
run() { printf '{"session_id":"t%s","stop_hook_active":%s,"cwd":"%s"}' "$1" "$2" "$t" | CLAUDE_PROJECT_DIR="$t" bash "$here/verify-gate.sh" >out 2>err; echo $?; }
ok=0; check() { if [ "$2" = "$3" ]; then ok=$((ok + 1)); else echo "실패: $1 (기대 $3, 실제 $2)"; cat err; fi; }

next M
check "선언 없음" "$(run a false)" 0
echo '<!-- dev:verify: exit 1 -->' > AGENTS.md
check "빨강이면 막음" "$(run b false)" 2
grep -q "dev:verify" err || echo "실패: stderr에 이유 없음"
check "재진입 2번째도 막음" "$(run b true)" 2
check "3번째는 경고만" "$(run b true)" 0
grep -q systemMessage out || echo "실패: 경고 없음"
echo '<!-- dev:verify: true -->' > AGENTS.md
check "초록이면 통과" "$(run c false)" 0
echo '<!-- dev:verify: exit 1 -->' > AGENTS.md; next S
check "S 등급은 안 돈다" "$(run d false)" 0
rm -rf "$t"
echo "ok $ok/6"
[ "$ok" = 6 ]
