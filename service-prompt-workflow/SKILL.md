---
name: service-prompt-workflow
description: |
  무엇을 만들지 아는 상태의 구현·버그 수정을 규모에 맞는 단계로 진행하는 얇은 워크플로우. 실행 절차는 superpowers가 맡고,
  이 스킬은 등급별로 어떤 단계를 거칠지, service-autopilot 설계를 어떻게 이어받을지, ponytail·프론트 스킬을 어디에 붙일지만 정한다.
  사용 시점: 기능 하나·게임/도구 프로토타입 만들기(M), 새 서비스 설계를 마친 뒤 구현 착수(L 신규), 기존 저장소의 결제·인증·개인정보
  변경(L 변경), 버그 수정, "구현해·리뷰해줘·커밋해·다음 진행해". 한 문장으로 설명되는 변경(S)에는 부르지 않는다.
  도메인을 모르는 새 서비스는 먼저 service-autopilot.
argument-hint: "[요청 한 문장 또는 단계명]"
metadata:
  version: "0.7.0"
  updated: "2026-09-29"
---

# service-prompt-workflow

superpowers가 실행 엔진이다. 이 스킬은 **규모에 맞게 단계를 고르고, 단계마다 어떤 스킬을 붙일지**만 정한다.
공통 작업 원칙·규모 판정·위임 상한은 전역 `~/.claude/CLAUDE.md`(원본 `_tools/CLAUDE.global.md`)를 따른다.

## 등급별 경로

| 등급 | 단계 | 문서 | 리뷰 |
|---|---|---|---|
| **S** | 이 스킬 없이 바로 수정 → 검증 명령 1회 | 없음 | 요청 시만 |
| **M** | FRAME(3줄) → SPEC(1쪽) → BUILD → VERIFY → REVIEW → SHIP. 모르는 코드면 EXPLORE. 작업이 5개를 넘으면 PLAN, 아니면 SPEC의 완료 기준 순서대로 메인에서 구현 | `SPEC.md` 1쪽 | 기능 단위 1회 |
| **L 신규** | autopilot GATE 뒤 **SPEC부터**(입력 `03·05·08`) → PLAN → BUILD → VERIFY → REVIEW → SHIP → REFLECT. PLAN 첫 작업 3개는 버티컬 슬라이스 | SPEC.md + tasks.md | 기능 단위 1회 + 고위험이면 보안 리뷰 |
| **L 변경** | 기존 저장소의 결제·인증·개인정보·마이그레이션. FRAME → EXPLORE → SPEC → PLAN → BUILD → VERIFY → REVIEW → SHIP | SPEC.md (+ tasks.md) | 기능 단위 1회 + `/security-review` |
| **버그** | 재현 → 원인 → 수정(`superpowers:systematic-debugging`) → VERIFY. 위험 모듈이면 REVIEW 1회 | 없음 | 위험 모듈만 |

게임·도구 프로토타입(M)은 SPEC 전에 버리는 프로토타입으로 핵심 가설(재미·성능·조작감) 하나를 먼저 확인하고 결과를 SPEC에 반영한다.
진행 중 L 신호(돈·보안·개인정보·법, 되돌리기 어려운 결정)가 나오면 등급을 올리고 한 줄로 알린다.

## 단계별로 붙이는 것

| 단계 | 하는 일 | 스킬 |
|---|---|---|
| FRAME | 사용자·문제·성공 기준·안 할 것을 3줄로. `superpowers:brainstorming`을 대신한다 | 없음 |
| EXPLORE | 관련 코드를 직접 읽고 file:line으로 인용. 여러 모듈을 넓게 훑을 때만 Explore 서브에이전트 | 없음 |
| SPEC | `references/spec-template.md` (M 1쪽 / L 전체) | 화면이 있으면 `frontend-design-taste` |
| PLAN | 작업 분해. 첫 3개는 버티컬 슬라이스, 그다음 위험 큰 것부터 | `superpowers:writing-plans` |
| BUILD | 같은 세션에서 구현. 코드 전에 ponytail 사다리 | `superpowers:executing-plans` · `superpowers:test-driven-development` · `ponytail:ponytail` · 화면이면 `frontend-design-taste` |
| VERIFY | 테스트·빌드·린트·(UI면) 스크린샷을 실행하고 결과를 붙인다. 실패하면 근본 원인 | `superpowers:verification-before-completion` · 실패 시 `superpowers:systematic-debugging` |
| REVIEW | diff와 SPEC만 주고 새 컨텍스트에서 정확성 1회. 과잉설계는 선택 | `/code-review` · `ponytail:ponytail-review` · 고위험 `/security-review` |
| SHIP | 작은 커밋, 한글 설명형 메시지, PR | `superpowers:finishing-a-development-branch` |
| REFLECT | 다음에도 쓸 규칙만 CLAUDE.md·AGENTS.md에, 결정은 decision-log에 | 없음 |

- `superpowers:subagent-driven-development`(작업마다 구현 1 + 리뷰 2 서브에이전트)는 크고 서로 독립인 작업이 한 세션에 안 들어갈 때만,
  요청당 작업 1개씩. 위임 여부·상한·모델은 `references/model-routing.md`.
- 리뷰어 서브에이전트를 띄우는 스킬(`superpowers:requesting-code-review`, `/code-review`)은 정확성 리뷰 1회 안에서 하나만.
- 리뷰 지적은 정확성·요구사항에 영향 있는 것만 반영한다. 나머지를 다 쫓으면 과잉설계가 된다.

## 라우터

- "구현해", "이 스펙대로 만들어" → BUILD (SPEC이 없으면 등급에 맞게 SPEC부터)
- "명세 써줘", "작업 쪼개줘" → SPEC / PLAN
- "버그야", "테스트가 깨져", "왜 안 되지" → 버그 경로
- "리뷰해줘" → REVIEW, "커밋해", "PR 만들어" → SHIP
- "다음 진행해", "이어서" → 루트 `NEXT.md`의 `NEXT-ACTION` 블록에 적힌 단계

## service-autopilot에서 이어받기

08의 핸드오프 프롬프트를 붙여 넣거나, NEXT.md의 "GATE 완료" 블록을 보고 "다음 진행해"라고 하면 설계 승인이다. brainstorming을 다시 하지 않는다.
SPEC 입력은 `03-prd.md`(요구사항·상수 표) + `05-api-contract.md` + `08`의 착수 조건·첫 작업 3개만. `04·06·07`은 필요할 때 읽는다.
08의 `<model_hints>`는 위임할 때의 모델 초기값이다(위임 여부는 따로 정한다).

## 상태 기록

단계를 마치면 루트 `NEXT.md`의 `NEXT-ACTION` 블록을 `등급 · service-prompt-workflow · 단계 · 다음 할 일 1~3줄 · 산출물 경로`로 덮어쓴다.
SPEC.md와 tasks.md가 진실원이고, 구현은 새 세션에서 그 파일을 보고 시작해도 된다.

## 참조 파일

- `references/spec-template.md` — M 1쪽 SPEC과 L SPEC 목차. SPEC 단계에서 읽는다.
- `references/model-routing.md` — 위임 여부·상한, 작업 클래스별 모델. 서브에이전트를 띄우기 전에 읽는다.
- `references/skill-routing.md` — ponytail 배선과 스킬 간 충돌 우선순위. 설치 스킬이 바뀌었을 때 읽는다.
- `references/anti-patterns.md` — 거짓 진척·프론트 slop 체크리스트. REVIEW와 프론트 작업 때 읽는다.
- `references/evidence.md` — 규칙별 출처. 규칙을 바꿀 때 읽는다.
