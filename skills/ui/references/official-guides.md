# Anthropic 공식 프론트엔드·디자인 권장 — 규칙 목록과 dev:ui 대조표

확인일 2026-10-08. 모든 인용은 그날 WebFetch/curl로 원문을 읽은 것이다. 읽지 못한 것은 "미확인"으로 적었다.
dev:ui의 **dial·프로파일·하드룰·DESIGN.md 체계는 그대로 두고**, 아래 "반영 제안"만 SKILL.md·tokens.md·anti-slop 표에 옮기면 된다.

## 0. 출처 (읽은 것 / 못 읽은 것)

| # | 출처 | 상태 | 라이선스·비고 |
|---|---|---|---|
| S1 | Cookbook "Prompting for frontend aesthetics" https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics | 읽음 | `DISTILLED_AESTHETICS_PROMPT`·`TYPOGRAPHY_PROMPT` 원문 포함 |
| S2 | 블로그 "Improving frontend design through Skills" https://claude.com/blog/improving-frontend-design-through-skills | 읽음 | "distributional convergence" 정의 |
| S3 | anthropics/skills `skills/frontend-design/SKILL.md` https://github.com/anthropics/skills/tree/main/skills/frontend-design | 읽음(raw 9.4KB 전문) | **Apache-2.0** (`LICENSE.txt` 확인). S1보다 최신·절제 쪽으로 바뀐 버전 |
| S4 | "Prompting Claude Opus 5.5" https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5 | 읽음 | "Frontend design defaults" 절 |
| S5 | "Prompting Claude Opus 4.8" https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8 | 읽음 | "Design and frontend defaults" 절 — 하우스 스타일 정의·대안 프롬프트 2개 |
| S6 | "Prompting Claude Sonnet 5" https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 | 읽음 | S5와 같은 절·같은 예시 |
| S7 | "Prompting best practices" https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | 읽음 | "Frontend design"·"Document creation"·Migration 3번 |
| S8 | Opus 5.5 출시 글 https://www.anthropic.com/news/claude-opus-5-5 (2026-09-22) | 읽음 | **디자인·모션·영상 언급 없음.** "design"은 설계 문서 뜻, 게임 사용 후기에 "graphics and polish" 한 줄 |
| S9 | "What's new in Claude Opus 5.5" https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5 | 읽음 | 프론트·모션 언급 없음. 비전(차트·스크린샷 판독 정밀화)만 |
| S10 | Claude Design 시작하기 https://support.claude.com/en/articles/14604416-get-started-with-claude-design | 읽음 | 2026-04-17 공개(검색 요약), Pro·Max·Team·Enterprise 베타 |
| S11 | Claude Design 디자인 시스템 설정 https://support.claude.com/en/articles/14604397-set-up-your-design-system-in-claude-design | 읽음 | 디자인 시스템 = 색·서체·컴포넌트·레이아웃. **모션 항목 없음** |
| S12 | 아티팩트 전용 공식 디자인 가이드 | **미확인** — 공개 문서를 못 찾음. S7이 "Claude Design"을 가리킬 뿐 | |

## 1. 공식 권장 — 규칙 목록 (O1~O30)

짧은 인용은 원문 그대로(영문). 괄호는 출처.

### 왜 (문제 정의)
- **O1** 모델은 평균으로 수렴한다 — "Safe design choices–those that work universally and offend no one–dominate web training data." (S2) / "You tend to converge toward generic, 'on distribution' outputs." (S1, S7)
- **O2** "avoid a generic AI look" 같은 **일반어는 안 통한다.** "a general instruction such as 'avoid a generic AI look' mostly swaps one default for another. It responds well to instructions that name specific patterns to avoid" (S4). "Generic instructions ('don't use cream,' 'make it clean and minimal') tend to shift the model to a different fixed palette rather than producing variety." (S5, S6)
- **O3** 현재 하우스 스타일(4.8 이후): "warm cream/off-white backgrounds (~#F4F1EA), serif display type (Georgia, Fraunces, Playfair), italic word-accents, and a terracotta/amber accent" — "will feel off for dashboards, dev tools, fintech, healthcare, or enterprise apps" (S5).
- **O4** S3가 적은 AI 티 5군: (1) 크림 배경 + 세리프 디스플레이 + 테라코타(#D97757 근처 — "Anthropic's own Claude-interaction accent, so on a user's brief it reads as a tell"), (2) 근검정 + 산성 초록/주홍 강조 하나, (3) 헤어라인·반경 0·신문 칼럼, (4) "the SaaS-card kit: content chopped into identical rounded cards, one border-radius on everything regardless of hierarchy, the same soft grey shadow (rgba(0,0,0,.1)) under each, and gradient washes as decoration", (5) 템플릿 크롬: "a tracked-out ALL-CAPS eyebrow label above every heading; meta strings joined with middle dots ('A · B · C'); labels built as 'WORD — fragment' with a spaced em dash; tinted near-black (#0B0B0B, #111) standing in for black; a monospace face for small data labels; a '→' appended to link and button text." 단, "the brief's own words always win".

### 프로세스
- **O5** 디자인 리드 역할: "Approach this as the design lead at a design studio known for giving every client a distinct visual identity that is not mistaken for anyone else's." (S3)
- **O6** 주제에서 출발: "If the brief does not identify what the product or subject matter is, identify it yourself before designing, and confirm with the client." (S3)
- **O7** 2패스: 먼저 "a compact token system with color, type, layout, and principles" — 색은 "4–6 named hex values", 레이아웃은 "one-sentence prose descriptions and ASCII wireframes" — 그다음 "review that plan against the brief before building: if any part of it reads like the generic default you would produce for any similar page … revise that part, say what you changed and why." (S3)
- **O8** 방향 후보 제안: "Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface — one-line rationale). Ask the user to pick one, then implement only that direction." (S5, S6)
- **O9** 구체 스펙이 통한다: "The model follows explicit specs precisely" — 예시 프롬프트에 반경 4px, 팔레트 5개 hex, "transition: all 160ms ease out" 같은 수치가 들어 있다 (S5, S6).
- **O10** 스크린샷 자기검토: "Critique your own work as you build, taking screenshots to review if your environment supports it — a picture is worth 1000 tokens." (S3)
- **O11** 반복: "Work iteratively: check which styles the first result used instead, and extend the list if needed." (S4)
- **O12** 애니메이션은 명시적으로 요청해야 나온다: "Animations and interactive elements should be requested explicitly when desired." (S7 Migration 3)

### 타이포
- **O13** 금지 서체: "Never use: Inter, Roboto, Open Sans, Lato, default system fonts" (S1). 대안군: Code(JetBrains Mono, Fira Code, Space Grotesk) / Editorial(Playfair Display, Crimson Pro, Fraunces) / Startup(Clash Display, Satoshi, Cabinet Grotesk) / Technical(IBM Plex family, Source Sans 3) / Distinctive(Bricolage Grotesque, Obviously, Newsreader). 단 "You still tend to converge on common choices (Space Grotesk, for example)".
- **O14** 페어링·극단: "High contrast = interesting. Display + monospace, serif + geometric sans" / "Use extremes: 100/200 weight vs 800/900, not 400 vs 600. Size jumps of 3x+, not 1.5x." (S1)
- **O15** 가족 수: "use one family or two, and if two, make them clearly distinct." (S3)
- **O16** 행 길이: "Default to line lengths of less than 80 characters." 세리프 본문은 line-height를 조금 더 (S3).
- **O17** 타이포 AI 티 3개: "Accenting just a single word or phrase in a headline" / "Using all caps for labels" / "Adding unnecessary typographic labels above content" (S3).

### 색·배경·구조
- **O18** "Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes." (S1) 클리셰: "purple gradients on white backgrounds".
- **O19** 배경 (S1, 구버전): "Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns" — 그러나 S3(신버전)는 "gradient washes as decoration"을 AI 티로 분류. 아래 충돌 C2.
- **O20** 구조는 정보: "Structural devices like outlines, borders, numbering, eyebrows, dividers, labels, etc., encode useful information about the content rather than decorate it." 01/02/03은 "only appropriate if the content actually is a sequence" (S3).
- **O21** 히어로 기본값 경계: "a big number with a small label, supporting stats, and a gradient accent is the default treatment, so only use it if that's truly the best option." (S3)
- **O22** 과감함은 한 곳: "Spend your boldness in one place. Let one element be the memorable thing, keep everything around it quiet and disciplined" / "remove one accessory" (S3).

### 모션
- **O23** (S1) "Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions."
- **O24** (S3) "Use non-user-triggered motion sparingly and deliberately, only to draw attention. A single orchestrated moment — one page-load sequence or one reveal — lands better than scattered effects; fade-and-slide-up entrances on each section and hover transitions on every card are the generic default and read as AI-generated. Motion that answers a person's action (opening, expanding, confirming) is welcome when it shows what changed."

### 품질 바닥·카피
- **O25** 품질 바닥: "responsive down to mobile, visible keyboard focus, reduced motion respected, visually accessible, harmonious color palettes." (S3)
- **O26** CSS 특이성 주의: ".section 같은 타입 선택자와 .cta 같은 요소 선택자가 서로 지우기 쉽다" 취지 (S3).
- **O27** 카피는 기능: "A CTA says exactly what happens when it is used: 'Save changes,' not 'Submit.' … the button that says 'Publish' produces a toast that says 'Published.'" (S3)
- **O28** 오류·빈 상태: "Errors don't apologize, and they are never vague about what happened. An empty screen is an invitation to act." / 사용자 언어: "A user manages notifications, not webhook config." / "sentence case, no filler" (S3)
- **O29** Claude Design 디자인 시스템 = "Color palette / Typography / Components / Layout patterns"; "Include real examples, not just specs. A finished landing page or marketing site tells Claude more about your brand's feel than a color palette alone." Claude Code에서 `/design-sync`로 React 컴포넌트·토큰을 읽어 만들 수 있다 (S11). 핸드오프: "hand it off to Claude Code, which continues from your existing work instead of starting over from a screenshot." (S10)
- **O30** Opus 5.5 비전: "even at its lowest effort setting it read values off dense charts more accurately than Claude Opus 5 did at its highest" (S4) → 스크린샷 자기검토(O10)의 비용이 낮아졌다. 출시 글(S8)·What's new(S9)에는 프론트·모션 권장이 **없다**.

## 2. dev:ui 대조표

상태: ✅ 있음 · ➕ 없음(추가) · ⚠️ 충돌(3절에서 판정) · ➖ 범위 밖

| # | 공식 권장 | dev:ui 상태 | 반영 제안(문구) |
|---|---|---|---|
| O1·O2 | 수렴 문제, 일반어 금지·**구체 패턴 이름으로** 금지 | ✅ 4절 anti-slop 표가 이미 구체적. 다만 "AI스럽다를 고칠 때"가 일반어 | SKILL.md 4절 머리에 한 줄: "'AI 티 나지 말라'는 말은 기본값을 다른 기본값으로 바꿀 뿐이다(공식 문서). 아래 표처럼 **이름을 붙인 패턴**으로 금지하고, 1차 결과에서 쓴 패턴을 보고 표를 늘린다." |
| O3·O4 | 하우스 스타일(크림·세리프·테라코타)과 5군 AI 티 | ➕ 표에 "John Doe·필러 카피·동적 클래스·정상 상태만" 4줄뿐 | 4절 표에 추가: `크림 배경(#F4F1EA) + 세리프 디스플레이 + 테라코타/앰버(#D97757) 강조` → DESIGN.md 팔레트; `헤드라인 한 단어만 이탤릭·색 강조` → 통째 위계; `모든 제목 위 자간 넓힌 ALL-CAPS 아이브로`·`'A · B · C' 메타`·`'WORD — fragment'`·`링크·버튼 끝 '→'` → 필요한 정보만; `카드 전부 같은 반경·같은 회색 그림자(rgba(0,0,0,.1))·장식 그라디언트` → 위계별 반경·tokens.md 그림자 1종; `01/02/03 번호` → 실제 순서일 때만 |
| O7·O8 | 토큰 계획 → 브리프 대조 → 코드; 방향 4개 제안 | ⚠️ 부분: DESIGN.md 받기 + "후보 2~3개 미리보기"는 있음. **브리프 대조 리뷰 단계 없음** | 2절 "디자인 기준" 뒤에 3줄: "DESIGN.md를 적용하기 전에 색 4~6 hex·서체 역할·레이아웃 한 문장(ASCII 와이어프레임 가능)을 적고, '비슷한 다른 브리프에도 같은 답이 나오는가'를 자문해 그런 부분만 고치고 무엇을 왜 바꿨는지 한 줄 남긴다." 사용자가 방향을 못 정하면 "bg hex / accent hex / 서체 / 한 줄 근거" 형식으로 **4개**를 내고 하나를 고르게 한다(현재 2~3개 → 4개로 맞추거나 "2~4개"로). |
| O9 | 구체 수치 스펙이 통한다 | ✅ "정성 표현 → 측정 가능 기준" 한 줄 | 그 줄에 예시 추가: "(예: 반경 4px 통일, 팔레트 5 hex, 버튼 hover `transition 160ms ease-out`)" |
| O10·O30 | 스크린샷 자기검토, 5.5는 판독 정밀 | ✅ Pre-Flight 폰 스크린샷 | 데스크톱 폭도 한 장(1440) 추가 권장 — 현재 390만 명시 |
| O12 | 애니는 명시 요청 시에만 | ✅ MOTION dial이 그 역할 | 변경 없음. motion.md에서 dial 값별로 구체화 |
| O13 | Inter·Roboto·Open Sans·Lato·시스템 금지 | ⚠️ tokens.md 페어링 3행 중 `Inter Tight`(대안) 포함. SKILL.md는 "Inter 하나로 덮으면 템플릿 티" | 3절 충돌 C1 참조. 제안: tokens.md 4절에서 `Inter Tight` 행을 `IBM Plex Sans`+`IBM Plex Mono`로 교체(공식 Technical 군). 주석: "Inter·Roboto·Open Sans·Lato·시스템 폰트는 공식 금지 목록(S1). 단 DESIGN.md가 정하면 그쪽." |
| O14 | 굵기 극단(100/200 vs 800/900), 크기 3배 점프 | ➕ 없음 | **마케팅/랜딩 프로파일에만**: "디스플레이는 굵기 극단(200↔800)과 3배 이상 크기 점프로 위계를 만든다. 제품·관제 화면은 1.25~1.5 배율 유지(판독)." |
| O15·O16 | 서체 1~2가족, 행 길이 < 80자 | ➕ 행 길이 없음 | 타이포 하드룰에 한 줄: "본문 행 길이 80자 이하(한글은 `max-w-prose` 기준 40~45자). 데이터 표는 예외." |
| O17 | 한 단어 강조·ALL-CAPS 라벨·불필요 라벨 | ➕ 없음 | 위 O4 행에 포함. 추가로 tokens.md 5절 "지표 라벨은 작게·저대비"에 "대문자·자간 넓힘 금지, sentence case" 보강 |
| O18 | CSS 변수로 일관, 지배색 + 날카로운 강조 | ✅ "테마 토큰 사용", "글로우·그라디언트는 강조 한 곳에만" | 변경 없음 |
| O19 | 배경에 분위기·깊이(그라디언트·패턴) | ⚠️ dev:ui는 절제. 충돌 C2 | 프로파일 분기: 랜딩(VARIANCE ≥ 6)만 "배경 한 레이어(그라디언트·패턴·grain)는 허용, 섹션마다가 아니라 히어로 한 곳". 제품·관제는 현행 유지 |
| O20·O21 | 구조 장치는 정보 인코딩; 히어로 기본값(큰 숫자+작은 라벨+통계+그라디언트) 경계 | ➕ 없음 | 4절 표에 `랜딩 히어로 = 큰 숫자 + 작은 라벨 + 보조 통계 + 그라디언트 강조` → "주제에서 가장 특징적인 것(헤드라인·이미지·라이브 데모) 하나" |
| O22 | 과감함은 한 곳, 액세서리 하나 빼기 | ✅ "글로우·그라디언트는 강조 한 곳에만" | Pre-Flight 마지막에 "장식 하나를 빼도 되는가? 빼라." 한 줄 |
| O23·O24 | 모션: 사용자 동작에 응답하는 모션은 환영, 비촉발 모션은 한 번의 오케스트레이션, 섹션마다 fade-slide-up·카드마다 hover = AI 티 | ⚠️ 부분: MOTION dial만 있고 **무엇을/언제**가 없음. 3절 C3 | `references/motion.md`로 연결. 4절 표에 `모든 섹션 fade+slide-up 등장 · 모든 카드 hover 들썩임` → "페이지 로드 1회 오케스트레이션(랜딩) 또는 동작 응답 모션만(제품·관제)" |
| O25 | 키보드 포커스 보임·reduced motion 존중 | ➕ 둘 다 없음 | Pre-Flight 추가 2줄: "[ ] 포커스 링이 보이나(`focus-visible`)? [ ] `prefers-reduced-motion`에서 이동·패럴랙스·자동재생이 꺼지나?" |
| O26 | CSS 특이성 충돌 | ➖ Tailwind 중심이라 거의 무관 | 변경 없음 |
| O27·O28 | CTA는 결과 동사("Save changes"), 같은 이름 유지, 오류는 사과 않고 구체, 빈 화면은 행동 초대 | ⚠️ 부분: "필러 카피 금지", 빈/에러 상태 **존재** 요구만 | 4절 표에 `"제출/확인/Submit"` → "일어나는 일 그대로('변경 저장')"; `"죄송합니다, 문제가 발생했습니다"` → "무엇이 안 됐고 무엇을 하면 되는지"; `빈 화면 '데이터가 없습니다'` → "다음 행동 버튼 하나" |
| O29 | Claude Design 디자인 시스템·`/design-sync` 핸드오프 | ➕ 없음 | design-md.md "받기" 앞에 한 줄: "팀이 Claude Design을 쓰면 그 디자인 시스템(색·서체·컴포넌트·레이아웃)을 DESIGN.md의 원천으로 쓴다. 모션은 거기 없으니 motion.md로 보강." |
| S8·S9 | Opus 5.5 자체의 디자인·모션 권장 | ➖ 공식 문서에 없음 | 스킬에 "Opus 5.5가 모션을 잘한다" 식 문구를 넣지 않는다. 근거가 되는 건 S4의 "Frontend design defaults" 절과 비전 향상뿐 |

## 3. 충돌 판정

**C1. 서체 — 공식 "Inter 금지" vs dev:ui `Inter Tight` 대안.**
공식(S1)은 Inter·Roboto·Open Sans·Lato·시스템 폰트를 명시 금지. dev:ui도 "Inter 하나로 덮으면 템플릿 티"라 취지는 같고, `Inter Tight`만 남아 있다. **공식이 맞다** — 변형이어도 같은 인상을 준다. `IBM Plex Sans + IBM Plex Mono`(공식 Technical 군)로 바꾼다. 단 DESIGN.md가 정한 서체는 예외(이미 SKILL.md 우선순위대로).

**C2. 배경·그라디언트 — 공식 구버전 "배경에 깊이" vs dev:ui "강조 한 곳만".**
S1(cookbook)은 그라디언트·패턴 배경을 권하지만 더 최신인 S3는 "gradient washes as decoration"을 AI 티로 분류하고 "Spend your boldness in one place"로 돌아섰다. 또 S5는 하우스 스타일이 "dashboards, dev tools, fintech, healthcare, or enterprise apps"에 맞지 않는다고 못 박는다. **dev:ui의 절제가 맞고, 프로파일로 나눈다**: 관제·제품 = 현행(평면 캔버스, 강조 한 곳) / 랜딩(VARIANCE ≥ 6) = 히어로 배경 한 레이어 허용. "섹션마다 그라디언트"는 모든 프로파일에서 금지.

**C3. 모션 — 공식 "한 번의 페이지 로드 오케스트레이션" vs dev:ui 관제 MOTION 2.**
충돌이 아니라 **프로파일 차이**. S3는 "non-user-triggered motion sparingly"와 "motion that answers a person's action … is welcome"을 구분한다. 관제(MOTION 2)는 후자만, 랜딩(MOTION 6)은 전자를 **한 번** 허용. 수치·easing은 motion.md.

**C4. 모노 — 공식 "small data labels에 모노 = 템플릿 크롬" vs dev:ui "숫자는 전부 font-mono".**
둘 다 맞다. 공식이 지적하는 건 **장식으로 쓰는 작은 라벨**(아이브로·메타)이고, dev:ui는 **값의 자릿수 정렬**이다. 문구를 정밀하게: "숫자·측정값·ID·시각 = 모노(정렬). 라벨·캡션·메타 텍스트 = 본문 서체. 모노를 '기술적 느낌' 장식으로 쓰지 않는다."

**C5. 근검정 — 공식 "#0B0B0B·#111 tinted near-black = 템플릿 크롬" vs dev:ui "순수 #000 대신 Zinc-950".**
대상이 다르다. 공식은 라이트 화면에서 **잉크(글자)색**으로 반사적으로 #111을 쓰는 버릇을 지적하고, dev:ui는 **다크 캔버스**의 눈 피로를 말한다. 유지하되 보강: "다크 캔버스는 Zinc-950 계열(유지). 라이트 화면 잉크는 DESIGN.md의 ink 토큰 — #111·#0B0B0B를 기본값처럼 쓰지 않는다."

**C6. 세리프 — 공식 Editorial 군(Playfair·Fraunces) 권장 vs dev:ui "데이터 화면 세리프 금지".**
공식 자신이 세리프·크림이 대시보드·엔터프라이즈에 안 맞는다고 했다(S5). dev:ui 현행대로: 랜딩·에디토리얼만 세리프, 데이터 표·지표는 산세리프+모노. 변경 없음.

## 4. 그대로 옮겨 써도 되는 것 (라이선스)

- S3 `frontend-design/SKILL.md`는 Apache-2.0 — 문장 인용·번역·개작 가능, 저작권·라이선스 고지를 남긴다. 이 파일의 O4·O17·O20~O28이 거기서 왔다.
- S1·S4~S7 문서 텍스트는 별도 라이선스 표기 없음 → 짧은 인용 + URL만(위 형식).
