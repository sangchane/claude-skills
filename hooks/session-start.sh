#!/usr/bin/env bash
# dev 플러그인 세션 시작 훅: 작업 규칙(rules) · 모델별 지침(model) · 프로젝트 NEXT.md 현재 작업 블록(next) 중 하나를 Claude 컨텍스트에 넣는다.
# 훅 출력은 문자열 하나에 10,000자를 넘으면 파일로 빠지고 앞 2,000자만 보인다. 한도는 훅마다 따로 잰다
# (공식 hooks 문서: 「each string on its own, even when several hooks run for the same event」).
# 그래서 hooks.json 이 이 스크립트를 rules · model · next 로 세 번 부른다 — 한 출력에 같이 담으면 규칙이 한도를 거의 다 써서
# NEXT 블록이 46자만 들어갔고, Fable 지침이 붙으면 10,203자로 넘쳐 규칙 전체가 2,000자 미리보기가 됐다(2026-11-04 측정).
# 크기 검사: hooks/test-session-start.sh
root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
LIMIT=9600
# 글자 수 = 바이트 모드(LC_ALL=C) awk 에서 UTF-8 이어지는 바이트(0x80~0xBF)를 뺀 길이. Claude Code 한도는 글자 단위다.
# awk 의 length() 는 OS 마다 단위가 다르다 — macOS awk(20200816)는 UTF-8 로캘에서도 바이트를 세서 한글이 3배로 잡혔고,
# 리눅스 gawk 는 글자를 센다. 그래서 같은 rules.md 가 Mac 에서만 조각 3 으로 넘쳐 끝 절이 빠졌다(1.14.0, CI 는 통과).
CLEN='function clen(s) { gsub(/[\200-\277]/, "", s); return length(s) }'
mode="${1:-rules}"
input=""; [ -t 0 ] || input="$(cat)"

rules_part() {
  # 규칙을 「## 」 절 경계에서 한도 안 조각으로 나눠 want 번째만 낸다(hooks.json 이 rules 1 · rules 2 로 부른다).
  # 한 출력에 다 담으면 규칙이 자랄 때마다 10,000자를 넘어 미리보기만 보였다(1.8.1 · 1.10.0 · 1.11.0 반복). 조각이 hooks.json 수보다 많아지면 test-session-start.sh 가 실패한다.
  LC_ALL=C awk -v max="$(( LIMIT - 300 ))" -v want="${1:-1}" "$CLEN"'
    function flush() { if (sec == "") return; n = clen(sec); if (size > 0 && size + n > max) { chunk++; size = 0 }
      if (chunk + 1 == want) printf "%s", sec; size += n; sec = "" }
    /^## / { flush() }
    { sec = sec $0 "\n" }
    END { flush() }' "$root/rules.md"
}

model_part() {
  # 모델별 지침: 훅 입력(JSON)의 model에서 claude-<계열>-<버전>을 읽어 rules-models/<계열>-<버전>.md를 낸다.
  # 그 버전 파일이 없으면 같은 계열의 가장 새 파일 + 갱신 권고 한 줄, 모델을 모르면 파일 경로만(자기 모델 것을 읽게 한다).
  model="$(printf '%s' "$input" | tr -d '\n' | grep -o '"model"[^}]*' | grep -o 'claude-[a-z]*-[0-9][0-9-]*' | head -n1)"
  key="${model#claude-}"; fam="${key%%-*}"; md="$root/rules-models"
  if [ -n "$model" ] && [ -f "$md/$key.md" ]; then cat "$md/$key.md"
  elif [ -n "$model" ] && ls "$md/$fam"-*.md >/dev/null 2>&1; then
    f="$(ls "$md/$fam"-*.md | sort -V | tail -n1)"; cat "$f"
    printf '\n> %s 전용 지침 파일이 없어 %s를 붙였다. 이 모델의 Anthropic 프롬프팅 가이드로 rules-models/%s.md를 만들 것(README "모델 지침 갱신").\n' "$model" "$(basename "$f")" "$key"
  else printf '## 모델별 지침 (모델 미확인) — 자기 모델 파일만 Read 한다: %s\n' "$(ls "$md"/*.md | tr '\n' ' ')"
  fi
}

next_part() {
  dir="${CLAUDE_PROJECT_DIR:-$PWD}"
  for f in "$dir/NEXT.md" "$dir/coordination/NEXT.md"; do
    if [ -f "$f" ]; then
      printf '## 현재 작업 (%s)\n' "${f#"$dir"/}"
      # 머리 줄과 잘림 알림 줄 몫으로 300자를 남긴다
      sed -n '/NEXT-ACTION:START/,/NEXT-ACTION:END/p' "$f" | LC_ALL=C awk -v max="$(( LIMIT - 300 ))" -v file="${f#"$dir"/}" "$CLEN"'
        { n += clen($0) + 1; if (n <= max) print; else cut = 1 }
        END { if (cut) printf "\n> NEXT 블록이 %d자라 앞 %d자만 붙였다 — 나머지는 %s 를 Read 한다. 끝난 블록은 NEXT-ACTION:END 아래로 옮길 것.\n", n, max, file }'
      break
    fi
  done
}

case "$mode" in
  rules) rules_part "${2:-1}" ;;
  model) model_part ;;
  next) next_part ;;
esac
exit 0
