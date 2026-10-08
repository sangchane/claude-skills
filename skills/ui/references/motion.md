# 웹 UI 모션 규칙 — MOTION dial별 duration·easing·쓰는 곳 + reduced-motion + 모션 그래픽(Opus 5.5 방식)

확인일 2026-10-08. 수치는 전부 출처가 있다. SKILL.md 하드룰 "애니메이션은 `transform`/`opacity`만"은 그대로이고, 이 파일은 **얼마나 길게·어떤 곡선으로·어디에**를 정한다.

## 0. 원칙 (출처 순)

1. **목적 없는 모션은 넣지 않는다.** "Add motion purposefully, supporting the experience without overshadowing it. Don't add motion for the sake of adding motion." (Apple HIG Motion)
2. **자주 일어나는 상호작용에는 모션을 더하지 않는다.** "In apps, generally avoid adding motion to UI interactions that occur frequently." / "Aim for brevity and precision in feedback animations." (Apple HIG)
3. **기다리게 하지 않는다.** "Let people cancel motion. Don't make people wait for an animation to complete before they can do anything" (Apple HIG)
4. **비촉발 모션은 한 번, 동작 응답 모션은 환영.** "A single orchestrated moment — one page-load sequence or one reveal — lands better than scattered effects; fade-and-slide-up entrances on each section and hover transitions on every card are the generic default and read as AI-generated. Motion that answers a person's action (opening, expanding, confirming) is welcome when it shows what changed." (Anthropic frontend-design 스킬, Apache-2.0)
5. **끌 수 있어야 한다.** "Make motion optional." (Apple HIG) — 5절 reduced-motion.
6. **HTML은 CSS만, React는 Motion 라이브러리**(있을 때). "Prioritize CSS-only solutions for HTML. Use Motion library for React when available." (Anthropic cookbook) — `package.json` 확인 하드룰은 그대로.

## 1. 수치 참조표 (출처별)

### Duration

| 출처 | 토큰 | ms | 쓰는 곳(출처 문구) |
|---|---|---|---|
| IBM Carbon | `duration-fast-01` | 70 | 버튼·토글 마이크로 인터랙션 |
| | `duration-fast-02` | 110 | 페이드 |
| | `duration-moderate-01` | 150 | 작은 확장·짧은 이동 |
| | `duration-moderate-02` | 240 | 확장·토스트 |
| | `duration-slow-01` | 400 | 큰 확장·알림 |
| | `duration-slow-02` | 700 | 배경 디밍 |
| Material 3 | `short1~4` | 50 / 100 / 150 / 200 | 작은 유틸리티 전환 |
| | `medium1~4` | 250 / 300 / 350 / 400 | 중간 요소 |
| | `long1~4` | 450 / 500 / 550 / 600 | 큰 요소·화면 전환 |
| | `extra-long1~4` | 700 / 800 / 900 / 1000 | 전체 화면·특수 |
| Anthropic 예시 | 버튼 hover | 160 | "transition: all 160ms ease out … rather than using dramatic motion" |

Carbon: https://carbondesignsystem.com/elements/motion/overview/ · M3 값: androidx `MotionTokens.kt`(m3.material.io 스펙 페이지는 JS 렌더라 WebFetch로 못 읽음 → 코드 원천으로 확인) https://raw.githubusercontent.com/androidx/androidx/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3/tokens/MotionTokens.kt · M3 "쓰는 곳" 칼럼은 토큰 이름에서 유추(공식 설명 페이지 미확인) · Anthropic: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8

### Easing

| 출처 | 이름 | cubic-bezier | 쓰는 곳 |
|---|---|---|---|
| Carbon | standard · productive | `(0.2, 0, 0.38, 0.9)` | 화면에 계속 보이는 요소의 이동·변형 |
| | standard · expressive | `(0.4, 0.14, 0.3, 1)` | 같은 용도, 큰 순간 |
| | entrance · productive | `(0, 0, 0.38, 0.9)` | 나타남 |
| | entrance · expressive | `(0, 0, 0.3, 1)` | |
| | exit · productive | `(0.2, 0, 1, 0.9)` | 사라짐(모달·토스트) |
| | exit · expressive | `(0.4, 0.14, 1, 1)` | |
| Material 3 | standard | `(0.2, 0, 0, 1)` | 기본 |
| | standard-decelerate | `(0, 0, 0, 1)` | 들어옴 |
| | standard-accelerate | `(0.3, 0, 1, 1)` | 나감 |
| | emphasized-decelerate | `(0.05, 0.7, 0.1, 1)` | 강조 들어옴 |
| | emphasized-accelerate | `(0.3, 0, 0.8, 0.15)` | 강조 나감 |
| | legacy (M2 standard) | `(0.4, 0, 0.2, 1)` | 구 Material |

Carbon의 두 스타일 정의: **productive** = "efficiency and responsiveness", 버튼 상태·데이터 렌더 같은 과업 순간 / **expressive** = "enthusiastic, vibrant, and highly visible movement", 페이지 열기·주요 동작.

공통 원리(두 시스템 모두 토큰이 그렇게 갈린다): **들어올 때 decelerate(끝에서 느려짐), 나갈 때 accelerate(시작부터 빨라짐), 머무르며 움직일 때 standard.** `ease`·`linear` 기본값은 쓰지 않는다 — Material도 `linear`를 별도 토큰으로만 둔다.

## 2. MOTION dial → 규칙

프로파일 기본값: 관제 **2** · 제품 **4** · 랜딩 **6** (SKILL.md 2절).

| MOTION | 허용 | duration · easing | 금지 |
|---|---|---|---|
| **1~2 관제/대시보드** | 상태 변화만: 칩·배지 색 바뀜, 토글, 드롭다운 열림, 토스트. 로딩 스켈레톤 펄스 | 70~150ms · Carbon productive(standard/entrance/exit). 토스트 240ms | 페이지 로드 시퀀스, 섹션 등장, 카드 hover 들썩임, 차트 그려지는 애니(실시간 데이터는 **갱신값을 즉시** 보여 준다 — 숫자가 굴러가면 판독이 늦어진다), 패럴랙스, 자동 캐러셀 |
| **3~5 제품/앱** | 사용자 동작에 응답하는 것 전부: 열기·확장·확인·정렬 변경·드래그. 리스트 항목 추가/삭제 1회 | 150~240ms · Carbon productive 또는 M3 standard(-decelerate/-accelerate). 큰 패널·모달 240~400ms | 페이지 로드 오케스트레이션(있어도 1개, 200ms 이내), 섹션별 fade+slide-up, 장식 루프 |
| **6~8 마케팅/랜딩** | **페이지 로드 1회** 오케스트레이션: 히어로 요소 3~6개가 `animation-delay`로 순차 등장. 스크롤 트리거 reveal은 섹션당 1회·`IntersectionObserver`·한 번만. 변화를 보여 주는 hover만 | 400~700ms · Carbon expressive 또는 M3 emphasized. 순차 지연 60~120ms 간격(Carbon fast-01/02 값을 간격으로 사용) | 모든 섹션 fade+slide-up, 모든 카드 hover, 두 번째 오케스트레이션, 무한 루프 장식(있으면 2.2.2에 따라 일시정지 제공) |
| **9~10 시네마틱** | 스크롤 연동 장면 전환·캔버스·3D | 700~1000ms(M3 extra-long) 이상 | 여전히 `transform`/`opacity`(또는 캔버스)만. **이 영역은 UI가 아니라 연출이다 — 6절 "범위 밖" 판단을 먼저** |

공통:
- `transition: all` 금지 — 바뀌는 속성만 나열(예: `transition: opacity 110ms cubic-bezier(0,0,0.38,0.9), transform 150ms …`). 공식 예시의 `all`은 프롬프트 스케치일 뿐이다.
- 같은 화면 안에서 duration·easing 쌍은 **3개 이하**(fast/moderate/slow). CSS 변수 `--dur-fast/--dur-base/--dur-slow`, `--ease-in/--ease-out/--ease-std`로 둔다(DESIGN.md에 motion 토큰이 없으면 여기 값을 넣는다 — awesome-design-md·Claude Design 디자인 시스템 둘 다 모션 항목이 없다).
- 나가는 모션은 들어오는 모션보다 짧게(Carbon이 exit 곡선을 따로 두는 이유 — 사용자는 이미 다음을 보고 있다).

## 3. 구현 규칙 (성능)

출처: Motion 문서 https://motion.dev/docs/performance

- "`transform` and `opacity` are 'the safest values to animate across all devices'" — 컴포지터에서 처리. SKILL.md 하드룰과 같다.
- 레이아웃 유발 속성(`height`·`padding`·`position`·`border-width`)은 "force full re-renders … potentially taking over 100ms". 펼침은 `grid-template-rows: 0fr → 1fr` 또는 `scaleY`+내용 opacity로.
- 페인트 무거운 속성 대체: `box-shadow` 애니 → `filter: drop-shadow()`, `border-radius` 애니 → `clip-path: inset(… round …)`.
- `will-change: transform`은 애니 직전에만, 상시 지정 금지(레이어 폭발).
- Motion(React)에서 `{x: 100, scale: 2}` 같은 개별 transform은 "not hardware accelerated" — 가속이 중요한 곳은 `transform` 문자열로 직접.
- 스크롤 감지는 `IntersectionObserver`(SKILL.md). `useEffect`는 cleanup.

## 4. 사용자 동작 응답 모션 — 무엇을 보여 주나

"shows what changed"가 기준. 각 모션은 **상태 변화 하나**를 설명해야 한다.
- 열림/닫힘: 출발 지점에서 자라남(`transform-origin`을 트리거 쪽에). 모달은 opacity + `scale(0.98→1)`, 배경 디밍 Carbon slow-02(700ms)는 과하니 240ms.
- 확장/접힘: 내용 opacity 110ms + 높이는 grid 트릭. 화살표 아이콘 `rotate` 150ms.
- 확인/저장: 버튼 라벨 교체("저장 → 저장됨")가 모션보다 먼저. 체크 아이콘 등장 150ms.
- 정렬/필터 변경: 행이 **바로** 바뀐다. 재정렬 애니(FLIP)는 항목 ≤ 20개일 때만, 240ms.
- 삭제: 항목 opacity 110ms exit → 빈 자리 150ms 닫힘. 되돌리기 토스트.
- 실시간 데이터(관제): 값은 즉시 갱신. 바뀐 셀에 배경 110ms 페이드 1회(지속 하이라이트 금지). stale이면 모션이 아니라 **색·라벨**로.

## 5. reduced-motion

근거
- WCAG 2.2 **2.3.3 Animation from Interactions (AAA)**: "Motion animation triggered by interaction can be disabled, unless the animation is essential to the functionality or the information being conveyed." 기법 C39(CSS `prefers-reduced-motion`)·SCR40(JS). https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html
- WCAG 2.2 **2.2.2 Pause, Stop, Hide (A)**: 자동 시작·5초 초과·다른 콘텐츠와 병행하는 움직임에는 "a mechanism for the user to pause, stop, or hide it"; 자동 갱신 정보도 "pause, stop, or hide it or to control the frequency of the update". https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html → **관제 실시간 피드·랜딩 무한 루프는 A 등급 의무.** 일시정지/갱신 주기 컨트롤을 둔다.
- Anthropic frontend-design 스킬 품질 바닥: "reduced motion respected".
- Apple HIG: "when the Reduce Motion accessibility setting is on, be sure to minimize or eliminate animations." (developer.apple.com HIG Motion)

규칙
- 끄는 것: 이동(`translate`·`scale`·`rotate`), 패럴랙스, 자동재생 영상, 순차 등장, 스켈레톤 펄스 → 정적.
- 남기는 것: `opacity`·색 전환(짧게). Motion 문서의 `reducedMotion` 동작과 같다 — "automatically disable transform and layout animations, while preserving the animation of other values like `opacity` and `backgroundColor`" https://motion.dev/docs/react-accessibility
- 정보 전달이 모션뿐이면 안 된다(Apple "avoid using it as the only way to communicate important information") — 상태는 색·텍스트로도.

CSS(MDN 패턴 — 같은 특이성, 뒤에 와서 이김 https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion):
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .parallax, .autoplay { transform: none; }
}
```
`0.01ms`는 `animationend`/`transitionend`에 의존하는 JS가 깨지지 않게 하는 관용구다(0으로 두면 이벤트가 안 온다). Tailwind는 `motion-safe:`/`motion-reduce:` 변형.

React(Motion):
```tsx
<MotionConfig reducedMotion="user">{children}</MotionConfig>   // 앱 루트 1회
const reduce = useReducedMotion();                               // 개별: 패럴랙스·자동재생 분기
```

Pre-Flight 추가분(SKILL.md 5절에 넣을 두 줄): "[ ] `prefers-reduced-motion`에서 이동·패럴랙스·자동재생이 꺼지고 opacity만 남나?" / "[ ] 5초 넘게 자동으로 움직이거나 자동 갱신되는 것에 일시정지 컨트롤이 있나(WCAG 2.2.2 A)?"

## 6. 모션 그래픽·런칭 영상 — Opus 5.5 방식과 dev:ui의 경계

### 사실 확인
- Anthropic의 Opus 5.5 출시 글(2026-09-22, https://www.anthropic.com/news/claude-opus-5-5)과 What's new 문서에는 **영상·애니메이션·모션 그래픽 언급이 없다.** "모션"은 사용자들이 X에 올린 쇼릴에서 나온 말이다(검색 요약; pasqualepillitteri.it 원문은 3회 접속 실패 — 미확인).
- 모델이 하는 일은 **그림을 그리는 코드를 쓰는 것**이다. 영상 파일을 직접 내지 않는다.

### 동작 방식 (laozhang.ai 가이드, https://blog.laozhang.ai/en/posts/claude-opus-5-5-video-generation)
1. 모델이 장면 코드를 쓴다 — HTML 한 파일, `<canvas>` 하나, 시간 함수.
2. 헤드리스 브라우저(Playwright)가 프레임마다 `seek(t)`를 호출해 스크린샷.
3. ffmpeg가 이어 붙여 H.264 MP4.

장면 계약(결정론이 핵심):
```js
window.DURATION = 12;            // 초
window.seek = async (t) => { /* 시각 t의 완전한 프레임을 그린다 */ };
```
"Every pixel must depend only on t. Do not use requestAnimationFrame, setTimeout, setInterval, Date, performance.now or CSS transitions to drive motion." — 시계를 읽으면 "rendering the same scene twice produces different videos".

렌더 루프·인코딩(같은 출처):
```js
for (let i = 0; i < total; i++) {
  await page.evaluate((t) => window.seek(t), i / fps);
  const buf = await page.screenshot(shotOpts);
  if (!ff.stdin.write(buf)) await once(ff.stdin, "drain");
}
```
```bash
ffmpeg -y -loglevel error -f image2pipe -framerate 30 -i - -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart out.mp4
```
속도(M4, 1920×1080, 360프레임): PNG 72ms/프레임, JPEG q92 32ms/프레임.

검색 요약(원문 미확인)에 따르면 Opus 5.5는 프로젝트에 Remotion이 있어도 **그냥 두면 가장 단순한 길(HTML + seek + Playwright)을 고른다** — 특정 프레임워크를 원하면 프롬프트에 명시.

### 도구 (확인일 2026-10-08)

| 도구 | 무엇 | 설치 | 비용·라이선스 | 출처 |
|---|---|---|---|---|
| 직접 스크립트 | HTML canvas + Playwright + ffmpeg | Node, `npm i playwright`, ffmpeg | 무료(토큰 비용만) | laozhang.ai |
| **HyperFrames** (HeyGen) | "Write HTML. Render video. Built for agents." — `data-*` 타이밍 + GSAP/CSS/Lottie/Three.js/Anime.js/WAAPI, "seeks each frame in headless Chrome and encodes the result with FFmpeg, so the same input produces the same video" | `claude plugin marketplace add heygen-com/hyperframes` → `claude plugin install hyperframes@hyperframes` 또는 `npx skills add heygen-com/hyperframes`, `npx hyperframes init my-video`. Node 22+, FFmpeg | **Apache-2.0**. GSAP는 "free for everyone since 2025, including commercial use"지만 Webflow 전용 라이선스(OSI 오픈소스 아님) | https://github.com/heygen-com/hyperframes · capitalandcompute.net |
| **Remotion** | React로 영상 | `npx skills add remotion-dev/skills`, `/remotion-create …` | 무료: "an individual", "a for-profit organization with up to 3 employees", 비영리. 그 외 Company License(remotion.pro). 제3자 글은 4인 이상 $25/월/인이고 "agentic coding tools"로 쓰는 사람도 좌석에 포함된다고 하나 LICENSE.md 원문에서 그 조항은 못 찾음 — 미확인 | https://www.remotion.dev/docs/ai/skills · raw LICENSE.md |
| Manim Community | Python 수식·그래프 설명 영상 | pip | MIT | capitalandcompute.net |
| Motion Canvas | TypeScript 제너레이터 | npm | MIT, 유지보수 느림(2026-07 마지막) | capitalandcompute.net |
| **Motion MCP** (Mosaic, motion.so) | 프롬프트 → 완성 영상(리서치·디자인·애니·보이스오버·편집을 서비스가 함). 도구 `create_video`·`create_followup`·`upload_asset`·`purchase_credits` 등 | 엔드포인트 `https://mcp.motion.so/mcp`, OAuth 또는 API 키(Settings → API). `claude mcp add` 예시는 문서에 없음 | **유료 크레딧**: "$6 per 200 credits (3¢ per credit)", Pro 월 1,000~50,000 크레딧. 200 크레딧 ≈ 영상 1~2개(검색 요약). **무료 등급·무료 크레딧 기재 없음 → 미확인** | https://docs.motion.so/guides/mcp · https://docs.motion.so/guides/credits |

### 공개된 프롬프트 구조
- 바이럴 원라이너(ayautomate.com 수집): "make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out."
- 엄격 계약형(laozhang.ai): "Write the video as a single file, scene.html, 1920x1080, one canvas. Rules: Set window.DURATION to the length in seconds. Expose async window.seek(t). It must draw the complete frame for time t (seconds) and nothing else may draw." + "springs as closed-form step responses"(스프링도 t의 닫힌식), 오디오 -14 LUFS(ayautomate.com 예).
- 실제로 잘 된 워크플로(ayautomate.com·charliehills.substack.com): ① 레퍼런스·무드보드·"정확한 상태(exact states)" 먼저 → ② **스토리보드/정지 프레임**을 먼저 받아 승인 → ③ 감독 노트로 수정 몇 라운드("It wasn't one prompt.") → ④ 렌더 → ⑤ "Check it before you post".
- HyperFrames 예: "Using `/hyperframes`, create a 10-second product intro with a fade-in title, a background video, and subtle background music."

### 한계 (출처 문구)
- 실사 불가: "this method cannot give you a realistic person talking to a camera" (laozhang.ai). "Living things and animals look off", "Lighting tends to be overexposed" (daily.dev).
- 품질: "Motion graphics aren't actually great. Being able to create them at all is the impressive part" (daily.dev 인용). 브랜드 정확도 약함 — "used the wrong logo, replaced Every's green with dark purple" (muz.li가 인용한 Every 테스트).
- 사운드는 별도: 테스트 클립은 무음, 음악은 Suno 등 외부 생성 후 ffmpeg로 합침(laozhang.ai·daily.dev). 효과음은 코드로 합성한 예 있음(ayautomate.com).
- 비용·시간: "Every revision repeats the cost", "Thinking counts as output"(laozhang.ai). 30초 영상에 31.8M 토큰·54분(ayautomate.com 사례), "Long builds eat a lot of Claude usage"(daily.dev). 긴 렌더는 크래시 → 구간별 렌더(daily.dev).
- 결정론을 깨는 코드(`performance.now`, CSS transition)는 프레임 누락·흔들림.

### 언제 dev:ui 범위 밖인가
dev:ui는 **UI의 모션**(상태 변화를 설명하는 150~700ms)을 다룬다. 아래는 범위 밖 — 별도 작업으로 넘긴다.
- 산출물이 **MP4·GIF·쇼릴·런칭 영상·광고**다 → HyperFrames 플러그인(무료, Apache-2.0) 또는 직접 Playwright+ffmpeg 스크립트. 사용자에게 길이·해상도·사운드 유무·레퍼런스를 먼저 받는다. 토큰 비용을 미리 말한다.
- 화면 안이라도 **t의 함수로 그려야 하는 장면**(캔버스 인트로, 스크롤 연동 3D, MOTION 9~10)이다 → UI 하드룰(transform/opacity)이 아니라 위 장면 계약이 적용된다. 그래도 `prefers-reduced-motion`에서는 정지 프레임으로 대체한다.
- 제품 UI에 "런칭 영상처럼" 모션을 넣어 달라는 요구 → 2절 dial 규칙으로 되돌린다. 페이지 로드 오케스트레이션 1회가 상한이다.

## 출처 (확인일 2026-10-08)

1. Apple HIG Motion — https://developer.apple.com/design/human-interface-guidelines/motion (JSON 엔드포인트로 본문 확인)
2. IBM Carbon Motion — https://carbondesignsystem.com/elements/motion/overview/
3. Material 3 MotionTokens.kt(androidx) — 위 raw URL. m3.material.io 토큰 페이지는 미확인
4. WCAG 2.2 Understanding 2.3.3 — https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html
5. WCAG 2.2 Understanding 2.2.2 — https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
6. MDN prefers-reduced-motion — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
7. Motion performance — https://motion.dev/docs/performance
8. Motion accessibility — https://motion.dev/docs/react-accessibility
9. Anthropic cookbook frontend aesthetics — https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics
10. anthropics/skills frontend-design SKILL.md(Apache-2.0) — https://github.com/anthropics/skills/tree/main/skills/frontend-design
11. Prompting Claude Opus 4.8(160ms 예시) — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8
12. Opus 5.5 출시 글 — https://www.anthropic.com/news/claude-opus-5-5
13. What's new in Opus 5.5 — https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5
14. laozhang.ai 영상 생성 가이드 — https://blog.laozhang.ai/en/posts/claude-opus-5-5-video-generation
15. ayautomate.com 프롬프트 모음 — https://www.ayautomate.com/resources/claude-opus-5-5-motion-graphics
16. charliehills.substack.com — https://charliehills.substack.com/p/opus-55-motion-graphics
17. daily.dev — https://daily.dev/posts/claude-opus-5-5-generates-motion-design-and-visual-scenes-entirely-in-code-yqmdx7qnw
18. muz.li — https://muz.li/blog/claude-opus-5-5-for-designers/
19. capitalandcompute.net 도구 비교 — https://capitalandcompute.net/blog/claude-motion-graphics-tools/
20. HyperFrames — https://github.com/heygen-com/hyperframes
21. Remotion skills — https://www.remotion.dev/docs/ai/skills · LICENSE.md raw
22. Motion MCP 문서 — https://docs.motion.so/guides/mcp · https://docs.motion.so/guides/credits · https://motion.so
23. pasqualepillitteri.it — https://pasqualepillitteri.it/en/news/19007/opus-5-5-motion-design-video-en **(접속 실패 3회, 미확인 — 검색 요약만 사용)**
