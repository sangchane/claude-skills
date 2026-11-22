#!/usr/bin/env bash
# rtk.sh 자체 시험 — 진짜 rtk 없이 가짜 rtk 로 여섯 경우.  bash hooks/test-rtk.sh
set -u
here="$(cd "$(dirname "$0")" && pwd)"
t="$(mktemp -d)"; mkdir -p "$t/bin" "$t/conf"
in='{"tool_name":"Bash","tool_input":{"command":"git status"}}'
want='{"hookSpecificOutput":{"hookEventName":"PreToolUse","updatedInput":{"command":"rtk git status"}}}'
# 가짜 rtk 를 PATH 맨 앞에 둔다. 진짜 rtk 가 깔린 PC 에서도 시험이 가짜만 보게 PATH 는 시스템 기본 폴더만 잇는다.
fake() { printf '#!/usr/bin/env bash\n%s\n' "$1" > "$t/bin/rtk"; chmod +x "$t/bin/rtk"; }
run() { printf '%s' "$in" | PATH="$t/bin:/usr/bin:/bin" CLAUDE_CONFIG_DIR="$t/conf" bash "$here/rtk.sh"; echo "exit=$?"; }
ok=0; check() { if [ "$2" = "$3" ]; then ok=$((ok + 1)); else printf '실패: %s\n  기대: %s\n  실제: %s\n' "$1" "$3" "$2"; fi; }

check "rtk 없음 → 그대로" "$(run)" "exit=0"
fake "[ \"\$1 \$2\" = 'hook claude' ] && grep -q 'git status' && echo '$want'"
check "rtk 있음 → 바꾼 명령" "$(run)" "$want
exit=0"
fake "cat >/dev/null; exit 0"
check "바꿀 것 없음 → 그대로" "$(run)" "exit=0"
fake "echo 'error: unrecognized subcommand hook' >&2; exit 2"
check "옛 rtk(hook 없음) → 그대로, 오류 안 샘" "$(run 2>&1)" "exit=0"
fake "echo '{\"partial'; exit 1"
check "rtk 가 내다가 실패 → 반쪽 출력을 넘기지 않음" "$(run)" "exit=0"
fake "echo '$want'"
echo '{"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"rtk hook claude"}]}]}}' > "$t/conf/settings.json"
check "전역 rtk 훅이 이미 있음 → 비킴" "$(run)" "exit=0"
rm -rf "$t"
echo "ok $ok/6"
[ "$ok" = 6 ]
