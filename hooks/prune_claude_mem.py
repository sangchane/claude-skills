"""SessionStart — claude-mem 플러그인의 옛 판 폴더를 지운다.

사건 2026-11-26: claude-mem 이 업데이트마다 plugins/cache/thedotmack/claude-mem/<판> 을 새로 받고
옛 판을 남겨, 13개 판이 10GB 를 차지했다(사용자 「쌓이지 않도록 조치해둬」).
남기는 것: installed_plugins.json 이 가리키는 판 + 그 밖에서 가장 최근 판 1개(아직 열린 다른 세션이 쓸 수 있음).
예약 작업이 아니라 세션 시작 때만 돈다(주기 실행 금지 — 사용자 2026-11-24). hooks.json 이 py-hook.sh 로 부른다.
시험: python -I prune_claude_mem.py --test
"""
import json, shutil, sys, tempfile
from pathlib import Path

HOME = Path.home() / ".claude" / "plugins"
KEY = "claude-mem@thedotmack"


def stale(base: Path, in_use: set) -> list:
    others = sorted((d for d in base.iterdir() if d.is_dir() and d.name not in in_use),
                    key=lambda d: d.stat().st_mtime, reverse=True)
    return others[1:]  # 가장 최근 1개는 남긴다


def main():
    try:
        rows = json.loads((HOME / "installed_plugins.json").read_text(encoding="utf-8"))["plugins"][KEY]
        paths = [Path(r["installPath"]) for r in rows]
    except (OSError, KeyError, ValueError):
        return  # 설치 정보가 없으면 아무것도 지우지 않는다
    base = paths[0].parent
    if not base.is_dir():
        return
    for d in stale(base, {p.name for p in paths}):
        shutil.rmtree(d, ignore_errors=True)  # 쓰는 중인 파일이 있으면 남는다 — 다음 세션에 다시 시도


def test():
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        import os, time
        for i, n in enumerate(["1.0", "1.1", "1.2", "2.0"]):
            (base / n).mkdir()
            os.utime(base / n, (time.time() + i, time.time() + i))
        got = sorted(d.name for d in stale(base, {"2.0"}))
        assert got == ["1.0", "1.1"], got
        assert stale(base, {"1.0", "1.1", "1.2", "2.0"}) == []
    print("ok")


if __name__ == "__main__":
    test() if "--test" in sys.argv else main()
