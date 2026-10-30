# dev — 말로 시키는 개발 키트

Claude Code에게 **평소 말투로 개발을 시키면, 일의 크기에 맞게 알아서 설계·구현·검증·리뷰까지 하도록** 만든 플러그인이다.
설치는 대화창에 두 줄, 그 뒤로는 그냥 말하면 된다. Windows·macOS 똑같다.

---

## 1. 설치

Claude Code **대화창에** 입력한다. 첫 줄은 Anthropic 공식 마켓이다(이미 있으면 그냥 넘어간다).

```
/plugin marketplace add anthropics/claude-plugins-official
/plugin marketplace add sangchane/claude-skills
/plugin install dev@sangchane
```

함께 쓰는 superpowers(구현 절차, 공식 마켓)와 ponytail(코드 적게 쓰기)은 **자동으로 같이 설치된다.** 설치가 끝나면 **새 세션**을 연다.

<details>
<summary>1.4.0 이전 버전에서 업데이트했더니 dev가 "failed to load"라면</summary>

`plugin update`는 새로 생긴 의존성을 설치하지 않는다. 터미널에서 한 번.

```bash
claude plugin marketplace update sangchane
claude plugin update dev@sangchane
claude plugin install superpowers@claude-plugins-official
claude plugin install ponytail@sangchane
claude plugin list        # dev@sangchane가 enabled인지 확인
```
`superpowers@superpowers-marketplace`나 `ponytail@ponytail`이 목록에 남아 있으면 `claude plugin uninstall <이름>`으로 지운다(두 벌 방지).
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
| 막힌 옛 프로젝트 | "이거 몇 주째 진도가 안 나가. 살려줘" | 실제로 돌려 보고 진단 → 막힌 원인 설명 → 경로 확인 1번 → 이어서 진행 |
| 어제 하던 거 | "다음 진행해" | NEXT.md에 적힌 곳부터 이어서 |
| 마무리 | "리뷰해줘", "커밋하고 PR 만들어줘" | 리뷰 1번 / 커밋·PR |

응답 첫 줄에 `등급: M — 기능 하나`처럼 크기 판정이 나온다. 너무 크거나 작게 잡았으면 "S로 해", "L로 해"라고만 하면 된다.

### 더 잘 말하는 요령 세 가지

1. **"뭐가 되면 성공인지"** — "잘 되게" 대신 "빈 칸으로 저장하면 에러 문구가 뜨면 성공".
2. **"어디를"** — 파일·화면 이름이나 비슷한 기존 기능을 알려준다. "회원가입 화면처럼 만들어줘".
3. **"안 할 것"** — "결제는 이번엔 빼고".

버그는 **증상 + 언제 + 기대했던 것**: "주문 목록에서 새로고침하면 방금 넣은 주문이 사라져. 남아 있어야 해."

### 가끔 내가 할 일

- Claude가 권하는 명령(`/effort high`, `/clear`, `/rewind`)을 그대로 입력한다. 언제 칠지는 Claude가 알려 준다. 위험한 작업 확인 질문에는 답한다.
- 스킬·규칙을 고쳤거나 한 달에 한 번 `/doctor prompt-audit` — 규칙끼리 부딪치거나 옛 모델용 문구가 남았는지 점검한다. 한도가 빨리 줄면 `/usage`.

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

**원격·클라우드 Codex(작업마다 새 컨테이너)** 는 홈 폴더가 매번 비므로, 작업할 저장소 안에 넣고 커밋한다.
```bash
python tools/export.py codex --project <게임 저장소 경로>   # AGENTS.md에 dev 블록 + .agents/skills/ui·setup
```
기존 AGENTS.md 내용은 그대로 두고 `dev:start~end` 블록만 넣거나 바꾼다. 스킬을 업데이트하려면 같은 명령을 다시 돌리고 커밋한다.

- 저장소가 바뀌면 `git pull` 후 같은 명령을 다시 돌린다. 같은 이름의 **다른** 스킬이 이미 있으면 덮어쓰지 않고 "건너뜀"이라고 알려 준다.
- **Claude와 같은 맥락**: `export.py codex`가 Codex 훅(`~/.codex/hooks/dev-context.py`)도 건다 — 세션 시작에 NEXT 블록 + 그 프로젝트의 Claude 메모리 목록(`~/.claude/projects/<프로젝트>/memory/MEMORY.md`), 질문마다 그 프로젝트 `.claude/settings.json`의 UserPromptSubmit 훅 출력 + `graphify-out/graph.json`이 있으면 질문으로 `graphify query`한 노드. 훅 명령은 설치에 쓴 파이썬 절대 경로(윈도우 `python3`는 Store 바로가기). Codex는 바뀐 훅 명령을 **사용자가 승인해야** 돌린다 — 설치 뒤 Codex를 한 번 열고 `/hooks`에서 dev-context 두 줄을 신뢰한다(명령이 같으면 다시 안 묻는다).
- **Claude가 Codex에 일을 나눌 때**(「코덱스한테 시켜·분담」): `python3 tools/codex_run.py --kind bulk|survey|build|judge|research -C <저장소> -o <결과> <지시문>`. 종류로 모델·reasoning effort를 고른다(빠른 모델 low · 주력 medium/high · 최상위 high/xhigh — 모델 이름은 `~/.codex/models_cache.json` 설명에서 찾아 새 모델이 나와도 그대로). 같은 맥락(NEXT 블록·볼트·그래프 노트)을 지시문 앞에 직접 붙여 훅 승인 전에도 간다. `--model`·`--effort`·`--dry-run`.
- Claude Code와 다른 점: design·build는 Claude 전용 절차(superpowers·서브에이전트)가 많아 스킬로 보내지 않고,
  규칙의 등급별 단계(SPEC → 구현 → 검증 → 리뷰, L 신규는 설계 문서 먼저)를 에이전트가 직접 한다. guide와 reviewer·deep·quick 에이전트도 없다.
- 대화형 세션의 모델·effort는 두 도구 모두 **사용자가** 바꾼다(Codex `/model`, Antigravity 모델 선택기의 사고 수준). Claude가 맡기는 `codex exec`는 위 실행기가 고른다. 모델 기본값으로 두고, 큰 작업(L)을 낮은 수준으로 하고 있을 때만 에이전트가 올리라고 한 줄로 권한다.

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
rules-models/                   모델별 지침 (훅이 세션 모델로 골라 주입)
hooks/                          세션 시작 훅 · Stop 검증 게이트(verify-gate.sh, 자체 시험 test-verify-gate.sh)
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
색·서체·컴포넌트 모양은 프로젝트 루트 `DESIGN.md` 한 장에 고정한다. 없으면 [awesome-design-md](https://github.com/VoltAgent/awesome-design-md)(74개 사이트)에서 프로파일에 맞는 것을 받아 브랜드를 지우고 한글 서체를 붙여 쓴다.
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

검토 후 넣지 않음(2026-09-30, 팁 영상 5편): OmniRoute(다른 모델로 우회 — Opus 유지 원칙과 충돌, 코드가 제3자 게이트웨이를 거침), Headroom(프롬프트를 압축하는 프록시 — 프롬프트 캐시와 충돌),
task-observer·프로젝트 맵류(NEXT.md·auto memory와 겹침), claude-code-setup(공식이지만 `/dev:setup`·`/dev:guide`와 겹침), ECC 호출법(이미 design이 L 설계 때 직접 부름).
넣은 것: 절대 규칙은 훅·deny로(setup), 읽기 명령 허용 목록(setup), `/clear`·`/rewind`를 알맞은 때 권하기(규칙), `/doctor prompt-audit` 정기 점검(README).

UI 후보(2026-09-30 조사, 미설치 — 웹·모바일 웹 프로젝트에서 한 번 켜 보고 비교 후 결정):
`nextlevelbuilder/ui-ux-pro-max-skill`(131.5k★, MIT — 스타일·팔레트·폰트 데이터로 디자인 시스템부터 정함, 웹·SwiftUI·Compose·RN·Flutter. 다른 글에서는 55.8k★로 적혀 있어 급증한 저장소),
`emilkowalski/skills`(42k★ — `mobile-native`: 웹을 폰에서 앱처럼, 안전 영역·탭 반응),
`vercel-labs/agent-skills`(31.5k★ — `web-design-guidelines` 터치·접근성 100여 규칙, `react-native-guidelines`),
`pbakaus/impeccable`(72k★ — AI 티 탐지 규칙 61개). `Leonxlnx/taste-skill`(70.1k★)은 ui 스킬의 원본 계열이라 중복.
시험 방법: `claude plugin install <이름> --scope project`로 그 프로젝트에만 켜고, 같은 화면을 켜기 전·후로 만들어 스크린샷 비교.
시험 결과(2026-09-30, 모바일 필라테스 예약 랜딩 1회): ui-ux-pro-max가 dev:ui보다 낫지 않았고(폰에서 가로 18px 밀림 버그, 날짜 선택이 고정 바에 가림), 스킬 7개·30MB라 연결하지 않음. 대신 ui Pre-Flight에 폰 스크린샷·가로 스크롤 확인을 추가.
Godot 게임 UI 쪽은 1만★ 넘는 스킬이 없어(godot-mcp 5.6k, awesome-gamedev-agent-skills 1.2k, GodotPrompter 370) ui 스킬 7절로 직접 만들었다.

흡수 완료: `ponytail`(121k★, 2026-09-04), `superpowers`(281k★, 2026-09-07 — 구현 단계 엔진으로 배선). 후보(미설치): `skill-creator`(공식 마켓, 스킬 평가 도구).
플러그인 사이 경계(누가 설계하고 누가 구현하나)는 dev 규칙(`rules.md`)에 사용자 지시로 둔다 — superpowers가 "사용자 지시 > 스킬"이라 명시하기 때문. 플러그인을 설치하면 같이 들어온다.
Remote Control 세션에서는 `/plugin`이 막혀 있으므로 같은 PC의 터미널에서 `claude plugin marketplace add <repo>` → `claude plugin install <name>@<marketplace>`를 쓴다.

## 변경 이력

**2026-10-30 — 1.9.1 Codex도 Claude와 같은 조건.** 사용자 「클로드랑 같은 컨디션에서 작업을 분담시키고 싶은거야 스킬이든 그래프 볼트 정리해둔거든 그래야 같은 퍼포먼스를 낼 수 있을거 같거든? 그 점을 확인해서 수정해서 업데이트해줘」. 확인한 빈 곳: ① 1.9.0의 「볼트·그래프 노트」는 프로젝트 질문 훅에만 기대 — 그런 훅이 없는 프로젝트(search-real-estate)는 0줄 → 그래프가 있으면 질문으로 `graphify query`해 붙임(`--query`, 없으면 지시문 첫 줄) ② Claude 자동 메모리(사용자 지적·선호)가 Codex에 없음 → 메모리 목록을 붙임 ③ 윈도우에서 실행기가 `codex`(npm `codex.cmd`)를 못 찾음(WinError 2)·cmd.exe가 인자의 `|`·줄바꿈을 깸 → `shutil.which` + 지시문은 표준 입력(`-`) ④ 훅 명령 `python3`가 윈도우 Store 바로가기(종료 49)라 늘 실패 → 설치 파이썬 절대 경로, 질문 훅 시간 제한 10 → 60초 ⑤ 윈도우 파이프 cp949로 한글 질문·맥락이 깨짐 → 훅 입출력 UTF-8 ⑥ 실행기 + 승인된 훅이면 같은 맥락이 두 벌 → 실행기가 `DEV_CONTEXT_INLINE`을 넘기면 훅은 건너뜀. 시험: 실제 훅 명령(PYTHONUTF8 없이)으로 SessionStart 6,171자(NEXT + 메모리)·UserPromptSubmit 5,033자(그래프 노드), 실행기 `--dry-run`에 NEXT·메모리·그래프 세 절, `judge` → gpt-6-astra·high로 실제 검토 실행.

**2026-10-30 — 1.9.0 Codex에 나눠 맡기기 · 같은 맥락.** 사용자 「코덱스한테 분담시켜라고만 해도 모델이랑 노력 지정해서 · 그래프나 볼트 참조까지 클로드랑 같은 조건에서」. 새 `tools/codex_run.py` — 일 종류(bulk · survey · build · judge · research, 서브에이전트 모델 고르기와 같은 기준)로 Codex 모델 · effort를 골라 `codex exec`(표준 입력 막음). 새 `hooks/codex-context.py` — Codex SessionStart · UserPromptSubmit 훅으로 NEXT 블록과 프로젝트 질문 훅 출력(볼트 · 그래프 노트)을 넣고, `export.py codex`가 `~/.codex/hooks.json`에 건다(예전 NEXT 전용 훅 대신). 알게 된 것: Codex는 훅 명령을 해시로 승인해 두고 바뀐 명령은 `/hooks` 승인 전까지 「Failed」 — 그래서 실행기가 같은 맥락을 지시문 앞에 직접 붙인다. 시험: 빠른 모델 low로 「받은 맥락 첫 줄」을 물어 NEXT 블록 · 볼트 노트 첫 줄을 그대로 받음. `rules.md` 위임 줄 · `build` REVIEW 줄에 실행기.

**2026-10-29 — 1.8.3 볼트 · 그래프가 다시 보이게.** 세션 시작 훅 출력은 10,000자를 넘으면 앞 2,000자만 보인다(공식 hooks 문서). 1.8.1 에서 설명 방식 11줄이 「문서 지도」 절 위에 들어가 그 절이 2,472자로 밀려났고, 프로젝트 NEXT 블록(4만 9천 자)이 같은 출력에 붙어 늘 잘렸다 — 그래서 볼트 · 그래프를 안 보고 원문을 처음부터 다시 셌다. 고친 것: `rules.md` 「문서 지도」를 맨 앞(394자)으로 · `session-start.sh` 는 규칙 · 모델 지침을 먼저 내고 NEXT 블록을 남은 글자 수만큼만 붙인다(넘으면 알림) · 모델 미확인이면 지침 파일 경로만 · 첫 줄에 「잘렸으면 저장 파일 전체를 Read」. `build` EXPLORE 는 볼트 · 그래프 먼저 · REVIEW 는 다른 도구(Codex)에 볼트 위치와 NEXT 블록을 함께 · REFLECT 는 바뀐 볼트 · 그래프를 SHIP 전에 다시 굽는다. 시험: opus · fable · sonnet · 모델 없음 × NEXT 4만 9천 자 · 977자 — 출력 6,555~9,388자, 「문서 지도」 394자.

**2026-10-28 — 1.8.2 맷 포콕 스킬에서 네 줄.** Codex 가 mattpocock/skills 38개를 우리 dev 와 대조했다(12개 이미 있음·21개 불필요·5개 효과). 기존 문장을 바꿔 줄 수는 그대로: build REFLECT — 반복 실수는 기존 검사가 도는지 먼저 보고 기계로 잡을 것은 검사로 막는다(retro) · REVIEW — 규칙 위반과 요구 대조(빠진 것·요청 밖 변경)를 나눠 보고(code-review) · 버그 — 원래 증상을 낸 명령을 고친 뒤 같은 명령으로 확인(diagnosing-bugs) · setup AGENTS 템플릿 — 문서 경로에 읽어야 하는 작업을 붙인다(writing-for-agents). guide 의 「추천 전 본문 읽기」는 효과가 작아 뺐다. grill 류(질문 반복)는 「답이 크게 갈릴 때만 묻는다」와 충돌해 들이지 않았다. 계기: 사용자 「이 typescript 스킬 우리 dev 스킬에 적용했을때 효과가 있는 부분이 있는지 검토 … 니가 적용해」.

**2026-10-26 — 1.8.1 설명 방식.** `rules.md` 작업 원칙: 사용자에게 쓰는 모든 글을 항공정비 문서 방식(ASD-STE100 간이 기술 영어)을 한국어에 적용해 쓴다 — 결론 먼저 · 한 문장 한 가지 · 짧은 문장 · 한 단어 한 뜻 · 누가 했는지 · 번호 붙인 명령형 할 일 · 위험 먼저 · 용어 풀어 쓰기 · 문단 다섯 줄 · 실제 값. 계기: 사용자 「앞으로 나한테 설명할때 항공정비용어 그 방식으로 … 무스말인지 모르겠다」. 사용자 PC 한 대의 `~/.claude/CLAUDE.md` 대신 플러그인에 둔 까닭: 플러그인을 설치한 모든 PC에 같이 적용된다.

**2026-10-21 — 1.7.1 문서 지도.** 실제 프로젝트에서 연구 문서 40여 개가 쌓였는데 인덱스가 1주일 전 상태라, 근거를 물을 때마다 grep으로 헤맨 일에서.
- `rules.md` "문서 지도" 절: 볼트 위치는 AGENTS.md에 적힌 곳 · 근거 질문은 인덱스 노트(질문 → 결론 → 문서#절)부터 · 코드 고치기 전 관련 노트와 `[[링크]]`로 영향 확인 · 고친 뒤 노트·인덱스 갱신(생성 노트는 원천을 고치고 다시 생성).

**2026-10-21 — 1.7.0 게임 이식 노하우.** 새 참조 `skills/build/references/game-port.md`: PC 게임 → 모바일 이식(원작이 동작 명세인 프로젝트)을 어둠의 전설(LOD)·메이플스토리 두 번 해 보며 통한 순서(분석서 → 지식 볼트 → 기획 → 엔진 가설 실기기 실측 → 정답 층 → 한 바퀴 뼈대 → 콘텐츠 SPEC → 운영), 정답지(참조 구현과 제품을 다른 손이, 원작 실행물로 벡터, 자료 전수 대조, 없는 수치는 지어내지 않음), 서버 권위 + 클라이언트 예측(같은 core 파일, 거절돼도 난수 소비, 「몹이 되살아남」의 세 원인), 시험 층(core 벡터·서버 봇·헤드리스 화면·긴 봇·눈가린 점검·실기기)과 흔들림 원인, 모바일 조작(가로 고정·390pt·두 손가락·편의 기능은 의도적 변경), 혼자 운영(본문까지 상태 확인·멈춘 사이 DB 보정·운영 기록부터), 시행착오 표. `reverse-engineering.md` 3-3: 실행 파일 역공학을 서브에이전트에 맡기는 법(우선순위 질문 목록·덤프 재사용·[관찰]/[추정] 표·핵심 분기는 메인이 재확인). build 본문·design 규칙 13 ⑤가 가리킨다. 계기: 사용자 「메이플 만들면서 개발 순서나 시행착오 구현 테스트 같은 전반적인 노하우 … Pc 게임을 모바일로 구현할때 필요한 노하우도 함께」.

**2026-10-17 — 1.6.9 현업 바닥선.** 새 참조 `skills/design/references/engineering-baseline.md`: 사용자가 기능만 말해도 설계에 들어가는 구현 품질 17항목(코드 구조·의존 조립·오류 두 갈래·입력 꼴 검사·구조화 로그·DB 구조(마이그레이션·쿼리별 색인 대조표·제약·트랜잭션)·DB 연결 시간 제한·설정 검사·종료 때 저장·주석·빈도 제한·상태 확인·백업 복원 연습·만료 정리·공유 계약·품질 도구·의존 패키지) — 항목마다 정할 문서·기본값·구현 확인. design 규칙 14·심문 12축(항목마다 마킹, 미루면 「언제」)·A4 「코드 구조」·A5 「저장소 설계」·A7 줄 추가, check_package C10(절이 없으면 HIGH). build 공통 5번 「현업 바닥선 대조」(SPEC 「코드 위치와 바닥선」, REVIEW·완료 체크), rules.md: 사용자가 말한 작업 방식은 메모리에만 두지 말고 AGENTS.md 규약·04에 올린다. 계기: 메이플 — 처음 지시 「현업 방식(레이어·서비스·예외·로그)으로」가 메모리에만 남아 새 서버가 한 파일로 만들어졌고, 사용자가 「분명 최초 요구사항에 있었을텐데」·「현업 기준 더 채울 곳까지 아예 스킬에서 기획 설계 단계에서 주입되도록」.

**2026-10-17 — 1.6.8 위임: 메인 컨텍스트 아끼기 조건·브리프·반환.** rules.md·`skills/build/references/model-routing.md`: 위임 기본값은 그대로 메인. 위임하는 경우에 「출력이 길고 다시 볼 일 없는 일(로그·대량 검색·파일 덤프)」을 더하고, 맥락을 이어 가는 구현 단계는 메인에서, 같은 파일·같은 결정에 닿는 구현은 병렬 위임 금지, 맡길 때 목표·범위·정한 결정·돌려받을 형식과 길이 상한을 적고 돌려받은 핵심은 경로·줄로 직접 확인. 근거·버린 안(작업마다 무조건 위임)은 `skills/build/references/evidence.md` 「위임과 메인 컨텍스트」. 계기: 사용자 「작업별로 서브에이전트에서 해서 메인 컨텍스트는 차지 안하게 하던데 효과적인게 맞다면 적용」.

**2026-10-17 — 1.6.7 검증 게이트·장시간 작업.** Stop 훅 `hooks/verify-gate.sh`: 프로젝트 AGENTS.md에 `<!-- dev:verify: 명령 -->`을 적어 두면, NEXT.md가 M·L의 BUILD·VERIFY 단계이고 커밋 안 된 변경이 있을 때 턴을 마치기 전에 그 명령을 돌려 빨간불이면 종료를 막고 실패 꼬리를 돌려준다(3번 연속이면 경고만). 선언이 없으면 아무것도 안 한다 — 훅은 권한 확인 없이 도니 남의 저장소의 선언은 열기 전에 확인할 것. rules.md: 끝이 명령 결과로 증명되는 일은 `/goal`을 권한다. build VERIFY: 장비·장시간 작업은 「시작」과 「결과 받기」로 나눠 백그라운드로. 근거·버린 대안(완료 약속 문자열 루프 등)은 `skills/build/references/evidence.md` 「하네스·루프」. 계기: 사용자 「하네스, 루프 엔지니어링이 적용되는 구조인지」 — 조사 결과 둘 다 「부분」, 외부 신호가 종료를 막는 장치가 없었다.

**2026-10-17 — 1.6.6 상수 표 밖 숫자 검사.** check_package C9: 04~07에 단위가 붙은 숫자(ms·초·px·%·비트 …)가 상수 이름 대신 직접 쓰인 줄을 INFO로 보인다(근거 인용 `File:줄`은 뺌). 계기: 메이플 GATE 검토관이 「03 상수 표에 없는 숫자가 06·07·04에 흩어져 있고 자기 검증 스크립트는 잡지 못한다」고 지적 — 첫 실행에서 실제 두 곳(틱·초대 코드 길이)을 잡았다. 오탐(데이터 형식 「64비트」 등)이 있어 막지 않고 보이기만.

**2026-10-17 — 1.6.5 이전 프로젝트 답습 금지·원작 이식.** design 규칙 12: 이전 비슷한 프로젝트는 비교 대상이지 기본값이 아니다 — A1에 「이전 프로젝트에서 안 된 것」 절(그 기록에서 실제로 어긋난 것), 가져오는 것은 고친 형태로만. 규칙 13(원작 이식·지식 볼트): 산출물은 볼트의 PRD 폴더, 요구사항 하나 = 스코프 노트의 `##` 절 하나(원작 동작 근거 `File:줄`·자료 ID·`관계::`), 의도적 변경 목록·옮기지 않는 원작 버그 목록을 03과 함께. 규칙 11: 완료 기준마다 잼 수단, 「지금」은 손글 대신 그 수단의 결과. 규칙 3 예외: 사용자가 받기로 한 결정 목록은 5문항을 넘어도 한 배치(check_package C5가 register의 「사용자 결정 목록」을 본다). 빈 곳 점검 프로파일 P8 원작 이식·리메이크. 계기: 메이플(LOD 다음 이식)에서 시드에 「LOD와 같은 해석」을 쓰자 사용자 「lod 껄 답습하지말고 개선해가면서 스킬도 수정시키면서」. LOD 실측: PRD 없이 기능 SPEC 폴더 18개, goals 「지금」 칸 손글이라 목표 5개 중 4개에 「낡음·안 잼」, 의도적 변경 목록은 끝내 안 만듦.

**2026-10-17 — 1.6.4 세 분석기 실측.** 같은 exe 를 Ghidra·IDA Free·Hopper 데모로 rea 에 물어 objdump 정답과 비교 — 생성자 호출 113곳 중 57·113·113. 실행 파일은 rea+Ghidra → rea+IDA Free 로 빈 곳 → objdump 로 수 세기 → 필요하면 Hopper. IDA Free 맥 설정(라이선스 `~/.idapro`, 연결 플러그인 127.0.0.1 빌드, 무료판 자동 실행 막힘 → `IDA_MCP_AUTOSTART`)과 Hopper 데모(기한 없음, 30분·저장 불가)를 `reverse-engineering.md` 3-1 에.

**2026-10-17 — 1.6.3 보이는 브라우저 기본.** 브라우저를 직접 눌러야 하는 일은 Aside(보이는 브라우저)가 기본이고, 사이트가 Aside 조작을 받지 않거나 창이 필요 없을 때(사진 한 장·수십 번 되풀이)만 헤드리스. 캡차·봇 차단·robots·약관 금지는 헤드리스로 바꿔 넘지 않는다(우회). 계기: 사용자 「사이트가 허락 안할때만 헤드리스로 전환하는 방식으로」.

**2026-10-17 — 1.6.2 역공학 도구 보강.** 실행 파일은 rea+Ghidra 하나를 「전부」로 믿지 않고 objdump 전체 풀이로 맞춰 보며, Ghidra 가 못 잡은 곳은 IDA Free(설치돼 있으면, rea native bridge)로 다시 본다 — 근거 칸에 도구를 적는다. 로그인한 화면을 직접 눌러야 하면 Aside CLI(`aside exec`·`aside repl`, 보이는 창이라 헤드리스로 안 될 때만). `skills/build/references/reverse-engineering.md` 3-1·3-2. 계기: 게임 클라이언트 역공학에서 Ghidra 가 vtable 함수·호출자 1개를 조용히 빠뜨림, 사용자 「ghidra, ida, hooper 를 모두 사용해서 분석을 했는지」.

**2026-10-16 — 1.6.1 받아쓰기 목표.** goals.md는 사용자 원문을 옮겨 적는 문서가 아니라, 원문을 입력으로 목표마다 깊이 조사해 세운 목표·완료 기준·정답지다. 기존 제품도 dev:design 목표 수립(lite)으로 만든다. 계기: 1.6.0 규칙대로 원문만 모은 goals.md에 사용자가 「곧이곧대로 … 말한대로 해준거다 같은 되지도 않는 방식」이라고 함.

**2026-10-14 — 1.6.0 덧대기·검증 공백.** 실제 프로젝트에서 사용자 말마다 기능을 덧대고(SPEC 20개), 테스트·리뷰가 내 SPEC만 확인해 "의미 없는 화면"이 통과한 사건에서.
- 목표 한 장(`docs/goals.md`) — 모든 요청을 대조, 목표가 바뀌면 거기부터. design이 만들고 목표 갱신(lite)으로 고친다.
- build 공통 4가지: 목표 대조 · 전제 도전(만들기 전에 도메인 조사로 "맞는 문제인가" 제안, 의미 표) · 정답지 채점(실제 사례와 대조해야 완료) · 눈가린 점검(코드·SPEC 없이 목표+앱만 본 새 에이전트가 실제 브라우저로).
- 모델별 지침: `rules-models/<계열>-<버전>.md`를 훅이 세션 모델로 골라 붙인다(Opus 5.5·Fable 5.1, Anthropic 모델별 프롬프팅 가이드 문구).
- 근거·외부 저장소(gstack·BMAD TEA·spec-kit): `skills/build/references/evidence.md`.

**모델 지침 갱신(새 모델이 나오면).** 훅이 "전용 지침 파일이 없어 …를 붙였다"를 띄우면: Claude Code 번들 `claude-api` 스킬의
`shared/model-migration.md`에서 그 모델의 "Migrating to … › Behavioral shifts (prompt-tunable)" 절을 읽고, 이전 파일을 복사해
`rules-models/<계열>-<버전>.md`로 만든 뒤 바뀐 버릇만 고친다(공식 문구는 그대로). 그다음 `/claude-api prompt-audit`으로 rules.md와 새 파일을 점검하고 evidence.md에 출처·날짜를 적는다.

**2026-10-14 — 1.5.9.** 남의 앱·웹 동작 파악 연결 — `morluto/rea`(Reverse Engineer Anything MCP, MIT ★20.8만): build EXPLORE·design A1에서 설치돼 있으면 사용. `skills/build/references/reverse-engineering.md`에 관문(robots·약관·봇 차단 → 허용/애매/금지, 우회·대량 수집 금지)과 덜 침습적인 순서(공유 URL 파싱 → 사용자가 연 페이지 읽기 → 공식 API → REA로 구조 파악)를 둠. 계기: 부동산 판정 앱에서 "네이버·KB·직방 어느 사이트 매물인지, 아직 있는지 추적" 요청 — 2026-10-14 확인 시 land.naver.com·kbland.kr robots 전면 금지, 직방 CloudFront 봇 차단, fin.land.naver.com은 /articles 허용.

**2026-10-14 — 1.5.8.** dev:ui 데이터 화면 보강. 기존 화면 개선 감사 절차 `references/audit.md`(1440·390 스크린샷 → 패스 10개 → 상위 3개만 → 위계→구성→글자→색→상태→모션 순 → 최대 3라운드, 스택·라우트·셀렉터 보존), 차트 패턴 `references/patterns/charts.md`(종류 고르기·가격 선 + 거래량 막대 겹치기·드문/빈 구간 끊기·높이 예약·표 보기), 하드룰(앱 셸 전폭·간격/시작선·`min-width:0`·높이 예약·숫자 `tabular-nums`(모노는 ID·코드만)·글자 크기 5개 이하·강조색 1곳·밀집 화면 쉬는 그림자 금지), 모션 AI 티 임계값(`motion.md`), 사이트 → DESIGN.md 추출기(`design-md.md`). 출처(전부 MIT): Leonxlnx/taste-skill ★9.6만, nextlevelbuilder/ui-ux-pro-max-skill ★13.5만, kylezantos/design-motion-principles, bergside/design-md-chrome, VoltAgent/awesome-claude-design(awesome-design-md와 겹쳐 미채택). 랜딩·이미지 생성 지침은 가져오지 않음. 계기: 부동산 판정 앱 "시세 추이 차트부터 엉망".

**2026-10-08 — 1.5.6.** dev:ui에 화면 패턴 층 추가. `references/patterns/`(11개 패턴군 — 측정 가능한 규칙·실제 예시·출처 236건, 무료 레퍼런스 출처 표 `sources.md`)를 화면마다 읽고 레퍼런스 2~3개·결정 근거를 남기는 단계, 정보 구조 하드룰(결론 1줄·기준 대비·설명 접기·핵심 화면 우선), Anthropic 공식 frontend-design 대조(`official-guides.md`)로 AI 티 4행·Pre-Flight 3줄·서체 대안 교체(Inter Tight → IBM Plex Sans), 모션 수치 `motion.md`. 계기: 부동산 판정 앱에서 "숫자만 나열·결론 없음·설명 상시 노출·핵심 화면이 밀림" 지적이 반복 — DESIGN.md(토큰)로는 못 막았다. Mobbin(유료) 대신 무료 SaaSUI.design MCP를 선택 연결로.

**2026-10-08 — 1.5.5.** dev:ui에 DESIGN.md 단계 추가: 프로젝트 루트 DESIGN.md를 디자인 기준으로 따르고, 없으면 VoltAgent/awesome-design-md(MIT, 74개)에서 프로파일별 추천 1개를 받아 브랜드 제거·한글 서체·토큰화·데이터 화면 보정 후 사용. 우선순위는 기능 하드룰 > DESIGN.md > tokens.md. 기존 테마가 있는 화면 수정에는 들이지 않는다.

**2026-09-30 — 1.5.4.** 웹 UI 후보 ui-ux-pro-max를 dev:ui와 같은 요청으로 비교 → 낫지 않아 미연결. ui Pre-Flight에 폰 너비 스크린샷·가로 스크롤 확인 추가.

**2026-09-30 — 1.5.3.** `export.py --project <폴더>`: 원격·클라우드 Codex용으로 저장소 안(AGENTS.md 블록, `.agents/skills`)에 설치. 빈 홈 폴더의 Codex CLI 0.158에서 규칙·스킬 로드 확인.

**2026-09-30 — 1.5.2.** Godot 모바일: 참조·아트가 없으면 색을 혼자 정하지 않고 색만 바꾼 시안 2~3개를 찍어 고르게 한다. 팔레트는 한 곳에, 광고 게임 색(채도 최대 배경+형광 강조) 피하기.

**2026-09-30 — 1.5.1.** Godot 모바일에 "게임다움" 절 추가(참조 게임 두 개, Kenney CC0·Google Fonts OFL 자원, 그라데이션 배경, 가운데 주인공 요소, 아이콘, 글자 외곽선, 깊이, 대기 애니메이션, 스크린샷 자문). 규칙만 있던 1.5.0은 "틀리지 않은" 화면에서 멈췄다.

**2026-09-30 — ui에 Godot 모바일 (1.5.0).** Godot 프로젝트면 웹 규칙 대신 `references/godot-mobile.md`(Theme·컨테이너·노치 SafeArea·터치 48dp·글자 크기·반응감)를 따르고, `scripts/godot_shots.gd`로 폰 2종·태블릿 1종 스크린샷을 찍어 보며 고친다(Godot 4.4.1에서 확인). 웹 UI 후보는 외부 스킬 흡수 기준에 정리.

**2026-09-30 — 1.4.2 (헤드리스 실측으로 고침).** "헬스장 회원 관리 서비스" 같은 작은 새 서비스가 M으로 판정돼 설계를 건너뛰던 것을 고쳤다. 새 서비스는 기능 수와 상관없이 L 신규이고, 크기는 design의 lite·spike가 조절한다. `/rewind` 권유 문구를 구체적으로 바꿨다(이전 문구로는 두 번 되돌려도 권유가 안 나왔다).

**2026-09-30 — 1.4.1.** superpowers는 공식 마켓(claude-plugins-official) 것을 의존성으로 쓴다(이미 설치한 사람과 두 벌이 되지 않게). ponytail은 HTTPS 주소로 받는다(`github` 방식은 SSH 키가 없는 PC에서 실패).

**2026-09-30 — 재정비 경로 (1.4.0).** 막히거나 지지부진한 기존 프로젝트를 build가 실행 기반으로 진단하고, 원인(버그·회귀·결정 공백·범위 팽창)에 맞는 경로로 넘긴다.

**2026-09-30 — 팁 영상 반영 (1.3.0).** 사람이 기억해야 하던 팁을 Claude가 알맞은 때 권하거나(규칙 "세션 관리"), 프로젝트 준비 때 한 번에 설정하게(setup: 허용 목록·절대 규칙 훅) 바꿨다. 겹치는 도구는 넣지 않았다(외부 스킬 흡수 기준 참고).

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
