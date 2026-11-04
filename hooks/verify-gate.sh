#!/usr/bin/env bash
# dev 플러그인 Stop 훅 — 검증 게이트. 프로젝트가 선언한 검증 명령이 빨간불이면 턴 종료를 막고 실패 꼬리를 모델에게 돌려준다.
# 선언: 프로젝트 AGENTS.md(또는 CLAUDE.md)에 한 줄  <!-- dev:verify: npm test -->
# 도는 조건: 선언이 있고, NEXT.md 현재 작업 블록이 M·L 등급의 BUILD·VERIFY 단계이고, 커밋 안 된 변경이 있을 때만.
# 같은 턴에서 3번 연속 빨강이면 막지 않고 사용자에게 경고만 보인다(무한 반복 방지 — Claude Code 자체 상한은 8).
# 안전: 훅은 권한 확인 없이 돈다 — 저장소 파일에 사람이 적은 명령만 실행하고, 명령을 추론하지 않는다.
# 근거: OpenAI "Harness engineering"(기계적 강제), Claude Code hooks(Stop exit 2), gstack verify-gate(재진입도 다시 검사).
input=""; [ -t 0 ] || input="$(cat)"
# 입력 JSON 은 bash 로 읽는다 — Windows 의 python3 는 스토어 안내용 가짜 실행 파일일 수 있다(2026-11-04).
field() { printf '%s' "$input" | grep -o "\"$1\" *: *\"[^\"]*\"" | head -n1 | sed -E 's/^.*: *"(.*)"$/\1/; s/\\\\/\\/g'; }
sid="$(field session_id)"; sid="${sid:-x}"
cwd="$(field cwd)"; cwd="${cwd:-.}"
active=0; printf '%s' "$input" | grep -qE '"stop_hook_active" *: *true' && active=1
dir="${CLAUDE_PROJECT_DIR:-$cwd}"
cmd="$(grep -ho '<!-- *dev:verify: *[^>]*-->' "$dir/AGENTS.md" "$dir/CLAUDE.md" 2>/dev/null | head -n1 | sed -E 's/<!-- *dev:verify: *//; s/ *-->$//')"
[ -n "$cmd" ] || exit 0
block="$(sed -n '/NEXT-ACTION:START/,/NEXT-ACTION:END/p' "$dir/NEXT.md" 2>/dev/null)"
printf '%s' "$block" | grep -qE '등급: *(M|L)' || exit 0
printf '%s' "$block" | grep -qE 'BUILD|VERIFY' || exit 0
[ -n "$(git -C "$dir" status --porcelain 2>/dev/null)" ] || exit 0

count="${TMPDIR:-/tmp}/dev-verify-$sid"
n=0
if [ "$active" = 1 ] && [ -f "$count" ]; then n="$(cat "$count")"; fi
out="$(cd "$dir" && bash -c "$cmd" 2>&1)"; rc=$?
if [ "$rc" -eq 0 ]; then rm -f "$count"; exit 0; fi
n=$((n + 1))
if [ "$n" -ge 3 ]; then
  rm -f "$count"
  esc="$(printf '%s' "$cmd" | sed 's/\\/\\\\/g; s/"/\\"/g')"
  printf '{"systemMessage": "[dev:verify] 검증 명령이 3번 연속 실패한 채로 턴을 마쳤다: %s"}\n' "$esc"
  exit 0
fi
echo "$n" > "$count"
{
  printf '[dev:verify] 검증 명령이 실패했다(종료 %s): %s\n' "$rc" "$cmd"
  printf '고치거나, 지금 고칠 수 없으면 무엇이 왜 빨간지 사용자에게 그대로 보고하고 끝내라(완료라고 하지 않는다).\n--- 마지막 20줄 ---\n'
  printf '%s\n' "$out" | tail -n 20
} >&2
exit 2
