# 목록+지도·목록+상세 (List + Map / Master-Detail)

> 언제 읽나: 검색 결과를 목록과 지도(또는 상세 패널)로 나란히 보여주는 화면 — 부동산·숙소·매장 찾기·후보지 탐색·메일함형 목록을 만들 때.
> 확인일 2026-10-08. 출처는 맨 아래. 수치 옆 [S1] 같은 표시는 출처 번호, 표시 없는 수치는 "권장(근거 약함)".

핵심 전제: 이 화면의 주인공은 **지도(또는 상세)** 이다. 헤더·필터·광고·설명 띠는 전부 조연이며 조연이 주인공을 밀어내면 실패다.

## 1. 데스크톱 분할 비율 (목록 : 지도)

**언제 쓰나** — 결과가 "어디에 있나"가 핵심 판단 축일 때(부동산·숙소·점포). 위치가 무관한 목록(주문 내역 등)은 지도 없이 표나 목록+상세(4절)로 간다.

**규칙(측정 가능)**
- 분할은 창 너비 641px 이상부터, 그 미만은 한 번에 한 패널만(스택) [S7].
- 지도 폭은 창 너비의 **최소 40%**, 기본 50~60%. 목록은 카드 2열이 들어가는 폭(≈ 560~720px)을 넘기지 않는다 (권장, 근거 약함).
- 목록 기본 상태는 "지도 옆에 열림". 지도를 기본으로 숨기면 사용자의 65%가 지도를 끝까지 안 쓴다 [S2]. 지도를 기본으로 보여준 사이트는 95%가 지도로 탐색했다 [S2].
- 필터는 **상단 가로 1줄 바**. 세로 필터 사이드바는 목록 폭을 깎아 "페이지가 작아진다"는 불만을 낳았다 [S2].
- 지도 옆 세로 광고·배너 금지 — 22% 사용자에게 가격 정보를 가리는 표시 버그를 냈다 [S2].
- 지도는 `position: sticky; top: <헤더높이>`로 고정, 목록만 스크롤. 지도 높이 = `100dvh − 헤더 − 필터바` (권장, 근거 약함).
- 지도 이동 후 목록·줌 상태는 유지한다 — 목록으로 돌아갔을 때 줌이 풀리면 75%가 기대와 다르다고 느꼈다 [S2].
- 지도 위에 띄우는 "분할 뷰 오버레이"(별도 레이어로 뜨는 분할 화면) 금지 — 사용자가 검색 페이지로 착각하고 정렬 기능을 못 찾았다 [S2].

**Do**
- 목록 카드 1장 = 썸네일 + 가격 + 핵심 수치 2~3개 + 판정 배지 1개. 설명 문장은 상세에서만.
- 지도 이동 시 "이 지역에서 다시 검색" 버튼 또는 자동 갱신 토글(기본 켜짐) 하나를 지도 상단 중앙에 둔다.
- 결과 수("N건")는 목록 머리 1줄에, 정렬 드롭다운과 같은 줄.

**Don't**
- 지도 위를 큰 안내 문구·큰 아이콘으로 덮지 않는다 — "아이콘·글씨가 너무 커서 지도가 안 보인다"가 실제 지적이다. 구석의 작은 칩/카드로(2절).
- 설명·범례·통계 띠를 지도 위에 올리지 않는다. "중요한 화면(지도)이 덜 중요한 띠 때문에 밑으로 밀린다"를 막는다(6절).
- 목록을 3열 이상 그리드로 넓혀 지도를 40% 아래로 밀지 않는다.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Airbnb 검색 결과 | https://www.airbnb.com/s/Seoul/homes | 목록 카드 구성(사진·가격·평점·배지), 좌측 필터, "Show map" 토글 [S14] |
| Baymard 숙소 split view 연구 | https://baymard.com/research-articles/accommodations-split-view | 지도 기본 노출·가로 필터바·오버레이 금지 근거 [S2] |
| Zillow 검색 | https://www.zillow.com/homes/ | 미확인(WebFetch 403, 직접 관찰 필요) — 좌 지도 / 우 목록, 하단 Draw 도구 |
| 네이버부동산 | https://new.land.naver.com | 미확인(호스트 차단, 직접 관찰 필요) — 좌 목록 패널 / 우 지도, 단지 가격 마커 |

## 2. 지도 위 오버레이 — 구석의 작은 칩/카드

**언제 쓰나** — 지도 위에 상태·범례·선택 항목 요약·컨트롤을 올릴 때.

**규칙(측정 가능)**
- 오버레이는 네 구석(top-left / top-right / bottom-left / bottom-right)에만 둔다. 지도 API의 컨트롤 슬롯도 그 12자리 체계다 [S3].
- 구석 카드 1장 폭 ≤ 지도 폭의 30%, 높이 ≤ 지도 높이의 25%. 넘치면 접힘 상태를 기본으로 (권장, 근거 약함).
- 칩 높이 28~32px, 글자 12~13px, 아이콘 16px. 지도 위에서 제목(H1·H2) 크기 글자 금지 (권장, 근거 약함).
- 팝업(핀 클릭 시)은 기본 최대 폭 240px [S13]. 그 안에 사진 1·가격·수치 2개·"상세 보기" 링크까지만.
- 범례는 좌하단, 기본 접힘(아이콘 1개). 펼쳐도 지도 높이의 25% 이내.
- 선택된 항목 요약 카드는 하단 중앙(모바일) 또는 우하단(데스크톱), 지도 높이의 25% 이내.
- 중앙 영역(지도 가로·세로 가운데 50%)에는 로딩 스피너 외에 아무것도 올리지 않는다 (권장, 근거 약함).

**Do**
- 오버레이 배경은 불투명(흰/다크 카드 + 그림자 1단) — 반투명은 지도와 겹쳐 대비가 떨어진다 [S11].
- 상태 메시지("이 지역 매물 없음")는 상단 중앙 칩 1줄.
- 핀 호버/클릭 요약은 팝업 1개만, 새 핀을 누르면 이전 팝업은 닫는다.

**Don't**
- 지도 위에 설명 문장 블록·통계 박스·큰 로고를 두지 않는다 — "구석에 작은 카드 태그로"가 실제 요구다.
- 오버레이가 핀을 가리면 안 된다. 카드가 핀을 덮으면 지도 패딩(`fitBounds padding`)으로 핀을 비켜 놓는다.
- 구석 4곳 모두 채우지 않는다. 최대 3곳, 한 곳은 비워 둔다.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Google Maps JS 컨트롤 | https://developers.google.com/maps/documentation/javascript/controls | 기본 컨트롤 자리(맵타입 좌상, 스트리트뷰·회전 우하), ControlPosition 12자리 [S3] |
| Mapbox GL JS Popup | https://docs.mapbox.com/mapbox-gl-js/api/markers/ | 팝업 maxWidth 240px, 마커 27×41px [S13] |

## 3. 지도 핀 라벨(가격 칩)·클러스터링

**언제 쓰나** — 핀마다 가격·점수 같은 한 값을 보여줘야 하고, 결과가 수십~수천 개일 때.

**규칙(측정 가능)**
- 가격 칩 = 타원/알약 모양, 글자 12~13px, 높이 24~28px. Airbnb는 "oval pins on a map showing the listing price"를 쓴다 [S1].
- 한 화면에 가격 칩은 **상위 N개만**(데스크톱 18개 수준) [S1]. 나머지는 값 없는 작은 점(mini-pin)으로 — 가격 없는 미니핀은 클릭률이 약 1/8이지만, 핀 수를 줄인 것이 Airbnb 역사상 최대 예약 개선 중 하나였다 [S1].
- 미니핀 지름 8~10px, 가격 칩과 색만 같고 글자 없음 (권장, 근거 약함).
- 클러스터링은 반경 50px, 줌 14 이상에서 해제가 라이브러리 기본값 [S4]. 클러스터 원 지름은 개수 단계별 20 / 30 / 40px, 숫자 12px [S4].
- 클러스터 숫자는 포함 개수를 표시하고, 확대하면 줄어들며 풀린다 [S5]. 큰 수는 5 또는 10 단위로 반올림해도 된다 [S6].
- 클러스터 호버 시 범위·개수·가격 구간을 툴팁으로 [S6]. 클릭 시 확대해 분해 [S5][S6].
- 대량 결과는 페이지네이션 대신 클러스터링 — 페이지로 나누면 "다 보고 있다"고 착각한다 [S12].
- 선택·호버 핀은 색 반전 + `z-index` 최상위, 크기는 키우지 않는다(주변 핀을 가림) (권장, 근거 약함).

**Do**
- 가격 단위는 짧게(`4.2억`, `$1.2M`). 칩 폭은 최대 7자.
- 같은 좌표에 핀이 겹치면 1개 칩 + "+N"로 합친다.
- 핀 색은 데이터 뜻 색 하나(판정 등급) 또는 단색 하나. 핀 종류가 3색을 넘으면 범례가 필요해져 오버레이가 는다.

**Don't**
- 모든 결과에 가격 칩을 달지 않는다 — 200개가 넘으면 칩이 서로 가려 지도가 안 보인다 [S1].
- 핀 안에 두 줄(가격 + 면적)을 넣지 않는다. 두 번째 값은 호버 팝업으로.
- "지도를 확대하세요" 에러로 막지 않는다 — Redfin에서 가장 흔한 반응은 이탈이었다 [S6].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Airbnb 엔지니어링 | https://airbnb.tech/?p=683 | 가격 타원 핀 vs 미니핀, 핀 수 제한의 효과 [S1] |
| Redfin 클러스터링 글 | https://www.redfin.com/news/cluster_buck_rogers/ | 개수 비례 클러스터, 호버 시 가격 범위 [S6] |
| Mapbox 클러스터 예제 | https://docs.mapbox.com/mapbox-gl-js/example/cluster/ | 반경·줌·원 크기 단계 [S4] |
| 직방 앱 | https://apps.apple.com/KR/app/id503098735 | "매매 가격, 평당가격, 시세 변동률"을 지도 위에서 보는 구성(앱 설명) [S15] |

## 4. 목록 ↔ 지도 ↔ 상세 연동

**언제 쓰나** — 목록과 지도가 같은 결과 집합을 보여줄 때(항상).

**규칙(측정 가능)**
- 목록 카드 호버 → 해당 핀 강조, 핀 호버 → 해당 카드 강조(테두리/배경 1단계). 지연 0ms, 전환 ≤ 150ms (권장, 근거 약함).
- 핀 클릭 → 목록을 그 카드로 스크롤(`scrollIntoView block:'nearest'`) + 팝업. 카드 클릭 → 상세(5절).
- 지도 이동(드래그·줌) → 목록 재조회. 자동 갱신 토글은 기본 켜짐, 끈 상태에서는 "이 지역 다시 검색" 버튼 노출 (권장, 근거 약함).
- 선택 항목은 목록·지도·상세 세 곳에서 같은 강조색. "selected"는 hover와 구분되는 시각이어야 한다 [S8].
- 상세로 갔다가 돌아오면 목록 스크롤 위치·지도 줌·필터가 그대로 [S2][S8].
- 키보드: 목록에서 위/아래(또는 j/k)로 이동, Enter로 상세 [S8].

**Do**
- 목록 정렬 기준(가격·점수·최신)을 지도 핀 표시 우선순위에도 똑같이 쓴다(상위 N개 가격 칩).
- 결과 0건이면 지도는 그대로 두고 목록 영역에 1줄 안내 + "필터 완화" 버튼.

**Don't**
- 지도 이동마다 목록을 맨 위로 튕기지 않는다.
- 핀 클릭이 즉시 새 페이지로 가면 안 된다. 먼저 팝업/카드 요약, 두 번째 클릭에 상세.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| SaaS list-detail 가이드 | https://www.saasui.design/blog/saas-list-detail-master-detail-ux-patterns | 선택 상태·키보드·복귀 시 스크롤 유지 [S8] |
| Microsoft List/details | https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/list-details | 선택 시각 + 상세 갱신 모델 [S7] |

## 5. 상세는 드로어 / 패널 / 새 페이지 중 무엇

**언제 쓰나** — 카드 클릭 뒤 "더 보기"를 어디에 열지 정할 때.

**규칙(측정 가능)**
| 조건 | 선택 | 근거 |
|---|---|---|
| 상세가 짧고(스크롤 1화면 이내) 목록과 왔다갔다 반복 | **고정 패널**(목록 옆 3번째 열) | [S8] 컬렉션을 반복 오가는 작업은 list-detail |
| 상세가 길거나 폼이 있고, 지도·목록 맥락은 유지 | **우측 드로어**(overlay) 기본 폭 378px, 큰 것은 736px [S9] | [S9] |
| 드로어가 지도를 가리면 안 됨(데스크톱 넓음) | **push 드로어**(본문을 밀어냄), 좁아지면 자동 overlay로 [S10] | [S10] |
| 상세가 독립된 목적지(공유 URL·인쇄·탭 10개) | **새 페이지**, 뒤로가기로 목록·스크롤·줌 복원 [S8] | [S8] |
| 잠깐 확인하고 닫는 짧은 내용 | 팝업/모달 | [S8] |

- 드로어 폭은 창 너비의 1/3~40% 이내(지도가 40% 아래로 안 가게). 378px 기본, 736px은 폼·표가 있을 때만 [S9].
- 드로어는 ESC·바깥 클릭·X 버튼 세 가지로 닫힌다 [S9]. 헤더·푸터는 고정, 본문만 스크롤 [S10].
- 중첩 드로어는 1단계까지, 뒤 드로어는 180px 밀림 [S9]. 2단계 이상이면 새 페이지로.
- 모바일(≤640px)에서는 드로어·패널 대신 전체 화면 스택 + 뒤로가기 [S7][S8].

**Do**
- 상세 첫 화면(접힘 상태) = 결론 1줄 + 핵심 수치 4~6개 + 판정 배지. 설명 문장은 "자세히" 접기 안에 — "설명 문장은 궁금해서 클릭했을 때만 보이면 좋겠다"가 실제 요구다.
- 드로어 URL을 `?id=`로 동기화해 새로고침·공유가 되게 한다.

**Don't**
- 상세를 모달(가운데 창)로 열어 지도·목록을 가리지 않는다 — 맥락 유지가 이 패턴의 존재 이유다.
- 드로어 안에 또 탭 6개를 두지 않는다. 3개 넘으면 새 페이지.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Ant Design Drawer | https://ant.design/components/drawer | 기본 378px / large 736px, 중첩 push 180px [S9] |
| Elastic EUI Flyout | https://eui.elastic.co/docs/components/containers/flyout/ | push vs overlay, 좁은 창에서 overlay 전환 [S10] |

## 6. 지도 위 컨트롤 위치·모바일 토글·상단 띠 상한

**언제 쓰나** — 지도 컨트롤 배치, 폰에서 목록/지도 전환, 헤더·필터바 높이를 정할 때.

**규칙(측정 가능)**
- 컨트롤 자리: 줌(+/−) **우상단**(또는 우하단), 전체화면 우상단, 지도타입 좌상단, 스트리트뷰·회전 우하단이 Google 기본 [S3]. 좌상단은 검색·필터 칩 자리로 비워 둔다.
- 컨트롤 버튼 1개 = 40×40px(데스크톱) / 44×44 이상(터치). 세로로 묶어 한 그룹, 그룹 간 8px.
- 헤더 높이 ≤ 56px, 필터 바 **1줄 ≤ 48px**, 합계 ≤ 104px. 1920×1080에서 지도 높이 ≥ 900px가 남아야 한다 (권장, 근거 약함). 고정 헤더는 "텍스트가 읽히는 최소 높이"로 줄이고 로고 때문에 키우지 않는다 [S11].
- 콘텐츠:크롬 비율 — 폰에서 13:1은 양호, 2:1은 실패 사례 [S11]. 지도 화면에서는 지도 높이 ≥ 화면의 75%를 목표로.
- 필터가 1줄을 넘치면 "필터 N" 버튼 하나로 접고 시트/드로어에서 펼친다. 2줄 필터 바 금지.
- 모바일(≤640px): 지도 전체 화면 + 하단 중앙 **"목록 N건" 플로팅 버튼**(높이 40~44px) ↔ 목록 화면 하단 중앙 "지도" 버튼. 또는 바텀시트(모바일 적응 파일 참조). 두 패널 동시 표시 금지 [S7].
- 지도 하단 24px는 저작권·로고 영역이므로 오버레이를 올리지 않는다 [S3].

**Do**
- 상단 띠는 스크롤 시 숨기고 위로 스크롤할 때만 다시 보이기(300~400ms) [S11] — 단, 지도 화면은 스크롤이 없으므로 처음부터 얇게.
- 현재 위치·내 위치 버튼은 줌 그룹 아래에 같은 열.

**Don't**
- 지도 위 좌상단에 큰 제목·설명 블록을 두지 않는다.
- 폰에서 지도 위에 헤더+필터+탭+안내 띠 4단을 쌓지 않는다. 지도 화면 상단 띠는 최대 2단(헤더 1 + 칩 1줄).
- 애니메이션이 있는 헤더·컨트롤은 피한다 — 가능하면 "애니메이션을 전혀 쓰지 않는 것이 최선" [S11].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Google Maps JS 컨트롤 | https://developers.google.com/maps/documentation/javascript/controls | 기본 컨트롤 위치 [S3] |
| NN/g Sticky Headers | https://www.nngroup.com/articles/sticky-headers/ | 헤더 높이 최소화, 콘텐츠:크롬 비율 [S11] |
| Google Developers Blog (지도 중심 UI) | https://developers.googleblog.com/en/how-to-make-maps-the-center-of-your-ui-and-how-not-to/ | 전체화면 지도에서 정보 삭감, 페이지네이션 vs 클러스터 [S12] |

## 출처
| # | 출처 | URL | 확인일 | 라이선스/비고 |
|---|---|---|---|---|
| S1 | Airbnb Tech Blog — Improving Search Ranking for Maps | https://airbnb.tech/?p=683 | 2026-10-08 | 저작권 유지(요약만) |
| S2 | Baymard — Accommodations Split View | https://baymard.com/research-articles/accommodations-split-view | 2026-10-08 | 저작권 유지(요약만) |
| S3 | Google Maps JS — Controls | https://developers.google.com/maps/documentation/javascript/controls | 2026-10-08 | CC-BY-4.0(Google 개발자 문서) |
| S4 | Mapbox GL JS — Cluster example | https://docs.mapbox.com/mapbox-gl-js/example/cluster/ | 2026-10-08 | 미확인 |
| S5 | Google Maps JS — Marker clustering | https://developers.google.com/maps/documentation/javascript/marker-clustering | 2026-10-08 | CC-BY-4.0(Google 개발자 문서) |
| S6 | Redfin News — Cluster Buck Rogers | https://www.redfin.com/news/cluster_buck_rogers/ | 2026-10-08 | 저작권 유지(요약만) |
| S7 | Microsoft Learn — List/details pattern | https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/list-details | 2026-10-08 | CC-BY-4.0(MS Docs) |
| S8 | saasui.design — List-detail / master-detail UX | https://www.saasui.design/blog/saas-list-detail-master-detail-ux-patterns | 2026-10-08 | 미확인 |
| S9 | Ant Design — Drawer | https://ant.design/components/drawer | 2026-10-08 | MIT |
| S10 | Elastic EUI — Flyout | https://eui.elastic.co/docs/components/containers/flyout/ | 2026-10-08 | Elastic License / SSPL(문서 요약만) |
| S11 | NN/g — Sticky Headers | https://www.nngroup.com/articles/sticky-headers/ | 2026-10-08 | 저작권 유지(요약만) |
| S12 | Google Developers Blog — Maps as the Center of Your UI | https://developers.googleblog.com/en/how-to-make-maps-the-center-of-your-ui-and-how-not-to/ | 2026-10-08 | 미확인 |
| S13 | Mapbox GL JS API — Markers and controls | https://docs.mapbox.com/mapbox-gl-js/api/markers/ | 2026-10-08 | 미확인 |
| S14 | Airbnb 검색 결과(서울) — 공개 화면 | https://www.airbnb.com/s/Seoul/homes | 2026-10-08 | 관찰만(목록·필터·"Show map" 텍스트만 읽힘, 지도는 미렌더) |
| S15 | 직방 — App Store 설명 | https://apps.apple.com/KR/app/id503098735 | 2026-10-08 | 관찰만(앱 설명 텍스트) |
| — | 미확인(읽기 실패) | Zillow(403) · Redfin 검색·지원(403) · Booking.com(405) · 직방 웹(403) · 네이버부동산(호스트 차단) · NN/g split-screen·maps-ux(404) · Apple HIG Maps(JS 렌더) | 2026-10-08 | 직접 관찰 필요 |
