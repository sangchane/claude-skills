# 필터·검색·정렬 (Filter / Search / Sort)

> 언제 읽나: 목록·표·지도 위에 필터 바, 검색창, 정렬 드롭다운, 적용된 필터 칩, 0건 화면을 올릴 때.
> 확인일 2026-10-08. 출처는 맨 아래. 수치 옆 [S1] 같은 표시는 출처 번호, 표시 없는 수치는 "권장(근거 약함)".

색·그림자·서체·모노 숫자 같은 하드룰은 SKILL.md·tokens.md에 있다. 여기선 "무엇을 어디에 몇 개, 무엇을 숨기나"만 쓴다.

## 1. 필터 바 위치와 개수

**언제 쓰나** — 결과 목록에 2개 이상의 필터 축(가격·면적·유형…)을 붙일 때. 축이 하나뿐이면 필터 바가 아니라 토글/세그먼트 하나로 끝낸다.

**규칙(측정 가능)**
- 필터 축 6~8개 이하 → 상단 가로 1줄. 그보다 많으면 좌측 사이드바 [S9]. 사이드바가 더 흔하고 안전한 선택(가로 툴바는 전자상거래 사이트의 24%) [S9].
- 가로 1줄에 넣을 때는 자주 쓰는 2~3개만 바에 노출(promoted)하고 나머지는 "필터" 버튼 뒤 팝오버·패널로 [S14][S15].
- 여러 카테고리의 필터는 절대 드롭다운 하나 안에 몰아넣지 않는다 [S7].
- 접힌 필터 버튼에는 적용된 필터 개수를 배지로 표시한다 [S7][S16][S17]. 배지만 보이고 내용이 안 보이는 상태로 두지 않는다(아래 2절 칩).
- 공개 사례의 가로 바 구성: Google Flights = Stops·Airlines·Times·More 버튼 4개 + Sort by [S21]; Airbnb = 상단 "Filters" 버튼 1개 → 시트 안에 추천 필터 1줄 + 전체 목록 [S22].
- 각 필터의 초기 상태는 "모두 미선택" 또는 "모두 선택" 중 하나로 고정하고 섞지 않는다 [S7].
- 단일 선택(라디오 성격)과 다중 선택(체크 성격)을 컨트롤 모양으로 구분한다 [S7].
- 필터 바 높이는 1줄(약 40~48px)로 제한하고, 2줄로 늘어나면 접기 버튼으로 넘긴다 (권장, 근거 약함).

**Do**
- 바에 노출할 2~3개는 로그·사용자 질문에서 "가장 자주 쓰는 축"으로 고른다 [S14].
- 필터 값 목록이 길면 팝오버 안에 검색 가능한 리스트를 넣는다 [S17].
- 지도·표가 주인공인 화면에서는 필터 바를 얇은 1줄로, 결과(지도)를 첫 화면 위쪽에 둔다.

**Don't**
- 중요한 화면(지도)이 필터 띠 2~3줄 때문에 아래로 밀리게 하지 않는다 — 사용자 지적 "중요한 화면이 덜 중요한 띠 때문에 밑으로 밀린다".
- "모든 필터 보기" 버튼에 핵심 필터를 숨기지 않는다 — 테스트 참가자가 그 버튼을 못 보거나 늦게 봤다 [S9].
- 필터 라벨을 아이콘만으로 쓰지 않는다. "필터"·"조건" 같은 실제 단어를 쓴다 [S3].
- 사이드바형을 상단 가로형으로 바꾸면서 축 수를 그대로 두지 않는다(8개 넘으면 넘침) [S9].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Google Flights | https://support.google.com/travel/answer/2475306 | 상단 버튼 4개(Stops·Airlines·Times·More) + Sort by, 기본 정렬 "Top flights" |
| Airbnb | https://www.airbnb.com/help/article/479 | "Filters" 버튼 1개 → 시트, 시트 상단에 추천 필터 1줄 |
| IBM Carbon 필터 패턴 | https://carbondesignsystem.com/patterns/filtering/ | 수직(좌측)/수평(상단) 배치, 접힌 필터의 개수 배지 |
| Amazon 검색 결과 | https://www.amazon.com (좌측 패싯) | 좌측 사이드바 패싯 — 미확인(WebFetch 503, 공개 페이지 직접 관찰 필요) |

## 2. 적용 방식·적용된 필터 칩·결과 건수

**언제 쓰나** — 필터를 하나라도 켤 수 있는 모든 목록. 칩과 건수는 "지금 무엇이 걸려 있고 몇 개가 남았나"를 한 줄로 답한다.

**규칙(측정 가능)**
- 즉시 적용(선택할 때마다 갱신)은 응답이 1초 미만일 때만 [S1]. 느린 데이터·다중 카테고리 조합·모바일은 "적용" 버튼의 배치 필터 [S1][S7].
- 배치 필터라도 1~2초 입력이 없으면 자동 갱신해도 된다. 갱신 중에는 결과 영역을 흐리게 하고 진행 표시 [S1].
- 갱신 시 스크롤 위치를 유지한다. 결과가 거의 없거나 0건일 때만 맨 위로 [S1].
- 적용된 필터는 제거 가능한 칩(x 버튼)으로 보여 주고, 옆에 "모두 지우기" 1개 [S7][S10][S14]. 개수만 보여 주는 것은 금지 [S10].
- 칩 위치(데스크톱): 결과 목록 바로 위 > 사이드바 위 > 가로 바 바로 아래 순으로 권장 [S10][S15]. 모바일은 가로 스크롤 1줄(잘린 칩을 반쯤 보여 스크롤 가능함을 알림) [S10].
- 같은 카테고리의 칩은 붙여서 배치. 라벨이 모호하면 축 이름을 붙인다("높음" → "위험도 높음", "폭: 90cm") [S10][S14].
- 결과 건수는 항상 보이게 — 모바일 필터 시트에서도 헤더에 고정 [S3].
- 칩은 별도 상태가 아니라 현재 쿼리(URL 파라미터)에서 파생해 그린다 [S15][S16].
- "모두 지우기"는 필터 파라미터·페이지 커서·선택된 행 ID를 함께 초기화한다 [S15].

**Do**
- 필터 변경 시 페이지네이션을 1페이지로 되돌린다 [S15][S16].
- 느린 요청은 AbortController로 취소해 옛 결과가 새 결과를 덮지 않게 한다 [S15][S16].
- 모바일에서는 "적용" 버튼 라벨에 건수를 넣는다("결과 128건 보기") (권장, 근거 약함).

**Don't**
- 칩 없이 필터 패널을 다시 열어야만 무엇이 걸려 있는지 알 수 있게 하지 않는다 [S10].
- 결과 건수를 목록 아래에만 두지 않는다 — 필터 바 옆 또는 시트 헤더에 [S3].
- 즉시 적용 + 1초 넘는 응답 조합으로 화면이 깜빡이게 하지 않는다 [S1].
- 칩 줄이 지도 위에 2줄 이상 쌓이게 하지 않는다 — 사용자 지적 "아이콘·글씨가 커서 지도가 안 보인다".

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Shopify Polaris Filters | https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/filters.md | 칩을 쿼리에서 파생, 250ms 디바운스, clear-all이 커서·선택도 초기화 |
| Shopify Index filters | https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/index-filters.md | 검색·필터·정렬·저장된 뷰 한 줄, 활성 필터 개수 버튼 |
| Elastic EUI FilterGroup | https://eui.elastic.co/docs/components/forms/search-and-filter/filter-group/ | 버튼 안 활성 개수 배지, 긴 목록은 팝오버+검색 |

## 3. 범위 입력 (가격·면적·연식)

**언제 쓰나** — 숫자 축을 "이상/이하"로 자를 때.

**규칙(측정 가능)**
- 정확한 값이 중요한 축(가격·면적·나이)은 슬라이더 단독 금지. 최소·최대 입력칸 2개가 기본 [S6].
- 슬라이더를 쓰면 반드시 값 표시를 슬라이더 위·옆에(아래는 손가락에 가림) 두고, 편집 가능한 숫자칸과 같이 둔다 [S6].
- 터치 화면에서는 슬라이더 대신 탭·입력 컨트롤을 우선한다 [S6].
- 최소·최대 칸은 숫자 전용(`inputmode="numeric"`)이고 단위는 접미사(만원·㎡)로 칸 밖에 [S19 참고: 숫자 입력 규칙은 forms.md 4절].
- 흔한 구간(예: ~3억·3~5억·5~7억)은 프리셋 버튼 3~5개로 먼저 주고, 세부는 입력칸 (권장, 근거 약함).
- 최소 > 최대로 입력하면 두 값을 바꿔 적용하거나 즉시 에러 1줄 (권장, 근거 약함).

**Do**
- 범위 칩 라벨은 "가격 3~5억"처럼 축 이름 + 값 [S10].
- 입력칸 폭은 예상 자릿수에 맞춘다(forms.md 1절).

**Don't**
- 슬라이더 두 손잡이만 주고 숫자를 못 치게 하지 않는다 [S6].
- 범위 축을 값 목록 체크박스 20개로 펼치지 않는다 — 텍스트 나열 지적.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Airbnb 가격 필터 | https://www.airbnb.com/help/article/479 | 총액 기준 범위 필터(세금 제외) — UI 세부는 로그인 없이 공개 화면에서 관찰 |
| NN/g 슬라이더 | https://www.nngroup.com/articles/gui-slider-controls/ | 슬라이더를 쓰면 안 되는 경우와 라벨 위치 |

## 4. 정렬

**언제 쓰나** — 결과가 한 화면(약 10~20건)을 넘을 때. 그 이하면 정렬 컨트롤을 생략한다 (권장, 근거 약함).

**규칙(측정 가능)**
- 정렬 드롭다운은 결과 목록 머리의 오른쪽 끝, 결과 건수와 같은 줄에 1개 [S16][S21](Google Flights "Sort by" 버튼 위치).
- 기본 정렬은 "추천/관련도"형으로 하되, 첫 20건(모바일 10건)에 주요 유형이 고루 섞이게 한다. 전체의 10% 넘는 유형은 첫 20건 안에 반드시 포함 [S12].
- 가격순·가나다순을 기본값으로 쓰지 않는다 — 품목 범위를 좁게 오해하게 만든다 [S12].
- 정렬 옵션은 5~15개 드롭다운 범위 안에서 [S20], 실무상 4~6개 (권장, 근거 약함). 필수 후보: 가격·평점·인기·최신(전자상거래 기준) [S12 검색 결과 기준, 본문은 default-sort만 확인].
- 정렬을 바꾸면 페이지네이션을 1페이지로 [S16].
- 현재 정렬 기준이 버튼 라벨에 보여야 한다("정렬: 가격 낮은순") (권장, 근거 약함).

**Do**
- 정렬 옵션 라벨에 방향을 쓴다("가격 낮은순" / "가격 높은순") (권장, 근거 약함).
- 표라면 열 머리 클릭 정렬과 드롭다운 중 하나만 둔다 (권장, 근거 약함).

**Don't**
- 정렬 컨트롤을 필터 패널 안에 숨기지 않는다 — 정렬은 필터와 다른 동작 [S16].
- "관련도"를 라벨만 바꾸고 실제로는 가격순으로 두지 않는다 [S12].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Google Flights | https://support.google.com/travel/answer/2475306 | 기본 "Top flights"(가격+편의 절충), Price·Duration·Departure time 옵션 |
| Baymard 기본 정렬 | https://baymard.com/blog/default-sort-type | 첫 20건 다양성 규칙 |

## 5. 검색 입력과 자동완성

**언제 쓰나** — 필터로 좁히기 어려운 자유 텍스트(주소·단지명·키워드)가 있을 때.

**규칙(측정 가능)**
- 검색창 너비는 최소 27자 [S19], 전형적 질의가 스크롤 없이 들어가야 한다 [S5]. 페이지 상단 우측(또는 좌측)에 [S5].
- 라벨은 보이지 않아도 반드시 둔다. 버튼에는 "검색" 단어를 넣고 submit 버튼으로 [S19].
- 지우기(x) 버튼은 입력이 있을 때만 보인다 [S8][S18]. Enter 제출, Esc 지우기 [S8].
- 제안 개수: 데스크톱 최대 10개, 모바일 4~8개 [S11]. 제안 목록에 스크롤바를 만들지 않는다 [S11].
- 포커스 시 최근 검색을 먼저 보여 주고, 입력이 시작되면 제안으로 교체 [S18]. 최근 검색도 10개 상한 (권장, 근거 약함).
- 입력 중 요청은 250ms 디바운스 [S15]. 키보드 위·아래·Enter 지원, 활성 항목은 배경색으로 강조 [S11].
- 제안 텍스트는 사용자가 친 부분과 아직 안 친 부분을 구분해 강조(굵게/색) [S4][S11]. 카테고리 범위 제안("in 송파구")은 들여쓰기·이탤릭으로 구분 [S4][S11].
- 플레이스홀더는 "무엇을 검색할 수 있나"를 짧게("동·단지명·주소") [S8][S14]. "여기에 입력" 같은 문구 금지 [S14].
- 좁은 화면에서는 돋보기 아이콘 1개로 접고, 누르면 전체 폭 검색창으로 [S18].

**Do**
- 제안마다 실제 결과가 있는 질의만 제안한다(제안 채택률은 23%에 불과) [S4].
- 제안이 10개를 넘으면 잘라낸다 — 선택 마비 [S11].

**Don't**
- 제안 목록에 광고·배너·채팅 아이콘이 겹치게 두지 않는다 [S11].
- 검색을 링크로 두지 않는다(검색창을 보이게 바꾸자 사용 91% 증가) [S5].
- 검색창 하나에 필터 문법("가격<5억")을 요구하지 않는다 — 필터는 필터 바로.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| USWDS Search | https://designsystem.digital.gov/components/search/ | 27자 최소 폭, 버튼 "Search", Big/Small 변형 |
| Fluent 2 SearchBox | https://fluent2.microsoft.design/components/web/react/core/searchbox/usage | 포커스 시 최근 → 입력 시 제안, 좁은 화면 아이콘 접기 |
| Carbon Search | https://carbondesignsystem.com/components/search/usage/ | 크기 4단(24/32/40/48px), 지우기 버튼 조건 |

## 6. 0건 처리·URL 상태·모바일 시트

**언제 쓰나** — 필터·검색이 있는 모든 화면의 마무리. 세 가지 중 하나라도 빠지면 사용자가 되돌아갈 길이 없다.

**규칙(측정 가능)**
- 0건 화면은 (1) 적용된 필터 칩을 그대로 보여 주고 (2) "모두 지우기" (3) 필터 하나씩 완화한 대안 질의 1~3개(키워드 제거 순열) (4) 더 넓은 카테고리 링크를 둔다 [S13][S10]. 막다른 길로 두지 않는다 [S13].
- 입력한 검색어는 0건이어도 검색창에 유지한다 (권장, 근거 약함; GOV.UK 폼 "입력 보존" 원칙 준용).
- 필터·검색어·정렬·페이지 커서·선택된 뷰 ID는 URL 파라미터가 단일 원본 [S15][S16]. 새로고침·뒤로가기·공유 링크에서 같은 화면이 복원돼야 한다.
- 파라미터 키 하나는 항상 같은 뜻 — 재사용 금지 (권장, 근거 약함).
- 모바일: 필터 버튼 1개(라벨 "필터", 적용 수 배지) → 결과 위에 겹치는 시트/패널. 배경 결과는 반투명 아래로 계속 보이고, 결과 건수는 시트 헤더에 고정 [S3].
- 시트는 오른쪽 가장자리에서 열어 왼쪽의 결과(사진·지도)가 보이게 [S3]. 하단 시트를 쓰면 지도의 윗부분이 남게 높이를 화면의 60% 이하로 (권장, 근거 약함).
- 모바일은 배치 적용(적용 버튼)이 기본 [S1].

**Do**
- 0건이면 결과 영역 맨 위로 스크롤한다 [S1].
- 에러(요청 실패) 시 선택한 컨트롤은 그대로 두고 "다시 시도"를 준다 [S16].

**Don't**
- 0건에 "결과가 없습니다" 한 줄만 두지 않는다 [S13].
- 필터 상태를 메모리(스토어)에만 두어 새로고침에 날아가게 하지 않는다 [S15].
- 모바일 시트가 결과·지도를 완전히 덮게 하지 않는다 [S3].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| NN/g 모바일 패싯 | https://www.nngroup.com/articles/mobile-faceted-search/ | 오버레이 트레이, 헤더 고정 건수, 배경 결과 유지 |
| Baymard 0건 | https://baymard.com/blog/no-results-page | 대안 검색·상위 카테고리·인기 상품 |
| Shopify Index filters | https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/index-filters.md | URL이 단일 원본, 뷰 ID 복원 |

## 출처
| # | 출처 | URL | 확인일 | 라이선스/비고 |
|---|---|---|---|---|
| S1 | NN/g, Applying Filters: Interactive vs. Batch | https://www.nngroup.com/articles/applying-filters/ | 2026-10-08 | 저작권 유지, 요약만 |
| S2 | NN/g, Filters vs. Facets | https://www.nngroup.com/articles/filters-vs-facets/ | 2026-10-08 | 저작권 유지, 요약만(수치 없음, 정의만) |
| S3 | NN/g, Mobile Faceted Search | https://www.nngroup.com/articles/mobile-faceted-search/ | 2026-10-08 | 저작권 유지, 요약만 |
| S4 | NN/g, Site Search Suggestions | https://www.nngroup.com/articles/site-search-suggestions/ | 2026-10-08 | 저작권 유지, 요약만 |
| S5 | NN/g, Search: Visible and Simple | https://www.nngroup.com/articles/search-visible-and-simple/ | 2026-10-08 | 저작권 유지, 요약만 |
| S6 | NN/g, Slider Design | https://www.nngroup.com/articles/gui-slider-controls/ | 2026-10-08 | 저작권 유지, 요약만 |
| S7 | IBM Carbon, Filtering pattern | https://carbondesignsystem.com/patterns/filtering/ | 2026-10-08 | Apache-2.0(Carbon) |
| S8 | IBM Carbon, Search usage | https://carbondesignsystem.com/components/search/usage/ | 2026-10-08 | Apache-2.0(Carbon) |
| S9 | Baymard, Horizontal Filtering Toolbar | https://baymard.com/blog/horizontal-filtering-sorting-design | 2026-10-08 | 저작권 유지, 요약만 |
| S10 | Baymard, Applied Filters | https://baymard.com/blog/how-to-design-applied-filters | 2026-10-08 | 저작권 유지, 요약만 |
| S11 | Baymard, Autocomplete Design | https://baymard.com/blog/autocomplete-design | 2026-10-08 | 저작권 유지, 요약만 |
| S12 | Baymard, Default Sort Type | https://baymard.com/blog/default-sort-type | 2026-10-08 | 저작권 유지, 요약만 |
| S13 | Baymard, No Results Page | https://baymard.com/blog/no-results-page | 2026-10-08 | 저작권 유지, 요약만 |
| S14 | Shopify Polaris Filters README(폴라리스 패키지 문서 사본) | https://cdn.jsdelivr.net/npm/superv5_polarisui@2.0.1/dist/docs/components/Filters/README.md | 2026-10-08 | 미확인(polaris.shopify.com은 shopify.dev 허브로 리다이렉트) |
| S15 | Shopify dev, Filters 마이그레이션 가이드 | https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/filters.md | 2026-10-08 | 미확인 |
| S16 | Shopify dev, Index filters 마이그레이션 가이드 | https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/index-filters.md | 2026-10-08 | 미확인 |
| S17 | Elastic EUI, Filter group | https://eui.elastic.co/docs/components/forms/search-and-filter/filter-group/ | 2026-10-08 | 미확인 |
| S18 | Microsoft Fluent 2, SearchBox usage | https://fluent2.microsoft.design/components/web/react/core/searchbox/usage | 2026-10-08 | 미확인 |
| S19 | USWDS, Search | https://designsystem.digital.gov/components/search/ | 2026-10-08 | 퍼블릭도메인/CC0(USWDS 문서) |
| S20 | Atlassian, Dropdown menu usage | https://atlassian.design/components/dropdown-menu/usage | 2026-10-08 | 미확인 |
| S21 | Google Flights 도움말 | https://support.google.com/travel/answer/2475306 | 2026-10-08 | 저작권 유지, 요약만 |
| S22 | Airbnb 도움말, 검색 필터 사용 | https://www.airbnb.com/help/article/479 | 2026-10-08 | 저작권 유지, 요약만 |

읽기 실패(출처에서 제외): NN/g search-results-sorting(404), NN/g search-no-results(404), NN/g mobile-filters(404), Atlassian patterns/filtering(404), polaris.shopify.com Filters·Index filters(리다이렉트, 허브만), Adobe Spectrum search-field(404), Baymard truncate-filter-values·price-range-slider(본문 미제공), Zillow(403), Amazon 도움말(503).
