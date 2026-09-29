# 근거 매핑 (Evidence Map)

이 워크플로우의 모든 규칙·단계는 아래 1차 출처에서 왔다. "인기 있어서"가 아니라
**여러 권위 출처가 수렴**할 때만 규칙으로 승격했다(solution-planner ETHOS와 동일 기준).

## 출처와 권위

| 출처 | 유형 | 권위 신호 | 제공한 것 |
|---|---|---|---|
| **gstack** (garrytan/gstack) | 오픈소스 하네스 | Garry Tan(YC CEO), ~120k★, MIT | 스프린트 모델, 페르소나 phased skill, hard gate, forcing question, completion enum, 핸드오프 아티팩트, 라우터, 품질 게이트, ETHOS 프리앰블, User Sovereignty |
| **Anthropic — Prompt engineering** | 1차 벤더 문서 | 대상 모델 제작사 | 명시성, 이유 제공, 예시(few-shot), XML 구조화, 역할, CoT, "하지마 대신 해라" |
| **Anthropic — Claude Code best practices** | 1차 도구 문서 | 대상 도구 제작사 | Explore→Plan→Code→Commit, 루프 닫기(증거), TDD Writer/Reviewer, CLAUDE.md, 인터뷰→SPEC.md, 컨텍스트 위생, 적대적 리뷰 |
| **Anthropic — Building effective agents / Context engineering** | 1차 엔지니어링 | 널리 인용 | 단순함 우선, 워크플로우 5패턴(chaining/routing/parallel/orchestrator/evaluator-optimizer), just-in-time 컨텍스트, 서브에이전트 |
| **OpenAI — Prompt engineering guide** | 1차 벤더 문서 | 업계 표준 레퍼런스 | 6전략(명확한 지시·참조 텍스트·작업 분할·생각할 시간·외부도구·체계적 테스트) |
| **GitHub spec-kit** | 오픈소스 | GitHub 공식, ~118k★ | Spec-Driven Development: constitution→specify→clarify→plan→tasks→analyze→implement, "명세가 진실원", test-first Article III, 작은 증분 |
| **Harper Reed — LLM codegen workflow** | 실무자 워크플로우 | Simon Willison 등 인용, 사실상 커뮤니티 표준 | idea honing(한 번에 한 질문)→prompt_plan.md+todo.md→실행 |
| **promptingguide.ai** (dair-ai) | 기법 색인 | ~76k★ | 기법 카탈로그(zero/few-shot, CoT, self-consistency, ReAct, RAG, reflexion) |
| **MengTo/Skills** | 스킬 라이브러리 | Design+Code 창립자, ~1.1k★ | SKILL.md 포맷(Use When/Workflow/Guardrails/Avoid), "prompts are assets", 프론트 slop 체크리스트, design dial |
| **f/awesome-chatgpt-prompts** | 프롬프트 모음 | ~165k★ | 역할/페르소나 프롬프트 대중화 |
| **DietrichGebert/ponytail** | 오픈소스 스킬·플러그인 | 121.6k★ (2026-09-03), MIT, v4.9.0, 자체 에이전틱 벤치마크(LOC −54%·비용 −20%·시간 −27%·안전 100%) | BUILD `<ladder>` 결정 사다리 7단, REVIEW의 과잉설계 전용 패스(`ponytail-review` 형식), "검증 하나는 남긴다" |
| **obra/superpowers** | 오픈소스 스킬 플러그인 | 280.8k★ (2026-09-03), MIT, v6.3.0 설치 2026-09-07 | PLAN 이후 실행 엔진: writing-plans(2~5분 작업·자리표시자 금지), executing-plans / subagent-driven-development, test-driven-development, systematic-debugging, verification-before-completion, requesting/receiving-code-review, finishing-a-development-branch. 이 스킬의 4)~8) 템플릿은 미설치 시 대체용으로 강등 |
| **affaan-m/everything-claude-code** (ecc) | 스킬 마켓플레이스 | 246.4k★ (2026-09-03), 설치 v1.10.0 | `skill-routing.md`의 단계별 1순위 스킬(product-lens·blueprint·tdd-workflow·verification-loop·git-workflow 등) |
| **Anthropic — Skill authoring best practices / agentskills.io** | 1차 벤더 문서·오픈 스펙 | 대상 도구 제작사 | `metadata`·`argument-hint` 프론트매터, 시간 민감 수치는 근거 파일로, `evals/evals.json` 형식 |
| **AGENTS.md 표준** | 오픈 규약 | Linux Foundation, >20k repos | 저장소 지침 파일 규약(CLAUDE.md 동종) |
| **Anthropic `claude-api` 번들 스킬** (Claude Code 2.1.259, 모델표 캐시 2026-06-24) + Agent 도구 `model` 파라미터 | 1차 벤더 문서 · 도구 스키마 | `references/model-routing.md`: 작업 클래스→등급 표, "캐스케이드 전에 최상위 모델+낮은 effort", "완료된 작업당 비용", 캐시는 모델 단위 |

## 13개 공통분모 원칙 → ETHOS 매핑

수렴 출처가 3개 이상인 것만 규칙으로 승격했다. 0.4.1(2026-09-08)부터 SKILL.md에는 8·4·6만 ETHOS 1·2·3으로 남는다.
나머지는 Fable 5.1에서 학습된 기본값이거나(1·2·3·5·9) superpowers·ponytail이 실행 시점에 주입한다(7·10).
Anthropic 번들 `claude-api` 스킬의 prompt-audit 기준("모델이 이미 아는 것은 지시가 아니라 비용")에 따라 뺐다. 아래 번호는 원래 번호다.

1. 명시·구체 — Anthropic, OpenAI, Claude Code, Brex
2. 이유(why) — Anthropic, OpenAI, Claude Code
3. 탐색/계획과 구현 분리 — Claude Code, spec-kit, Harper Reed, OpenAI
4. 명세·계획 파일화 — spec-kit, gstack, Harper Reed, Claude Code
5. 작게 쪼개 개별 검증 — OpenAI, spec-kit, prompt chaining, Harper Reed
6. 루프 닫기(증거) — Claude Code, OpenAI, evaluator-optimizer, spec-kit
7. 테스트 우선 — Claude Code, spec-kit Article III
8. 사용자 주권(한 번에 하나) — gstack, Claude Code
9. 컨텍스트 위생 — Claude Code, Context engineering
10. 단순함 우선 — Building effective agents, spec-kit

+ 구조화(XML/구분자), 역할/페르소나, 예시(few-shot), 사고 유도(CoT), 근거+독립 리뷰는
프롬프트 작성 기법으로 각 단계 템플릿에 반영.

## Anthropic Fable 5.1 공식 지침 반영 (2026-09-09)

출처: Claude Code 번들 `claude-api` 스킬 `shared/model-migration.md` "Migrating to Claude Fable 5.1" 두 절.
- 반영: BUILD 템플릿에 scope/test-coverage 지침(요청 밖 수정·테스트 증식 억제). catch-up WORKLOG에 압축 요약 보존 항목.
- 반영 안 함(하네스가 이미 적용): 진행 상황 알림, 독립 도구 호출 묶음, 승인 작업 끝까지(autonomy), 대화 기록 추가 전용 — Claude Code 시스템 프롬프트가 같은 문장을 넣는다. 스킬에 다시 쓰면 중복.
- 보류(autopilot 실행 중이라 나중에): 긴 산출물은 effort high(`effort:` 프론트매터), 검토관·서브에이전트 effort 표, 진척 주장은 도구 결과로 대조.

## Anthropic Opus 5.5 공식 지침 반영 (2026-09-29)

출처: platform.claude.com "Prompting Claude Opus 5.5", "Prompting Claude Opus 5", "Migrating to Claude Opus 5.5", "Effort",
Claude Code prompt-caching·sub-agents 문서 (모두 2026-09-29 확인).
- 반영: 위임 기본값을 메인으로, 위임 조건·상한(동시 3, 요청당 5) 명시, VERIFY·소규모 기계적 작업 위임 제거,
  BUILD 1순위를 `executing-plans`로, EXPLORE 1순위를 직접 Read/Grep으로. 근거 문장: "delegates to subagents more readily …
  it multiplies cost and time when applied to small tasks … give explicit guidance on which scenarios warrant delegation,
  or set deterministic caps" (Prompting Claude Opus 5).
- 반영: 서브에이전트 effort는 정의 파일 `effort:`로 준다(이전 문장 "effort를 따로 못 준다"는 틀림 — sub-agents 문서에 `effort` 필드가 있다).
- 사실 갱신: Opus 5.5 기본 effort medium(Opus 5는 high), medium ≥ Opus 5 high, xhigh·max는 측정된 이득이 있을 때만,
  effort 변경은 Opus 5.5·Fable 5.1에서 캐시 유지.
- 회귀 미실행: 이 변경은 `eval/` 대리 A/B를 돌리지 않았다. 다음 구현 작업에서 서브에이전트 수·토큰을 이전 기록과 비교한다.

## 규모 등급 S·M·L (2026-09-29)

출처(2026-09-29 확인): Claude Code "Best practices"("If you could describe the diff in one sentence, skip the plan", 큰 기능은 인터뷰 → SPEC.md → 새 세션,
"Chasing every finding leads to over-engineering"), Google "Design Docs at Google"(구현 방법만 적는 문서면 코드를 먼저, 작은 개선은 1~3쪽),
Google eng-practices "Small CLs"(약 100줄), Amazon Type 1/Type 2 결정, Basecamp Shape Up(appetite·circuit breaker), Kiro Quick Spec,
게임 프로토타입 → 버티컬 슬라이스(Rami Ismail "Levelling The Playing Field").
- 반영: 등급별 경로 표(S 문서·리뷰 없음, M 1쪽 SPEC + 리뷰 1회, L 전체), 게임·도구 프로토타입은 버리는 프로토타입 먼저, NEXT.md 갱신, "다음 진행해" 라우팅.
- 미실행: `eval/` 대리 A/B. 다음 M 작업에서 단계 수·토큰을 이전 기록과 비교한다.

## 얇은 층으로 축소 (0.7.0, 2026-09-29)

- 근거: superpowers(obra/superpowers)가 계획·TDD·디버깅·검증·리뷰·브랜치 마무리를 이미 제공한다. 이 스킬의 고유 가치는 등급별 단계 선택,
  autopilot 핸드오프, ponytail·프론트 배선뿐이라 나머지를 지웠다. 단계별 복붙 템플릿(221줄)은 superpowers 없는 PC용 대체였는데 모든 PC에 설치하므로 삭제.
- ETHOS 1~3 삭제: 1(사용자 주권)·3(증거로 완료)은 전역 CLAUDE.md 작업 원칙과 superpowers verification이, 2(파일이 진실원)는 "상태 기록" 절이 대신한다.
- SPEC 자기채점 루프(7/10 미만이면 최대 3회 재작성) 삭제: "Prompting Claude Opus 5" — 이 세대는 스스로 검증하며 명시적 재확인 지시는 비용만 늘린다.
- evals.json 1·2번 단언을 새 경로에 맞게 수정. 회귀 미실행.

## ecc 구현 라우팅 제거 (2026-09-29)

- 실측(사용자 PC `skill_catalog.py --unassigned`): 항상 로드 설명문 약 74,490자(추정 1만 9천 토큰), ecc가 스킬 181·명령 76·에이전트 47.
- 구현 라우팅의 ecc 49개는 대부분 언어별 패턴·리뷰어·테스트 변형으로 superpowers·번들 명령과 겹치고, 효과를 잰 기록이 없다. 설계 쪽(autopilot)은
  9월 3일 스모크에서 ecc 조합이 값을 했으므로 유지하되, 플러그인은 그 프로젝트에서만 켠다(Claude Code `enabledPlugins` 범위: user < project < local).
- santa-method(ecc) 대신 `/security-review` + 다른 등급 fresh-reviewer 1명.

## 주의(변동 사항)

- Anthropic의 고전 "프리필(assistant 턴 미리 채우기)" 기법은 **Claude 4.6+에서 미지원**.
  대체: 시스템 프롬프트 직접 지시 / 구조화 출력 / 도구 호출. 템플릿은 프리필을 쓰지 않는다.
- 스타 수·버전은 조사 시점(2026-07, ponytail·ecc·Anthropic 행은 2026-09-03) 값이며 규칙의 근거는 "수렴"이지 "인기"가 아니다.
