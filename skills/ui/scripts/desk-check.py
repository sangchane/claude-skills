# 데스크톱 앱 화면 자동 검사(웹 ui-check 의 데스크톱판) — agent-desktop 으로 창의 접근성 나무·스크린샷을 받아 결함을 이름으로 내고 종료 코드로 판정한다.
#   python desk-check.py --app SMS_C.exe                        # 떠 있는 앱의 모든 창 검사 + 창마다 PNG
#   python desk-check.py --launch C:\app\X.exe --cwd C:\app --flow qa.json --out shots
#   python desk-check.py --selftest                              # 판정 함수 자체 시험(앱 없이)
# 끝 줄 「desk-check passed」(종료 0) 또는 「desk-check failed」(종료 1). 2 = agent-desktop·앱 문제.
# 흐름 파일(JSON 목록, 위에서 아래로): {"click":"button:로그인"} {"set":"textfield:아이디","value":"x"}
#   {"wait":"statictext:접속됨","timeout":15} {"gone":"window:불러오는 중"} {"expect":"textfield:상태","value":"정상"}
#   {"shot":"로그인 뒤"} {"sleep":500} — 고르개는 「역할:이름 일부」(역할을 비우면 아무 역할). 단계마다 오류 창 검사.
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

INTERACTIVE = {"button", "textfield", "checkbox", "radiobutton", "combobox", "link", "menuitem", "tab", "slider",
               "spinbutton", "switch", "togglebutton", "searchfield"}
ERROR_TITLE = re.compile(r"error|exception|오류|예외|에러", re.I)  # 창 제목만 본다(로그 목록의 「[오류]」 줄은 정상)
CRASH_TEXT = re.compile(r"unhandled exception|처리되지 않은 예외|has stopped working|작동이 중지", re.I)
EDGE_PX, OVERLAP_RATIO, TINY_PX = 2, 0.3, 12
UNRESPONSIVE_RETRIES = 6


def agent_desktop_cmd() -> list:
    """npm 전역 설치의 네이티브 실행 파일을 먼저 쓴다(Node 실행기는 호출마다 0.1초 더 든다)."""
    if os.environ.get("AGENT_DESKTOP"):
        return [os.environ["AGENT_DESKTOP"]]
    w = shutil.which("agent-desktop")
    if not w:
        raise SystemExit("desk-check: agent-desktop 이 없습니다 — npm install -g agent-desktop")
    native = Path(w).parent / "node_modules" / "agent-desktop" / "bin" / "agent-desktop-win32-x64.exe"
    return [str(native)] if native.exists() else [w]


def ad(*args) -> dict:
    """agent-desktop 한 번. 앱이 바빠 APP_UNRESPONSIVE 면 다시 시도한다."""
    r = {}
    for _ in range(UNRESPONSIVE_RETRIES):
        p = subprocess.run(agent_desktop_cmd() + [str(a) for a in args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=180)
        try:
            r = json.loads(p.stdout)
        except ValueError:
            r = {"ok": False, "error": {"code": "NOT_JSON", "message": (p.stdout + p.stderr)[-400:]}}
        if r.get("ok") or (r.get("error") or {}).get("code") != "APP_UNRESPONSIVE":
            return r
        time.sleep(2)
    return r


# ---------- 판정(순수 함수 — selftest 대상) ----------

def _box(n):
    b = n.get("bounds") or {}
    if b.get("width", 0) <= 0 or b.get("height", 0) <= 0:
        return None
    return (b["x"], b["y"], b["x"] + b["width"], b["y"] + b["height"])


def _label(n):
    return f'{n.get("role")}「{(n.get("name") or "")[:30]}」'


def judge(tree: dict, title: str = "", ignore=None) -> list:
    """창 하나의 나무 → [(fail|warn, 코드, 설명)]."""
    out = []
    skip = (lambda n: bool(ignore and ignore.search(n.get("name") or "")))
    if ERROR_TITLE.search(title or ""):
        out.append(("fail", "error-dialog", f"창 제목에 오류 낱말: {title}"))
    win = _box(tree)

    def visit(n, parent):
        kids = n.get("children") or []
        role, box = n.get("role"), _box(n)
        visible = "offscreen" not in (n.get("states") or [])
        text = " ".join(str(n.get(k) or "") for k in ("name", "value", "description"))
        if CRASH_TEXT.search(text):
            out.append(("fail", "error-dialog", f"앱 고장 문구: {text[:80]}"))
        if role in INTERACTIVE and visible and box and not skip(n):
            pb = _box(parent) if parent else None
            if win and (box[0] < win[0] - EDGE_PX or box[1] < win[1] - EDGE_PX or box[2] > win[2] + EDGE_PX or box[3] > win[3] + EDGE_PX):
                out.append(("fail", "outside-window", f"{_label(n)} 이 창 밖으로 나감 {box} / 창 {win}"))
            elif pb and parent.get("role") in ("group", "pane", "toolbar", "window") and (
                    box[0] < pb[0] - EDGE_PX or box[1] < pb[1] - EDGE_PX or box[2] > pb[2] + EDGE_PX or box[3] > pb[3] + EDGE_PX):
                out.append(("warn", "clipped-by-parent", f"{_label(n)} 이 담는 칸 밖으로 나감(잘려 보일 수 있음)"))
            if not (n.get("name") or "").strip():
                out.append(("warn", "no-name", f"{role} 이름 없음 {box} — 화면 읽기·자동 시험이 못 고른다"))
            nid = n.get("native_id") or {}
            if nid.get("kind") == "automation_id" and str(nid.get("value", "")).isdigit():
                out.append(("warn", "unstable-id", f"{_label(n)} 자동화 ID 가 창 번호({nid['value']}) — 실행마다 바뀜(WinForms 면 컨트롤 Name 을 준다)"))
            if min(box[2] - box[0], box[3] - box[1]) < TINY_PX:
                out.append(("warn", "tiny-target", f"{_label(n)} 누를 자리가 {TINY_PX}px 보다 작음"))
        # 같은 부모 아래 누르는 요소끼리 겹침
        sib = [(c, _box(c)) for c in kids if c.get("role") in INTERACTIVE and _box(c) and "offscreen" not in (c.get("states") or []) and not skip(c)]
        for i in range(len(sib)):
            for j in range(i + 1, len(sib)):
                a, b = sib[i][1], sib[j][1]
                w, h = min(a[2], b[2]) - max(a[0], b[0]), min(a[3], b[3]) - max(a[1], b[1])
                inside = lambda p, q: p[0] <= q[0] and p[1] <= q[1] and p[2] >= q[2] and p[3] >= q[3]
                if sib[i][0].get("role") == sib[j][0].get("role") and (inside(a, b) or inside(b, a)):
                    continue  # 같은 종류가 통째로 감쌈 = 한 부품의 겉·속(DevExpress 입력 칸 안의 실제 입력 칸)
                if w > 0 and h > 0:
                    small = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
                    if w * h > OVERLAP_RATIO * small:
                        out.append(("fail", "overlap", f"{_label(sib[i][0])} 와 {_label(sib[j][0])} 가 겹침"))
        for c in kids:
            visit(c, n)

    visit(tree, None)
    return out


# ---------- 흐름 ----------

def find_ref(app: str, sel: str):
    role, _, name = sel.partition(":")
    args = ["find", "--app", app, "--timeout-ms", "20000"]  # 큰 나무(DevExpress)는 기본 5초에 못 다 돈다
    if role:
        args += ["--role", role]
    if name:
        args += ["--name", name]
    r = ad(*args)
    data = r.get("data")
    items = data.get("matches", data.get("elements", [])) if isinstance(data, dict) else (data or [])
    for m in items:  # 누를 수 없는 요소(글자 칸)는 ref 가 없다 — 있음·값 확인엔 그 일치 자체를 쓴다
        return m.get("ref_id") or m.get("ref") or "", m
    return None, r


def wait_for(app: str, sel: str, timeout: float, gone: bool = False):
    """(맞음, 마지막 find 결과) — 실패 줄에 마지막 오류를 보이려고 돌려준다."""
    end, last = time.time() + timeout, None
    while time.time() < end:
        ref, last = find_ref(app, sel)
        if (ref is None) == gone:
            return True, last
        time.sleep(0.5)
    return False, last


def run_flow(app: str, steps: list, shots: Path, problems: list) -> None:
    for k, st in enumerate(steps, 1):
        tag = f"단계 {k} {json.dumps(st, ensure_ascii=False)}"
        if "sleep" in st:
            time.sleep(st["sleep"] / 1000)
        elif "shot" in st:
            screenshot_all(app, shots, st["shot"])
        elif "wait" in st or "gone" in st:
            sel = st.get("wait") or st.get("gone")
            ok, last = wait_for(app, sel, st.get("timeout", 10), gone="gone" in st)
            if not ok:
                err = (last or {}).get("error") if isinstance(last, dict) else None
                problems.append(("fail", "flow", f"{tag}: {st.get('timeout', 10)}초 안에 {'안 사라짐' if 'gone' in st else '안 나타남'}"
                                 + (f" — 마지막 오류 {json.dumps(err, ensure_ascii=False)[:160]}" if err else "")))
                return
        else:
            sel = st.get("click") or st.get("set") or st.get("expect")
            ref, info = find_ref(app, sel)
            if ref is None or (not ref and "expect" not in st):
                problems.append(("fail", "flow", f"{tag}: 요소를 못 찾음 {json.dumps(info, ensure_ascii=False)[:200]}"))
                return
            if "click" in st:
                r = ad("click", ref)
            elif "set" in st:
                r = ad("set-value", ref, st.get("value", ""))
            elif not ref:
                r = {"ok": True, "data": info}
                got = json.dumps(info, ensure_ascii=False)
                if "value" in st and str(st["value"]) not in got:
                    problems.append(("fail", "flow", f"{tag}: 값이 다름 — 받은 것 {got[:120]}"))
                    return
            else:
                r = ad("get", ref, "--property", st.get("property", "value" if "value" in st else "text"))
                got = json.dumps(r.get("data"), ensure_ascii=False)
                if r.get("ok") and "value" in st and str(st["value"]) not in got:
                    problems.append(("fail", "flow", f"{tag}: 값이 다름 — 받은 것 {got[:120]}"))
                    return
            if not r.get("ok"):
                problems.append(("fail", "flow", f"{tag}: {json.dumps(r.get('error'), ensure_ascii=False)[:200]}"))
                return
        for w in windows(app):  # 단계마다 오류 창
            if ERROR_TITLE.search(w.get("title") or ""):
                problems.append(("fail", "error-dialog", f"{tag} 뒤 오류 창: {w.get('title')}"))
                return


def windows(app: str) -> list:
    r = ad("list-windows", "--app", app)
    return [w for w in (r.get("data") or []) if w.get("visible") and not w.get("minimized")]


def screenshot_all(app: str, shots: Path, tag: str) -> None:
    shots.mkdir(parents=True, exist_ok=True)
    for i, w in enumerate(windows(app)):
        safe = re.sub(r"[^\w가-힣-]+", "_", f"{app}-{tag}-{i}")
        ad("screenshot", "--window-id", w["id"], str((shots / f"{safe}.png").resolve()))


def check(app: str, shots: Path, ignore=None) -> list:
    problems = []
    wins = windows(app)
    if not wins:
        return [("fail", "no-window", f"{app} 창이 없음")]
    for w in wins:
        r = ad("snapshot", "--window-id", w["id"], "--include-bounds", "--max-depth", "40", "--timeout-ms", "20000")
        if not r.get("ok"):
            problems.append(("fail", "snapshot", f"창 {w.get('title')!r}: {json.dumps(r.get('error'), ensure_ascii=False)[:200]}"))
            continue
        for lvl, code, msg in judge(r["data"]["tree"], w.get("title") or "", ignore):
            problems.append((lvl, code, f"[{w.get('title') or w['id']}] {msg}"))
    screenshot_all(app, shots, "끝")
    return problems


def selftest() -> int:
    btn = lambda name, x, y, w=80, h=24, nid="btnOk": {"role": "button", "name": name, "bounds": {"x": x, "y": y, "width": w, "height": h},
                                                          "native_id": {"kind": "automation_id", "value": nid}}
    win = lambda kids: {"role": "window", "bounds": {"x": 0, "y": 0, "width": 400, "height": 300}, "children": kids}
    good = win([{"role": "group", "bounds": {"x": 0, "y": 0, "width": 400, "height": 300},
                 "children": [btn("확인", 10, 10), btn("취소", 100, 10, nid="btnCancel"),
                              {"role": "listbox", "children": [{"role": "option", "name": "09:00 [오류] 모뎀 응답 없음"}]}]}])
    bad = win([btn("확인", 10, 10), btn("취소", 20, 12, nid="btnCancel"), btn("", 380, 10, nid="123456"),
               btn("x", 200, 200, 8, 8, nid="btnX"), {"role": "statictext", "name": "Unhandled exception has occurred"}])
    codes = lambda t, title="": sorted({c for _, c, _ in judge(t, title)})
    cases = [(codes(good), []),
             (codes(bad), ["error-dialog", "no-name", "outside-window", "overlap", "tiny-target", "unstable-id"]),
             (codes(good, "Microsoft .NET Framework 오류"), ["error-dialog"]),
             (sorted({c for _, c, _ in judge(win([{"role": "textfield", "name": "알람", "bounds": {"x": 0, "y": 0, "width": 300, "height": 22}},
                                                  {"role": "textfield", "name": "알람", "bounds": {"x": 4, "y": 3, "width": 290, "height": 16}}]))}), []),
             (sorted({c for _, c, _ in judge(win([btn("새파일", 10, 10, nid="a"), btn("파일 열기", 10, 10, nid="b")]), "", re.compile("^새파일$"))}), [])]
    ok = sum(a == b for a, b in cases)
    for a, b in cases:
        if a != b:
            print("  틀림:", a, "기대", b)
    print(f"desk-check selftest {ok}/{len(cases)}")
    return 0 if ok == len(cases) else 1


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="데스크톱 앱 화면 자동 검사(agent-desktop)")
    ap.add_argument("--app", help="list-apps 가 보이는 이름(예: SMS_C.exe)")
    ap.add_argument("--launch", help="띄울 실행 파일 경로(끝나면 닫는다)")
    ap.add_argument("--cwd")
    ap.add_argument("--arg", action="append", default=[])
    ap.add_argument("--flow", type=Path, help="흐름 JSON 파일")
    ap.add_argument("--out", type=Path, default=Path("shots"))
    ap.add_argument("--keep-open", action="store_true")
    ap.add_argument("--ignore", help="이름이 이 정규식에 맞는 요소는 판정에서 뺀다 — 사진으로 확인한 거짓 경보만(예: DevExpress 가 숨긴 리본 단추를 보이는 자리로 알려 줌), 끝 보고에 이유")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    app = a.app or (Path(a.launch).name if a.launch else None)
    if not app:
        ap.error("--app 이나 --launch 가 필요합니다")
    launched = False
    if a.launch:
        args = ["launch", a.launch, "--timeout", "30000"] + (["--cwd", a.cwd] if a.cwd else [])
        for x in a.arg:
            args.append(f"--arg={x}")
        r = ad(*args)
        if not r.get("ok"):
            print("desk-check: 앱을 못 띄움", json.dumps(r.get("error"), ensure_ascii=False)[:300])
            return 2
        launched = True
        wait_for(app, "", 20)  # 창이 뜰 때까지
    problems = []
    try:
        if a.flow:
            run_flow(app, json.loads(a.flow.read_text(encoding="utf-8")), a.out, problems)
        problems += check(app, a.out, re.compile(a.ignore) if a.ignore else None)
    finally:
        if launched and not a.keep_open:
            ad("close-app", app, "--force")
    for lvl, code, msg in problems:
        print(f"{lvl.upper():4} {code:18} {msg}")
    print(f"스크린샷: {a.out.resolve()}")
    tool = any(c in ("snapshot", "no-window") for _, c, _ in problems)
    failed = any(l == "fail" for l, _, _ in problems)
    print("desk-check failed" if failed else "desk-check passed")
    return 2 if tool and not any(c not in ("snapshot", "no-window") and l == "fail" for l, c, _ in problems) else (1 if failed else 0)


if __name__ == "__main__":
    sys.exit(main())
