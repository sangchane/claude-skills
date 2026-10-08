# 데이터 표·비교 표 (Data table & comparison table)

> 언제 읽나: 매물·구역·거래 같은 레코드 목록을 표로 보여 주거나, 후보 여러 개를 기준별로 나란히 비교하는 화면을 만들 때.
> 확인일 2026-10-08. 출처는 맨 아래. 수치 옆 [S1] 같은 표시는 출처 번호, 표시 없는 수치는 "권장(근거 약함)".

숫자 `font-mono`·산세리프·상태색 쌍은 SKILL.md·tokens.md가 정한다. 여기서는 "열을 어디에 어떻게, 몇 개, 무엇을 숨기나"만 다룬다.

## 1. 열 정렬과 숫자 서식

**언제 쓰나** — 모든 표. 특히 숫자 열이 2개 이상인 표.

**규칙(측정 가능)**
- 숫자 열은 우측 정렬, 텍스트 열은 좌측 정렬 [S5][S6][S11]. 헤더도 데이터와 같은 쪽으로 정렬한다 [S11]
- 짧은 범주값(등급 A/B, 예/아니오)만 가운데 정렬 가능 (권장, 근거 약함)
- 한 열 안에서 소수 자릿수·반올림·단위 접두/접미를 통일한다 [S11]. 통화 기호는 헤더에 1번만 쓰고 셀에서는 뺀다 (권장, 근거 약함)
- 숫자는 등폭(tabular) 숫자로 자릿수를 맞춘다 [S11][S6]. 날짜·전화번호에는 모노를 쓰지 않는다 [S6]
- 첫 열은 사람이 읽을 수 있는 레코드 식별자(이름·주소). 자동 생성 ID를 첫 열에 두지 않는다 [S7]
- 열 순서: 조회용 텍스트 열이 첫 열, 조회용 숫자 열은 첫 또는 둘째 열. 관련 열은 서로 붙인다 [S7][S11]
- 열 제목은 1~2단어, 문장 부호 없는 sentence case. 길면 2줄까지 줄바꿈 후 말줄임 + 툴팁 [S1]
- 열 폭은 내용량에 맞춘다(짧은 값은 좁게, 긴 텍스트는 넓게). 셀 내용이 2줄로 흐르지 않게 폭을 잡는다 [S11]
- 행 단위로 세는 기준(주/일 등)을 섞지 않는다 [S6]

**Do**
- 표를 그리기 전에 열마다 `타입(텍스트/숫자/날짜/상태)` → 정렬 방향을 표로 적는다.
- 셀 값이 길면 `ellipsis` + 전체값 툴팁 [S3].
- 헤더 배경을 데이터 행과 구분되게 한 단계 다르게 [S11].

**Don't**
- 숫자를 좌측 정렬하거나 가운데 정렬하지 않는다.
- 같은 열에 `12.3`, `12`, `12.345`를 섞지 않는다.
- 첫 열에 UUID·일련번호를 두지 않는다 [S7].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| GOV.UK Table | https://design-system.service.gov.uk/components/table/ | `--numeric` 클래스로 숫자 열 우측 정렬 [S5] |
| USWDS Table | https://designsystem.digital.gov/components/table/ | 숫자 우측 정렬 + 밀집 숫자에 모노 서체, 날짜에는 금지 [S6] |
| data.europa.eu Table scannability | https://data.europa.eu/apps/data-visualisation-guide/table-design-scannability | 정렬·등폭 숫자·열 순서 규칙 [S11] |

## 2. 행 높이·밀도와 고정 헤더·고정 열

**언제 쓰나** — 20행 이상이거나 열이 화면 폭을 넘는 표.

**규칙(측정 가능)**
- 행 높이 단계는 3~5개 중 하나의 체계를 골라 고정. Carbon: xs 24 · sm 32 · md 40(기본) · lg 48 · xl 64px [S1]. Primer: condensed · normal(기본) · spacious [S4]. Ant: small · middle · large [S3]. Spectrum: compact · regular(기본) · spacious [S10]
- 기본은 중간 밀도(40px). 관제/Cockpit 프로파일(DENSITY ≥ 8)은 xs·sm, 읽기 위주는 lg (권장, Carbon 설명 기준 [S1])
- 헤더 행 높이 = 데이터 행 높이. 툴바·일괄작업 바·페이지네이션 높이도 행 높이와 맞춘다(xl만 lg 사용) [S1]
- 세로 스크롤이 생기면 헤더를 고정한다 [S6][S7]. 가로 스크롤이 생기면 첫 열(식별자)을 고정한다 [S7][S3]
- 가로 스크롤 표는 키보드 접근을 위해 컨테이너에 `tabindex="0"` [S6]
- 행 hover 강조는 항상 켠다 [S1]. 줄무늬(zebra)는 가로 스캔이 긴 표(열 6개 이상)에만 (개수는 권장, 근거 약함; zebra 자체는 [S1][S6][S7])
- 폰에서는 열을 쌓는(stacked) 변형으로 바꾸고 각 셀에 열 이름 라벨을 붙인다 [S6]. 쌓인 표에서는 정렬 기능을 끈다 [S6]
- 밀도 전환을 사용자에게 열어 주려면 토글 1개(행 높이 선택) [S9]

**Do**
- 밀도 단계를 토큰으로 두고 표마다 같은 단계를 쓴다.
- 긴 표는 `scroll.y`를 주고 헤더 고정 [S3]; 열이 많으면 `scroll.x` + 첫 열 고정 [S3].
- 큰 데이터 집합은 폰에서 글자 크기를 한 단계 줄이는 변형을 쓰되, 작은 표에는 쓰지 않는다 [S5].

**Don't**
- 표마다 행 높이를 다르게 하지 않는다.
- 헤더와 행의 높이를 다르게 하지 않는다 [S1].
- 셀 안에 문단·불릿 여러 개를 넣지 않는다 — 그건 아코디언·상세 페이지로 [S6].
- 가로 스크롤 표를 폰에서 그대로 두지 않는다 — 쌓기 또는 열 숨기기(3절).

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| IBM Carbon Data table | https://carbondesignsystem.com/components/data-table/usage/ | 5단계 행 높이 수치, 헤더·툴바·페이지네이션 높이 일치 [S1] |
| USWDS Table | https://designsystem.digital.gov/components/table/ | sticky header · scrollable · stacked(모바일) · compact 변형 [S6] |
| Ant Design Table | https://ant.design/components/table | `scroll.x/y`로 고정 헤더·고정 열, size 3단계 [S3] |

## 3. 열 개수 상한·열 숨기기·정렬·필터 표시

**언제 쓰나** — 열이 7개를 넘거나, 사용자가 정렬·필터를 바꿀 수 있는 표.

**규칙(측정 가능)**
- 기본 노출 열은 데스크톱 6~8개, 폰 2~3개. 나머지는 열 선택기(column selector)로 켜게 한다 (개수는 권장, 근거 약함; 선택기는 [S7][S9])
- 숨겨진 열이 있으면 "숨김 n개" 표시를 보이는 곳에 둔다 [S7]
- 열 순서 바꾸기는 드래그로, 켜고 끄기는 체크 목록으로 [S9]
- 정렬 가능한 표는 기본 정렬 열 1개를 항상 정한다 [S4]. 사용자 정렬 시 첫 클릭은 오름차순, 다시 누르면 내림차순 [S4]
- 정렬 아이콘은 정렬 중인 열에만 보인다. 나머지 열은 hover 시에만 [S1]
- 정렬 상태 변화는 `aria-live`로 알린다. 서식 붙은 숫자는 원시값(`data-sort-value`)으로 정렬 [S6]
- 필터는 찾기 쉽고 빠르게. 필터가 적용 중이면 적용 개수·내용을 항상 표시한다 [S7]
- 열 필터 메뉴는 다중 선택이 기본, 항목이 많으면 메뉴 안 검색 [S3]
- 툴바 액션은 최대 5개, 나머지는 overflow 메뉴 [S1]
- 많은 열 + 균일한 데이터 + 정렬 중요 → 데이터 그리드. 그 외는 일반 표 [S9]

**Do**
- "이 표에서 무엇을 찾나"를 먼저 정하고 그 기준 열을 기본 정렬·좌측에 둔다 [S7].
- 필터 적용 중에는 칩(선택값)을 표 위 1줄에 나열하고 전체 해제 버튼 1개.
- 정렬·필터·검색·열 선택기를 같은 툴바 한 줄에 모은다.

**Don't**
- 열을 전부 보이게 두고 가로 스크롤로 해결하지 않는다.
- 모든 열 헤더에 정렬 화살표를 상시 노출하지 않는다 [S1].
- 필터가 걸린 채로 "결과 0"을 빈 표로만 보여 주지 않는다 — 어떤 필터 때문인지 표시 + 해제 버튼.
- 병합 셀·쌓인(모바일) 표에서 정렬을 켜지 않는다 [S6].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Elastic EUI Data grid | https://eui.elastic.co/docs/components/tabular-content/data-grid/ | 열 선택기·드래그 순서·밀도 토글·전체화면 [S9] |
| GitHub Primer DataTable | https://primer.style/product/components/data-table/ | 기본 정렬 열 필수, 클릭 순서, 열 폭 옵션 [S4] |
| NN/g Data Tables | https://www.nngroup.com/articles/data-tables/ | 열 숨기기·활성 필터 표시·고정 헤더/열 [S7] |

## 4. 셀 상태·빈 셀·행 액션·행 선택·일괄 작업

**언제 쓰나** — 상태(진행/승인/위험)가 있는 레코드, 행마다 할 일이 있는 표.

**규칙(측정 가능)**
- 빈 셀은 비워 두지 않고 `—`(em dash) 1자. `<td>`는 항상 둔다 [S6](태그) (대시 표기는 권장, 근거 약함)
- 상태는 배지 1개, 배지 색은 tokens.md 의미쌍 5종 이내. 배지에 텍스트를 반드시 넣는다(색만으로 전달 금지) [S2]
- 상태 열은 첫 열(식별자) 바로 오른쪽 또는 맨 오른쪽 액션 열 직전 한 곳으로 통일 (권장, 근거 약함)
- 행 액션이 1개면 마지막 열에 아이콘 버튼 1개(헤더는 시각적으로 숨김). 여러 개면 드롭다운 메뉴, 자주 쓰는 1개만 밖으로 꺼낸다 — "1개 이상 꺼내지 않는다" [S4]
- 여러 행에 같은 작업을 하려면 체크박스 + 일괄 작업 바. 인라인 액션을 늘리지 않는다 [S7]
- 선택 유형은 다중(체크박스) 또는 단일(라디오) 둘 중 하나 [S1][S3]. 다중 선택이면 체크박스 열이 자동으로 첫 열 앞에 생긴다 [S10]
- 헤더 체크박스는 전체 선택과 부분 선택(indeterminate) 상태를 가진다 [S1]. "Select all" 단축을 제공한다 [S7]
- 일괄 작업 모드에서는 인라인 행 액션을 비활성화한다 [S1]
- 행 편집은 표 안 입력칸이 아니라 모달 또는 전용 페이지 [S2]; 단, 다른 행을 참조하며 고쳐야 하면 모달 대신 비모달 사이드 패널 [S7]
- 행 삭제 후 포커스는 다음 포커스 가능 항목으로 이동 [S2]
- 확장 행은 보조 데이터만. 확장 영역이 비좁으면 전용 페이지로 보낸다 [S1]

**Do**
- 배지 텍스트는 2~4자 명사(`승인`, `보류`, `위험`)로 통일.
- 선택된 행 수를 일괄 작업 바에 표시하고, 바의 높이는 행 높이와 맞춘다 [S1].
- 행 클릭 = 상세 열기, 체크박스 클릭 = 선택. 두 동작을 섞지 않는다.

**Don't**
- 강조된 행 배경만으로 선택·포커스·의미를 전달하지 않는다 [S2].
- 행마다 버튼 3개씩 늘어놓지 않는다 [S4][S7].
- 빈 셀을 `0`·`N/A`·공백으로 제각각 쓰지 않는다.
- 상태를 설명 문장으로 쓰지 않는다 — 배지 + 궁금하면 툴팁.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| IBM Carbon Data table | https://carbondesignsystem.com/components/data-table/usage/ | batch action 모드, indeterminate 헤더 체크박스, 확장 행 [S1] |
| GitHub Primer DataTable | https://primer.style/product/components/data-table/ | 행 액션 1개 규칙, 액션 열 헤더 숨김 [S4] |
| Atlassian Dynamic table | https://atlassian.design/components/dynamic-table/usage | 편집은 모달/전용 페이지, 삭제 후 포커스, 강조 행 금지 [S2] |

## 5. 비교 표 — 열=후보, 행=기준, 차이 강조

**언제 쓰나** — 매물·구역·요금제처럼 "후보 몇 개를 기준별로 나란히" 볼 때. 판정 결과를 사용자가 한눈에 비교해야 할 때.

**규칙(측정 가능)**
- 후보(열)는 최대 5개. 그 이상이면 먼저 걸러 5개 이하로 줄인다 [S8]
- 배치는 후보 = 열, 기준(속성) = 행. 행 라벨은 왼쪽, 열 라벨은 위 [S8]
- 모든 후보에 같은 기준 행을 채운다. 빠진 값은 `—`로 두되, 빠진 기준이 많으면 비교 표로 만들지 않는다 [S8]
- "차이만 보기" 토글 1개. 켜면 같은 값인 행을 숨기거나 다른 값 셀을 강조한다 [S8]
- 기준별로 "좋음/나쁨" 방향이 있으면 셀에 통과/미달 표시(아이콘 + 텍스트)를 넣는다. 숫자만 두지 않는다 (권장, 근거 약함)
- 열 헤더(후보 이름)는 스크롤해도 고정 [S8]. 행 라벨 열도 가로 스크롤 시 고정 [S7]
- 폰에서는 한 번에 2개 이상 보이게 하거나, 후보별 탭으로 전환 [S8]
- 기준 행은 중요한 순서로, 결정에 쓰이는 상위 5개를 먼저 두고 나머지는 접힘 그룹 (개수는 권장, 근거 약함)

**Do**
- 기준 행 그룹(입지·사업성·리스크 등)마다 그룹 헤더 행을 두고, 그룹 사이 여백을 더 준다 [S11].
- 기준선(법정 요건·목표)이 있는 행은 기준값 열을 맨 왼쪽 고정 열로 두어 후보 값과 바로 대조하게 한다.
- 각 후보 열 맨 위에 요약(충족 n / N 또는 점수) 1줄을 둔다 — 열 전체를 안 읽어도 순위가 보이게.

**Don't**
- 후보 6개 이상을 한 표에 넣지 않는다 [S8].
- 후보마다 기준이 다른 표를 만들지 않는다 — "가장 큰 문제는 디자인이 아니라 콘텐츠" [S8].
- 숫자만 늘어놓고 어떤 기준을 충족하는지 사용자가 계산하게 두지 않는다 — 통과/미달 표시와 차이 강조를 넣는다.
- 설명 문장을 셀에 쓰지 않는다 — 기준 행 라벨의 `?` 툴팁으로.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| NN/g Comparison Tables | https://www.nngroup.com/articles/comparison-tables/ | 최대 5개, 열=옵션 행=속성, 차이 강조 토글, 고정 헤더, 모바일 탭 [S8] |
| GOV.UK Table | https://design-system.service.gov.uk/components/table/ | `scope="row"` 행 헤더로 기준 라벨 구조화 [S5] |

## 6. 페이지네이션 vs 무한 스크롤

**언제 쓰나** — 행이 한 화면을 넘는 모든 목록.

**규칙(측정 가능)**
- 목표 지향 작업(특정 레코드 찾기·되돌아가기·비교)은 페이지네이션. 무한 스크롤은 흐름형·발견형 콘텐츠에만 [S12]
- 페이지 크기 기본값은 25 또는 50, 선택지는 3개(예: 50·100·200) [S9]. 총 행이 50을 넘을 때만 페이지 크기 선택기를 보인다 [S3]
- 페이지가 1개뿐이면 페이지네이션을 숨긴다 [S3]
- 페이지네이션 바 높이 = 행 높이(xl 표는 lg) [S1]
- 현재 범위(`1–50 / 1,284`)와 총 개수를 항상 표시 (권장, 근거 약함)
- 대시보드 안의 요약 표는 상위 5~10행만 + "View All" 링크로 전체 목록 페이지로 [S13]
- 1,000행 이상을 한 페이지에 두어야 하면 가상 스크롤(virtual) + 고정 높이 [S3][S9]
- CSV 내보내기는 패널당 상한(예: 250행)을 명시한다 [S13]

**Do**
- 페이지네이션은 표 아래 오른쪽 1곳 [S3]. 표 위에는 두지 않는다.
- URL에 페이지·정렬·필터를 담아 뒤로 가기·공유가 되게 한다.
- 가상 스크롤을 쓸 때도 헤더 고정과 첫 열 고정을 유지한다.

**Don't**
- 비교·되돌아가기가 필요한 표에 무한 스크롤을 쓰지 않는다 [S12].
- 페이지 크기 선택지를 5개 이상 주지 않는다.
- 무한 스크롤 아래에 푸터·다음 섹션을 두지 않는다 — 영원히 못 닿는다.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Ant Design Table | https://ant.design/components/table | 하단 우측 페이지네이션, total > 50일 때 크기 선택기, `hideOnSinglePage`, virtual [S3] |
| Elastic EUI Data grid | https://eui.elastic.co/docs/components/tabular-content/data-grid/ | `pageSizeOptions: [50, 100, 200]`, react-window 가상화 [S9] |
| Vercel Web Analytics | https://vercel.com/docs/analytics | 패널은 상위 항목만, View All로 확장, CSV 250행 상한 [S13] |
| NN/g Infinite Scrolling | https://www.nngroup.com/articles/infinite-scrolling/ | 목표 지향 작업에는 페이지네이션 [S12] |

## 출처
| # | 출처 | URL | 확인일 | 라이선스/비고 |
|---|---|---|---|---|
| S1 | IBM Carbon — Data table usage | https://carbondesignsystem.com/components/data-table/usage/ | 2026-10-08 | 페이지에 표기 없음(© IBM) · 코드는 Apache-2.0 |
| S2 | Atlassian Design — Dynamic table usage | https://atlassian.design/components/dynamic-table/usage | 2026-10-08 | 미확인 |
| S3 | Ant Design — Table | https://ant.design/components/table | 2026-10-08 | MIT(코드) · 문서 미확인 |
| S4 | GitHub Primer — DataTable | https://primer.style/product/components/data-table/ | 2026-10-08 | MIT(코드) · 문서 미확인 · 컴포넌트는 experimental |
| S5 | GOV.UK Design System — Table | https://design-system.service.gov.uk/components/table/ | 2026-10-08 | Open Government Licence v3.0(페이지 명시) |
| S6 | USWDS — Table | https://designsystem.digital.gov/components/table/ | 2026-10-08 | 퍼블릭 도메인(미 연방 정부, 페이지 명시) |
| S7 | NN/g — Data Tables: Four Major User Tasks | https://www.nngroup.com/articles/data-tables/ | 2026-10-08 | 저작권 유지(NN/g, 요약만) |
| S8 | NN/g — Comparison Tables | https://www.nngroup.com/articles/comparison-tables/ | 2026-10-08 | 저작권 유지(NN/g, 요약만) |
| S9 | Elastic EUI — Data grid | https://eui.elastic.co/docs/components/tabular-content/data-grid/ | 2026-10-08 | 미확인 |
| S10 | Adobe Spectrum Web Components — Table | https://opensource.adobe.com/spectrum-web-components/components/table/ | 2026-10-08 | 미확인(오픈소스 표기만) |
| S11 | data.europa.eu — Table design: scannability | https://data.europa.eu/apps/data-visualisation-guide/table-design-scannability | 2026-10-08 | 미확인(© 2023 eu academy) |
| S12 | NN/g — Infinite Scrolling Is Not for Every Website | https://www.nngroup.com/articles/infinite-scrolling/ | 2026-10-08 | 저작권 유지(NN/g, 요약만) |
| S13 | Vercel Docs — Web Analytics | https://vercel.com/docs/analytics | 2026-10-08 | 미확인(제품 도움말, 요약만) |

읽기 실패(출처로 쓰지 않음): Shopify Polaris data-table·index-table(shopify.dev로 301 후 404, GitHub README도 404) · Salesforce Lightning data-tables(JS 렌더, 본문 없음; HXL 문서는 403) · NN/g `table-design` 404 · Adobe `spectrum.adobe.com/page/table` 404 · Microsoft Fluent 2 datagrid·table 404 · Material 3(시도 안 함).
