#!/usr/bin/env python3
"""ste_check.py 자체 시험 — 좋은 끝 보고는 통과, 어긋난 것은 항목 이름으로 막힘, 두 번째는 통과, 짧은 답·python 없음은 건너뜀.
  python3 -I hooks/test_ste_check.py"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
from ste_check import problems  # noqa: E402

GOOD = """됐습니다. 이벤트 탭을 만들어 커밋했습니다.

줄을 한 번 누르면 그 이벤트 10초 전부터 재생합니다.
클립이 끝나면 다음 이벤트를 이어서 틉니다. 재생할 수 없는 클립을 만나면 멈추고 원인을 보입니다.
타임라인은 카메라마다 한 줄이고, 끌면 둘러보기만 합니다.
확인 묶음 `qa.sh` 가 모두 통과했습니다. `SC-002` 같은 시험 이름은 백틱 안이라 재지 않습니다.

1. 대화창에 `! brew install rtk-ai/tap/rtk-oss` 를 치세요.
2. 새 세션을 여세요.

확인하지 않은 것: 아이폰 실기기의 두 손가락 확대.
위험: 없음. 가짜 서버(개발 서버 전용 흉내 API)는 제품에 들어가지 않습니다. 출력 스타일(output style)은 요청마다 들어갑니다.
"""
assert len(GOOD) > 300 and problems(GOOD) == [], problems(GOOD)
assert problems("짧은 답입니다.") == []

bad = GOOD.replace("됐습니다. 이벤트 탭을", "이벤트 탭을", 1)
assert [p[:2] for p in problems(bad)] == ["1항"], problems(bad)
assert problems("## 됐습니다\n" + GOOD.split("\n", 1)[1]) == []  # 제목 표시가 붙어도 결론으로 본다

arrows = GOOD + "\n흐름: 빌드 → 시험 → 커밋 → 배포 순서로 돌았습니다.\n"
assert any(p.startswith("화살표") for p in problems(arrows)), problems(arrows)
assert problems(GOOD + "\n버전은 1.12.0 → 1.15.0 으로 올랐습니다.\n") == []  # 바뀐 값 하나는 괜찮다

jargon = GOOD + "\nSC-008 닿음과 HMR, e2e, RLS 모두 확인했습니다.\n"
assert any(p.startswith("8항") for p in problems(jargon)), problems(jargon)
explained = GOOD + "\nRLS(행 단위 접근 제한)와 HMR(코드 바꾸면 화면만 다시 그림)을 확인했습니다.\n"
assert problems(explained) == [], problems(explained)

long = GOOD + "\n" + ("이 문장은 일부러 아주 길게 써서 한 문장에 여러 가지를 담고 쉼표로 계속 이어 붙인 나쁜 예라서 검사가 잡아야 합니다, 그리고 카메라와 서버와 화면과 시험을 한꺼번에 설명하느라 더 길게 이어집니다. " * 2) + "\n"
assert any(p.startswith("3항") for p in problems(long)), problems(long)
para = GOOD + "\n" + "\n".join(f"{i}번째 줄입니다." for i in range(7)) + "\n"
assert any(p.startswith("9항") for p in problems(para)), problems(para)


def hook(msg, active=False, env=None):
    r = subprocess.run([shutil.which("bash"), str(here / "ste-check.sh")], input=json.dumps({"last_assistant_message": msg, "stop_hook_active": active}).encode(),
                       capture_output=True, env=env or os.environ)
    return r.returncode, r.stdout.decode("utf-8")


code, out = hook(bad)
assert code == 0 and json.loads(out)["decision"] == "block" and "1항" in json.loads(out)["reason"], out
assert hook(bad, active=True) == (0, "")  # 한 번 돌려보낸 뒤에는 막지 않는다
assert hook(GOOD) == (0, "")
# Windows 의 가짜 python3(실행하면 안내만 찍고 실패)만 있는 PATH — 검사를 건너뛰어야 한다(1.9.9)
stub = Path(tempfile.mkdtemp())
(stub / "python3").write_text("#!/bin/sh\necho Python\nexit 9009\n")
(stub / "python3").chmod(0o755)
assert hook(bad, env={"PATH": str(stub)}) == (0, ""), hook(bad, env={"PATH": str(stub)})
print("ok ste_check")
