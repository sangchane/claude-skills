"""큰 단위 작업 끝 정리(사용자 2026-11-18 「timeout.exe·workerd.exe 같은 것, node 런타임, 내가 모르는 프로세스 포함 — 알아서 끄고 부산물은 지워라」).

이름으로 끄지 않는다. 같은 PC 에 다른 Claude 세션·사용자 서버가 살아 있다(이름이 같은 node·python).
대신 프로세스 나무로 주인을 가린다:
  1 이 세션 작업   = 이 세션 claude 아래 모든 프로세스(이름 무관: node·workerd·python·timeout·브라우저·conhost …).
                     빼는 것: MCP 서버 나무(claude 가 뜬 지 120초 안에 띄운 직계 자식 또는 명령줄에 mcp), 이 도구를 부른 셸 사슬.
  2 끝난 세션 MCP  = 부모가 죽은 나무 중 명령줄에 mcp 가 든 것(닫힌 Claude 세션이 남긴 node 런타임).
  3 주인 없는 것   = 이 세션이 뜬 뒤 생겼고 부모가 죽은 나무. 다른 세션 것일 수 있어 --mine 정규식에 맞는 것만 끈다.
부산물 = git 밖(추적 안 하고 무시도 안 하는) 파일 중 이 세션이 뜬 뒤 생겼고 어느 추적 파일도 경로를 가리키지 않는 것 + --scratch 폴더 안.
점(.)으로 시작하는 폴더·node_modules 안은 보지 않는다(.wrangler 로컬 DB 등).
지키기: 프로젝트 .claude/keep-processes.txt(줄마다 명령줄 정규식) · --keep 정규식 · --keep-file 경로 앞부분.

  python leftovers.py --mark                  # 큰 단위 시작에(부산물 기준 시각)
  python leftovers.py                         # 목록만
  python leftovers.py --kill --clean --scratch <스크래치 폴더> [--mine "wrangler|cdp.mjs"] [--keep-file autopilot/x/]
"""
import argparse, json, os, re, shutil, subprocess, sys, time
from pathlib import Path

# Windows 콘솔 기본 인코딩(cp1252 등)에서 한글 출력이 죽지 않게(2026-11-22 windows CI).
for _s in (sys.stdout, sys.stderr):
    _s.reconfigure(encoding="utf-8", errors="replace")

WIN = os.name == "nt"
MCP = re.compile(r"mcp", re.I)
BOOT = 120   # claude 가 뜬 뒤 이 초 안에 띄운 직계 자식 = MCP·훅 같은 세션 기반
T0 = time.time()   # 이 도구가 띄운 powershell·conhost 는 이 뒤에 생긴다 — 빼고 본다


def procs():
    """pid → (부모, 이름, 명령줄, 시작 유닉스초)"""
    if WIN:
        ps = ("Get-CimInstance Win32_Process | ForEach-Object { [pscustomobject]@{p=$_.ProcessId;q=$_.ParentProcessId;n=$_.Name;"
              "c=$_.CommandLine;t=if($_.CreationDate){([DateTimeOffset]$_.CreationDate).ToUnixTimeSeconds()}else{0}} } | ConvertTo-Json -Compress")
        out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
        return {r["p"]: (r["q"], r["n"] or "", r["c"] or "", r["t"] or 0) for r in json.loads(out)}
    now, P = time.time(), {}
    out = subprocess.run(["ps", "-axo", "pid=,ppid=,etime=,args="], capture_output=True, text=True).stdout
    for line in out.splitlines():
        pid, ppid, et, *cmd = line.split(None, 3)
        d, _, hms = et.rpartition("-"); s = 0
        for x in hms.split(":"): s = s * 60 + int(x)
        cmd = cmd[0] if cmd else ""
        P[int(pid)] = (int(ppid), os.path.basename(cmd.split(" ")[0]), cmd, now - s - int(d or 0) * 86400)
    return P


def alive_parent(P, pid):
    """부모가 살아 있고 자식보다 먼저 떴나(윈도우는 죽은 부모 번호를 다른 프로세스가 다시 쓴다)"""
    q = P[pid][0]
    return q in P and q != pid and P[q][3] <= P[pid][3]


def kids(P):
    K = {}
    for pid in P:
        if alive_parent(P, pid): K.setdefault(P[pid][0], []).append(pid)
    return K


def tree(K, root):
    out, st = [], [root]
    while st:
        x = st.pop(); out.append(x); st += K.get(x, [])
    return out


def find_claude(P):
    pid = os.getpid()
    while pid in P:
        n, c = P[pid][1].lower(), P[pid][2].lower()
        if n.startswith("claude") or ("node" in n and re.search(r"claude(-code)?[\\/]", c)): return pid
        if not alive_parent(P, pid): return None
        pid = P[pid][0]
    return None


def classify(P, me, mine, keep):
    K = kids(P); start = P[me][3]
    chain, x = set(), os.getpid()   # 이 도구를 부른 셸 사슬
    while x in P and x != me:
        chain.add(x); x = P[x][0] if alive_parent(P, x) else me
    skip = set()
    for c in K.get(me, []):
        if P[c][3] - start <= BOOT or any(MCP.search(P[t][2]) for t in tree(K, c)): skip |= set(tree(K, c))
    kept = lambda t: P[t][3] >= T0 - 2 or any(k.search(P[x][2]) for x in tree(K, t) for k in keep)
    session = [c for c in K.get(me, []) if c not in skip and c not in chain and not kept(c)]
    # 이 세션 사슬 안 셸(Bash 도구)의 다른 자식(백그라운드로 남은 것)
    for s in chain:
        session += [c for c in K.get(s, []) if c not in chain and not kept(c)]
    roots = [p for p in P if not alive_parent(P, p) and p not in (0, 4) and P[p][3] > 0]
    # 뿌리나 바로 밑 자식 명령줄에 mcp(cmd /c npx …mcp) — 나무 전체로 보면 explorer 같은 시스템 뿌리까지 걸린다. 산 claude 가 든 나무는 빼고
    near = lambda r: [r] + K.get(r, [])
    dead_mcp = [r for r in roots if any(MCP.search(P[t][2]) for t in near(r)) and not any(P[t][1].lower().startswith("claude") for t in tree(K, r)) and not kept(r)]
    orphan = [r for r in roots if r not in dead_mcp and P[r][3] >= start and not kept(r)]
    return K, session, dead_mcp, [r for r in orphan if mine and any(mine.search(P[t][2]) for t in tree(K, r))], [r for r in orphan if not (mine and any(mine.search(P[t][2]) for t in tree(K, r)))]


def kill(P, K, root):
    if WIN:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(root)], capture_output=True)
    else:
        for x in reversed(tree(K, root)):
            try: os.kill(x, 15)
            except OSError: pass


def show(P, K, roots, label):
    for r in roots:
        t = tree(K, r)
        print(f"  [{label}] {P[r][1]}#{r} 외 {len(t) - 1}개 — {P[r][2][:110]}")


def git_top():
    try:
        return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def mark_path(me):
    """큰 단위 시작 표시 — .git 안이라 부산물로 안 잡힌다"""
    top = git_top()
    return Path(subprocess.run(["git", "-C", top, "rev-parse", "--git-dir"], capture_output=True, text=True).stdout.strip() or ".git").resolve() / f"leftovers-mark-{me}" if top else None


def byproducts(start, keep_files, scratch):
    out = []
    top = git_top()
    if top:
        files = subprocess.run(["git", "-C", top, "ls-files", "--others", "--exclude-standard", "-z"], capture_output=True, text=True, encoding="utf-8").stdout.split("\0")
        cand = []
        for f in filter(None, files):
            if any(s.startswith(".") or s == "node_modules" for s in f.split("/")[:-1]) or any(f.startswith(k) for k in keep_files): continue
            st = os.stat(os.path.join(top, f))
            if getattr(st, "st_birthtime", st.st_mtime) >= start: cand.append(f)
        if cand:   # 추적 파일(NEXT·WORKLOG·문서·코드)이 경로나 파일 이름으로 가리키면 증거 — 남긴다
            pats = sorted({f for f in cand} | {os.path.basename(f) for f in cand})
            r = subprocess.run(["git", "-C", top, "grep", "-h", "-o", "-F", "-f", "-"], input="\n".join(pats), capture_output=True, text=True, encoding="utf-8")
            hit = set(r.stdout.splitlines())
            out += [Path(top, f) for f in cand if f not in hit and os.path.basename(f) not in hit]
    if scratch and Path(scratch).is_dir():
        out += [p for p in Path(scratch).iterdir()]
    return out


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--kill", action="store_true"); a.add_argument("--clean", action="store_true")
    a.add_argument("--mine", help="주인 없는 것 중 이 세션이 띄운 것의 명령줄 정규식"); a.add_argument("--keep", action="append", default=[])
    a.add_argument("--keep-file", action="append", default=[], help="지우지 않을 경로 앞부분(저장소 기준)"); a.add_argument("--scratch")
    a.add_argument("--mark", action="store_true", help="큰 단위 시작에 부른다 — 부산물은 이 시각 뒤에 생긴 것만")
    o = a.parse_args()
    P = procs(); me = find_claude(P)
    if not me: sys.exit("이 세션의 claude 프로세스를 못 찾았다 — 아무것도 끄지 않는다")
    mp = mark_path(me)
    if o.mark:
        if mp: mp.write_text(str(time.time()), encoding="utf-8"); print(f"시작 표시 {time.strftime('%m-%d %H:%M')} — {mp}")
        return
    since = float(mp.read_text(encoding="utf-8")) if mp and mp.exists() else P[me][3]   # 표시가 없으면 claude 가 뜬 때부터
    kf = Path(git_top() or ".", ".claude/keep-processes.txt")
    keep = [re.compile(k, re.I) for k in o.keep + ([l.strip() for l in kf.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")] if kf.exists() else [])]
    K, session, dead_mcp, orphan_mine, orphan_other = classify(P, me, re.compile(o.mine, re.I) if o.mine else None, keep)
    print(f"이 세션 claude#{me} — 뜬 때 {time.strftime('%m-%d %H:%M', time.localtime(P[me][3]))} · 부산물 기준 {time.strftime('%m-%d %H:%M', time.localtime(since))}")
    show(P, K, session, "이 세션"); show(P, K, dead_mcp, "끝난 세션 MCP"); show(P, K, orphan_mine, "주인 없음·내 것"); show(P, K, orphan_other, "주인 없음·모름 — 안 끔")
    doomed = session + dead_mcp + orphan_mine
    if o.kill:
        for r in doomed: kill(P, K, r)
        print(f"끈 나무 {len(doomed)}개(프로세스 {sum(len(tree(K, r)) for r in doomed)}개)")
    files = byproducts(since, o.keep_file, o.scratch)
    for f in files[:40]: print(f"  [부산물] {f}")
    if len(files) > 40: print(f"  … 외 {len(files) - 40}개")
    if o.clean:
        n = 0
        for f in files:
            try:
                shutil.rmtree(f) if f.is_dir() else f.unlink(); n += 1
            except OSError as e:
                print(f"  못 지움 {f}: {e}")
        print(f"지운 부산물 {n}개")
        if mp and mp.exists(): mp.unlink()   # 다음 큰 단위는 새로 --mark
    elif not o.kill:
        print(f"목록만 냈다. 끄기 --kill · 지우기 --clean (끌 나무 {len(doomed)}개 · 부산물 {len(files)}개)")


if __name__ == "__main__":
    main()
