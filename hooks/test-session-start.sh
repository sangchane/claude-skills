#!/usr/bin/env bash
# session-start.sh 크기 검사 — 규칙 · 모델 지침 · NEXT 세 출력이 각각 한도 9,600자 안인지(규칙·지침은 300자 여유), 서로 섞이지 않는지 본다.
# 규칙(rules.md)·모델 지침이 길어지면 여기서 실패한다(2026-11-04 — 한 출력에 같이 담아 NEXT 블록이 46자만 들어갔고 Fable 은 한도를 넘었다).
#   bash hooks/test-session-start.sh
set -u
here="$(cd "$(dirname "$0")" && pwd)"; root="$(cd "$here/.." && pwd)"
LIMIT=9600; MARGIN=300
# 글자 수(session-start.sh 와 같은 방법 — OS·awk 종류와 상관없이 글자). 아래 0) 이 이 방법을 바로 시험한다.
count() { LC_ALL=C awk '{ s = $0; gsub(/[\200-\277]/, "", s); n += length(s) + 1 } END { print n + 0 }'; }
ok=0; total=0
check() { total=$((total + 1)); if [ "$2" = 0 ]; then ok=$((ok + 1)); else echo "실패: $1"; fi; }
run() { printf '{"model":"%s"}' "$2" | CLAUDE_PLUGIN_ROOT="$root" CLAUDE_PROJECT_DIR="$3" bash "$here/session-start.sh" $1; }

t="$(mktemp -d)"
# 0) 재는 단위가 글자인가 — macOS awk 는 length() 가 바이트라 한글이 3배로 잡혔다(1.14.0). python 이 있으면 rules.md 전체도 맞대 본다.
[ "$(printf '가나다\n' | count)" = 4 ]; check "글자 수 재기가 글자가 아니다(「가나다」+줄바꿈 = 4 여야 함, 실제 $(printf '가나다\n' | count)) — awk 단위 문제" $?
if py="$(command -v python3)" && "$py" -c 'pass' 2>/dev/null; then
  [ "$(count < "$root/rules.md")" = "$("$py" -c 'import sys; print(len(open(sys.argv[1], encoding="utf-8").read()))' "$root/rules.md")" ]
  check "rules.md 글자 수가 python 과 다르다" $?
fi
# 1) 규칙: hooks.json 이 부르는 조각(rules 1 · rules 2)마다 한도에서 여유 300자, 조각을 이으면 rules.md 와 같아야 하고(빠짐 없음), 그 밖 조각은 비어야 한다
parts="$(grep -o 'session-start.sh\\" rules [0-9]*' "$root/hooks/hooks.json" | grep -o '[0-9]*$')"
: > "$t/joined"; used=0
for p in $parts; do
  run "rules $p" "" "$t" > "$t/part"; n="$(count < "$t/part")"; used=$((used + n)); cat "$t/part" >> "$t/joined"
  [ "$n" -le $((LIMIT - MARGIN)) ]; check "규칙 조각 $p 출력이 ${n}자 (한도 ${LIMIT}에서 ${MARGIN}자 여유 필요)" $?
done
next_part=$(( $(printf '%s\n' $parts | sort -n | tail -n1) + 1 ))
[ -z "$(run "rules $next_part" "" "$t")" ]; check "규칙이 hooks.json 조각 수를 넘어 조각 $next_part 이 생겼다 — rules.md 를 줄이거나 자세한 내용을 스킬 references 로 옮길 것" $?
cmp -s "$t/joined" "$root/rules.md"; check "조각을 이은 것이 rules.md 와 다르다(빠지거나 겹친 줄)" $?
echo "  규칙: ${used}자 / 조각 $(echo $parts | wc -w | tr -d ' ')개 (남는 자리 $(( $(echo $parts | wc -w) * (LIMIT - MARGIN) - used )))"
for f in "$root"/rules-models/*.md; do
  m="$(basename "$f" .md)"
  n="$(run model "claude-$m" "$t" | count)"
  [ "$n" -le $((LIMIT - MARGIN)) ] && [ "$n" -gt 100 ]; check "모델 지침 출력이 ${n}자 — $m" $?
  echo "  모델 지침 · ${m}: ${n}자"
done
run model "" "$t" | grep -q "모델 미확인"; check "모델을 모르면 경로만 알린다" $?
run rules "claude-opus-5-5" "$t" | grep -q "모델 미확인"; [ $? -ne 0 ]; check "규칙 출력에 모델 지침이 섞이면 안 된다" $?

# 2) NEXT: 따로 나온다 — 작은 블록은 그대로, 큰 블록은 한도 안에서 잘리고 알림
printf '<!-- NEXT-ACTION:START -->\n▶ 시험 할 일\n<!-- NEXT-ACTION:END -->\n' > "$t/NEXT.md"
out="$(run next "" "$t")"
printf '%s' "$out" | grep -q "▶ 시험 할 일"; check "작은 NEXT 블록이 다 들어가야 한다" $?
printf '%s' "$out" | grep -q "작업 원칙"; [ $? -ne 0 ]; check "NEXT 출력에 규칙이 섞이면 안 된다" $?
{ echo '<!-- NEXT-ACTION:START -->'; for i in $(seq 1 400); do echo "- 긴 줄 $i: 연동 편집기 현장 설치 확인 항목을 길게 적은 줄"; done; echo '<!-- NEXT-ACTION:END -->'; } > "$t/NEXT.md"
out="$(run next "" "$t")"
n="$(printf '%s\n' "$out" | count)"
[ "$n" -le "$LIMIT" ]; check "큰 NEXT 블록 출력이 ${n}자 — 한도 ${LIMIT} 안이어야 한다" $?
printf '%s' "$out" | grep -q "앞 .*자만 붙였다"; check "큰 NEXT 블록은 잘림 알림이 있어야 한다" $?
rm -f "$t/NEXT.md"
[ -z "$(run next "" "$t")" ]; check "NEXT.md 가 없으면 아무것도 내지 않는다" $?
rm -rf "$t"

echo "ok $ok/$total"
[ "$ok" = "$total" ]
