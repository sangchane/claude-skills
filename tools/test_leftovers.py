"""leftovers.classify 자체 시험 — 가짜 프로세스 표로 주인 가리기만 본다(아무것도 끄지 않는다).  python3 -I tools/test_leftovers.py"""
import re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import leftovers as L

S = 100_000   # 이 세션 claude 가 뜬 때
P = {
    4: (0, "System", "", 1),
    100: (1, "explorer.exe", "explorer", 10),                 # 부모 죽은 시스템 뿌리(나무 안에 claude·MCP)
    200: (100, "claude.exe", "claude", S),                    # 이 세션
    201: (200, "cmd.exe", "cmd /c npx -y @playwright/mcp", S + 5),   # MCP — 지킴
    202: (201, "node.exe", "node mcp/cli.js", S + 6),
    210: (200, "bash.exe", "bash -c wrangler dev", S + 900),  # 이 세션 백그라운드 명령 — 끔
    211: (210, "node.exe", "node wrangler dev", S + 901),
    212: (211, "workerd.exe", "workerd serve", S + 902),
    300: (100, "claude.exe", "claude", S - 500),              # 다른 산 세션 — 손대지 않음
    301: (300, "cmd.exe", "cmd /c npx rea-mcp", S - 499),
    400: (9999, "cmd.exe", "cmd /c npx -y @playwright/mcp", S - 9000),   # 닫힌 세션 MCP — 끔
    401: (400, "node.exe", "node mcp/cli.js", S - 9000),
    500: (9998, "timeout.exe", "timeout 900 python -m pytest", S + 950),  # 주인 없음, --mine 에 안 맞음 — 안 끔
    600: (9997, "node.exe", "node scripts/cdp.mjs steps.json", S + 960), # 주인 없음, --mine 에 맞음 — 끔
    700: (9996, "cmd.exe", "cmd /c npx wrangler@4 dev --port 8790", S + 970),  # 지킬 서버(keep)
}
L.T0 = S + 10_000
L.os.getpid = lambda: 202   # 도구를 부른 사슬이 MCP 쪽이어도 이 세션 claude 를 찾는다
assert L.find_claude(P) == 200
K, session, dead_mcp, mine, other = L.classify(P, 200, re.compile("cdp|wrangler"), [re.compile("--port 8790")])
assert session == [210], session
assert dead_mcp == [400], dead_mcp
assert mine == [600], mine
assert 500 in other and 700 not in other and 100 not in other + dead_mcp, other
assert sorted(L.tree(K, 210)) == [210, 211, 212]
print("leftovers ok")
