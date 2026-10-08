# 차트 범례·지도 범례·주석 (Legend & Annotation)

> 언제 읽나: 차트에 범례·축·참조선·툴팁을 붙이거나, 지도 위에 범례 카드·핀 라벨(가격 칩)·클러스터·컨트롤을 올릴 때.
> 확인일 2026-10-08. 출처는 맨 아래. 수치 옆 [S1] 같은 표시는 출처 번호, 표시 없는 수치는 "권장(근거 약함)".

색 팔레트 값·모노 숫자·대비 비율 같은 토큰은 SKILL.md·tokens.md·dataviz 스킬에 있으므로 여기서는 다루지 않는다.
이 파일은 "라벨·범례·주석을 어디에 몇 개, 무엇을 숨기나"만 정한다.

## 1. 차트 범례 vs 직접 라벨

**언제 쓰나** — 계열이 2개 이상인 선·막대·영역·파이 차트에서 "이 색이 무엇인지"를 알려야 할 때.

**규칙(측정 가능)**
- 계열이 1개면 범례를 두지 않는다. 제목이 계열을 설명한다 [S3][S23].
- 직접 라벨이 우선이다. "use labels directly on the chart to avoid long legends" [S1]. 선 차트는 선 끝(오른쪽 끝)에 계열 이름을 쓴다 — 라벨이 한 세로선에 정렬돼 읽기가 빠르다 [S22].
- 직접 라벨과 범례를 동시에 쓰지 않는다. 둘 중 하나다 [S23].
- 범례가 필요해지는 기준 = 직접 라벨이 겹치는 순간이다. 범례는 차트 **밖**에, 데이터와 겹치지 않는 위치(아래 또는 오른쪽)에 둔다 [S20][S23]. 항목이 많으면(대략 6개↑) 오른쪽 세로 배치 [S23].
- 계열 수 상한: 선 차트 5개 이하, 누적 영역 3개(최대 5), 파이·도넛 5조각 이하, 그룹 막대는 그룹당 4개·그룹 6개 이하, 누적 막대 세그먼트 5개 이하 [S3]. 이 상한을 넘기면 범례도 못 살린다 — 차트를 나누거나 "기타"로 묶는다.
- 범례 항목 순서는 데이터 순서(마지막 값 기준 위→아래, 누적이면 쌓인 순서)와 같게 한다 [S20].
- 범례 글자 크기 = 축 라벨 글자 크기(예: 둘 다 12px). 범례만 크거나 작지 않게 [S20].
- 한 화면에 차트가 여러 개면 범례 위치를 모두 같은 자리(예: 전부 상단 좌측)로 통일한다 (권장, 근거 약함).
- 직접 라벨 글자색은 계열 색과 같게 해서 "어느 선의 이름인지"를 색으로도 잇는다 [S15][S22].

**Do**
- 선 끝 라벨 + 범례 없음을 기본값으로 시작하고, 겹칠 때만 범례로 후퇴한다.
- 범례 항목에 마우스를 올리면 해당 계열만 강조(나머지는 흐리게)하고, 클릭으로 끄고 켤 수 있게 한다 (권장, 근거 약함).
- 파이·도넛은 조각 안·옆에 값(%)을 직접 쓰고 범례를 없앤다 [S1][S21]. 3° 미만 조각은 callout(지시선)으로 [S1].
- 데이터가 없는 계열(전부 0·null)은 범례에서 뺀다 (권장, 근거 약함).

**Don't**
- 범례를 플롯 영역 안쪽 데이터 위에 띄우지 않는다 — 데이터를 가린다 [S12].
- 계열 10개짜리 범례를 만들지 않는다. 계열 상한 [S3]을 먼저 지킨다.
- 범례 항목 이름을 코드값(`cat_a`, `series1`)으로 두지 않는다. 사람이 읽는 이름으로.
- 모바일(390px)에서 범례가 두 줄 넘게 접히면 차트 아래로 옮기거나 항목을 줄인다 — "숫자·글자가 많아 한눈에 안 보인다"는 지적의 원인.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Datawrapper River(공개 갤러리) | https://www.datawrapper.de/blog/automatically-label-values-in-line-charts | 선 끝 라벨·값 라벨이 겹치지 않게 자동 배치되는 모습 |
| Primer 데이터 시각화 | https://primer.style/product/ui-patterns/data-visualization/ | 계열 상한표와 "1개 계열이면 범례 없음" |
| Carbon chart anatomy | https://carbondesignsystem.com/data-visualization/chart-anatomy/ | 범례·축·툴팁이 차트에서 차지하는 위치 |

## 2. 축 레이블·단위·틱

**언제 쓰나** — 수치 축이 있는 모든 차트. 특히 단위(원·㎡·%·건)가 섞이는 부동산 지표.

**규칙(측정 가능)**
- 단위는 축 제목 또는 틱 값 뒤에 한 번만 붙인다(`억`, `%`, `㎡`). 틱마다 긴 단위를 반복하지 않는다 [S12].
- 축 제목은 기본 포함 [S3]. 단, 제목·설명이 "무엇을 측정했는지"를 이미 말하면 축 제목을 생략해 폭을 번다 — 특히 좁은 모바일 [S12].
- 틱 라벨을 회전시키지 않는다. 안 들어가면 틱 수를 줄이거나(예: 5개) 짧게 쓴다(`2024-01` → `1월`) [S12].
- 선 차트·막대 차트의 값 축 원점은 0. 아니면 축에 명시한다 [S4].
- 축 라벨·틱·격자는 "비율과 단위"를 알려주는 보조 요소다 — 데이터보다 옅게, 격자선은 주 눈금만 [S1].
- 축 라벨 대비는 4.5:1 이상 [S3] (색값은 tokens.md).
- 큰 수는 축약한다: `1,200,000,000` → `12억`, `1.2B`. 자릿수가 4자리를 넘으면 축약 (권장, 근거 약함).
- 축 위 값 라벨(데이터 라벨)은 정확한 값이 중요할 때만. 아니면 툴팁·표로 보낸다 [S23].

**Do**
- 차트 제목에 단위·기간을 넣어 축 제목을 생략할 수 있게 쓴다(`평당가(만원), 2024–2026`) [S12].
- 두 축의 단위가 다르면(가격·건수) 각 축 끝에 단위 라벨을 둔다. 이중 축은 2개까지.
- 숫자 포맷(천 단위 쉼표·소수 자리)을 축·툴팁·범례에서 동일하게 쓴다 [S16].

**Don't**
- 틱 라벨을 45° 기울이지 않는다 [S12].
- 축 제목·축 단위·툴팁 단위를 세 군데 모두 반복하지 않는다 — 한 곳이면 된다.
- 축 범위를 데이터 최소값에서 시작해 차이를 부풀리지 않는다 [S4].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Datawrapper Academy | https://www.datawrapper.de/academy/why-datawrapper-does-not-include-axis-labels-for-many-charts | 축 제목 대신 제목·설명·Append 단위를 쓰는 근거 |
| USWDS data visualizations | https://designsystem.digital.gov/components/data-visualizations/ | 원점 0·접근성 표 대체 |

## 3. 주석: 참조선·임계선·하이라이트 영역·텍스트 주석

**언제 쓰나** — "기준선(법정 노후도 2/3, 손익분기)을 넘었는지"처럼 숫자 나열 대신 한눈에 판정이 보여야 할 때.

**규칙(측정 가능)**
- 임계선·참조선은 라벨을 **선 끝**(오른쪽 끝 또는 위 끝)에 붙인다. 범례에 "기준선" 항목을 만들지 않는다 (권장, 근거 약함; 선 끝 정렬 근거 [S22]).
- 라벨 문구는 `값 + 뜻` 한 토막: `66.7% 법정 기준`, `손익분기 0`. 10자 안팎 (권장, 근거 약함).
- 참조선은 점선·데이터보다 옅은 색. 데이터 선(2px 실선 [S3])과 구분되게 1px 점선 (권장, 근거 약함).
- 수평선은 `y=값`, 수직선은 `x=날짜` 하나로 정의되는 것만 참조선으로 쓴다 [S14]. 구간(범위)은 반투명 영역(range highlight)으로 — "threshold value or a certain date or timespan"을 가리키는 용도 [S13].
- 차트 하나에 참조선·하이라이트 영역은 합쳐 3개 이하 (권장, 근거 약함).
- 텍스트 주석은 데이터 옆 빈 공간에, 필요하면 화살표·원으로 대상 지점을 지정한다 [S13][S14]. 주석은 특정 행(데이터 포인트)에 묶는다 — 정렬·재배치 후에도 따라간다 [S13].
- 모바일에서는 텍스트 주석을 차트 밖 아래 "키"로 내리거나 일부만 보인다 [S13][S14]. 데스크톱 전용 주석을 지정할 수 있게 한다.
- 값 라벨은 전부 쓰지 않는다: 첫·끝값, 또는 봉우리·골 같은 "흥미로운 지점"만 [S15].

**Do**
- 기준선 라벨 색을 판정 뜻(통과·미달)과 맞춘다(의미색은 tokens.md).
- 강조 구간(예: 발표일~지정일)은 영역 채우기 + 상단 한 줄 라벨.
- 주석 글자 크기는 축 라벨과 같거나 한 단계 작게, 본문보다 크지 않게 [S20].

**Don't**
- 참조선의 뜻을 설명 문단으로 차트 아래에 늘어놓지 않는다 — 선 끝 라벨 한 토막이면 된다. 긴 설명은 접기(클릭 시).
- 주석을 데이터 선 위에 겹쳐 쓰지 않는다 [S21].
- 기준선 5개가 한 차트에 교차하게 두지 않는다 — 판정 기준이 여럿이면 차트를 나누거나 체크리스트로 보낸다.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Datawrapper 막대 주석 | https://www.datawrapper.de/blog/annotations-in-bar-charts | 라인·범위 하이라이트가 임계값·기간을 가리키는 방식 |
| Datawrapper 산점도 주석 | https://www.datawrapper.de/academy/customizing-your-scatter-plot-annotate | `y=50` 참조선, 공간 있을 때만 보이는 라벨 |

## 4. 툴팁

**언제 쓰나** — 호버·탭으로 정확한 값을 보여줄 때. 직접 라벨·데이터 라벨을 줄이는 대신 쓴다.

**규칙(측정 가능)**
- 툴팁은 해당 지점의 **양 축 값**을 모두 반복한다(x: 날짜·범주, y: 값+단위) + 계열 이름 [S1].
- 구조: 1행 = x값(굵게), 2행~ = 계열별 `색점 이름 값`. 계열이 여럿이면 한 툴팁에 전부(최대 계열 상한 5 [S3]).
- 단위·숫자 포맷은 축과 동일 [S16].
- 툴팁은 커서를 가리지 않게 커서 오른쪽 위에, 화면 가장자리에서는 반대쪽으로 뒤집는다 (권장, 근거 약함).
- 큰 숫자 하나짜리 KPI 타일에는 툴팁을 두지 않는다 — 값을 덮는다 [S23].
- 터치 기기에서는 탭 고정형 툴팁(탭하면 열리고 바깥 탭으로 닫힘)으로 (권장, 근거 약함).

**Do**
- 툴팁에 정확한 값을 두고, 차트 위 데이터 라벨은 첫·끝값만 남긴다 [S15][S23].
- 지도 폴리곤·심볼도 같은 구조(지역명 → 값+단위 → 보조 정보) [S16].

**Don't**
- 툴팁에 설명 문단을 넣지 않는다. 값만. 설명은 클릭 시 패널로.
- 툴팁에만 있는 정보로 판정을 설명하지 않는다 — 호버 없이도 결론은 보여야 한다.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Carbon chart anatomy | https://carbondesignsystem.com/data-visualization/chart-anatomy/ | "repeat the corresponding values of the data point on both axes" |

## 5. 색 범례: 연속·구간·범주

**언제 쓰나** — 코로플레스 지도·히트맵·버블 차트처럼 색이 값을 뜻할 때.

**규칙(측정 가능)**
- 범례는 세 종류 중 하나를 **명시**한다: 범주(categorical) · 구간(stepped, bins) · 연속(continuous, gradient) [S16]. 섞지 않는다.
- 구간 범례는 각 구간의 경계값을 쓴다("ranges": 색 견본 옆 `0–10`, `10–20`…). 연속 범례는 최소·최대(+선택적 중앙값)만 쓴다 [S16].
- 구간 수: 코로플레스 5~8단계. Leaflet 예시 8단계 [S5], Carbon 순차 팔레트 10단계 이산 또는 연속 [S2]. 그 이상은 눈으로 구분이 안 된다 (권장, 근거 약함).
- 구간 나누기 방식(선형·분위·자연 구분·반올림·사용자 지정)을 하나 고르고 범례 제목이나 캡션에 적는다 [S17].
- 범주 팔레트는 Carbon 기준 최대 14색 순서 고정 [S2]. 실무 상한은 항목 1의 계열 상한(5~6)을 따른다.
- 발산(diverging) 팔레트는 중심값(0·평균)을 범례 가운데에 표시한다. Carbon 발산 팔레트는 8단계 [S2].
- 밝은 테마에서는 가장 어두운 색이 가장 큰 값, 어두운 테마에서는 가장 밝은 색이 가장 큰 값 [S2].
- 그라디언트를 순차 팔레트 대신 장식용으로 쓰지 않는다 [S2].
- 범례 제목 = 변수명 + 단위 (`노후도(%)`) [S16]. 범례 방향은 가로·세로 중 공간에 맞는 것, 지도 안이면 네 모서리 중 하나 [S16].
- 범례 항목 호버 시 지도의 해당 구간을 강조한다 [S16][S18] (권장).

**Do**
- 구간 경계를 반올림된 값(10·20·50)으로 — "rounded values" 방식 [S17].
- 범례 숫자 포맷을 툴팁·축과 맞춘다 [S16].
- "데이터 없음"에 별도 회색 견본 1개를 범례 끝에 둔다 (권장, 근거 약함).

**Don't**
- 연속 그라디언트 범례에 중간 눈금 10개를 쓰지 않는다 — 최소·최대·중앙이면 된다 [S16].
- 같은 색을 다른 변수에 재사용하지 않는다 [S4].
- 범주 색 14개를 한 범례에 다 쓰지 않는다 — 상한 [S2]은 팔레트 크기이지 권장 개수가 아니다.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Leaflet choropleth | https://leafletjs.com/examples/choropleth/ | 8단계 구간 범례, 우하단 반투명 카드 |
| Datawrapper 색 범례 | https://www.datawrapper.de/academy/maps-how-to-create-a-custom-map-key | 범주·구간(ruler/ranges)·연속(range) 세 형식 |
| Carbon color palettes | https://carbondesignsystem.com/data-visualization/color-palettes/ | 순차 10단계·발산 8단계·범주 14색 |

## 6. 지도 범례·오버레이·핀 라벨(가격 칩)·클러스터

**언제 쓰나** — 지도가 주인공인 화면(매물·구역 지도). 지도 위에 올리는 모든 것(범례·컨트롤·핀·라벨·칩)의 크기와 개수.

**규칙(측정 가능)**
- 범례·정보 카드는 **구석** 하나(좌상 또는 우하)에 작은 카드로. Leaflet 예시: 정보 카드 좌상(기본), 범례 우하 `position: 'bottomright'`, 배경 `rgba(255,255,255,0.8)`, 패딩 `6px 8px`, 글자 `14px` [S5]. Google Maps 컨트롤 슬롯도 9개 구석·변 위치 중 하나를 고른다 [S6].
- 오버레이 카드의 지도 면적 대비 상한: 폭은 지도 폭의 1/4 이하, 높이는 지도 높이의 1/3 이하. 폰(390px)에서는 폭 160px 이하 (권장, 근거 약함). Google Maps는 200×200px보다 작은 지도에서 컨트롤을 자동으로 숨긴다 [S6] — 이보다 작으면 범례도 숨긴다.
- 범례는 **접기 가능**: 기본은 폰에서 접힘(아이콘 1개), 데스크톱에서 펼침. 접힌 상태는 24~32px 버튼 하나 (권장, 근거 약함).
- 범례가 중요한 지역을 가리면 지도 밖(위·아래)으로 옮긴다 [S18]. 지도 안쪽에 둘 때는 offset·padding으로 빈 모서리에 둔다 [S16][S18].
- 같은 구석에 컨트롤을 겹쳐 두지 않는다. 겹침은 보장되지 않는다 [S6]. 구석당 1묶음, 세로로 쌓는다.
- 핀 라벨(가격 칩): 글자 6자 이내(`5.2억`, `12.5억`, `3.1억↑`), 글자 11~12px, 높이 20~24px, 반경 큰 캡슐 (권장, 근거 약함). 축약 단위(억·천)로 자릿수를 줄인다.
- 라벨 충돌: 겹치면 숨긴다. Mapbox 기본 `text-allow-overlap: false`, `icon-allow-overlap: false`, `text-optional: false` [S10]. Google Maps는 `OPTIONAL_AND_HIDES_LOWER_PRIORITY`로 zIndex가 낮은 마커를 숨긴다(기본 `REQUIRED`는 항상 표시) [S7]. 우선순위는 사용자가 선택·강조한 매물 > 판정 통과 > 나머지 (권장).
- 라벨 수: 데스크톱 화면에 동시에 보이는 가격 칩 30~40개를 넘으면 클러스터로 묶는다. Datawrapper 지명 라벨 상한 30개 [S19] (권장).
- 클러스터: Mapbox 예시 `clusterRadius: 50px`, `clusterMaxZoom: 14`, 원 크기 20/30/40px(100·750개 경계), 숫자 12px [S9]. Leaflet.markercluster 기본 반경 80px, 색 경계 10·100개 [S11]. 클러스터 숫자는 "몇 개가 들어있는지"다 [S8].
- 줌 임계: 라벨은 최소 줌 이상에서만 보인다 [S19]. 예: 줌 14 미만 = 클러스터+숫자, 14 이상 = 개별 칩 (권장, Mapbox 예시 [S9] 기준).
- 상위 N개(사용자가 고른 매물·판정 1등)는 화면이 작아도 항상 보이게 고정한다 [S19].
- 핀 색은 뜻 하나만(판정 등급). 모양·크기로 두 번째 변수(면적 등)를 넣을 수 있지만 범례에 둘 다 쓴다 [S18].

**Do**
- 지도 화면 첫 로드 시 보이는 것: 지도 + 구석 범례 1개 + 가격 칩. 나머지(필터·설명)는 시트·패널로.
- 핀 호버·탭 시 툴팁(항목 4 구조)을 띄우고, 상세는 패널로.
- 폰에서는 범례를 접고, 하단 시트가 지도 높이의 40% 이상 올라오지 않게 한다 (권장, 근거 약함).

**Don't**
- 아이콘·글씨를 키워 지도를 덮지 않는다. "아이콘·글씨가 너무 커서 지도가 안 보인다 → 구석에 작은 카드 태그로"가 실제 지적이다.
- 지도 위에 설명 문장·숫자 표를 띄우지 않는다. 지도 위는 범례·칩·컨트롤만.
- 겹친 라벨을 그대로 그리지 않는다(`allow-overlap: true` 금지) [S10].
- 중요한 지도를 상단 띠·배너 때문에 아래로 밀지 않는다 — 배너 규칙은 `notification-badge.md`.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Mapbox cluster 예시 | https://docs.mapbox.com/mapbox-gl-js/example/cluster/ | 50px 반경·줌 14·3단계 원 크기 |
| Leaflet choropleth 예시 | https://leafletjs.com/examples/choropleth/ | 좌상 정보 카드 + 우하 범례, 0.8 투명 배경 |
| Google Maps 컨트롤 | https://developers.google.com/maps/documentation/javascript/controls | 컨트롤 슬롯 위치·200×200 미만 숨김 |
| Google Maps collision | https://developers.google.com/maps/documentation/javascript/advanced-markers/collision-behavior | 겹치는 마커 숨김 우선순위 |
| Zillow 지도 가격 칩 | https://www.zillow.com/homes/ (WebFetch 차단, 공개 화면 직접 확인) | 핀 위 `$1.2M` 축약 칩 |

## 출처
| # | 출처 | URL | 확인일 | 라이선스/비고 |
|---|---|---|---|---|
| S1 | IBM Carbon — Chart anatomy | https://carbondesignsystem.com/data-visualization/chart-anatomy/ | 2026-10-08 | Apache-2.0(Carbon) |
| S2 | IBM Carbon — Color palettes | https://carbondesignsystem.com/data-visualization/color-palettes/ | 2026-10-08 | Apache-2.0(Carbon) |
| S3 | GitHub Primer — Data visualization | https://primer.style/product/ui-patterns/data-visualization/ | 2026-10-08 | MIT(Primer) |
| S4 | USWDS — Data visualizations | https://designsystem.digital.gov/components/data-visualizations/ | 2026-10-08 | 퍼블릭도메인/CC0(USWDS 문서) |
| S5 | Leaflet — Choropleth 튜토리얼 | https://leafletjs.com/examples/choropleth/ | 2026-10-08 | BSD-2(Leaflet 코드), 문서 미확인 |
| S6 | Google Maps JS — Controls | https://developers.google.com/maps/documentation/javascript/controls | 2026-10-08 | 미확인 |
| S7 | Google Maps JS — Collision behavior | https://developers.google.com/maps/documentation/javascript/advanced-markers/collision-behavior | 2026-10-08 | 미확인 |
| S8 | Google Maps JS — Marker clustering | https://developers.google.com/maps/documentation/javascript/marker-clustering | 2026-10-08 | 미확인 |
| S9 | Mapbox GL JS — Cluster 예시 | https://docs.mapbox.com/mapbox-gl-js/example/cluster/ | 2026-10-08 | 미확인 |
| S10 | Mapbox Style Spec — Layers(symbol) | https://docs.mapbox.com/style-spec/reference/layers/ | 2026-10-08 | 미확인 |
| S11 | Leaflet.markercluster README | https://github.com/Leaflet/Leaflet.markercluster | 2026-10-08 | MIT |
| S12 | Datawrapper Academy — 축 레이블 생략 이유 | https://www.datawrapper.de/academy/why-datawrapper-does-not-include-axis-labels-for-many-charts | 2026-10-08 | 저작권 유지, 요약만 |
| S13 | Datawrapper Blog — 막대 차트 주석 | https://www.datawrapper.de/blog/annotations-in-bar-charts | 2026-10-08 | 저작권 유지, 요약만 |
| S14 | Datawrapper Academy — 산점도 주석 | https://www.datawrapper.de/academy/customizing-your-scatter-plot-annotate | 2026-10-08 | 저작권 유지, 요약만 |
| S15 | Datawrapper Blog — 선 차트 값 라벨 | https://www.datawrapper.de/blog/automatically-label-values-in-line-charts | 2026-10-08 | 저작권 유지, 요약만 |
| S16 | Datawrapper Academy — 색 범례 | https://www.datawrapper.de/academy/maps-how-to-create-a-custom-map-key | 2026-10-08 | 저작권 유지, 요약만 |
| S17 | Datawrapper Academy — 구간 색 스케일 | https://www.datawrapper.de/academy/how-to-customize-stepped-color-scales | 2026-10-08 | 저작권 유지, 요약만 |
| S18 | Datawrapper Blog — 코로플레스·심볼 지도 | https://www.datawrapper.de/blog/choropleth-symbol-maps-easier-faster-better-looking/ | 2026-10-08 | 저작권 유지, 요약만 |
| S19 | Datawrapper Academy — 지도 라벨 | https://www.datawrapper.de/academy/how-to-add-map-labels | 2026-10-08 | 저작권 유지, 요약만 |
| S20 | QuantHub — Chart legends | https://quanthub.com/designing-charts-chart-legends | 2026-10-08 | 저작권 유지, 요약만 |
| S21 | QuantHub — Labeling data directly | https://quanthub.com/designing-charts-labeling-data-directly-on-the-chart | 2026-10-08 | 저작권 유지, 요약만 |
| S22 | Jon Schwabish — Graph labeling strategies | https://jschwabish.substack.com/p/graph-labeling-strategies | 2026-10-08 | 저작권 유지, 요약만 |
| S23 | Yellowfin — Legends, labels & tooltips | https://www.yellowfinbi.com/best-practice-guide/charts-visualizations/legends-labels-tooltips | 2026-10-08 | 저작권 유지, 요약만 |

읽기 실패(출처로 쓰지 않음): Carbon basic-charts(404), NN/g chart-legends(404), Atlassian data-visualization(404), Mapbox 예시 목록(본문 없음)·add-a-legend(403), Datawrapper 범례 추가·better labels·direct-labeling(404), think-cell(403), Zillow(403).
