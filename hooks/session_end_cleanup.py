"""SessionEnd — 세션이 남긴 프로세스와 스크래치 폴더를 치운다.

사용자 2026-11-26 「작업하면서 생기는 테스트 파일이나 부산물, 프로세스는 알아서 정리하게 … 메모리나 리소스 낭비시키지 않도록」.
규칙(rules.md 「내가 띄운 것은 내가 끈다」)은 Claude 가 기억해야 돈다. 이 훅은 Claude 를 끝낼 때 늘 돈다 — 예약 작업이 아니다.
SessionEnd 훅은 1.5초 안에 끝나야 하고 플러그인은 이 시간을 늘리지 못한다(공식 hooks 문서). 그래서
1 프로세스: 이 세션 claude 아래 나무를 그 자리에서 끈다. 이름이 아니라 나무로 고른다. 목록은 Windows ToolHelp(ctypes)·ps 로 빨리 읽는다
  (tools/leftovers.py 의 powershell 목록은 1.7초). 이 훅 사슬과 방금(3초 안) 뜬 형제 훅은 뺀다.
2 스크래치: <임시 폴더>/claude*/<해시>/<session_id> — 세션 스크래치·백그라운드 출력. 따로 띄운 프로세스가 지운다.
저장소 안 부산물(git 밖 새 파일)은 지우지 않는다 — 아직 커밋 안 한 새 코드와 구별할 수 없다. 그건 Claude 가 목록을 보고 leftovers.py --clean 으로.
닫힌 세션이 남긴 MCP 는 명령줄이 있어야 가려진다 — leftovers.py --kill 이 맡는다.
시험: python -I session_end_cleanup.py --test
"""
import json, os, signal, subprocess, sys, tempfile, time
from pathlib import Path

WIN = os.name == "nt"
FRESH = 3  # 초 — 이보다 최근에 뜬 프로세스는 같이 도는 다른 종료 훅일 수 있어 남긴다


def procs():
    """pid → (부모, 이름 소문자, 시작 유닉스초)"""
    if not WIN:
        now, P = time.time(), {}
        out = subprocess.run(["ps", "-axo", "pid=,ppid=,etime=,comm="], capture_output=True, text=True).stdout
        for line in out.splitlines():
            pid, ppid, et, *cmd = line.split(None, 3)
            d, _, hms = et.rpartition("-"); s = 0
            for x in hms.split(":"): s = s * 60 + int(x)
            P[int(pid)] = (int(ppid), os.path.basename(cmd[0] if cmd else "").lower(), now - s - int(d or 0) * 86400)
        return P
    import ctypes
    from ctypes import wintypes as w
    class PE(ctypes.Structure):
        _fields_ = [("dwSize", w.DWORD), ("cntUsage", w.DWORD), ("pid", w.DWORD), ("heap", ctypes.c_size_t),
                    ("mod", w.DWORD), ("threads", w.DWORD), ("ppid", w.DWORD), ("pri", w.LONG), ("flags", w.DWORD),
                    ("exe", w.WCHAR * 260)]
    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.CreateToolhelp32Snapshot.restype = w.HANDLE
    k.OpenProcess.restype = w.HANDLE
    snap, e, P = k.CreateToolhelp32Snapshot(2, 0), PE(), {}
    e.dwSize = ctypes.sizeof(PE)
    ok = k.Process32FirstW(snap, ctypes.byref(e))
    while ok:
        t, h = 0.0, k.OpenProcess(0x1000, False, e.pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if h:
            c, x = w.FILETIME(), w.FILETIME()
            if k.GetProcessTimes(h, ctypes.byref(c), ctypes.byref(x), ctypes.byref(x), ctypes.byref(x)):
                t = ((c.dwHighDateTime << 32) | c.dwLowDateTime) / 1e7 - 11644473600
            k.CloseHandle(h)
        P[e.pid] = (e.ppid, e.exe.lower(), t)
        ok = k.Process32NextW(snap, ctypes.byref(e))
    k.CloseHandle(snap)
    return P


def alive_parent(P, pid):
    """부모가 살아 있고 자식보다 먼저 떴나(윈도우는 죽은 부모 번호를 다시 쓴다). 시각을 못 읽으면(0) 부모로 보지 않는다"""
    q = P[pid][0]
    return q in P and q != pid and 0 < P[q][2] <= P[pid][2]


def doomed(P, me, now):
    """me 의 조상 중 claude 를 찾아, 그 아래에서 끌 나무 뿌리들을 돌려준다"""
    chain, x, claude = set(), me, None
    while x in P:
        chain.add(x)
        if P[x][1].startswith("claude"):
            claude = x; break
        if not alive_parent(P, x): return []
        x = P[x][0]
    if claude is None: return []
    kids = [p for p in P if p != claude and P[p][0] == claude and alive_parent(P, p)]
    return [p for p in kids if p not in chain and P[p][2] < now - FRESH]


def kill(P, roots):
    for r in roots:
        if WIN:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(r)], capture_output=True)
            continue
        tree, st = [], [r]
        while st:
            x = st.pop(); tree.append(x); st += [c for c in P if P[c][0] == x and alive_parent(P, c)]
        for x in reversed(tree):
            try: os.kill(x, signal.SIGTERM)
            except OSError: pass


def scratch_dirs(tmp: Path, sid: str) -> list:
    if not sid or not all(c.isalnum() or c == "-" for c in sid):
        return []  # 경로 조각이 아닌 값이면 아무것도 지우지 않는다
    return [d for d in tmp.glob(f"claude*/*/{sid}") if d.is_dir()]


def main():
    now = time.time()
    try:
        sid = json.load(sys.stdin).get("session_id", "")
    except ValueError:
        sid = ""
    P = procs()
    kill(P, doomed(P, os.getpid(), now))
    dirs = [str(d) for d in scratch_dirs(Path(tempfile.gettempdir()), sid)]
    if dirs:  # 큰 폴더는 1.5초를 넘길 수 있어 떼어 낸 프로세스가 지운다
        flags = 0x00000008 | 0x00000200 if WIN else 0  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        subprocess.Popen([sys.executable, "-I", "-c", "import shutil,sys\nfor d in sys.argv[1:]: shutil.rmtree(d, ignore_errors=True)", *dirs],
                         creationflags=flags, start_new_session=not WIN, stdin=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)


def test():
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        (t / "claude" / "h1" / "abc-1" / "scratchpad").mkdir(parents=True)
        (t / "claude" / "h1" / "other").mkdir(parents=True)
        assert [d.name for d in scratch_dirs(t, "abc-1")] == ["abc-1"]
        assert scratch_dirs(t, "") == [] and scratch_dirs(t, "../x") == [] and scratch_dirs(t, "*") == []
    # 나무: claude(10) → bash(11) → 훅(12) / claude → node(20) / claude → 방금 뜬 형제 훅(30) / 번호를 다시 쓴 가짜 자식(40)
    P = {1: (0, "explorer.exe", 50), 10: (1, "claude.exe", 100), 11: (10, "bash.exe", 900), 12: (11, "python.exe", 901),
         20: (10, "node.exe", 200), 21: (20, "workerd.exe", 201), 30: (10, "bash.exe", 899), 40: (10, "chrome.exe", 90)}
    assert doomed(P, 12, 900) == [20], doomed(P, 12, 900)
    assert doomed({5: (0, "bash", 1), 6: (5, "python", 2)}, 6, 10) == []  # claude 아래가 아니면 아무것도 끄지 않는다
    t0 = time.perf_counter(); n = len(procs())
    assert n > 5, n
    print(f"ok (프로세스 {n}개 목록 {time.perf_counter() - t0:.2f}초)")


if __name__ == "__main__":
    test() if "--test" in sys.argv else main()
