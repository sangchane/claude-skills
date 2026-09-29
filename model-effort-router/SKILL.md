---
name: model-effort-router
description: |
  메인 세션 모델은 그대로 두고, 요청을 작업 클래스(모델)와 난이도(effort)로 판정해 위임이 이득인 부분만 알맞은
  모델·effort의 서브에이전트에 넘긴다. 모델 전환 없이 캐시를 지키면서 비용과 추론 강도를 맞춘다.
  사용 시점: 코딩·분석·문서 작업을 시작할 때, 난이도가 섞인 작업을 나눌 때, "이거 어떤 모델로 해야 해?",
  "얼마나 깊게 봐야 해?". 설계 파이프라인(service-autopilot)·구현 파이프라인(service-prompt-workflow) 안에서는
  각자의 references/model-routing.md가 우선한다.
metadata:
  version: "0.2.0"
  updated: "2026-09-29"
---

# model-effort-router

메인 세션은 사용자가 고른 모델로 계속 간다(권장: Opus 5.5). Claude는 `/model`·`/effort`를 직접 실행할 수 없다.
스킬 프론트매터 `model:`·`effort:`는 그 턴에만 적용되므로, 작업 일부만 모델·effort를 달리하는 실용적인 수단은 서브에이전트 위임이다. 서브에이전트는 별도 컨텍스트에서 돌고 결과만 메인 대화 끝에 붙어
메인 캐시가 유지된다. 대부분의 요청은 위임 없이 메인에서 끝난다.

## 1. 판정 (응답 첫 줄, 한 줄)

형식: `라우팅: 메인 <effort> | 위임: <모델>·<effort> <무엇> — <이유 한 구절>` (위임이 없으면 `위임 없음`)

### effort — 얼마나 깊게

| effort | 이런 요청 |
|---|---|
| low | 파일 찾기, 이름 변경, 포맷 정리, git 조작, 짧은 사실 답변 |
| medium | 범위가 분명한 수정, 기능 추가, 문서 요약. Opus 5.5 기본값이며 Opus 5의 high와 같거나 낫다 |
| high | 여러 파일에 걸친 변경, 원인 불명 버그, 설계 결정, 긴 문서 작성·검토, 법률·수치 검증 |
| xhigh · max | 한 단계 낮은 effort로 해 봤더니 부족했던 작업만. 공식 가이드는 품질 향상을 확인한 경우에만 쓰라고 한다 |

긴 산출물(수십 KB 문서)은 xhigh보다 high가 낫다. 생각을 줄이려면 지시문보다 effort를 낮추는 쪽이 확실하다("Prompting Claude Opus 5.5").

### 모델 — 위임한다면 누구에게

| 작업 클래스 | 예 | 모델 |
|---|---|---|
| 기계적 대량 | 수십 파일 리네임·포맷·문구 일괄 | `haiku` |
| 패턴 반복 묶음 | 독립 CRUD·화면·테스트 여러 개, 대용량 원문 읽기·조사 | `sonnet` |
| 판단 집약 | 불변식, 동시성, 인증·권한, 마이그레이션, 설계 판단 | `opus` |
| 장기 조사 | 여러 저장소·수십 파일을 오래 파고드는 원인 추적 | `fable` (Opus 5.5의 2.5배 가격) |

클래스 기준은 `service-prompt-workflow/references/model-routing.md`와 같다. 두 클래스에 걸치면 높은 쪽.

## 2. 위임할지 먼저 정한다

- **위임한다**: 크고 서로 독립적이라 나눠서 이득인 작업, 메인 컨텍스트를 크게 잡아먹는 대용량 읽기,
  다른 모델·effort가 분명히 이득인 작업.
- **위임하지 않는다**: 도구 호출 몇 번으로 끝나는 작업, 테스트·빌드 실행과 결과 확인, 방금 한 작업을 다시 확인하는 용도.
- **상한**: 동시 3개, 한 요청에서 새로 띄우는 서브에이전트 5개. 넘을 것 같으면 묶거나 사용자에게 먼저 알린다.

## 3. 위임하는 법

1. 모델만 다르면 Agent 도구에 `model`을 준다(`general-purpose` 또는 알맞은 타입).
2. effort도 다르면 에이전트 정의 파일을 쓴다(호출로는 effort를 못 준다). 호출 때 준 `model`이 정의 파일보다 우선한다.
   - `deep-worker`(effort high) — 판단 집약·장기 조사. 호출 시 `model: opus` 또는 `fable`.
   - `quick-worker`(effort low) — 기계적 대량 작업. 호출 시 `model: haiku` 또는 `sonnet`.
3. 목표·제약·관련 파일 경로·확인된 사실·검증 명령만 준다(서브에이전트는 대화 기록을 못 본다). 같은 등급 작업은 묶어서 넘긴다.
4. 결과는 메인이 확인하고 보고한다. 독립 검토가 필요하면 기능 단위로 한 번, `fresh-reviewer`로.
5. 위임한 작업이 두 번 실패하면 한 등급 올린다. 그래도 실패하면 명세 문제로 보고 사용자에게 알린다.

## 4. 메인 세션 자체를 바꿔야 할 때

작업 전체가 다른 모델·effort에 맞으면 판정 줄 다음에 한 줄로 권한다. 실행은 사용자가 한다.
- `/effort <level>` — Opus 5.5·Fable 5.1에서는 바꿔도 캐시가 유지된다.
- `/model <alias>` — 첫 응답이 캐시 없이 대화 전체를 다시 읽는다. 새 작업을 시작할 때만 권한다.

## 5. 알아둘 사실 (확인 2026-09-29, Anthropic 공식 문서)

- 별칭: `opus` = Opus 5.5, `sonnet` = Sonnet 5, `haiku` = Haiku 4.5, `fable` = Fable 5.1.
- 가격(입력/출력 $ per 1M): Fable 10/50 · Opus 5.5 4/20 · Sonnet 5 2/10 · Haiku 4.5 1/5.
- 기본 effort: Opus 5.5 medium, Fable 5.1·Sonnet 5 high. Haiku 4.5는 xhigh·max 미지원.
- 캐스케이드 전에 "상위 모델 + 낮은 effort"를 먼저 재 본다. 완료된 작업당 비용으로 판단한다.

## 6. 준비 (PC당 1회)

`~/.claude/agents/deep-worker.md`, `quick-worker.md`가 없으면 사용자에게 묻고 `~/.claude/skills/_tools/agents/`에서 복사한다.
복사 후 새 세션에서 인식된다. 예전 `opus-deep.md`·`opus-quick.md`와 `opus-effort-router` 스킬이 남아 있으면 지운다.
