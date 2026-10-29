#!/usr/bin/env bash
# dev 플러그인 세션 시작 훅: 작업 규칙(rules.md)과 프로젝트 NEXT.md의 현재 작업 블록을 Claude 컨텍스트에 넣는다.
# 훅 출력은 10,000자를 넘으면 파일로 빠지고 앞 2,000자만 보인다(공식 hooks 문서 「JSON output」).
# 그래서 규칙 · 모델 지침을 먼저 내고, NEXT 블록은 남은 글자 수만큼만 붙인다(2026-10-29 — NEXT 블록이 커져 규칙까지 잘렸다).
root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
LIMIT=9600
input=""; [ -t 0 ] || input="$(cat)"

head_part() {
  echo "(이 출력이 잘려 미리보기로만 보이면 저장된 파일 전체를 Read 한다 — 규칙 대부분이 뒤에 있다.)"
  cat "$root/rules.md"
  # 모델별 지침: 훅 입력(JSON)의 model에서 claude-<계열>-<버전>을 읽어 rules-models/<계열>-<버전>.md를 붙인다.
  # 그 버전 파일이 없으면 같은 계열의 가장 새 파일 + 갱신 권고 한 줄, 모델을 모르면 전부(자기 모델 절만 따르라고 적음).
  model="$(printf '%s' "$input" | tr -d '\n' | grep -o '"model"[^}]*' | grep -o 'claude-[a-z]*-[0-9][0-9-]*' | head -n1)"
  key="${model#claude-}"; fam="${key%%-*}"; md="$root/rules-models"
  if [ -n "$model" ] && [ -f "$md/$key.md" ]; then printf '\n'; cat "$md/$key.md"
  elif [ -n "$model" ] && ls "$md/$fam"-*.md >/dev/null 2>&1; then
    f="$(ls "$md/$fam"-*.md | sort -V | tail -n1)"; printf '\n'; cat "$f"
    printf '\n> %s 전용 지침 파일이 없어 %s를 붙였다. 이 모델의 Anthropic 프롬프팅 가이드로 rules-models/%s.md를 만들 것(README "모델 지침 갱신").\n' "$model" "$(basename "$f")" "$key"
  # 전부 붙이면 한도를 넘어 규칙까지 잘린다 — 경로만 적고 자기 모델 것을 읽게 한다
  else printf '\n## 모델별 지침 (모델 미확인) — 자기 모델 파일만 Read 한다: %s\n' "$(ls "$md"/*.md | tr '\n' ' ')"
  fi
}

# 글자 수 — UTF-8 로캘이면 글자로, 없으면 바이트로 센다(바이트가 더 커서 늘 짧게 끊긴다)
count() { LC_ALL=C.UTF-8 awk '{ n += length($0) + 1 } END { print n + 0 }'; }

pre="$(head_part)"
printf '%s\n' "$pre"
left=$(( LIMIT - $(printf '%s\n' "$pre" | count) ))

dir="${CLAUDE_PROJECT_DIR:-$PWD}"
for f in "$dir/NEXT.md" "$dir/coordination/NEXT.md"; do
  if [ -f "$f" ]; then
    printf '\n## 현재 작업 (%s)\n' "${f#"$dir"/}"
    sed -n '/NEXT-ACTION:START/,/NEXT-ACTION:END/p' "$f" | LC_ALL=C.UTF-8 awk -v max="$(( left - 300 ))" -v file="${f#"$dir"/}" '
      { n += length($0) + 1; if (n <= max) print; else cut = 1 }
      END { if (cut) printf "\n> NEXT 블록이 %d자라 앞 %d자만 붙였다 — 나머지는 %s 를 Read 한다. 끝난 블록은 NEXT-ACTION:END 아래로 옮길 것.\n", n, max, file }'
    break
  fi
done
exit 0
