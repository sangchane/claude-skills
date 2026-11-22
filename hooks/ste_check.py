#!/usr/bin/env python3
"""정비 문체 검사(output-styles/ste-korean.md) — Stop 훅이 그 턴의 끝 보고를 잰다. tools/ste_measure.py 도 같은 함수를 쓴다.
재는 것: 1항 첫 줄 결론 · 3항 긴 문장 · 8항 풀지 않은 약어 · 9항 긴 문단 · 화살표 잇기. 어긋나면 한 번 막고 고쳐 쓰게 한다.
입력(stdin, Claude Code Stop 훅): {"last_assistant_message": "...", "stop_hook_active": false, ...}
  python3 -I hooks/ste_check.py < input.json"""
import json
import re
import sys

MIN_CHARS = 300  # 이보다 짧은 답(한두 줄 대답)은 재지 않는다
VERDICT = re.compile(r"^(됐|되었|안 됐|답이 필요|못 했|끝났)")
ABBR = re.compile(r"(?<![\w./-])(?:[A-Z][A-Z0-9]+(?:-[A-Z0-9]+)*|[a-z]+\d[a-z0-9]*)(?![\w/.-]*[a-z])")
KNOWN = {"PC", "OS", "CCTV", "QR", "IP", "URL", "AI", "PDF", "ID", "OK", "PIN", "TV", "USB", "GPS", "UI", "API", "JSON", "CSS", "HTML", "SQL", "DB", "CPU", "GPU", "LTE", "SNS", "KST", "UTC", "MIT", "GPL", "BSD"}
ABBR_MAX, LONG_LEN, LONG_MAX, PARA_MAX = 2, 90, 1, 5
LISTY = re.compile(r"^\s*([-*>|#]|\d+\.)")


def plain(t):
    """코드 블록·인라인 코드·링크 주소를 지운 본문(백틱 안은 재지 않는다)."""
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    t = re.sub(r"`[^`\n]*`", "X", t)
    t = re.sub(r"\]\([^)]*\)", "]", t)
    return re.sub(r"https?://\S+", "", t)


def problems(msg):
    """어긋난 항목 목록(빈 목록 = 통과)."""
    body = plain(msg)
    if len(body.strip()) < MIN_CHARS:
        return []
    out = []
    first = next((l for l in msg.splitlines() if l.strip()), "")
    head = re.sub(r"^[\s#>*_-]+", "", first)
    if not VERDICT.match(head):
        out.append(f"1항: 첫 줄이 결론이 아닙니다(「{head[:40]}」). 첫 줄을 「됐습니다 / 안 됐습니다 / 답이 필요합니다」로 시작하세요.")
    arrows = [l for l in body.splitlines() if l.count("→") >= 2]
    if arrows:
        out.append(f"화살표 잇기 {len(arrows)}줄(「{arrows[0].strip()[:40]}」). 단계는 문장으로 나눠 쓰세요.")
    explained = {m.group(1) for m in re.finditer(r"([A-Za-z][\w-]*)\s?\(", body)} | {w for m in re.finditer(r"\(([^)]*)\)", body) for w in re.findall(r"[A-Za-z][\w-]*", m.group(1))}
    bare = sorted({a for a in ABBR.findall(body) if a not in KNOWN and a not in explained})
    if len(bare) > ABBR_MAX:
        out.append(f"8항: 풀지 않은 약어·내부 용어 {len(bare)}개({', '.join(bare[:6])}). 빼거나 처음 나올 때 괄호로 풀어 쓰세요.")
    prose = [l for l in body.splitlines() if l.strip() and not LISTY.match(l)]
    longs = [s for l in prose for s in re.split(r"(?<=[.!?])\s+", l.strip()) if len(s) > LONG_LEN]
    if len(longs) > LONG_MAX:
        out.append(f"3항: {LONG_LEN}글자 넘는 문장 {len(longs)}개(「{longs[0][:40]}…」). 한 문장에 한 가지로 나누세요.")
    run = worst = 0
    for l in body.splitlines():
        run = run + 1 if l.strip() and not LISTY.match(l) else 0
        worst = max(worst, run)
    if worst > PARA_MAX:
        out.append(f"9항: {worst}줄짜리 문단이 있습니다. 다섯 줄 이하로 나누세요.")
    return out


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    except ValueError:
        return 0
    if data.get("stop_hook_active"):  # 이미 한 번 돌려보냈다 — 고쳐 쓴 답은 다시 막지 않는다
        return 0
    found = problems(data.get("last_assistant_message") or "")
    if found:
        reason = "정비 문체 검사(dev): 끝 보고가 문체 규칙과 어긋납니다. 내용은 그대로 두고 형식만 고쳐 끝 보고를 다시 쓰세요.\n- " + "\n- ".join(found)
        sys.stdout.buffer.write((json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False) + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
