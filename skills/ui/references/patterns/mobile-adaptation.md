# 모바일 적응 (Mobile Adaptation)

> 언제 읽나: 데스크톱용으로 만든 표·차트·지도·분할 화면을 폰 너비(390px 기준)에서 쓰이게 바꿀 때, 터치 타깃·바텀시트·고정 바 크기를 정할 때.
> 확인일 2026-10-08. 출처는 맨 아래. 수치 옆 [S1] 같은 표시는 출처 번호, 표시 없는 수치는 "권장(근거 약함)".

공통 전제: 폰에서는 "둘 다 작게"가 아니라 "하나씩 크게". 두 패널을 나란히 줄여 둘 다 못 쓰게 만드는 대신 스택(드릴다운)으로 바꾼다 [S9][S10].
브레이크포인트는 기존 프로젝트 것을 따르되 없으면: 스택 ≤ 640px, 나란히 ≥ 641px [S10]. 참고 그리드: Carbon 320/672/1056/1312/1584px [S6], Atlassian 모바일 320~479px 2열·거터 12·여백 16 [S7].

## 1. 터치 타깃·간격

**언제 쓰나** — 버튼·칩·행·핀·탭 등 손가락으로 누르는 모든 것.

**규칙(측정 가능)**
- 최소 법적 기준: **24×24 CSS px** (WCAG 2.2 SC 2.5.8, AA) [S1]. 24px 미만이면 지름 24px 원이 이웃 타깃과 겹치지 않을 때만 허용 [S1].
- 예외: 인라인 링크, 브라우저 기본 컨트롤, 같은 기능의 다른 큰 컨트롤이 있을 때, 지도·데이터 시각화처럼 크기가 정보 자체일 때(essential) [S1].
- 플랫폼 권장: Android/Material **48×48dp**(약 9mm), 타깃 간격 **8dp 이상** [S2]. Apple **44×44pt** [S3]. 웹 앱은 두 값 중 큰 44~48px를 기본으로.
- 텍스트는 11pt 이상 [S3]. 고정 바 안 글자는 약 16pt, 탭 타깃은 1cm×1cm 이상 [S11].
- 스와이프 영역은 최소 45px 높이·너비 [S4].
- 시각 크기와 히트 영역을 분리해도 된다: 아이콘 20px + 패딩으로 44px (권장, 근거 약함).

**Do**
- 목록 행 높이 48px 이상(Carbon lg 48 / xl 64) [S5]. 행 전체를 탭 영역으로.
- 칩·필터 버튼 높이 36px 이상 + 가로 간격 8px.
- 지도 핀은 essential 예외지만, 가격 칩은 높이 28px 이상·탭 패딩으로 44px 확보.

**Don't**
- 24px 미만 아이콘 버튼을 붙여 놓지 않는다(원 겹침으로 2.5.8 위반) [S1].
- 호버에만 뜨는 메뉴·툴팁에 기능을 숨기지 않는다 — 터치 기기는 호버가 없다. Carbon 표는 터치면 오버플로 메뉴를 항상 보이게 한다 [S5].
- 데스크톱 폰트 그대로 12px 링크를 본문 밖에 두지 않는다(inline 예외는 본문 안에서만).

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| WCAG 2.2 Understanding 2.5.8 | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html | 24px·간격 예외·essential 예외 [S1] |
| Android 접근성 도움말 | https://support.google.com/accessibility/android/answer/7101858 | 48dp·8dp 간격·9mm [S2] |
| Apple UI Design Tips | https://developer.apple.com/design/tips/ | 44pt·11pt [S3] |

## 2. 표 — 열 우선순위·카드 변환·첫 열 고정

**언제 쓰나** — 열이 3개 이상인 데이터 표를 폰에서 보여줄 때.

**규칙(측정 가능)**
- 폰에서 읽히는 열은 **2개**(숫자 위주면 3~4개). 확대 없이 읽혀야 한다 [S8].
- 열이 3개 이상이면 **스택(카드)** 또는 **가로 스크롤** 중 하나를 고른다 [S12]. 문자 정보가 많으면 스택, 숫자 비교가 목적이면 가로 스크롤 [S12].
- 스택 변환: 각 셀 앞에 열 머리글을 `data-label`로 붙인다(USWDS `usa-table--stacked`) [S12]. 첫 셀이 이름이면 그것을 카드 제목으로(stacked-header) [S12].
- 가로 스크롤: **첫 열(식별자) 고정**, 머리글 행 고정(sticky) [S8]. 잘린 열 가장자리나 화살표로 "더 있음"을 보인다 — 점(dot)보다 효과적 [S8].
- 고정 머리글은 스크롤·스택 변형과 함께 쓸 수 없다(USWDS) [S12] — 둘 중 하나만.
- 숫자 열 오른쪽 정렬 + 모노 [S12][S13]. 태블릿 미만에서 글자 크기 1단계 축소 클래스 사용(GOV.UK `--small-text-until-tablet`) [S13].
- 열 순서 = 우선순위. 1열 식별자, 2열 결론(판정·총점), 3열부터 근거 수치. 숨길 땐 뒤에서부터 (권장, 근거 약함).
- 행 높이: 폰 터치면 48px(lg) 이상 [S5]. 데스크톱 밀집 표의 24/32px(xs/sm)는 폰에서 쓰지 않는다 [S5].

**Do**
- 보여줄 열을 사용자가 고르게(열 표시/숨김 또는 사전 필터) [S8]. 그룹이 많으면 아코디언으로 묶는다 [S8].
- 카드 변환 시 카드 1장 = 제목 + 결론 배지 + 수치 2~3개. 나머지 열은 "더 보기" 접기.
- 열 수를 줄이는 것이 먼저 — "긴 행을 아래로 읽는 것이 긴 열을 옆으로 읽는 것보다 쉽다" [S12].

**Don't**
- 표를 그대로 축소(`transform: scale`·8px 글자)해서 넣지 않는다.
- 숫자만 늘어놓은 카드를 만들지 않는다 — "어떤 기준을 충족하는지, 뭐가 부족하고 뭐가 강점인지 한눈에 안 보인다"가 실제 지적이다. 카드마다 기준선 대비 상태(충족/미달) 표시 1개를 넣는다.
- 가로 스크롤 표에 첫 열 고정 없이 10열을 두지 않는다 — 무엇의 값인지 잃는다 [S8].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| USWDS Table | https://designsystem.digital.gov/components/table/ | stacked / stacked-header / scrollable 변형, data-label [S12] |
| NN/g Mobile Tables | https://www.nngroup.com/articles/mobile-tables/ | 2열 한계, 첫 열 고정, 스크롤 단서 [S8] |
| GOV.UK Table | https://design-system.service.gov.uk/components/table/ | 숫자 우측 정렬, 소형 화면 글자 축소 [S13] |
| Carbon Data Table | https://carbondesignsystem.com/components/data-table/usage/ | 행 높이 5단계, 터치 시 메뉴 상시 노출 [S5] |

## 3. 차트 — 터치 툴팁·범례·높이

**언제 쓰나** — 데스크톱 대시보드 차트를 폰에 내릴 때.

**규칙(측정 가능)**
- 차트 폭 500px 미만이면 범례를 숨기거나 아래로 내리고 축 라벨 공간을 줄이는 반응형 규칙을 둔다 [S14]. 범례 대신 선 끝 직접 라벨을 우선한다 [S15].
- 폰 차트 높이 200~280px, 한 화면(844px)에 차트 2개 + 제목이 들어가는 높이 (권장, 근거 약함).
- 툴팁은 호버가 기본이므로 [S15] 터치에서는 탭/드래그로 열고, 바깥 탭으로 닫는다. 탭 타깃은 데이터 점이 아니라 x축 구간 전체(폭 ≥ 24px) (권장, 근거 약함) [S1].
- 시리즈 수 ≤ 3. 더 많으면 차트를 나누거나 선택 칩으로 바꾼다 — "너무 많은 요소로 채우지 말라" [S15].
- x축 라벨은 3~5개만, 나머지는 생략(최소/최대/중간) (권장, 근거 약함).
- 숫자 요약(최신값·변화량)을 차트 위 1줄로 먼저 보여주고 차트는 보조로 (권장, 근거 약함).

**Do**
- 범례는 차트 아래 가로 1줄, 칩 형태(탭하면 시리즈 토글).
- 가로 막대는 폰에서 세로 막대보다 라벨 공간이 남아 유리하다.

**Don't**
- 데스크톱 차트를 비율 유지로 축소해 글자 8px로 만들지 않는다.
- 차트 하나에 범례·축제목·주석·툴팁을 다 올리지 않는다 [S15].
- 핀치 줌에 의존하지 않는다(페이지 줌과 충돌).

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Highcharts Responsive | https://www.highcharts.com/docs/chart-concepts/responsive | maxWidth 500 규칙, 범례·축 조정 [S14] |
| Carbon Chart Anatomy | https://carbondesignsystem.com/data-visualization/chart-anatomy/ | 직접 라벨 우선, 과밀 금지, 호버 툴팁 [S15] |

## 4. 지도 — 전체화면 + 바텀시트·목록 토글

**언제 쓰나** — 목록+지도 분할 화면(패턴군 ④)을 폰으로 내릴 때.

**규칙(측정 가능)**
- ≤640px에서는 지도 전체화면 **또는** 목록 전체화면, 둘 중 하나만 [S10]. 전환은 하단 중앙 플로팅 버튼("목록 N건" ↔ "지도") 1개, 높이 44px.
- 바텀시트를 쓰면 스냅 3단: **peek**(핸들 + 결과 수 1줄, 64~88px) → **half**(화면의 45~50%) → **full**(상단 safe area까지). 기본은 peek (권장, 근거 약함). 바텀시트 정의·모달/비모달 구분은 [S16].
- peek·half 상태는 비모달(지도 조작 가능), full은 모달로 전환해도 된다 [S16].
- 시트에는 그랩 핸들 + **보이는 닫기(X) 버튼**을 둔다 — 핸들만으로 닫게 하지 않는다 [S16]. 뒤로가기 제스처로도 닫힌다 [S16].
- 시트를 겹쳐 쌓지 않는다(시트 위에 시트) [S16]. 상세는 시트 full 또는 새 화면.
- 지도 컨트롤은 우상단(줌은 핀치가 있으니 숨겨도 됨), 내 위치 우하단, 시트가 가리지 않게 시트 peek 높이만큼 위로 [S17].
- 지도 위 상단 띠는 최대 2단(검색 1 + 필터 칩 1줄, 합 ≤ 100px). 지도는 화면 높이의 75% 이상 보이게 (권장, 근거 약함) [S11].
- 선택한 핀의 요약 카드는 시트 peek 자리에 교체 표시(높이 ≤ 120px), 지도 중앙을 덮지 않는다.

**Do**
- 가격 칩은 상위 N개만, 폰에서는 데스크톱보다 적게(화면이 작으니) [S18].
- "이 지역 다시 검색" 칩은 상단 필터 줄 아래 중앙, 높이 32px.

**Don't**
- 폰에서 지도를 화면의 40%로 줄이고 아래 목록을 붙박이로 두지 않는다 — 지도도 목록도 못 쓴다 [S9].
- 아이콘·글씨가 큰 안내 오버레이를 지도 중앙에 두지 않는다 — 구석의 작은 칩으로. "아이콘·글씨가 너무 커서 지도가 안 보인다"가 실제 지적이다.
- "바닥에 있으면 다 닿는다"고 믿지 않는다 — 다양한 그립에서는 화면 중간이 더 닿기 쉽다 [S16].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| NN/g Bottom Sheets | https://www.nngroup.com/articles/bottom-sheet/ | 모달/비모달·확장형, 닫기 버튼 필수, 중첩 금지 [S16] |
| Google Maps JS Controls | https://developers.google.com/maps/documentation/javascript/controls | 전체화면 컨트롤 모바일 기본 켜짐, 위치 상수 [S17] |
| Airbnb Tech Blog | https://airbnb.tech/?p=683 | 모바일은 핀 수를 더 줄임 [S18] |
| Material 3 Bottom sheets | https://m3.material.io/components/bottom-sheets/guidelines | 미확인(JS 렌더, 본문 미수신) — 스냅 수치는 직접 관찰 필요 |

## 5. 폰 너비 390에서 가로 스크롤 없음·고정 바 상한·엄지 영역

**언제 쓰나** — 완료 선언 전 폰 레이아웃 점검, 하단 탭·상단 헤더·FAB 자리 결정.

**규칙(측정 가능)**
- 390px에서 `document.documentElement.scrollWidth ≤ 390`. 흔한 원인: 음수 마진, 고정 폭 표, `100vw` + 스크롤바, 긴 URL/숫자 문자열(`overflow-wrap: anywhere`로 해결) (권장, 근거 약함; 점검 항목은 SKILL.md Pre-Flight).
- 페이지 좌우 여백 16px [S6][S7]. 카드 안 패딩 12~16px.
- 고정 바 합계(상단 헤더 + 하단 탭/버튼) ≤ 화면 높이의 20% (844px에서 ≤ 170px). 상단 ≤ 56px, 하단 탭 ≤ 56px + safe-area. 콘텐츠:크롬 비율 13:1은 양호, 2:1은 실패 사례 [S11].
- 고정 바 안 탭 타깃 1cm×1cm 이상, 글자 약 16pt [S11]. 고정 바는 불투명 배경 [S11].
- 긴 목록 화면은 스크롤 내릴 때 헤더를 숨기고 올릴 때 보이기, 전환 300~400ms, 몇 px 이상 올려야 반응 [S11].
- 엄지 영역: 한 손 사용 49%, 상호작용 75%가 엄지 [S4]. 하단 중앙 = 자연 영역(주 액션·탭 바), 중간·반대편 = 스트레치, **상단 모서리 = 가장 어려움**(뒤로·닫기·드물게 쓰는 것) [S4].
- 하단 safe area(홈 인디케이터)만큼 `padding-bottom: env(safe-area-inset-bottom)` (권장, 근거 약함).

**Do**
- 주 액션 1개는 하단 중앙 또는 하단 전폭 버튼(높이 48px) [S4].
- 파괴적 액션(삭제)은 자연 영역에서 떼어 놓는다 — 상단 모서리나 확인 단계 뒤로 (권장, 근거 약함).
- 자주 쓰는 링크 ≤ 5개는 하단 고정 메뉴, 긴 메뉴는 전체화면 오버레이 [S4].

**Don't**
- 상단 헤더 + 탭 + 필터 + 안내 띠를 4단으로 고정하지 않는다 — 콘텐츠가 밀린다. "중요한 화면이 덜 중요한 띠 때문에 밑으로 밀린다"가 실제 지적이다.
- 반투명 고정 헤더를 쓰지 않는다 — 콘텐츠와 겹쳐 대비가 떨어진다 [S11].
- 데스크톱 사이드바를 폰에서 좌측 60px로 접어 콘텐츠 폭을 330px로 만들지 않는다. 햄버거 1개(44px)로.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Smashing — The Thumb Zone | https://www.smashingmagazine.com/2016/09/the-thumb-zone-designing-for-mobile-users/ | 자연/스트레치/어려움 영역, 하단 고정 메뉴 [S4] |
| NN/g — Sticky Headers | https://www.nngroup.com/articles/sticky-headers/ | 높이 최소화, 콘텐츠:크롬 비율, 숨김 애니 300~400ms [S11] |
| Atlassian Grid | https://atlassian.design/foundations/grid | 모바일 320~479: 2열·거터 12·여백 16 [S7] |
| Carbon 2x Grid | https://carbondesignsystem.com/elements/2x-grid/overview/ | 브레이크포인트 320/672/1056/1312/1584, 패딩 16 [S6] |

## 출처
| # | 출처 | URL | 확인일 | 라이선스/비고 |
|---|---|---|---|---|
| S1 | W3C — Understanding SC 2.5.8 Target Size (Minimum) | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html | 2026-10-08 | W3C Document License |
| S2 | Google — Android 접근성 도움말: Touch target size | https://support.google.com/accessibility/android/answer/7101858 | 2026-10-08 | 미확인(요약만) |
| S3 | Apple — UI Design Dos and Don'ts | https://developer.apple.com/design/tips/ | 2026-10-08 | 저작권 유지(요약만) |
| S4 | Smashing Magazine — The Thumb Zone (Hoober 인용) | https://www.smashingmagazine.com/2016/09/the-thumb-zone-designing-for-mobile-users/ | 2026-10-08 | 저작권 유지(요약만) |
| S5 | IBM Carbon — Data table usage | https://carbondesignsystem.com/components/data-table/usage/ | 2026-10-08 | Apache-2.0(코드)/문서 요약 |
| S6 | IBM Carbon — 2x Grid overview | https://carbondesignsystem.com/elements/2x-grid/overview/ | 2026-10-08 | Apache-2.0(코드)/문서 요약 |
| S7 | Atlassian Design — Grid | https://atlassian.design/foundations/grid | 2026-10-08 | 미확인 |
| S8 | NN/g — Mobile Tables | https://www.nngroup.com/articles/mobile-tables/ | 2026-10-08 | 저작권 유지(요약만) |
| S9 | saasui.design — List-detail UX | https://www.saasui.design/blog/saas-list-detail-master-detail-ux-patterns | 2026-10-08 | 미확인 |
| S10 | Microsoft Learn — List/details (320~640 epx 스택) | https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/list-details | 2026-10-08 | CC-BY-4.0 |
| S11 | NN/g — Sticky Headers | https://www.nngroup.com/articles/sticky-headers/ | 2026-10-08 | 저작권 유지(요약만) |
| S12 | USWDS — Table | https://designsystem.digital.gov/components/table/ | 2026-10-08 | 퍼블릭 도메인/CC0 |
| S13 | GOV.UK Design System — Table | https://design-system.service.gov.uk/components/table/ | 2026-10-08 | OGL v3.0 / MIT(GOV.UK Frontend) |
| S14 | Highcharts — Responsive charts | https://www.highcharts.com/docs/chart-concepts/responsive | 2026-10-08 | 미확인 |
| S15 | IBM Carbon — Chart anatomy | https://carbondesignsystem.com/data-visualization/chart-anatomy/ | 2026-10-08 | Apache-2.0/문서 요약(work in progress 표기) |
| S16 | NN/g — Bottom Sheets | https://www.nngroup.com/articles/bottom-sheet/ | 2026-10-08 | 저작권 유지(요약만) |
| S17 | Google Maps JS — Controls | https://developers.google.com/maps/documentation/javascript/controls | 2026-10-08 | CC-BY-4.0 |
| S18 | Airbnb Tech Blog — Improving Search Ranking for Maps | https://airbnb.tech/?p=683 | 2026-10-08 | 저작권 유지(요약만) |
| — | 미확인(읽기 실패) | Material 3 Bottom sheets(JS 렌더, 본문 없음) · M3 accessibility-basics(404) · Apple HIG Layout/Maps(JS 렌더) · Polaris layout(301→API 인덱스) · GOV.UK layout(브레이크포인트 px 미기재, 페이지 폭 1020px만 확인) | 2026-10-08 | 직접 관찰 필요 |
