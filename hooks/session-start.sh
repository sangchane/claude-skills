#!/usr/bin/env bash
# dev 플러그인 세션 시작 훅: 작업 규칙(rules.md)과 프로젝트 NEXT.md의 현재 작업 블록을 Claude 컨텍스트에 넣는다.
root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
cat "$root/rules.md"
dir="${CLAUDE_PROJECT_DIR:-$PWD}"
for f in "$dir/NEXT.md" "$dir/coordination/NEXT.md"; do
  if [ -f "$f" ]; then
    printf '\n## 현재 작업 (%s)\n' "${f#"$dir"/}"
    sed -n '/NEXT-ACTION:START/,/NEXT-ACTION:END/p' "$f"
    break
  fi
done
exit 0
