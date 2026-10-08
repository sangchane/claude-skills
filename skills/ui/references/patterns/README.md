# 화면 패턴 레퍼런스 카탈로그

> dev:ui 스킬의 "화면 패턴·정보 구조" 층. SKILL.md(하드룰·dial)와 `tokens.md`(색·그림자·서체)는 "어떻게 보이나"를 정하고,
> 이 폴더는 "**무엇을 어디에 얼마나 두고, 무엇을 숨기나**"를 정한다. 화면을 만들기 전에 해당 패턴 파일을 읽고 그 규칙·예시대로 만든다.

## 사용법

1. 만들 화면이 아래 표의 어느 행에 해당하는지 고른다(보통 2~3개 파일).
2. 그 파일의 "규칙(측정 가능)"을 체크리스트로 쓰고, "실제 예시" 중 하나를 열어 구조를 본 뒤 만든다.
3. 완료 전 각 파일 끝의 체크 항목과 SKILL.md Pre-Flight를 함께 돈다.
4. 규칙과 DESIGN.md가 부딪히면: 기능 하드룰 > 이 카탈로그의 구조 규칙 > DESIGN.md의 색·서체 > tokens.md.

## 어떤 화면에 어느 파일

| 만들 화면 | 먼저 읽을 파일 | 같이 읽을 파일 |
|---|---|---|
| 판정 결과·점수·등급·감사 리포트(매물 판정, SEO/보안/성능 점수, 신용·건강 리포트) | `verdict-score-report.md` | `progressive-disclosure.md`, `legend-annotation.md` |
| KPI 타일·지표 요약 줄·대시보드 홈 | `kpi-dashboard.md` | `verdict-score-report.md`(기준선), `states.md` |
| 데이터 표·후보 비교 표 | `data-table.md` | `filter-search-sort.md`, `mobile-adaptation.md` |
| 목록+지도(부동산·여행·배달), 목록+상세 패널 | `list-map-detail.md` | `legend-annotation.md`(지도 오버레이), `mobile-adaptation.md` |
| 설명 문장·근거·정의를 어디에 숨길지(접기·툴팁·팝오버·드로어) | `progressive-disclosure.md` | — |
| 빈·로딩·에러·계산 중·오래된 데이터 | `states.md` | `notification-badge.md` |
| 필터 바·검색·정렬·적용된 필터 칩 | `filter-search-sort.md` | `forms.md`, `mobile-adaptation.md` |
| 입력 폼·설정 화면·검증 오류 | `forms.md` | `states.md` |
| 차트 범례·지도 범례·기준선 주석·핀 라벨 | `legend-annotation.md` | `verdict-score-report.md` |
| 배너·토스트·인라인 알림·상태 배지·카운트 | `notification-badge.md` | `states.md` |
| 폰에서 표·차트·지도 접기, 바텀시트, 터치 크기 | `mobile-adaptation.md` | 해당 화면 파일 |
| 출처 모음(전 파일 공통 URL·라이선스) | `sources.md` | — |

## 이 카탈로그가 막아야 하는 것 (실제 사용자 지적, 2026-10-08 부동산 판정 앱)

| 지적 | 담당 파일 · 규칙 |
|---|---|
| 텍스트·정보를 한 페이지에 나열해 너무 많다 → 이미지화·직관적으로 | `verdict-score-report.md` §0·§3(값+기준선 불릿 차트), `kpi-dashboard.md`(타일 수·위계) |
| 숫자만 늘어놓아 기준 충족·강점·약점이 한눈에 안 보인다 | `verdict-score-report.md` §1(결론 1줄)·§3(값·기준·차이)·§4(강점/약점 최대 3개) |
| 설명 문장은 궁금해서 클릭했을 때만 | `verdict-score-report.md` §5, `progressive-disclosure.md`(기본 접힘·2단계 이내) |
| 아이콘·글씨가 커서 지도가 안 보인다 → 구석에 작은 카드 태그로 | `list-map-detail.md`(지도 오버레이), `legend-annotation.md`(지도 범례·핀 라벨 크기) |
| 중요한 화면(지도)이 덜 중요한 띠 때문에 밑으로 밀린다 | `list-map-detail.md`(헤더·필터 바 높이 상한), `notification-badge.md`(배너 높이·개수), `kpi-dashboard.md`(위계) |

## 패턴 항목 형식 (모든 파일 공통)

- **언제 쓰나** · **규칙(측정 가능)** · **Do / Don't** · **실제 예시**(제품/시스템 + 공개 URL + 무엇을 볼 것) · 파일 끝 **출처 표**.
- 수치 옆 `[S1]`은 그 파일의 출처 번호. 출처 표시 없는 수치는 "권장(근거 약함)"으로 명시돼 있다 — 프로젝트 사정에 맞게 바꿔도 된다. 출처 있는 수치를 바꿀 땐 이유를 남긴다.
- "미확인"으로 적힌 항목은 2026-10-08에 직접 읽지 못한 출처다. 쓰기 전에 다시 확인한다.

## 출처 정책

- **무료·공개 자료만**: 공개 디자인 시스템 문서(Carbon·Polaris·Atlassian·Primer·GOV.UK·USWDS·Ant·Fluent·Spectrum·EUI·Lightning), 공개 제품 화면과 그 도움말, UX 연구 요약(NN/g 등), 데이터 시각화 원전(Stephen Few 등). 유료 자료(Mobbin 등)는 쓰지 않는다.
- **링크 + 자체 요약**이 원칙. 인용은 라이선스가 허용하는 범위에서 한 문장 이내로만. 저작권이 유지되는 글(NN/g, 제품 도움말)은 요약만.
- **이미지를 저장하지 않는다**. 스크린샷·도판은 링크로만 가리킨다. 실제 제품 화면은 "URL + 무엇을 볼 것"으로 적고 에이전트가 필요할 때 직접 연다.
- **대량 자동 수집 금지**. 페이지를 읽어 규칙을 뽑는 것만 한다. 작성 시점에 WebFetch로 직접 읽은 페이지만 출처로 올리고, 읽지 못한 것은 "미확인"으로 둔다(기억으로 쓰지 않음).
- 각 출처에 **확인일**과 **라이선스/비고**를 적는다. 라이선스를 모르면 "미확인".
- 재개발닷컴처럼 약관이 자동 수집을 금하는 사이트는 읽지 않는다(프로젝트 AGENTS.md 규약 준수).

## 유지

- 패턴 파일은 하나의 패턴군만, 150~300줄. 넘치면 쪼갠다.
- 새 프로젝트에서 반복된 지적이 나오면 위 "막아야 하는 것" 표와 해당 파일의 Don't에 추가한다.
- 출처 URL이 죽으면 지우지 말고 "미확인(YYYY-MM-DD 404)"로 표시한다.
