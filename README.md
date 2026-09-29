# dev — 말로 시키는 개발 키트

Claude Code에게 **평소 말투로 개발을 시키면, 일의 크기에 맞게 알아서 설계·구현·검증·리뷰까지 하도록** 만든 플러그인이다.
설치는 대화창에 두 줄, 그 뒤로는 그냥 말하면 된다. Windows·macOS 똑같다.

---

## 1. 설치

Claude Code **대화창에** 입력한다.

```
/plugin marketplace add sangchane/claude-skills
/plugin install dev@sangchane
```

함께 쓰는 superpowers(구현 절차)와 ponytail(코드 적게 쓰기)은 **자동으로 같이 설치된다.** 설치가 끝나면 **새 세션**을 연다.

<details>
<summary>superpowers·ponytail을 예전에 따로 설치했다면</summary>

같은 플러그인이 두 벌이 되니 예전 것을 지운다. 터미널에서 한 번.

```bash
claude plugin uninstall superpowers@superpowers-marketplace
claude plugin uninstall ponytail@ponytail
```
</details>

<details>
<summary>새 서비스 설계를 자주 한다면 (선택)</summary>

설계 도구 상자 ecc를 설치하고, 무거우니 평소엔 꺼 둔다. 설계하는 프로젝트에서만 켠다.

```
/plugin marketplace add https://github.com/affaan-m/ECC
/plugin install ecc@ecc
```
```bash
claude plugin disable ecc --scope user          # 평소엔 끔
claude plugin enable ecc --scope project        # 설계하는 프로젝트 폴더에서만
```
</details>

## 2. 이름표

보통은 **안 쳐도 된다** — 말로 하면 맞는 것이 자동으로 뜬다. 직접 부르고 싶을 때만 `/dev:` 뒤에 한 단어.

| 입력 | 언제 |
|---|---|
| `/dev:design` | 새 서비스를 처음 만들 때 (아이디어 → 설계 문서) |
| `/dev:build` | 기능 만들기 · 버그 고치기 · 리뷰 · 커밋 |
| `/dev:ui` | 화면 만들 때 (AI 티 안 나게) |
| `/dev:setup` | 새 프로젝트 폴더에서 처음 한 번 |
| `/dev:guide 하고 싶은 것` | 뭘 써야 할지 모를 때 |

## 3. 쓰는 법

**Claude는 목수다. 원하는 걸 평소 말투로 말하면, 목수가 일의 크기를 보고 방법을 고른다.**
작은 수리는 바로 고치고, 방 하나는 한 장짜리 도면을 그리고, 집을 새로 지을 때만 설계부터 한다.

**새 프로젝트를 시작할 때 한 번만** `/dev:setup`(작업 일지 NEXT.md를 붙여 두는 것). 그다음부터는 그냥 말한다.

### 상황별로 이렇게 말한다

| 이럴 때 | 이렇게 말한다 | 그러면 |
|---|---|---|
| 아이디어만 있다 | "헬스장 회원 관리 서비스 만들고 싶어" | 조사 후 객관식 질문 몇 개(최대 5개) → 설계 문서 → "다음 진행해"로 구현 시작 |
| 기능 하나·작은 게임 | "테트리스 만들어줘", "로그인에 구글 로그인 붙여줘" | 1쪽 계획 → 만들고 → 돌려 보고 → 리뷰 1번 |
| 작은 수정 | "버튼 색 파란색으로 바꿔줘" | 바로 고치고 확인만 |
| 버그 | "로그인 누르면 흰 화면 떠. 고쳐줘" | 재현 → 원인 찾기 → 수정 → 확인 |
| 어제 하던 거 | "다음 진행해" | NEXT.md에 적힌 곳부터 이어서 |
| 마무리 | "리뷰해줘", "커밋하고 PR 만들어줘" | 리뷰 1번 / 커밋·PR |

응답 첫 줄에 `등급: M — 기능 하나`처럼 크기 판정이 나온다. 너무 크거나 작게 잡았으면 "S로 해", "L로 해"라고만 하면 된다.

### 더 잘 말하는 요령 세 가지

1. **"뭐가 되면 성공인지"** — "잘 되게" 대신 "빈 칸으로 저장하면 에러 문구가 뜨면 성공".
2. **"어디를"** — 파일·화면 이름이나 비슷한 기존 기능을 알려준다. "회원가입 화면처럼 만들어줘".
3. **"안 할 것"** — "결제는 이번엔 빼고".

버그는 **증상 + 언제 + 기대했던 것**: "주문 목록에서 새로고침하면 방금 넣은 주문이 사라져. 남아 있어야 해."

### 가끔 내가 할 일

- Claude가 `/effort high`를 권하면 그대로 입력한다. 위험한 작업 확인 질문에는 답한다.
- 전혀 다른 일을 시작할 때는 `/clear` 또는 새 세션. 같은 문제를 두 번 고쳐도 안 되면 새 세션에서 더 구체적으로 다시 말한다.

### 안 해도 되는 것

스킬 이름 외우기 · 모델 바꾸기(`/model`) · 매번 처음부터 맥락 설명하기 · 서브에이전트 쓰라고 시키기.

---

## 4. 업데이트

```
/plugin update dev@sangchane
```

매번 치기 귀찮으면 `/plugin` → Marketplaces → sangchane → 자동 업데이트를 켠다. 바뀐 내용은 새 세션부터 적용된다.

## 5. 예전 방식에서 옮기기 (`~/.claude/skills`에 clone해 쓰던 PC)

플러그인을 설치한 뒤, 예전 복사본이 같은 스킬을 두 번 띄우지 않게 치운다. **아무것도 지우지 않고 옮기기만 한다.**
예전 저장소에 있던 스킬만 `skills-old`로 빠지고, 그 밖의 개인 스킬(archify·graphify 등)은 제자리에 남는다.
**Claude Code를 모두 닫고** 실행한다.

**Windows PowerShell**
```powershell
$C = "$env:USERPROFILE\.claude"
$old = "service-autopilot","service-prompt-workflow","frontend-design-taste","catch-up","sk","solution-planner","opus-effort-router","model-effort-router","_tools","learned",".git",".gitignore",".gitattributes","README.md"
New-Item -ItemType Directory -Force "$C\skills-old" | Out-Null
Get-ChildItem -Force "$C\skills" | Where-Object { $old -contains $_.Name } | Move-Item -Destination "$C\skills-old" -Force
Get-ChildItem "$C\agents" -Include fresh-reviewer.md,deep-worker.md,quick-worker.md -Recurse | Move-Item -Destination "$C\skills-old" -Force
if (Test-Path "$C\CLAUDE.md") { Move-Item "$C\CLAUDE.md" "$C\CLAUDE.md.pre-plugin" -Force }
```

**macOS**
```bash
C=~/.claude; mkdir -p $C/skills-old
for n in service-autopilot service-prompt-workflow frontend-design-taste catch-up sk solution-planner opus-effort-router model-effort-router _tools learned .git .gitignore .gitattributes README.md; do
  [ -e "$C/skills/$n" ] && mv "$C/skills/$n" $C/skills-old/
done
for a in fresh-reviewer deep-worker quick-worker; do [ -f $C/agents/$a.md ] && mv $C/agents/$a.md $C/skills-old/; done
[ -f $C/CLAUDE.md ] && mv $C/CLAUDE.md $C/CLAUDE.md.pre-plugin
```

- 전역 `CLAUDE.md`는 `CLAUDE.md.pre-plugin`으로 이름만 바꾼다. 작업 규칙은 이제 플러그인이 넣어 준다.
  예전 CLAUDE.md에 **직접 적어 둔 개인 메모**가 있었다면 그 줄만 새 `~/.claude/CLAUDE.md`에 옮긴다
  (Karpathy 4절이나 예전 규칙은 옮기지 않는다 — 플러그인 규칙과 중복).
- 예전에 `/catch-up`으로 세팅한 프로젝트에는 `.claude/settings.json`의 `print_next_action.py` 훅 항목과 `tools/hooks/print_next_action.py` 파일이 있다.
  둘 다 지운다(같은 내용을 두 번 넣는다). 그 프로젝트에서 `/dev:setup`을 돌리면 제거를 제안해 준다.
- 새 세션에서 잘 동작하면 `skills-old`와 `CLAUDE.md.pre-plugin`은 지워도 된다.

## 6. Codex · Antigravity에서도 쓰기

같은 규칙(등급 S·M·L, NEXT.md 이어가기)과 스킬 ui·setup을 두 도구의 **전역 설정**에 복사한다. 어떤 모델(GPT·Gemini·Claude)을 골라도 똑같이 적용된다. 터미널에서 한 번.

```bash
git clone https://github.com/sangchane/claude-skills   # 처음 한 번 (이미 있으면 git pull)
cd claude-skills
python tools/export.py              # 둘 다. 하나만: python tools/export.py codex
```

| 도구 | 규칙이 들어가는 곳 | 스킬이 들어가는 곳 | 부르는 법 |
|---|---|---|---|
| Codex | `~/.codex/AGENTS.md` (기존 내용은 두고 `dev:start~end` 블록만 교체) | `~/.agents/skills/` | `$ui`, `$setup` 또는 그냥 말하기 |
| Antigravity | `~/.gemini/config/rules/dev.md` | `~/.gemini/config/skills/` | 그냥 말하기 |

- 저장소가 바뀌면 `git pull` 후 같은 명령을 다시 돌린다. 같은 이름의 **다른** 스킬이 이미 있으면 덮어쓰지 않고 "건너뜀"이라고 알려 준다.
- Claude Code와 다른 점: 세션 시작 훅이 없어서 NEXT.md는 에이전트가 규칙대로 직접 읽는다. design·build는 Claude 전용 절차(superpowers·서브에이전트)가 많아 스킬로 보내지 않고,
  규칙의 등급별 단계(SPEC → 구현 → 검증 → 리뷰, L 신규는 설계 문서 먼저)를 에이전트가 직접 한다. guide와 reviewer·deep·quick 에이전트도 없다.
- 모델·effort는 두 도구 모두 **사용자가** 바꾼다(Codex `/model`, Antigravity 모델 선택기의 사고 수준). 모델 기본값으로 두고, 큰 작업(L)을 낮은 수준으로 하고 있을 때만 에이전트가 올리라고 한 줄로 권한다.

---

# 자세한 설명 (궁금할 때만)

## 구조

| 층 | 무엇 | 하는 일 |
|---|---|---|
| **규칙** `rules.md` | 세션 시작 훅(`hooks/session-start.sh`)이 매 세션 Claude에게 넣는다 | 작업 원칙(Karpathy 가이드라인의 Opus 5.5판) · 규모 판정(S·M·L) · superpowers 경계 · 모델·위임 규칙 |
| **NEXT.md** (프로젝트 루트) | 스킬이 단계마다 덮어쓰는 "지금 어디까지 왔나" 블록 | 같은 훅이 세션 시작 때 함께 넣는다. "다음 진행해"가 여기서 이어진다 |
| **스킬** `skills/` | design · build · ui · setup · guide | 필요할 때만 로드되는 단계별 절차 |
| **에이전트** `agents/` | `dev:reviewer`(high) · `dev:deep`(high) · `dev:quick`(low) | 독립 리뷰, 깊은 작업, 대량 기계 작업 위임. 모델은 부를 때 준다 |

```
.claude-plugin/plugin.json      플러그인 정보(이름 dev, 버전)
.claude-plugin/marketplace.json 마켓플레이스 정보(이름 sangchane)
rules.md                        작업 규칙 (훅이 주입)
hooks/                          세션 시작 훅
skills/design|build|ui|setup|guide
agents/reviewer|deep|quick
tools/skill_catalog.py          설치 스킬·토큰·라우팅 표 검사
tools/export.py                 규칙·스킬을 Codex·Antigravity로 복사
docs/                           과거 분석 기록
```

## 흐름 (큰 그림)

```
요청 ─→ dev 규칙 규모 판정 ─────┬─ S ─→ 스킬 없이 바로 수정 → 검증 명령 1회
                                   ├─ M ─→ dev:build: FRAME 3줄 → SPEC(1쪽) → BUILD → VERIFY → REVIEW 1회
                                   ├─ L 신규 ─→ dev:design: A0~A7 + GATE ─→ dev:build: SPEC부터 (버티컬 슬라이스 먼저)
                                   ├─ L 변경 ─→ dev:build: FRAME~REFLECT 전체 + 보안 리뷰
                                   └─ 버그 ─→ dev:build: 디버깅 분기
                                                                                         └─ 화면이 있으면 dev:ui
각 단계 끝 ─→ 루트 NEXT.md 갱신 ─→ 다음 세션 시작 때 훅이 주입 ─→ "다음 진행해"로 이어감
위임 ─→ 기본은 메인 세션. 크고 독립적인 작업·대용량 읽기·최종 리뷰만 서브에이전트(동시 3·요청당 5)
```

비유하면: **작은 수리는 바로 고치고(S), 방 하나 리모델링은 한 장짜리 도면으로(M), 집을 새로 지을 때만 설계 사무소(design)를 부른다(L).**
공사 일지(NEXT.md)가 현장에 붙어 있어서 다음 날 누가 와도 이어서 일한다.

## 현업 근거 (2026-09-29 조사)

- **무게는 되돌리기 어려운 정도에 비례**: Amazon Type 1/Type 2 결정, Google은 불확실성 질문 3개 이상일 때만 설계 문서
  ("구현 방법만 적고 대안이 없으면 코드를 먼저 써라"), Kiro Quick Spec, Claude Code "diff를 한 문장으로 설명할 수 있으면 계획 생략".
- **문서는 한 번 쓰고 고쳐 가며 쓴다**: Google 설계 문서는 구현 중 갱신하는 living doc. 단계마다 전체 재검토를 하지 않는다.
- **검증은 실행으로**: Claude Code "검증할 수단(테스트·빌드·스크린샷)을 줘라", 게임은 플레이테스트.
- **작게, 시간 상한**: Google 변경당 약 100줄, Shape Up 6주 초과 시 연장 없이 중단, 게임은 프로토타입 → 버티컬 슬라이스 → 제작.
- **리뷰는 1회**: "지적을 전부 쫓으면 과잉설계가 된다"(Claude Code best practices).

---

## /dev:design — 새 서비스 설계

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
  lite는 질문 0·검색 ≤5·위협모델 조건부·GATE 자기 점검(실측 20만, 상한 25만). full은 상한 80만(서브에이전트 포함). `/dev:design spike|lite|full …`로 강제 가능.
- **자기 선언 검증**: GATE 전에 `python scripts/check_package.py autopilot/<slug>` — FR→05 커버리지, SC→06 시나리오, 미결정, register 마킹,
  버전 전파를 스크립트가 센다. CRITICAL이면 GATE 진입 금지.
- **개정 전파·상수 표**: 산출물마다 `버전:`, 04~07은 `기준 03 v`. 숫자는 03 상수 표에만.
- **착수 자산**: A3 화면 스케치 1장, A7 디렉터리 구조·`.env.example`(값 없음)·첫 작업 3개(워킹 스켈레톤).
- **예산·재개**: GATE 재실행 1회, 끊기면 없는 첫 파일의 단계부터 재개, 런 끝에 비용 기록. 단계마다 루트 `NEXT.md`를 갱신하므로 다음 날 "다음 진행해"로 이어진다.
- **산출물**: `autopilot/<slug>/`의 `00-seed.md` ~ `08-readiness-report.md` + `decision-log.md`.
- **평가**: `eval/PROTOCOL.md`(블라인드 pairwise A/B, 동결 시드 10개) + `evals/evals.json`(skill-creator 호환).

```
> 회의실 예약 서비스 만들고 싶어           ← 자동 발동
> /dev:design 라즈베리파이로 IP 카메라 모니터링 서비스
```

---

## /dev:build — 구현·버그·리뷰·커밋 (superpowers 위의 얇은 층)

**실행 절차는 superpowers가 맡고, 이 스킬은 규모에 맞게 단계를 고르고 단계마다 어떤 스킬을 붙일지만 정한다.** (0.7.0, 77줄)

- **등급별 경로**: S는 이 스킬 없이 처리. M은 FRAME 3줄 → 1쪽 SPEC → BUILD → VERIFY → REVIEW 1회 → SHIP
  (게임·도구 프로토타입은 버리는 프로토타입으로 핵심 가설부터). L 신규는 autopilot 뒤 SPEC부터, 첫 작업 3개는 버티컬 슬라이스.
  L 변경(기존 저장소의 결제·인증 등)은 전체 경로 + `/security-review`. 버그는 `superpowers:systematic-debugging`.
- **단계별로 붙이는 것**: PLAN `superpowers:writing-plans`, BUILD `superpowers:executing-plans`(같은 세션) + TDD + `ponytail:ponytail` 사다리
  (+ 화면이면 `dev:ui`), VERIFY `verification-before-completion`, REVIEW `/code-review` 1회(+ `ponytail-review` 선택),
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

## /dev:ui — 화면 품질

**웹 UI에서 "AI가 만든 티(slop)"를 없애고 의도된 고급 결과를 강제하는 취향 하네스.** React·Tailwind·Zustand 특화.
3개 dial(밀도·모션·파격)과 프로파일(관제 8 / 제품 UI 5 / 랜딩 3)을 정하고, 하드룰 위반은 반려한다.
dev:build의 BUILD·REVIEW에 프론트가 포함되면 자동 참조된다.

---

## /dev:setup — 프로젝트 준비 (처음 한 번, 직접 호출)

프로젝트에 얇은 `CLAUDE.md`(`@AGENTS.md` 포인터) · `AGENTS.md`(다른 AI 툴과 같이 쓰는 단일 원본) · `NEXT.md`(지금 할 일) · `WORKLOG.md`(히스토리) ·
폴더별 `CLAUDE.md`를 **처음 한 번** 만든다. 바꾸기 전에 diff를 보여주고 승인받는다.
세션마다 `NEXT.md`의 현재 작업을 넣는 일은 dev 플러그인의 세션 시작 훅이 하므로, 프로젝트에 따로 훅을 깔지 않는다.

```
> /dev:setup
> /dev:setup --tools antigravity,cursor
```

---

## /dev:guide — 뭘 써야 할지 안내 (직접 호출)

스킬 이름을 몰라도 되게 하는 얇은 스킬. 라우팅 표 2개(사람이 근거를 단 1순위 후보)를 먼저 보고,
없으면 설치 카탈로그를 의미로 훑어 최대 3개를 이유·실행 명령과 함께 추천한다.

```
> /dev:guide 회의실 예약 서비스 기획 시작하고 싶어
> /dev:guide 지난 작업 이어서            ← "스킬 필요 없음, 훅이 이미 주입함" 이라고 알려준다
```

이미 이름을 아는 요청에는 쓰지 않는다. 그냥 그 스킬을 부르는 게 빠르다.

---

## 도구

```bash
python tools/skill_catalog.py              # 켜진 스킬 수 · 항상 로드 설명문 토큰 · 라우팅 표 검사
python tools/skill_catalog.py --catalog    # 전체 목록 (id | 출처 | description)
python tools/skill_catalog.py --unassigned # 켜져 있지만 라우팅 표에 없는 스킬
python tools/skill_catalog.py --available  # 마켓플레이스에 있지만 미설치인 플러그인
python tools/export.py                     # 규칙·스킬을 Codex·Antigravity 전역 설정으로 복사 (6절)
```

설치된 플러그인 폴더나 이 저장소를 clone한 곳에서 실행한다. 꺼진 플러그인(`enabledPlugins`, user < project < local)은 토큰 합계에서 뺀다.

## 스킬을 고칠 때

1. 이 저장소를 clone해서 고친다.
2. `.claude-plugin/plugin.json`의 `version`을 올린다 — **안 올리면 `/plugin update`가 "이미 최신"이라며 받지 않는다.**
3. 커밋·푸시. 다른 PC는 `/plugin update dev@sangchane`.
4. 회귀 평가: design은 `skills/design/eval/PROTOCOL.md` 스모크(시드 3개), build는 `skills/build/evals/evals.json`.

## 외부 스킬 흡수 기준

새 스킬을 들일 때 아래를 전부 확인하고, 통과하면 **복사하지 말고 플러그인으로 설치**한 뒤 라우팅 표에 배정한다.

1. **신호**: GitHub ★ 5만 이상 또는 Anthropic 공식(anthropics/skills, claude-plugins-official). ★는 GitHub API로 당일 확인.
2. **활성**: 마지막 push 90일 이내. 멈춘 저장소는 배정하지 않는다.
3. **라이선스**: OSI 승인(MIT·Apache-2.0 등). 스킬 본문을 복사하지 않으므로 라이선스 표기 의무는 evidence.md 한 줄로 충분.
4. **근거**: 자체 벤치마크나 평가가 있는가. 없으면 우리 스모크 회귀(시드 3개)로 직접 잰다.
5. **겹침**: `--unassigned`와 라우팅 표를 보고 이미 같은 역할을 하는 스킬이 있으면 둘 중 하나만 남긴다.
6. **컨텍스트 비용**: description이 항상 로드된다. 플러그인 하나가 수십 개 스킬을 들여오면 `--catalog`로 토큰 추정치를 보고 결정.

흡수 완료: `ponytail`(121k★, 2026-09-04), `superpowers`(281k★, 2026-09-07 — 구현 단계 엔진으로 배선). 후보(미설치): `skill-creator`(공식 마켓, 스킬 평가 도구).
플러그인 사이 경계(누가 설계하고 누가 구현하나)는 dev 규칙(`rules.md`)에 사용자 지시로 둔다 — superpowers가 "사용자 지시 > 스킬"이라 명시하기 때문. 플러그인을 설치하면 같이 들어온다.
Remote Control 세션에서는 `/plugin`이 막혀 있으므로 같은 PC의 터미널에서 `claude plugin marketplace add <repo>` → `claude plugin install <name>@<marketplace>`를 쓴다.

## 변경 이력

**2026-09-29 — superpowers·ponytail 자동 설치 (1.2.0).** `plugin.json`의 `dependencies`로 선언하고, 두 플러그인을 원본 GitHub 저장소 그대로 sangchane 마켓플레이스에 올렸다. 설치가 두 줄로 줄었다.

**2026-09-29 — Codex·Antigravity 내보내기 (1.1.0 → 1.1.1).** `tools/export.py`가 `rules.md`를 각 도구 형식으로 바꿔 전역 규칙에 넣고 스킬 ui·setup을 복사한다. 규칙 원본은 `rules.md` 하나다.
1.1.1: GPT-6·Gemini 3.x 기준으로 effort 문구를 모델 기본값 기준으로 바꾸고, Claude 전용 절차가 많은 design·build는 내보내지 않는다(예전 복사본은 자동 삭제).

**2026-09-29 — 플러그인으로 전환.** clone·파일 복사 설치를 없애고 `dev@sangchane` 플러그인으로 묶었다. 이름을 짧게:
service-autopilot → `design`, service-prompt-workflow → `build`, frontend-design-taste → `ui`, catch-up → `setup`, sk → `guide`,
에이전트 fresh-reviewer·deep-worker·quick-worker → `reviewer`·`deep`·`quick`. 전역 CLAUDE.md 복사 대신 세션 시작 훅이 `rules.md`와 NEXT.md 현재 작업을 넣는다.
setup은 프로젝트별 훅을 더 이상 깔지 않는다. 산출물 폴더 이름 `autopilot/<slug>/`는 검사 스크립트·평가 호환을 위해 그대로 둔다.

**2026-09-29 — 플러그인 정리.** 실측(항상 로드 설명문 약 1만 9천 토큰, 대부분 ecc) 기준으로 ecc는 평소 끄고 autopilot 프로젝트에서만 켜기,
claude-mem 끄기 → **항상 로드 설명문 약 1만 9,013 토큰 → 2,614 토큰(약 86% 감소, 사용자 PC `skill_catalog.py` 실측)**. 구현 워크플로우 라우팅에서 ecc 49개 참조를 빼고 superpowers·ponytail·번들 명령만 남겼다(santa-method → `/security-review` + 다른 등급 fresh-reviewer).
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
