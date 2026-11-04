#!/usr/bin/env bash
# session-start.sh 크기 검사 — 규칙 · 모델 지침 · NEXT 세 출력이 각각 한도 9,600자 안인지(규칙·지침은 300자 여유), 서로 섞이지 않는지 본다.
# 규칙(rules.md)·모델 지침이 길어지면 여기서 실패한다(2026-11-04 — 한 출력에 같이 담아 NEXT 블록이 46자만 들어갔고 Fable 은 한도를 넘었다).
#   bash hooks/test-session-start.sh
set -u
here="$(cd "$(dirname "$0")" && pwd)"; root="$(cd "$here/.." && pwd)"
LIMIT=9600; MARGIN=300
count() { LC_ALL=C.UTF-8 awk '{ n += length($0) + 1 } END { print n + 0 }'; }
ok=0; total=0
check() { total=$((total + 1)); if [ "$2" = 0 ]; then ok=$((ok + 1)); else echo "실패: $1"; fi; }
run() { printf '{"model":"%s"}' "$2" | CLAUDE_PLUGIN_ROOT="$root" CLAUDE_PROJECT_DIR="$3" bash "$here/session-start.sh" "$1"; }

t="$(mktemp -d)"
# 1) 규칙 · 모델 지침: 각각 한도에서 여유 300자를 남겨야 한다(모델 지침은 파일마다, 모델을 모를 때도)
n="$(run rules "" "$t" | count)"
[ "$n" -le $((LIMIT - MARGIN)) ]; check "규칙 출력이 ${n}자 (한도 ${LIMIT}에서 ${MARGIN}자 여유 필요)" $?
echo "  규칙: ${n}자 (남는 자리 $((LIMIT - n)))"
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
