# 작업 방식 (전역)

<!-- 원본: ~/.claude/skills/_tools/CLAUDE.global.md — ~/.claude/CLAUDE.md에 이 내용을 넣는다. 고칠 때는 원본을 고치고 다시 복사한다. -->

## 이어가기
- 세션을 시작하면 프로젝트 루트 `NEXT.md`의 `NEXT-ACTION` 블록을 확인하고(catch-up 훅이 있으면 이미 주입돼 있다), 있으면 그 등급·스킬·단계에서 이어간다. "다음 진행해", "이어서"는 그 블록의 다음 할 일이다.
- M·L 작업은 단계를 마치거나 멈출 때 그 블록을 덮어쓴다(등급 · 스킬 · 단계 · 다음 할 일 1~3줄 · 산출물 경로). S 작업은 쓰지 않는다. 히스토리는 `WORKLOG.md`에만.

## 규모 판정
새 요청을 받으면 응답 첫 줄에 `등급: S|M|L — 이유 한 구절`을 쓴다. 이어가는 요청이면 NEXT.md의 등급을 따른다.
- **S**: 변경을 한 문장으로 설명할 수 있고 되돌리기 쉽다. 스킬을 부르지 않고 바로 고친 뒤 검증 명령을 한 번 돌린다.
- **M**: 기능 하나, 여러 파일, 게임·도구 프로토타입. `service-prompt-workflow` M 경로(1쪽 SPEC → 구현 → 검증 → 리뷰 1회).
- **L 신규**: 새 서비스, 모르는 도메인, 되돌리기 어려운 설계 결정. `service-autopilot`으로 설계한 뒤 `service-prompt-workflow` L 경로.
- **L 변경**: 기존 저장소에서 돈·인증·개인정보·데이터 마이그레이션을 건드리는 변경. autopilot 없이 `service-prompt-workflow` L 경로(SPEC + 보안 리뷰).
- 버그는 규모와 상관없이 `service-prompt-workflow`의 디버깅 분기(재현 → 원인 → 수정)로 가고, 위험 모듈이면 리뷰를 1회 더한다.
- 애매하면 한 등급 낮게 시작하고, 진행 중 L 신호가 보이면 그때 올리며 한 줄로 알린다. 웹 UI가 있으면 `frontend-design-taste`를 함께 쓴다.
- superpowers 스킬은 `service-prompt-workflow`가 부르는 단계에서만 쓴다. M의 FRAME과 L의 autopilot이 `superpowers:brainstorming`을 대신한다(이 규칙이 using-superpowers보다 우선).

## 모델·effort·위임
- 메인 세션 모델은 그대로 둔다. 등급에 맞는 effort는 S low~medium, M medium, L high다. L 작업을 low로 하거나 S 작업을 xhigh 이상으로 하고 있을 때만 `/effort <level>`을 한 줄로 권한다.
- 서브에이전트는 크고 서로 독립적인 작업, 대용량 읽기, 기능 단위 최종 독립 리뷰에만 쓴다. 도구 호출 몇 번으로 끝나는 일과 내 작업을 다시 확인하는 일에는 쓰지 않는다. 동시 3개, 요청당 5개까지.
- 위임할 때 모델은 기계적 대량 `haiku`, 패턴 반복·조사 `sonnet`, 판단 집약 `opus`, 장기 조사 `fable`. effort가 달라야 하면 `deep-worker`(high)·`quick-worker`(low) 에이전트에 `model`을 줘서 부른다.
