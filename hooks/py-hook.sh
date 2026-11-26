#!/usr/bin/env bash
# 파이썬 훅 실행기: 쓸 수 있는 python 으로 hooks/<스크립트> 를 돌린다. 없으면(Windows 의 가짜 python3 포함) 조용히 건너뛴다 — 정리 훅이 일을 막아서는 안 된다.
here="$(cd "$(dirname "$0")" && pwd)"
for py in python3 python; do
  if "$py" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1; then
    "$py" -I "$here/$1" >/dev/null 2>&1
    exit 0
  fi
done
exit 0
