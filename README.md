# 개인 Claude Code 스킬 모음

`~/.claude/skills/`에 두고 쓰는 **개인 제작 스킬 저장소**다. 어느 PC에서든 이 저장소를
`~/.claude/skills`로 clone하면 Claude Code가 세션 시작 시 자동으로 인식한다.

형식은 Anthropic Agent Skills 표준(agentskills.io 스펙 + Anthropic 작성 가이드 + Claude Code 확장)을 따른다.
버전·갱신일은 각 SKILL.md 프론트매터 `metadata`에 있다. 모델 기준은 **Opus 5.5 메인 세션**(2026-09-29 점검)이다.

## 쓰는 법 — 그냥 말하면 된다

스킬 이름을 부를 필요가 없다. 역할은 세 층으로 나뉜다.

| 층 | 무엇 | 하는 일 |
|---|---|---|
| **전역 CLAUDE.md** (항상 로드) | `_tools/CLAUDE.global.md`를 `~/.claude/CLAUDE.md`로 복사 | 작업 원칙(Karpathy 가이드라인의 Opus 5.5판), 규모 판정, superpowers 경계, 모델·위임 규칙 |
| **NEXT.md** (프로젝트 루트) | 스킬이 단계마다 덮어쓰는 "지금 어디까지 왔나" 블록 | "다음 진행해"·"이어서"가 여기서 이어진다. catch-up 훅이 세션 시작 때 주입 |
| **스킬** (필요할 때만 로드) | autopilot · 구현 워크플로우 · 프론트 취향 | 단계별 절차 |

| 등급 | 이런 요청 | 흐름 |
|---|---|---|
| **S** | "로그 한 줄 추가해", "이 변수 이름 바꿔" — 한 문장으로 설명되는 변경 | 바로 구현 → 검증 명령 1회. 문서 없음 |
| **M** | "로그인에 소셜 로그인 붙여줘", "테트리스 만들어줘" — 기능 하나, 미니 프로젝트 | 1쪽 SPEC → 구현 → 검증 → 리뷰 1회. 게임은 버리는 프로토타입으로 재미부터 확인 |
| **L 신규** | "회의실 예약 서비스 만들고 싶어", 모르는 도메인, 되돌리기 어려운 설계 결정 | autopilot 설계 패키지 → 구현 워크플로우 SPEC부터(버티컬 슬라이스 먼저) |
| **L 변경** | 기존 저장소의 결제·인증·개인정보·마이그레이션 변경 | autopilot 없이 구현 워크플로우 전체 경로 + 보안 리뷰 |
| 버그 | "결제 모듈 버그 고쳐줘" | 등급과 별개로 디버깅 분기(재현 → 원인 → 수정), 위험 모듈이면 리뷰 1회 더 |

응답 첫 줄에 `등급: M — 기능 하나, 파일 여러 개`처럼 판정이 나온다. 틀렸으면 "S로 해"라고만 하면 된다.
뭘 불러야 할지 궁금하면 `/sk <하고 싶은 것>`.

## 구성

| 스킬·파일 | 역할 | 발동 |
|---|---|---|
| `service-autopilot` | L 신규: 한 줄 아이디어 → 설계 패키지(PRD·아키텍처·API·테스트·운영) | 자동 |
| `service-prompt-workflow` | M·L 구현과 버그: 등급별로 단계를 건너뛰는 구현·검증·리뷰·배포 | 자동 |
| `frontend-design-taste` | 웹 UI의 AI 티 제거, 하드룰 강제 | 자동(프론트 작업 시) |
| `catch-up` | 프로젝트에 CLAUDE.md·AGENTS.md·NEXT.md·세션 훅 구조를 1회 세팅 | `/catch-up` |
| `sk` | 맞는 스킬 최대 3개 추천 | `/sk 문구` |
| `_tools/CLAUDE.global.md` | 전역 `~/.claude/CLAUDE.md` 원본: 작업 원칙·이어가기·규모 판정·superpowers 경계·모델·위임 (32줄) | 항상 |
| `_tools/agents/` | 서브에이전트 정의(fresh-reviewer·deep-worker·quick-worker) | 위임할 때 |
| `_tools/skill_catalog.py` | 설치 스킬 카탈로그 + 라우팅 표 정합성 검사 | 수동 |
| `learned/` | 세션에서 배운 패턴을 스킬로 쌓는 자리(현재 비어 있음) | — |
| `archify`, `graphify` | 저장소 밖에서 따로 설치해 쓰는 외부 스킬(graphify는 `graphify install`로 재생성, git 추적 제외) | 자동 |

**플러그인 구성 (2026-09-29)**: superpowers(구현 절차) · ponytail(단순함 사다리) · claude-dashboard는 켜 두고,
ecc는 **평소 꺼 두고 autopilot을 돌리는 프로젝트에서만 켠다**(스킬 181개 설명문이 매 세션 로드된다), claude-mem은 끈다(NEXT.md·WORKLOG·자동 메모리와 중복).

## 흐름 (큰 그림)

```
요청 ─→ 전역 CLAUDE.md 규모 판정 ─┬─ S ─→ 스킬 없이 바로 수정 → 검증 명령 1회
                                   ├─ M ─→ service-prompt-workflow: FRAME 3줄 → SPEC(1쪽) → BUILD → VERIFY → REVIEW 1회
                                   ├─ L 신규 ─→ service-autopilot: A0~A7 + GATE ─→ service-prompt-workflow: SPEC부터 (버티컬 슬라이스 먼저)
                                   ├─ L 변경 ─→ service-prompt-workflow: FRAME~REFLECT 전체 + 보안 리뷰
                                   └─ 버그 ─→ service-prompt-workflow: 디버깅 분기
                                                                                         └─ 화면이 있으면 frontend-design-taste
각 단계 끝 ─→ 루트 NEXT.md 갱신 ─→ 다음 세션 시작 때 훅이 주입 ─→ "다음 진행해"로 이어감
위임 ─→ 기본은 메인 세션. 크고 독립적인 작업·대용량 읽기·최종 리뷰만 서브에이전트(동시 3·요청당 5)
```

비유하면: **작은 수리는 바로 고치고(S), 방 하나 리모델링은 한 장짜리 도면으로(M), 집을 새로 지을 때만 설계 사무소(autopilot)를 부른다(L).**
공사 일지(NEXT.md)가 현장에 붙어 있어서 다음 날 누가 와도 이어서 일한다.

## 현업 근거 (2026-09-29 조사)

- **무게는 되돌리기 어려운 정도에 비례**: Amazon Type 1/Type 2 결정, Google은 불확실성 질문 3개 이상일 때만 설계 문서
  ("구현 방법만 적고 대안이 없으면 코드를 먼저 써라"), Kiro Quick Spec, Claude Code "diff를 한 문장으로 설명할 수 있으면 계획 생략".
- **문서는 한 번 쓰고 고쳐 가며 쓴다**: Google 설계 문서는 구현 중 갱신하는 living doc. 단계마다 전체 재검토를 하지 않는다.
- **검증은 실행으로**: Claude Code "검증할 수단(테스트·빌드·스크린샷)을 줘라", 게임은 플레이테스트.
- **작게, 시간 상한**: Google 변경당 약 100줄, Shape Up 6주 초과 시 연장 없이 중단, 게임은 프로토타입 → 버티컬 슬라이스 → 제작.
- **리뷰는 1회**: "지적을 전부 쫓으면 과잉설계가 된다"(Claude Code best practices).

---

## 1. service-autopilot — 기획·설계 오토파일럿

**L 신규 전용. 한 줄 아이디어를 "구현 착수 가능한 설계 패키지"로 바꾼다.** AI가 스스로 조사하고, 사각지대를 찾아 덮고,
가정으로 못 덮는 위험한 결정만 객관식 최대 5문항으로 **딱 1번** 묻는다.

- **언제 쓰나**: 새 서비스, 모르는 도메인, 되돌리기 어려운 설계 결정. 기능 하나·미니 프로젝트·게임 프로토타입(S·M), 기존 저장소의 결제·인증 변경(L 변경), 버그에는 쓰지 않는다.
- **파이프라인**: A0 SEED → A1 RECON(조사) → A2 INTERROGATE(사각지대 심문, 질문 1회) → A3 PRD → A4 아키텍처+위협모델(STRIDE)
  → A5 API계약+ERD → A6 테스트설계 → A7 배포/관측성 → GATE(새 컨텍스트 적대적 검토).
- **단계별 스킬 라우팅** (`references/skill-routing.md`): 단계 진입 시 설치된 전문 스킬을 호출한다.
  예: A1은 `ecc:research-ops`, A4는 `ecc:architecture-decision-records`+`ecc:security-review`, A5는 `ecc:api-design`,
  A6은 `ecc:tdd-workflow`, A7은 `ecc:deployment-patterns`. ecc는 평소 꺼 두므로 꺼져 있으면 이 프로젝트에서 켜라고 한 줄 안내하고, 안 켜면 대체 절차로 간다. 사용 기록은 decision-log에 남는다.
- **단계 진입 사전조사**: A3~A7은 각 단계의 결정에 필요한 근거를 정량(숫자+출처+확인일)·정성(실무자 인용)·사용자 영향 3줄로 산출물 상단에 남긴다.
- **단계별 모델 라우팅** (`references/model-routing.md`): 위임은 세 곳뿐이다 — A1 조사 `sonnet`, A4 독립 검토·GATE 검토관은 생성 모델 이상.
  판단 단계(A2~A5)는 위임하지 않는다. 08 핸드오프의 `<model_hints>`는 구현 쪽이 위임할 때 쓸 모델이다.
- **강도 spike/lite/full**: 플랫폼·범위·핵심 루프가 미확정이면 spike(엔진+시뮬 워킹 스켈레톤 먼저, 10만 토큰). 아니면 A0에서 신호(돈·안전·법·민감정보, 외부 연동 2개↑, 사용자 100명↑, 하드웨어, 팀 2명↑, "납품")로 lite/full 판정.
  lite는 질문 0·검색 ≤5·위협모델 조건부·GATE 자기 점검(실측 20만, 상한 25만). full은 상한 80만(서브에이전트 포함). `/service-autopilot spike|lite|full …`로 강제 가능.
- **자기 선언 검증**: GATE 전에 `python scripts/check_package.py autopilot/<slug>` — FR→05 커버리지, SC→06 시나리오, 미결정, register 마킹,
  버전 전파를 스크립트가 센다. CRITICAL이면 GATE 진입 금지.
- **개정 전파·상수 표**: 산출물마다 `버전:`, 04~07은 `기준 03 v`. 숫자는 03 상수 표에만.
- **착수 자산**: A3 화면 스케치 1장, A7 디렉터리 구조·`.env.example`(값 없음)·첫 작업 3개(워킹 스켈레톤).
- **예산·재개**: GATE 재실행 1회, 끊기면 없는 첫 파일의 단계부터 재개, 런 끝에 비용 기록. 단계마다 루트 `NEXT.md`를 갱신하므로 다음 날 "다음 진행해"로 이어진다.
- **산출물**: `autopilot/<slug>/`의 `00-seed.md` ~ `08-readiness-report.md` + `decision-log.md`.
- **평가**: `eval/PROTOCOL.md`(블라인드 pairwise A/B, 동결 시드 10개) + `evals/evals.json`(skill-creator 호환).

```
> 회의실 예약 서비스 만들고 싶어           ← 자동 발동
> /service-autopilot 라즈베리파이로 IP 카메라 모니터링 서비스
```

---

## 2. service-prompt-workflow — 구현 워크플로우 (superpowers 위의 얇은 층)

**실행 절차는 superpowers가 맡고, 이 스킬은 규모에 맞게 단계를 고르고 단계마다 어떤 스킬을 붙일지만 정한다.** (0.7.0, 77줄)

- **등급별 경로**: S는 이 스킬 없이 처리. M은 FRAME 3줄 → 1쪽 SPEC → BUILD → VERIFY → REVIEW 1회 → SHIP
  (게임·도구 프로토타입은 버리는 프로토타입으로 핵심 가설부터). L 신규는 autopilot 뒤 SPEC부터, 첫 작업 3개는 버티컬 슬라이스.
  L 변경(기존 저장소의 결제·인증 등)은 전체 경로 + `/security-review`. 버그는 `superpowers:systematic-debugging`.
- **단계별로 붙이는 것**: PLAN `superpowers:writing-plans`, BUILD `superpowers:executing-plans`(같은 세션) + TDD + `ponytail:ponytail` 사다리
  (+ 화면이면 `frontend-design-taste`), VERIFY `verification-before-completion`, REVIEW `/code-review` 1회(+ `ponytail-review` 선택),
  SHIP `finishing-a-development-branch`. FRAME이 `brainstorming`을 대신한다.
- **위임**: 기본은 메인 세션. `subagent-driven-development`는 크고 독립적인 작업만, 요청당 작업 1개. 상한·모델은 `references/model-routing.md`.
- **SPEC 템플릿**: `references/spec-template.md` (M 1쪽 / L 전체). 옛 단계별 복붙 템플릿은 superpowers와 겹쳐 삭제했다(git 기록에 있음).
- **이어가기**: 단계마다 루트 `NEXT.md` 갱신, "다음 진행해"는 거기 적힌 단계로.

```
> 테트리스 만들어줘             ← M: 프로토타입 → 1쪽 SPEC → 구현
> 이 스펙대로 구현해            ← BUILD
> 결제 모듈 버그 고쳐줘         ← 버그 경로
```

---

## 3. frontend-design-taste — 프론트엔드 디자인 취향

**웹 UI에서 "AI가 만든 티(slop)"를 없애고 의도된 고급 결과를 강제하는 취향 하네스.** React·Tailwind·Zustand 특화.
3개 dial(밀도·모션·파격)과 프로파일(관제 8 / 제품 UI 5 / 랜딩 3)을 정하고, 하드룰 위반은 반려한다.
service-prompt-workflow의 BUILD·REVIEW에 프론트가 포함되면 자동 참조된다.

---

## 4. catch-up — 세션 이어받기 부트스트랩 (1회 세팅, 사용자 호출 전용)

**"지난 작업 확인" 스킬이 아니다.** 프로젝트에 얇은 `CLAUDE.md`(행동규칙 + `@AGENTS.md`) · `AGENTS.md`(크로스툴 단일 원본) ·
`NEXT.md`(다음-할일) + SessionStart 훅 · 폴더별 `CLAUDE.md` · `WORKLOG.md` 구조를 **처음 한 번** 깔아 주는 스킬이다.
그 뒤로는 세션 시작마다 훅이 `NEXT.md`의 현재 작업 블록을 자동 주입하므로, "지난 작업 이어서"는 아무 스킬도 부를 필요가 없다.
상세 이력이 필요하면 `WORKLOG.md`를 읽는다. autopilot·구현 워크플로우가 단계마다 이 블록을 덮어써서 설계 → 구현이 자연스럽게 이어진다.

```
> /catch-up                                   ← diff를 먼저 보여주고 승인 후 적용
> /catch-up --tools antigravity,cursor
```

---

## 5. sk — 스킬 추천기 (사용자 호출 전용)

스킬 이름을 몰라도 되게 하는 얇은 스킬. 라우팅 표 2개(사람이 근거를 단 1순위 후보)를 먼저 보고,
없으면 설치 카탈로그를 의미로 훑어 최대 3개를 이유·실행 명령과 함께 추천한다.

```
> /sk 회의실 예약 서비스 기획 시작하고 싶어
> /sk 지난 작업 이어서            ← "스킬 필요 없음, 훅이 이미 주입함" 이라고 알려준다
```

이미 이름을 아는 요청에는 쓰지 않는다. 그냥 그 스킬을 부르는 게 빠르다.

---

## _tools/ — 전역 규칙·에이전트·정비 도구

**`CLAUDE.global.md`** — 전역 `~/.claude/CLAUDE.md` 원본(32줄). 이 파일 전체를 복사해 쓴다.
- **작업 원칙 6줄**: Karpathy 가이드라인을 Anthropic "Prompting Claude Opus 5/5.5" 권장 문구에 맞춰 줄였다. 범위대로 하기 · 해석이 크게 갈릴 때만 묻기 ·
  최소 코드 · 외과적 변경 · 영향 있는 오류만 정정 · 할 수 있는 다음 단계는 멈추지 않고 진행. "검증될 때까지 반복"은 뺐다(모델이 스스로 검증하고,
  명시 지시는 과잉 검증을 낳는다는 Opus 5 가이드). 단순함의 세부 기준은 ponytail이, 검증 절차는 superpowers가 맡는다.
- **이어가기 · 규모 판정 · superpowers 경계 · 모델·effort·위임**: 위 "쓰는 법" 참고.
- 프로젝트 CLAUDE.md에는 행동 규칙을 두지 않는다(catch-up 템플릿이 전역 포인터 + `@AGENTS.md`만 만든다). 예전 프로젝트에 Karpathy 4절이 있으면 지운다.

**`agents/`** — `~/.claude/agents/`에 복사해 쓴다. effort는 Agent 호출로 못 주므로 이 파일로 주고, 모델은 호출할 때 지정한다.

| 파일 | effort | 쓰는 곳 |
|---|---|---|
| `fresh-reviewer.md` | high | autopilot A4 독립 검토·GATE, 구현 REVIEW 정확성, eval judge (읽기 전용) |
| `deep-worker.md` | high | 판단 집약·장기 조사 위임 (`model: opus` 또는 `fable`) |
| `quick-worker.md` | low | 기계적 대량 작업 위임 (`model: haiku` 또는 `sonnet`) |

**`skill_catalog.py`**

```bash
python _tools/skill_catalog.py              # 설치 스킬 요약 + 항상-로드 메타데이터 토큰 추정 + 라우팅 표 정합성 검사
python _tools/skill_catalog.py --catalog    # 설치 스킬 전체 목록 (id | 출처 | description)
python _tools/skill_catalog.py --unassigned # 설치됐지만 어느 라우팅 표에도 없는 스킬
python _tools/skill_catalog.py --available  # 마켓플레이스에 있지만 미설치인 플러그인
```

스킬 id 표기: 플러그인 `ecc:api-design`, 번들 `/code-review`, 개인 `frontend-design-taste`.
토큰 합계는 settings의 `enabledPlugins`(user < project < local)를 읽어 꺼진 플러그인과 다른 프로젝트 전용 플러그인을 뺀 값이다. 꺼진 플러그인의 스킬도 "설치됨"으로 보고 라우팅 검사에서는 미설치로 치지 않는다.
라우팅 표가 미설치 스킬을 가리키면 종료코드 1.

## 외부 스킬 흡수 기준

새 스킬을 들일 때 아래를 전부 확인하고, 통과하면 **복사하지 말고 플러그인으로 설치**한 뒤 라우팅 표에 배정한다.

1. **신호**: GitHub ★ 5만 이상 또는 Anthropic 공식(anthropics/skills, claude-plugins-official). ★는 GitHub API로 당일 확인.
2. **활성**: 마지막 push 90일 이내. 멈춘 저장소는 배정하지 않는다.
3. **라이선스**: OSI 승인(MIT·Apache-2.0 등). 스킬 본문을 복사하지 않으므로 라이선스 표기 의무는 evidence.md 한 줄로 충분.
4. **근거**: 자체 벤치마크나 평가가 있는가. 없으면 우리 스모크 회귀(시드 3개)로 직접 잰다.
5. **겹침**: `--unassigned`와 라우팅 표를 보고 이미 같은 역할을 하는 스킬이 있으면 둘 중 하나만 남긴다.
6. **컨텍스트 비용**: description이 항상 로드된다. 플러그인 하나가 수십 개 스킬을 들여오면 `--catalog`로 토큰 추정치를 보고 결정.

흡수 완료: `ponytail`(121k★, 2026-09-04), `superpowers`(281k★, 2026-09-07 — 구현 단계 엔진으로 배선). 후보(미설치): `skill-creator`(공식 마켓, 스킬 평가 도구).
플러그인 사이 경계(누가 설계하고 누가 구현하나)는 `~/.claude/CLAUDE.md`에 사용자 지시로 둔다 — superpowers가 "사용자 지시 > 스킬"이라 명시하기 때문. 새 PC에서는 이 파일도 복사한다.
Remote Control 세션에서는 `/plugin`이 막혀 있으므로 같은 PC의 터미널에서 `claude plugin marketplace add <repo>` → `claude plugin install <name>@<marketplace>`를 쓴다.

## 새 PC 세팅

```bash
git clone https://github.com/sangchane/claude-skills "$HOME/.claude/skills"
mkdir -p ~/.claude/agents && cp ~/.claude/skills/_tools/agents/*.md ~/.claude/agents/
cp ~/.claude/skills/_tools/CLAUDE.global.md ~/.claude/CLAUDE.md   # 기존 파일은 먼저 백업
```

Windows PowerShell:

```powershell
git clone https://github.com/sangchane/claude-skills "$env:USERPROFILE\.claude\skills"
Copy-Item "$env:USERPROFILE\.claude\skills\_tools\agents\*.md" "$env:USERPROFILE\.claude\agents\"
Copy-Item "$env:USERPROFILE\.claude\skills\_tools\CLAUDE.global.md" "$env:USERPROFILE\.claude\CLAUDE.md"
```

프로젝트마다 한 번 `/catch-up`을 돌리면 NEXT.md 세션 훅이 깔린다(없어도 전역 CLAUDE.md가 NEXT.md를 확인하게 한다).
플러그인은 이 저장소에 포함되지 않는다. `/plugin marketplace add` → `/plugin install`로 superpowers·ponytail·ecc를 설치한 뒤
ecc와 claude-mem은 사용자 범위에서 끈다(이름은 `/plugin` 목록에 보이는 대로).

```bash
claude plugin disable <ecc 플러그인 이름> --scope user
claude plugin disable <claude-mem 플러그인 이름> --scope user
# 새 서비스 설계(autopilot)를 하는 프로젝트에서만
claude plugin enable <ecc 플러그인 이름> --scope project
```

`python _tools/skill_catalog.py`로 라우팅 표가 가리키는 스킬이 다 있는지, 항상 로드되는 설명문이 얼마인지 확인한다.

## 평소 동기화 루틴

- 스킬을 **고친 PC에서**: `git add . && git commit -m "무엇을 왜" && git push`
- **다른 PC에서** 세션 시작 전: `git pull`. `_tools/agents/`나 `CLAUDE.global.md`가 바뀌었으면 다시 복사한다.
- 원칙: 원본은 GitHub 하나. 두 PC에서 동시에 같은 스킬을 고치지 않는다.
- 스킬을 고치면 회귀 평가: autopilot은 `eval/PROTOCOL.md` 스모크(시드 3개), prompt-workflow는 `eval/` 대리 A/B.

## 변경 이력

**2026-09-29 — 플러그인 정리.** 실측(항상 로드 설명문 약 1만 9천 토큰, 대부분 ecc) 기준으로 ecc는 평소 끄고 autopilot 프로젝트에서만 켜기,
claude-mem 끄기. 구현 워크플로우 라우팅에서 ecc 49개 참조를 빼고 superpowers·ponytail·번들 명령만 남겼다(santa-method → `/security-review` + 다른 등급 fresh-reviewer).
autopilot은 ecc가 꺼져 있으면 켜라고 한 줄 안내하고, 안 켜면 대체 절차로 진행.

**2026-09-29 — 중복 정리.** 전역 CLAUDE.md의 Karpathy 4절을 Opus 5.5판 작업 원칙 6줄로 바꿔 `CLAUDE.global.md` 하나로 합쳤다
(§4 "검증될 때까지 반복" 삭제, §1 "불확실하면 멈춘다" → "해석이 크게 갈릴 때만 묻는다"). catch-up 프로젝트 템플릿에서 행동 규칙 제거.
service-prompt-workflow를 superpowers 위의 얇은 층으로 줄였다(135 → 77줄, 단계별 복붙 템플릿 221줄 삭제 → 1쪽 SPEC 템플릿).

**2026-09-29 — 규모 등급 구조.** 현업 조사(위 "현업 근거")를 바탕으로 개편.
- S·M·L 등급 도입: 전역 CLAUDE.md가 판정, autopilot은 L 신규 전용, 기존 저장소의 위험 변경은 L 변경 경로, 구현 워크플로우는 등급별로 단계 생략.
- 상태 통일: autopilot의 `autopilot/<slug>/NEXT.md` → 프로젝트 루트 `NEXT.md` 블록. 세션 훅이 읽는 곳과 스킬이 쓰는 곳이 같아졌다.
- `model-effort-router` 삭제: 규칙을 `_tools/CLAUDE.global.md`로 흡수(따로 부를 스킬이 하나 줄었다).
- 미실행: 등급 경로의 `eval/` 회귀.

**2026-09-29 — Opus 5.5.** Anthropic "Prompting Claude Opus 5.5"·"Migrating to Claude Opus 5.5"·"Prompting Claude Opus 5"·Effort 문서 기준.
- 위임 과다 수정: 구현 기본값을 "메인에서 직접"으로, 위임 조건·상한(동시 3, 요청당 5). BUILD 1순위 `executing-plans`, EXPLORE 직접 Read/Grep,
  VERIFY 메인. 원인은 `subagent-driven-development`의 작업당 서브에이전트 3개와 이 세대 모델의 높은 위임 성향이 겹친 것.
- `opus-effort-router` → `model-effort-router`(모델까지 판정). 에이전트 `opus-deep`/`opus-quick` → `deep-worker`/`quick-worker`.
- 사실 갱신: `opus` = Opus 5.5(4/20 달러), `fable` 10/50 달러, 기본 effort(Opus 5.5 medium, Fable·Sonnet high), effort 변경 시 캐시 유지.
  "서브에이전트는 effort를 따로 못 준다"는 틀려서 정정.
- 정리: 폐기 상태로 남아 있던 `solution-planner` 삭제(git 기록에 남음). 설명문이 매 세션 로드되고 service-autopilot과 트리거가 겹쳤다.
- 미실행: 구현 워크플로우 위임 변경의 `eval/` A/B.

**2026-09-08 — Fable 5.1.** Anthropic prompt-audit(번들 `claude-api` 스킬) 적용. 압력 어조·사건 서술·교육 문장·중복 절차를 뺐고
택소노미·라우팅·검사 스크립트·형식 계약·GATE는 그대로. ponytail 페르소나는 구현 서브에이전트에만 주입(`~/.claude/settings.json` env
`PONYTAIL_SUBAGENT_MATCHER`). 상세는 `service-autopilot/references/evidence.md`.
