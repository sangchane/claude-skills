"""SessionStart — 설치된 모든 플러그인의 옛 판 폴더(plugins/cache/<마켓>/<플러그인>/<판>)를 지운다.

사건 2026-11-26: claude-mem 이 업데이트마다 새 판을 받고 옛 판을 남겨 13개 판이 10GB 를 차지했다(1.19.0 은 claude-mem 만 지웠다).
사건 2026-11-27: dev 도 같은 까닭으로 판 11개가 쌓였다(사용자 「위험도 해결해서 스킬 업데이트해」). 그래서 플러그인 이름을 박지 않고 전부 본다.
남기는 것: installed_plugins.json 이 가리키는 판 + 그 밖에서 가장 최근 판 1개(아직 다시 시작하지 않은 열린 세션이 쓰는 판).
지우는 곳은 plugins/cache 아래 판 폴더뿐이다 — 설치 경로가 그 밖(로컬 디렉터리 설치 등)이면 건드리지 않는다.
예약 작업이 아니라 세션 시작 때만 돈다(주기 실행 금지 — 사용자 2026-11-24). hooks.json 이 py-hook.sh 로 부른다.
시험: python -I prune_plugin_cache.py --test
"""
import json, shutil, sys, tempfile
from pathlib import Path

HOME = Path.home() / ".claude" / "plugins"


def stale(base: Path, in_use: set) -> list:
    others = sorted((d for d in base.iterdir() if d.is_dir() and d.name not in in_use),
                    key=lambda d: d.stat().st_mtime, reverse=True)
    return others[1:]  # 가장 최근 1개는 남긴다


def targets(plugins: dict, cache: Path) -> list:
    """플러그인마다 (판 폴더들의 부모, 쓰는 판 이름들). cache/<마켓>/<플러그인>/<판> 꼴만 고른다."""
    groups = {}
    for rows in plugins.values():
        for r in rows:
            p = Path(r.get("installPath", ""))
            try:
                rel = p.resolve().relative_to(cache.resolve())
            except (ValueError, OSError):
                continue
            if len(rel.parts) == 3:
                groups.setdefault(p.parent, set()).add(p.name)
    return list(groups.items())


def main():
    try:
        plugins = json.loads((HOME / "installed_plugins.json").read_text(encoding="utf-8"))["plugins"]
    except (OSError, KeyError, ValueError):
        return  # 설치 정보가 없으면 아무것도 지우지 않는다
    for base, in_use in targets(plugins, HOME / "cache"):
        if base.is_dir():
            for d in stale(base, in_use):
                shutil.rmtree(d, ignore_errors=True)  # 쓰는 중인 파일이 있으면 남는다 — 다음 세션에 다시 시도


def test():
    import os, time
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        for i, n in enumerate(["1.0", "1.1", "1.2", "2.0"]):
            (base / n).mkdir()
            os.utime(base / n, (time.time() + i, time.time() + i))
        got = sorted(d.name for d in stale(base, {"2.0"}))
        assert got == ["1.0", "1.1"], got
        assert stale(base, {"1.0", "1.1", "1.2", "2.0"}) == []
        # 플러그인 둘(사용자 · 프로젝트 범위 판이 다름) · cache 밖 설치 하나
        cache = base / "cache"
        a, b = cache / "m" / "a", cache / "m" / "b"
        for d in (a / "1", a / "2", a / "3", b / "9"):
            d.mkdir(parents=True)
        plugins = {
            "a@m": [{"installPath": str(a / "3")}, {"installPath": str(a / "1")}],
            "b@m": [{"installPath": str(b / "9")}],
            "c@local": [{"installPath": str(base / "elsewhere" / "c")}],
        }
        got = sorted((g.name, sorted(u)) for g, u in targets(plugins, cache))
        assert got == [("a", ["1", "3"]), ("b", ["9"])], got
    print("ok")


if __name__ == "__main__":
    test() if "--test" in sys.argv else main()
