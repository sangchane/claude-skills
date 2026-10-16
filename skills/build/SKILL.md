---
name: build
description: |
  무엇을 만들지 아는 상태의 구현·버그 수정을 규모에 맞는 단계로 진행하는 얇은 워크플로우. 실행 절차는 superpowers가 맡고,
  이 스킬은 등급별로 어떤 단계를 거칠지, dev:design 설계를 어떻게 이어받을지, ponytail·프론트 스킬을 어디에 붙일지만 정한다.
  사용 시점: 기능 하나·게임/도구 프로토타입 만들기(M), 새 서비스 설계를 마친 뒤 구현 착수(L 신규), 기존 저장소의 결제·인증·개인정보
  변경(L 변경), 버그 수정, 막히거나 지지부진한 기존 프로젝트 재정비("막혔어·살려줘"), "구현해·리뷰해줘·커밋해·다음 진행해". 한 문장으로 설명되는 변경(S)에는 부르지 않는다.
  도메인을 모르는 새 서비스는 먼저 dev:design.
argument-hint: "[요청 한 문장 또는 단계명]"
metadata:
  version: "0.10.0"
  updated: "2026-10-14"
---

# dev:build

superpowers가 실행 엔진이다. 이 스킬은 **규모에 맞게 단계를 고르고, 단계마다 어떤 스킬을 붙일지**만 정한다.
공통 작업 원칙·규모 판정·위임 상한은 dev 규칙(`rules.md`, 세션 시작 때 자동으로 들어온다)을 따른다.

## 목표와 검증 — 모든 등급 공통

세상에 없는 제품을 만들 때 사용자가 세부를 다 정해 줄 수 없다. 그래서 이 네 가지는 등급과 상관없이 내가 먼저 한다.
근거·사건은 `references/evidence.md` "2026-10-14 덧대기·검증 공백".

1. **목표 대조.** 요청을 `docs/goals.md`(목표 한 장)의 번호에 붙인다. 목표를 바꾸는 말이면 goals.md부터 고친다(rules.md). goals.md가 없거나 사용자 말이 목표를 바꾸면 `dev:design` 목표 수립·갱신(lite, 규칙 11)으로 조사해 세운다 — 사용자 말을 모아 옮겨 적는 것으로 대신하지 않는다.
2. **전제 도전.** 기능 요청을 받으면 만들기 전에, 도메인 조사(실무자·공식 자료)로 "이게 목표에 맞는 문제인가, 더 나은 형태가 있나"를 한 단락 제안한다. 사용자도 그 분야를 모르면 화면·기능 전에 **의미 표**(보여 줄 정보 → 그걸로 무엇을 판단하나 → 무엇과 비교해야 의미가 생기나 → 근거 출처)를 만든다. 이유: 요청을 그대로 받아 만들면 사용자가 기획자 역할을 떠안고, 데이터만 나열된 화면이 된다. (gstack `/office-hours`·`/plan-ceo-review` 방식)
3. **정답지 채점.** goals.md 완료 기준마다 *실제 세계의 정답*(실제 사례·공식 값·실무자 판정)과 대조하는 검증이 있어야 완료다. 내가 쓴 SPEC에서 만든 테스트는 "코드가 내 생각대로 도는가"만 보므로 완료 근거가 아니다. 정답지가 없으면 정답지를 모으는 것이 첫 작업이다. 결과는 맞은 수/전체로 보고한다. (BMAD TEA trace 방식: 요구 → 증명하는 검증을 표로 잇고 통과/우려/실패)
4. **눈가린 점검.** 화면이나 판정이 있는 기능은 REVIEW에서, 코드·SPEC·diff를 주지 않은 새 에이전트(`dev:reviewer`)에게 goals.md와 돌아가는 앱만 준다. 실제 브라우저로 "이 화면만 보고 목표의 판단을 할 수 있나, 어디서 막히나"를 스크린샷 증거와 함께 보고받는다. 이유: 내 SPEC을 아는 리뷰는 내 맹점을 그대로 공유한다. (gstack `/qa-only` 방식) 기능당 1회 — 같은 코드를 다시 확인하는 용도가 아니다.

## 등급별 경로

| 등급 | 단계 | 문서 | 리뷰 |
|---|---|---|---|
| **S** | 이 스킬 없이 바로 수정 → 검증 명령 1회 | 없음 | 요청 시만 |
| **M** | FRAME(3줄) → SPEC(1쪽) → BUILD → VERIFY → REVIEW → SHIP. 모르는 코드면 EXPLORE. 작업이 5개를 넘으면 PLAN, 아니면 SPEC의 완료 기준 순서대로 메인에서 구현 | `SPEC.md` 1쪽 | 기능 단위 1회 |
| **L 신규** | design GATE 뒤 **SPEC부터**(입력 `03·05·08`) → PLAN → BUILD → VERIFY → REVIEW → SHIP → REFLECT. PLAN 첫 작업 3개는 버티컬 슬라이스 | SPEC.md + tasks.md | 기능 단위 1회 + 고위험이면 보안 리뷰 |
| **L 변경** | 기존 저장소의 결제·인증·개인정보·마이그레이션. FRAME → EXPLORE → SPEC → PLAN → BUILD → VERIFY → REVIEW → SHIP | SPEC.md (+ tasks.md) | 기능 단위 1회 + `/security-review` |
| **버그** | 재현 → 원인 → 수정(`superpowers:systematic-debugging`) → VERIFY. 위험 모듈이면 REVIEW 1회 | 없음 | 위험 모듈만 |
| **재정비** | 막힌 기존 프로젝트. 아래 "재정비" 절차로 진단한 뒤 위 경로 중 하나로 넘긴다 | NEXT.md 블록 | 넘긴 경로를 따름 |

게임·도구 프로토타입(M)은 SPEC 전에 버리는 프로토타입으로 핵심 가설(재미·성능·조작감) 하나를 먼저 확인하고 결과를 SPEC에 반영한다.
진행 중 L 신호(돈·보안·개인정보·법, 되돌리기 어려운 결정)가 나오면 등급을 올리고 한 줄로 알린다.

## 재정비 (막히거나 지지부진한 기존 프로젝트)

1. **정리**: 커밋 안 된 변경이 있으면 WIP 커밋을 제안하고 승인받는다. NEXT.md가 없거나 CLAUDE.md가 200줄을 넘으면 `/dev:setup`을 먼저 권한다(사용자가 직접 부르는 스킬이다).
2. **진단**: 추측하지 않고 실행해서 사실을 모은다. 빌드·테스트·실행을 돌리고, 최근 커밋·NEXT.md·WORKLOG.md·README로 원래 목표를 확인한다.
   결과는 한 화면으로 보고한다. 되는 것 / 깨진 것(명령과 에러 한 줄) / 반쯤 된 것 / 목표 대비 남은 것 / 막힌 원인.
3. **원인 분류와 경로** (여러 개면 이 순서로):

   | 원인 | 신호 | 넘길 경로 |
   |---|---|---|
   | 특정 버그 | 같은 에러에서 반복해 멈춤 | 버그 분기 |
   | 회귀 | 한 곳을 고치면 다른 곳이 깨짐, 테스트가 없거나 적음 | 지금 동작을 특성 테스트로 먼저 고정한 뒤 M(돈·인증·개인정보면 L 변경) |
   | 결정 공백 | 도메인·요구를 몰라 무엇이 맞는지 정하지 못함 | 그 부분만 `dev:design lite` |
   | 범위 팽창 | 반쯤 된 기능이 여러 개, 끝이 안 보임 | 남은 것 중 출시에 꼭 필요한 3개로 M SPEC, 나머지는 NEXT.md "보류"로 |
   | 목표 표류 | 사용자 말마다 SPEC이 새로 생김(SPEC 폴더가 목표 수보다 훨씬 많음), 사용자가 "같은 말을 반복한다" | 사용자 원문을 입력으로 `dev:design` 목표 갱신(lite)으로 goals.md를 다시 세우고 열린 일을 거기 대조 |
   | 검증 공백 | 테스트는 통과하는데 결과가 실제와 맞는지 잰 적이 없음, 사용자가 "의미를 모르겠다" | 정답지 채점과 눈가린 점검부터. 기능 추가는 그 뒤 |

4. **확인 1회**: 진단 보고와 고른 경로·순서를 보여 주고 한 번 확인받는다. 방향이 크게 갈리는 결정이라서다. 그 뒤에는 넘긴 경로대로 진행하고 NEXT.md 블록에 등급·경로·다음 할 일을 적는다.
- "전부 다시 짜기"는 진단에서 되는 것이 거의 없고 사용자가 원할 때만 제안한다.

## 단계별로 붙이는 것

| 단계 | 하는 일 | 스킬 |
|---|---|---|
| FRAME | 사용자·문제·성공 기준·안 할 것을 3줄로. `superpowers:brainstorming`을 대신한다 | 없음 |
| EXPLORE | 관련 코드를 직접 읽고 file:line으로 인용. 여러 모듈을 넓게 훑을 때만 Explore 서브에이전트. 바깥 자료(라이브러리 이슈·공식 문서·영상 자막)가 필요하면 원문으로 읽는다. 연동·재현할 기능이 남의 앱·웹 안에 있으면 `references/reverse-engineering.md` 관문(robots·약관·봇 차단)부터 | `agent-reach`(설치돼 있으면, 없으면 WebFetch) · 남의 앱·웹 동작은 `rea`(설치돼 있으면) · 실행 파일은 rea+objdump(+IDA Free) · 브라우저 직접 조작은 `aside` 기본(설치돼 있으면, 사이트가 안 받으면 헤드리스) — `references/reverse-engineering.md` 3-1·3-2 |
| SPEC | `references/spec-template.md` (M 1쪽 / L 전체) | 화면이 있으면 `dev:ui` |
| PLAN | 작업 분해. 첫 3개는 버티컬 슬라이스, 그다음 위험 큰 것부터 | `superpowers:writing-plans` |
| BUILD | 같은 세션에서 구현. 코드 전에 ponytail 사다리 | `superpowers:executing-plans` · `superpowers:test-driven-development` · `ponytail:ponytail` · 화면이면 `dev:ui` |
| VERIFY | 테스트·빌드·린트·(UI면) 스크린샷을 실행하고 결과를 붙인다. 완료 기준에 정답지 채점이 있으면 맞은 수/전체를 붙인다. 사용자 손이 필요한 확인은 스케줄·로그로 돌게 해 두고 다음에 내가 읽는다. 실패하면 근본 원인 | `superpowers:verification-before-completion` · 실패 시 `superpowers:systematic-debugging` |
| REVIEW | diff·SPEC·goals.md를 주고 새 컨텍스트에서 정확성 1회 + 화면·판정이 있으면 눈가린 점검 1회(위 공통 4). 과잉설계는 선택 | `/code-review` · `ponytail:ponytail-review` · 고위험 `/security-review` |
| SHIP | 작은 커밋, 한글 설명형 메시지, PR. 배포는 남은 작업 묶음 끝에 한 번 — 뒷작업이 남았는데 배포를 앞에 두면 두 번 배포한다 | `superpowers:finishing-a-development-branch` |
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

## dev:design에서 이어받기

08의 핸드오프 프롬프트를 붙여 넣거나, NEXT.md의 "GATE 완료" 블록을 보고 "다음 진행해"라고 하면 설계 승인이다. brainstorming을 다시 하지 않는다.
SPEC 입력은 `03-prd.md`(요구사항·상수 표) + `05-api-contract.md` + `08`의 착수 조건·첫 작업 3개만. `04·06·07`은 필요할 때 읽는다.
08의 `<model_hints>`는 위임할 때의 모델 초기값이다(위임 여부는 따로 정한다).

## 상태 기록

단계를 마치면 루트 `NEXT.md`의 `NEXT-ACTION` 블록을 `등급 · dev:build · 단계 · 다음 할 일 1~3줄 · 산출물 경로`로 덮어쓴다.
SPEC.md와 tasks.md가 진실원이고, 구현은 새 세션에서 그 파일을 보고 시작해도 된다.

## 참조 파일

- `references/spec-template.md` — M 1쪽 SPEC과 L SPEC 목차. SPEC 단계에서 읽는다.
- `references/model-routing.md` — 위임 여부·상한, 작업 클래스별 모델. 서브에이전트를 띄우기 전에 읽는다.
- `references/skill-routing.md` — ponytail 배선과 스킬 간 충돌 우선순위. 설치 스킬이 바뀌었을 때 읽는다.
- `references/anti-patterns.md` — 거짓 진척·프론트 slop 체크리스트. REVIEW와 프론트 작업 때 읽는다.
- `references/reverse-engineering.md` — 남의 앱·웹 동작 파악: 관문(robots·약관·봇 차단 → 허용·애매·금지) → 공유 URL·사용자가 연 페이지 읽기 → 필요할 때만 REA. EXPLORE에서 외부 서비스 데이터가 필요할 때 읽는다.
- `references/evidence.md` — 규칙별 출처. 규칙을 바꿀 때 읽는다.
