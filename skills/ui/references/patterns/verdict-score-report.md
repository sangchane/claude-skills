# 판정·점수·리포트 (Verdict, Score & Audit Report)

> 언제 읽나: 어떤 대상(매물·사이트·계정·몸 상태·코드)을 기준에 대고 **합격/불합격·점수·등급**으로 판정해 보여 주는 화면을 만들 때.
> 지표 묶음을 나열해야 하는 모든 화면(부동산 판정, SEO·보안·성능 감사, 신용점수, 건강 리포트)이 해당한다.
> 확인일 2026-10-08. 출처는 맨 아래. 수치 옆 [S1] 같은 표시는 출처 번호, 표시 없는 수치는 "권장(근거 약함)".

이 파일이 막아야 하는 실제 지적(2026-10-08): "숫자만 늘어놓아 어떤 기준을 충족하는지, 뭐가 부족하고 뭐가 강점인지 한눈에 안 보인다",
"텍스트를 한 페이지에 나열해 너무 많다", "설명 문장은 클릭했을 때만".

## 0. 리포트 화면의 고정 순서 (위에서 아래로)

1. **결론 1줄** — 판정(합격/보류/불합격 또는 등급)+한 문장 이유. 리포트에서 가장 큰 글자·가장 높은 대비.
2. **총점 1개** — 게이지 또는 등급 글자 하나. 바로 옆에 기준 구간 라벨("90–100 양호").
3. **강점/약점 요약** — 각 최대 3개. 기준을 넘긴 항목(강점)과 못 미친 항목(약점)을 분리해 나열.
4. **항목별 기준 대비 시각화** — 항목마다 값 + 기준선 + 여유/부족 차이. 불릿 차트가 기본.
5. **상세·근거** — 계산식, 데이터 출처, 설명 문장. **기본 접힘**.

순서 근거: 결론 먼저(역피라미드)는 웹에서 사용자가 끝까지 읽지 않고 훑기 때문이다 [S9][S10]. Lighthouse·PageSpeed Insights도
"통과/실패 → 점수 → 개선 기회 → 통과한 감사(접힘)" 순서다 [S3][S4]. GOV.UK 태스크 리스트는 완료 항목을 무채색으로 두고
"할 일이 남은 항목에 더 주목"하게 한다 [S14].

---

## 1. 결론 먼저 (Verdict line)

**언제 쓰나** — 지표가 2개 이상 묶여 있고 사용자가 "그래서 되는 거야?"를 묻는 모든 화면.

**규칙(측정 가능)**
- 지표 묶음 맨 위에 **결론 1줄**: `[판정 라벨] + [가장 큰 이유 한 문장]`. 한 줄은 폰 너비에서 2행 이내 (권장, 근거 약함).
- 판정 라벨은 **3~5단계**로 고정하고 화면마다 같은 단어를 쓴다 — Lighthouse는 3단계(0–49 Poor / 50–89 Needs improvement / 90–100 Good) [S3],
  Oura는 4단계(85–100 Optimal / 70–84 Good / 60–69 Fair / 0–59 Pay attention) [S11], FICO는 5단계 [S12]. 구간 수가 5를 넘으면 지각 효율이 떨어진다 [S1].
- 결론에는 **색+텍스트+아이콘 중 2개 이상**을 같이 쓴다. 색만으로 판정을 전달하지 않는다 [S7].
- 결론 아래 바로 "**무엇이 모자라서**"를 1줄로: 약점 중 가장 큰 1개와 그 차이(예: "노후도 57% — 기준 60%에 3%p 부족").
- 페이지에서 결론보다 큰 글자·높은 대비의 요소는 없어야 한다 — 가장 중요한 데이터가 가장 큰 면적·가장 높은 대비를 차지한다 [S2]. 강조 크기 단계는 3개 이하 [S8].
- 판정이 **계산 중/데이터 부족**이면 결론 자리에 그 상태를 쓴다(빈 결론 금지). 상태 표현은 `states.md`.

**Do**
- "조건부 가능 — 노후도만 3%p 모자람" 처럼 판정+이유를 한 문장에.
- 판정 라벨 옆에 기준 구간 라벨("기준 60% 이상") 을 붙여 왜 그 판정인지 바로 보이게.
- PageSpeed Insights처럼 "Core Web Vitals 평가: 통과/실패"를 맨 위 한 줄에 두고 그 아래 지표를 펼친다 [S4].

**Don't**
- 지표 표를 먼저 보여 주고 결론을 맨 아래·사이드에 두기.
- 결론 없이 숫자 타일만 나열하기 — "뭐가 부족하고 뭐가 강점인지 안 보인다"는 지적의 직접 원인.
- 판정 단어를 화면마다 바꾸기("양호/좋음/OK" 혼용).

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| PageSpeed Insights | https://pagespeed.web.dev/ (아무 URL 분석) | 맨 위 "Core Web Vitals 평가: 통과/실패" 한 줄 → 그 아래 지표 분포 → 점수 → 감사 |
| Google Search Console CWV 보고서(문서) | https://support.google.com/webmasters/answer/9205520 | URL 상태를 Good/Needs improvement/Poor 3단계로, 가장 나쁜 지표가 전체 상태를 결정 |
| Oura Readiness(문서) | https://support.ouraring.com/hc/en-us/articles/360025589793-Readiness-Score | 0–100 점수 + 4단계 라벨 + 기여 요인 목록(약점 식별) |
| GitHub Community profile(문서) | https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories | 기준 항목별 체크(충족)/주황 원 "Not added yet"(미충족) + 바로 "Add" 행동 |

---

## 2. 총점 표시 — 게이지·등급·숫자

**언제 쓰나** — 항목 점수를 합산한 단일 점수가 있을 때. 합산 점수가 없으면 이 절은 건너뛰고 3절(체크리스트)로 간다.

**규칙(측정 가능)**
- 총점은 **화면에 1개**만. 두 개 이상의 "총점"이 보이면 어느 것이 결론인지 흐려진다 (권장, 근거 약함).
- 점수 옆에 **구간 라벨과 구간 경계**를 같이 쓴다: `72 / 100 · 보통(50–89)`. 점수만 있으면 좋은지 나쁜지 모른다 [S3][S12].
- 게이지(반원·원형)는 **작은 공간에 총점 1개**를 보일 때만. 항목별 비교에는 선형(불릿·막대)을 쓴다 — 선형은 길이·위치로 읽어 각도·면적보다 정확하다 [S1][S6].
- 등급 글자(A+~F)를 쓸 때는 등급↔점수 구간표를 툴팁이나 접힘 영역에 둔다 — Observatory는 13단계(100+ A+ … 0–24 F) [S13].
- 점수 산식은 기본 접힘. 가중치가 있으면 접힘 안에 표(지표·가중치)로 — Lighthouse 성능 점수는 5개 지표 가중 평균(TBT 30%, LCP 25%, CLS 25%, FCP 10%, SI 10%) [S3].
- 색은 구간당 1색, 같은 색조의 명도 단계(진함=나쁨, 연함=좋음)가 색각이상에 안전하다 [S1]. 상태색 토큰은 `tokens.md`.

**Do**
- Lighthouse처럼 카테고리별 점수 게이지를 **한 줄**에 작게(각 ~60–80px) 나열하고, 클릭하면 해당 섹션으로 이동.
- 점수 변동(전회 대비 ±)을 작은 보조 텍스트로.

**Don't**
- 게이지를 화면 폭의 절반 이상으로 키우기 — 면적만 먹고 정보는 숫자 하나.
- 총점 없이 항목 점수만 있는데 억지로 평균 내서 총점 만들기(기준 통과 여부가 더 중요하면 3절).
- 진행률 막대(progress bar)를 점수 시각화로 쓰기 — 로딩 상태와 혼동된다 [S16].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Lighthouse 점수 문서 | https://developer.chrome.com/docs/lighthouse/performance/performance-scoring | 0–49/50–89/90–100 3구간 색, 가중치 표, "99→100은 90→94만큼 어렵다" |
| MDN HTTP Observatory 채점 문서 | https://developer.mozilla.org/en-US/observatory/docs/tests_and_scoring | 100점 기준에서 감점·가점, 등급표 13단계 |
| Experian 신용점수 구간 | https://www.experian.com/blogs/ask-experian/credit-education/score-basics/what-is-a-good-credit-score/ | 300–850을 5구간 라벨로, "helping/hurting" 요인 색 분리 |

---

## 3. 기준 대비 시각화 — 불릿 차트·체크리스트·신호등

**언제 쓰나** — 항목마다 "기준(threshold)이 있고 값이 그 위/아래"일 때. 판정 리포트의 본체.

**규칙(측정 가능) — 불릿 차트 (Stephen Few 사양 [S1])**
- 구성 5가지: 텍스트 라벨 · 선형 눈금 · 측정값 막대 · 비교 기준 마커(1~2개) · 구간 배경(2~5개, 이상적 3개).
- 측정값 막대 두께는 **컨테이너의 약 1/3**, 100% 검정(가장 진함). 비교 마커는 막대에 **수직인 짧은 선**, 막대보다 덜 진하게(두 번째 마커는 75%).
- 구간 배경은 **같은 색조의 명도 단계**: 2구간 35%/10%, 3구간 40%/25%/10%, 4구간 50/35/20/10%, 5구간 50/35/20/10/3% 검정. 진한 쪽이 나쁨.
- 라벨은 가로 차트에서 왼쪽, 세로 차트에서 위. 눈금은 0부터(음수 가능). 눈금이 0에서 시작하지 않으면 막대 대신 점·X 기호.
- "낮을수록 좋은" 항목(비용·결함)은 구간 색 순서를 뒤집어 다른 항목과 구별되게 한다.
- 가로 방향 여러 개를 세로로 쌓는 것이 기본(라벨 폭 정렬). 높이 행당 24–32px (권장, 근거 약함).

**규칙(측정 가능) — 값+기준선+차이 텍스트**
- 항목 행에 반드시 세 값: **현재값 · 기준값 · 차이(여유/부족, 부호 포함)**. 예: `57% · 기준 60% · −3%p`. 차이 없이 값만 두지 않는다 (권장, 근거 약함; "뭐가 부족한지 안 보인다" 지적의 직접 처방).
- 충족/미충족은 아이콘(체크/느낌표)+텍스트 라벨로도 표시(색만 금지) [S7][S15].
- 항목 순서: **미충족 → 충족** 또는 **가중치 큰 순**. 알파벳·입력 순서로 두지 않는다 (권장, 근거 약함). GOV.UK는 완료 항목의 색을 빼서 미완료에 주목시킨다 [S14].
- 항목 수가 **7개를 넘으면 그룹 헤더**로 묶고 그룹별 소결론("3/4 충족")을 헤더에 쓴다 (권장, 근거 약함; GOV.UK 태스크 리스트 그룹화 권고 [S14]).

**규칙(측정 가능) — 신호등(3색 상태)**
- 상태는 3단계(양호/주의/미달)까지. 4단계 이상이면 불릿 차트나 등급 글자로.
- 상태 점(dot) 지름 8–10px + 텍스트 라벨, 색만 단독 금지 [S7]. 상태 단어는 형용사(동사 금지, 클릭 유도 오해) [S15].
- 같은 상태엔 화면 전체에서 같은 색 [S15].

**Do**
- 한 항목 = 한 행: `라벨 | 불릿 차트(값·기준선·구간) | 값 · 기준 · 차이 | 상태 태그`.
- Search Console처럼 "가장 나쁜 지표가 전체 상태를 결정"하는 규칙이면 그 규칙을 결론 옆 1줄에 명시 [S5].
- 기준이 법령·규정이면 기준값 옆에 출처 링크(툴팁/접힘).

**Don't**
- 값만 있는 숫자 타일을 격자로 나열(기준선 없음) — 이 파일의 1번 지적.
- 항목마다 다른 시각화(어떤 건 게이지, 어떤 건 막대, 어떤 건 숫자).
- 구간을 무지개색으로(빨·주·노·초·파) — 명도 단계 또는 상태색 토큰 3색만.
- 기준 미달인데 초록 계열로 "거의 다 됨"을 표현하기.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Stephen Few 불릿 차트 사양 | https://www.perceptualedge.com/articles/misc/Bullet_Graph_Design_Spec.pdf | 5요소 구조, 구간 명도 표, 양수/음수·역방향 변형, 예측치 분할 막대 |
| PageSpeed Insights 필드 데이터 | https://pagespeed.web.dev/ | 지표마다 Good/NI/Poor 분포를 한 줄 적층 막대로, 75퍼센타일 값에 마커 |
| GOV.UK Task list | https://design-system.service.gov.uk/components/task-list/ | 항목별 상태 태그, 완료는 무채색, 그룹 헤더로 묶기 |
| GOV.UK Summary list | https://design-system.service.gov.uk/components/summary-list/ | 키-값 행, 누락 값은 "Enter X" 링크로 다음 행동 제시 |

---

## 4. 강점/약점 요약 블록

**언제 쓰나** — 항목이 4개 이상이라 전부 훑기 전에 "어디가 세고 어디가 약한지"를 먼저 알아야 할 때.

**규칙(측정 가능)**
- 두 열(또는 폰에서 두 묶음): **강점(기준 초과)** · **약점(기준 미달)**. 각 **최대 3개**, 나머지는 "+N개 더" 로 접힘 (권장, 근거 약함; 강조 요소 수 제한 원칙 [S8]).
- 각 항목은 `라벨 + 차이`: "대지지분 +4.2㎡ 여유", "노후도 −3%p 부족". 설명 문장은 쓰지 않는다 — 클릭(툴팁·접힘)에서만.
- 약점을 **먼저**(왼쪽/위). 행동이 필요한 쪽이 먼저 [S14].
- 아이콘: 강점 체크(또는 ↑), 약점 느낌표(또는 ↓). 색은 상태색 토큰 2색만.
- 약점 항목에는 가능하면 **다음 행동 1개**(예: "현장 확인 필요", "서류 추가") — GitHub 커뮤니티 프로필은 미충족 항목 옆에 바로 "Add" 버튼 [S17].

**Do**
- Experian처럼 "helping / hurting" 두 묶음으로 요인을 나누고 기여도를 수치로 [S12].
- Oura처럼 점수 아래 "기여 요인" 목록에서 저하 요인을 특정 [S11].

**Don't**
- 강점·약점을 한 문단 산문으로.
- 강점만 나열(약점 숨김) — 판정의 신뢰를 깎는다.
- 요약 블록이 항목별 시각화보다 커지기.

---

## 5. 설명 문장·근거는 접힘 (Why/How 영역)

**언제 쓰나** — 계산식, 법령 근거, 지표 정의, "왜 이 기준인가" 같은 설명 문장이 있을 때. 항상 있다.

**규칙(측정 가능)**
- 설명 문장은 **기본 접힘**. 펼치는 단계는 최대 2단계(항목 → 상세) [S9].
- 접힘 헤더에 **요약 값**을 노출: "계산 근거 (지표 5개 · 가중 평균)". 헤더만 보고도 내용을 짐작할 수 있어야 한다.
- 행 단위 짧은 정의(1문장)는 아이콘 툴팁, 2문장 이상·링크 포함이면 접힘/팝오버. 툴팁에 필수 정보 금지 (상세는 `progressive-disclosure.md`).
- 본문 폭에서 설명 문장이 3행을 넘으면 무조건 접는다 (권장, 근거 약함).
- Lighthouse처럼 "통과한 감사"는 묶어서 접고 건수만 노출("통과 23") [S3][S4].
- 데이터 출처·수집일은 리포트 맨 아래 1줄(작게). 오래된 데이터 표시는 `states.md`.

**Do**
- 항목 라벨 옆 (i) 아이콘 → 호버/탭 시 1문장 정의. 더 알고 싶으면 "자세히" 링크로 접힘 영역 펼침.
- 결론 바로 아래 "왜 이 판정인가 ▸" 접힘 하나에 근거를 모아 둔다.

**Don't**
- 지표마다 설명 문단을 펼쳐 둔 채 나열 — "설명 문장은 클릭했을 때만" 지적의 직접 원인.
- 접힘 헤더를 "자세히 보기"만으로(무엇이 들어 있는지 모름).
- 모달에 설명 넣기 — 비교하며 읽을 수 없다.

---

## 6. 리포트 밀도·배치 체크 (완료 전)

- [ ] 첫 화면(폰 844px 높이)에 결론 1줄 + 총점(또는 충족 n/m) + 약점 최대 3개가 들어오나?
- [ ] 모든 항목 행에 값·기준·차이가 있나? 색 외에 텍스트/아이콘으로도 상태가 읽히나?
- [ ] 설명 문장이 기본 펼침으로 노출된 곳이 있나? → 접어라.
- [ ] 시각화 종류가 항목별로 통일돼 있나(불릿 차트 하나로)?
- [ ] 강조(크기/색) 요소가 3개 이하인가? 결론보다 큰 글자가 있나?
- [ ] 총점이 1개뿐인가? 판정 라벨 단어가 화면 전체에서 같은가?

---

## 출처
| # | 출처 | URL | 확인일 | 라이선스/비고 |
|---|---|---|---|---|
| S1 | Stephen Few, Bullet Graph Design Specification (2013) | https://www.perceptualedge.com/articles/misc/Bullet_Graph_Design_Spec.pdf | 2026-10-08 | © Stephen Few, 요약·짧은 수치 인용만 |
| S2 | IBM Carbon — Data visualization: Dashboards | https://carbondesignsystem.com/data-visualization/dashboards/ | 2026-10-08 | Apache-2.0 (Carbon 문서) |
| S3 | Chrome Developers — Lighthouse performance scoring | https://developer.chrome.com/docs/lighthouse/performance/performance-scoring | 2026-10-08 | CC-BY-4.0 (developer.chrome.com 콘텐츠) |
| S4 | PageSpeed Insights — About | https://developers.google.com/speed/docs/insights/v5/about | 2026-10-08 | CC-BY-4.0 (developers.google.com 콘텐츠) |
| S5 | Google Search Console — Core Web Vitals report | https://support.google.com/webmasters/answer/9205520 | 2026-10-08 | 저작권 유지, 요약만 |
| S6 | NN/g — Dashboards: Making Charts and Graphs Easier to Understand (preattentive) | https://www.nngroup.com/articles/dashboards-preattentive/ | 2026-10-08 | 저작권 유지, 요약만 |
| S7 | W3C WCAG 2.2 Understanding 1.4.1 Use of Color | https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html | 2026-10-08 | W3C Document License |
| S8 | NN/g — Visual Hierarchy | https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ | 2026-10-08 | 저작권 유지, 요약만 |
| S9 | NN/g — Progressive Disclosure | https://www.nngroup.com/articles/progressive-disclosure/ | 2026-10-08 | 저작권 유지, 요약만 |
| S10 | NN/g — Inverted Pyramid / F-shaped pattern | https://www.nngroup.com/articles/inverted-pyramid/ · https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/ | 2026-10-08 | 저작권 유지, 요약만 |
| S11 | Oura Help — Readiness Score | https://support.ouraring.com/hc/en-us/articles/360025589793-Readiness-Score | 2026-10-08 | 저작권 유지, 구간 수치만 인용 |
| S12 | Experian — What Is a Good Credit Score? | https://www.experian.com/blogs/ask-experian/credit-education/score-basics/what-is-a-good-credit-score/ | 2026-10-08 | 저작권 유지, 구간 수치만 인용 |
| S13 | MDN HTTP Observatory — Tests and scoring | https://developer.mozilla.org/en-US/observatory/docs/tests_and_scoring | 2026-10-08 | CC-BY-SA-2.5 (MDN) |
| S14 | GOV.UK Design System — Task list | https://design-system.service.gov.uk/components/task-list/ | 2026-10-08 | MIT (GOV.UK Frontend) / OGL v3 (문서) |
| S15 | GOV.UK Design System — Tag | https://design-system.service.gov.uk/components/tag/ | 2026-10-08 | MIT / OGL v3 |
| S16 | Atlassian Design — Progress bar usage ("Don't use the progress bar for data visualization") | https://atlassian.design/components/progress-bar/usage | 2026-10-08 | 저작권 유지, 요약만 |
| S17 | GitHub Docs — About community profiles | https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories | 2026-10-08 | CC-BY-4.0 (GitHub Docs) |
| S18 | GOV.UK Design System — Summary list | https://design-system.service.gov.uk/components/summary-list/ | 2026-10-08 | MIT / OGL v3 |
| S19 | IBM Carbon — Progress bar usage (텍스트를 막대 안에 넣지 말 것, 5초 미만은 로딩) | https://carbondesignsystem.com/components/progress-bar/usage/ | 2026-10-08 | Apache-2.0 |
| S20 | Elastic EUI — EuiStat | https://eui.elastic.co/docs/components/display/stat/ | 2026-10-08 | Elastic License 2.0 / SSPL (문서), 요약만 |
| — | 미확인(읽기 실패): Material 3 Cards(JS 렌더), Ahrefs/Semrush Site Audit 도움말(404), Few "The Problem with Gauges"(404), Carbon simple-charts(게이지 규칙 없음) | | 2026-10-08 | 기억으로 쓰지 않음 |
