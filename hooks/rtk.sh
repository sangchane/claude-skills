#!/usr/bin/env bash
# PreToolUse(Bash) 훅: RTK(rtk-ai/rtk, Apache-2.0)가 깔려 있으면 `git status` 같은 명령을 `rtk git status` 로 바꿔
# 출력을 줄인 뒤 Claude 에게 넘긴다. 바꿀 것이 없으면 아무것도 내지 않는다(명령 그대로).
# - rtk 가 없으면 조용히 비킨다(설치는 사용자 몫: README 1절).
# - 사용자가 `rtk init -g` 로 전역 훅을 이미 붙였으면 비킨다(두 번 돌지 않게).
# - 권한 판정(자동 허용·물어보기)은 rtk 가 사용자 설정의 allow·ask·deny 규칙대로 한다. 이 훅은 결과만 넘긴다.
command -v rtk >/dev/null 2>&1 || exit 0
settings="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"
grep -qs -e 'rtk hook claude' -e 'rtk-rewrite' "$settings" && exit 0
out="$(rtk hook claude 2>/dev/null)" || exit 0 # 옛 rtk(hook 명령 없음)·오류는 명령을 그대로 둔다
[ -n "$out" ] && printf '%s\n' "$out"
exit 0
