#!/usr/bin/env bash
# Stop 훅: 끝 보고의 정비 문체(output-styles/ste-korean.md)를 잰다 — 검사 내용은 ste_check.py.
# 쓸 수 있는 python 이 없으면(Windows 의 가짜 python3 포함, 1.9.9) 조용히 건너뛴다. 문체 검사가 일을 막아서는 안 된다.
here="$(cd "$(dirname "$0")" && pwd)"
for py in python3 python; do
  if "$py" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1; then
    exec "$py" -I "$here/ste_check.py"
  fi
done
exit 0
