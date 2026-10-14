#!/usr/bin/env bash
# dev 플러그인 세션 시작 훅: 작업 규칙(rules.md)과 프로젝트 NEXT.md의 현재 작업 블록을 Claude 컨텍스트에 넣는다.
root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
cat "$root/rules.md"
# 모델별 지침: 훅 입력(JSON)의 model에서 claude-<계열>-<버전>을 읽어 rules-models/<계열>-<버전>.md를 붙인다.
# 그 버전 파일이 없으면 같은 계열의 가장 새 파일 + 갱신 권고 한 줄, 모델을 모르면 전부(자기 모델 절만 따르라고 적음).
input=""; [ -t 0 ] || input="$(cat)"
model="$(printf '%s' "$input" | tr -d '\n' | grep -o '"model"[^}]*' | grep -o 'claude-[a-z]*-[0-9][0-9-]*' | head -n1)"
key="${model#claude-}"; fam="${key%%-*}"; md="$root/rules-models"
if [ -n "$model" ] && [ -f "$md/$key.md" ]; then printf '\n'; cat "$md/$key.md"
elif [ -n "$model" ] && ls "$md/$fam"-*.md >/dev/null 2>&1; then
  f="$(ls "$md/$fam"-*.md | sort -V | tail -n1)"; printf '\n'; cat "$f"
  printf '\n> %s 전용 지침 파일이 없어 %s를 붙였다. 이 모델의 Anthropic 프롬프팅 가이드로 rules-models/%s.md를 만들 것(README "모델 지침 갱신").\n' "$model" "$(basename "$f")" "$key"
else printf '\n## 모델별 지침 (모델 미확인 — 자기 모델 절만 따른다)\n'; for f in "$md"/*.md; do printf '\n'; cat "$f"; done
fi
dir="${CLAUDE_PROJECT_DIR:-$PWD}"
for f in "$dir/NEXT.md" "$dir/coordination/NEXT.md"; do
  if [ -f "$f" ]; then
    printf '\n## 현재 작업 (%s)\n' "${f#"$dir"/}"
    sed -n '/NEXT-ACTION:START/,/NEXT-ACTION:END/p' "$f"
    break
  fi
done
exit 0
