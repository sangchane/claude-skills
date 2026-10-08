# 점진적 공개 (Progressive Disclosure)

> 언제 읽나: 한 화면에 결론·값·상태와 그 설명·근거·정의가 같이 있어서 "무엇을 기본으로 보이고 무엇을 접을지"를 정해야 할 때(판정 카드, 지표 타일, 상세 패널, 지도 위 카드, 설정 화면).
> 확인일 2026-10-08. 출처는 맨 아래. 수치 옆 [S1] 같은 표시는 출처 번호, 표시 없는 수치는 "권장(근거 약함)".

공통 원칙(모든 항목에 적용)
- 공개 단계는 **최대 2단계**(기본 화면 → 1번 열기). 3단계부터는 사용자가 길을 잃으므로 구조를 단순화한다 [S1].
- 기본 화면에는 "자주 쓰는 소수의 핵심"만, 2단계에는 "드물게 쓰는 것"을 둔다. 자주 필요한 것을 숨기면 안 되고, 드문 것을 기본에 끼워도 안 된다 [S1].
- 무엇이 자주 쓰이는지는 추측이 아니라 사용 빈도(분석 로그·태스크 분석)로 정한다 [S1].
- 기본(0단계)에 보이는 것: 결론 한 줄, 값, 상태(충족/미달), 건수. 숨기는 것(1단계): 설명 문장, 계산 근거, 용어 정의, 출처. (권장, 근거 약함 — 아래 사용자 지적을 겨냥)
- 숨긴 내용으로 들어가는 아이콘(셰브론·말줄임·접기)은 항상 글자 라벨과 짝지어 쓴다 [S12].
- 열고 닫아도 사용자의 시선 기준점이 크게 이동하면 안 된다 [S12].

## 1. 접기 (Accordion / Details)

**언제 쓰나** — 한 페이지에서 사용자가 일부 섹션만 골라 읽는 경우, 또는 모바일처럼 공간이 좁은 경우 [S3][S5]. 모든 사용자가 읽어야 하는 내용에는 쓰지 않는다 [S14][S15].

**규칙(측정 가능)**
- 기본 상태는 **전부 접힘** — 사용자가 먼저 개요를 훑고 고른다 [S5][S14][S22]. 단, 첫 섹션만 기본 펼침은 허용(`aria-expanded="true"`) [S17].
- 한 번에 **여러 개** 펼칠 수 있게 한다 — 섹션 간 비교가 필요하기 때문 [S3][S5]. USWDS 기본은 단일 선택이며 다중 선택은 명시 옵션이다 [S17].
- 열고 닫은 상태는 사용자가 바꾸기 전까지 **유지**한다 [S3]. GOV.UK는 같은 세션 안에서 펼친 섹션을 자동 기억한다 [S15].
- 접힌 헤더에도 **값·건수·상태 뱃지**(예: "체크리스트 7/10 충족", "경고 2")가 보여야 한다. 헤더가 제목만이면 사용자가 열어봐야 알 수 있어 공개 단계가 하나 늘어난 셈이다. (권장, 근거 약함)
- 헤더 제목은 짧고 서술적으로, 제목 요소(h2~h6)로 마크업한다 [S5]. "자세히"·"여기를 클릭" 같은 무의미 라벨 금지 [S17].
- 헤더 전체가 클릭 영역이고 `<button>`이다 [S17]. 패널 안 버튼은 헤더에서 충분히 떨어뜨려 오동작을 막는다 [S17].
- 접기 안에 접기(중첩) 금지 [S15]. 깊은 트리 데이터는 접기가 아니라 트리 뷰 [S5].
- 접힌 내용이 1~2개뿐이고 덜 중요하면 아코디언 대신 **Details(단일 접기)** [S14][S15]. Details는 섹션 1개만 담는다 [S14].
- 펼쳐도 페이지가 "조금" 길어질 뿐이고 모두 관련 있는 내용이면 접지 말고 그냥 보여준다 — 스크롤이 클릭 결정보다 싸다 [S3].
- 전부 펼치면 페이지 로드가 느려질 양이면 접기 대신 페이지 분할 [S15].

**Do**
- 지표 카드: 헤더 = 지표명 + 값 + 충족/미달 색점, 패널 = 기준선·계산식·출처.
- "설명 문장은 궁금할 때만" — 설명·정의·근거는 패널에만 두고 헤더에는 결론만.
- 섹션 열림 상태를 URL이나 세션에 보존해 뒤로 가기 후에도 유지.
- 셰브론은 접힘=아래, 펼침=위로 일관 [S5][S22].

**Don't**
- 헤더에 제목만 쓰고 값은 안에 숨기기 — 사용자는 "숫자만 나열돼 뭐가 충족인지 안 보인다"고 지적한다.
- 설명 문장을 기본으로 펼쳐 두기 — "텍스트가 한 페이지에 너무 많다"는 지적의 원인.
- 모든 사용자가 봐야 할 경고·필수 안내를 접기 안에 넣기 [S14][S15].
- 접힌 섹션을 가로 스크롤 패널로 만들기(세로만) [S5].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| GOV.UK Design System Accordion | https://design-system.service.gov.uk/components/accordion/ | 전부 접힘 기본, 섹션별 요약 줄(summary line) 예시 |
| GOV.UK Details | https://design-system.service.gov.uk/components/details/ | 덜 중요한 내용 1개를 담는 단일 접기 |
| USWDS Accordion | https://designsystem.digital.gov/components/accordion/ | 단일/다중 선택 변형, 헤더 전체 클릭 |
| Carbon Accordion | https://carbondesignsystem.com/components/accordion/usage/ | 헤더 구성(제목·셰브론), 접힘 기본 |

## 2. 탭 (Tabs)

**언제 쓰나** — 내용이 명확한 그룹 몇 개로 나뉘고, 그룹끼리 동시에 비교할 필요가 없으며, 빠른 전환이 중요할 때 [S4][S16]. 순서대로 다 읽어야 하거나 비교가 필요하면 탭이 아니다 [S16].

**규칙(측정 가능)**
- 탭 줄은 **1줄만** — 2줄로 쌓이면 공간 기억이 깨진다 [S4]. 가로 탭은 줄바꿈하지 않고 스크롤한다 [S8].
- 라벨은 **1~2단어** [S4][S8]. 더 길어지면 탭이 잘못된 선택이라는 신호 [S4]. 전부 대문자 금지 [S4].
- 개수: 그리드 정렬 탭은 **4개 이하**, 넓은 화면의 라인 탭도 **최대 8개** [S8]. "적을수록 좋다" [S4].
- 항상 **1개가 선택**돼 있고 보통 첫 번째 [S8]. 첫 탭 = 가장 자주 쓰는 내용 [S4][S16].
- 선택 표시는 최소 **2가지 신호**(밑줄 + 굵기/색, 또는 패널과 같은 배경) [S4]. 비선택 탭도 읽혀야 한다 [S4].
- 탭 목록은 패널 **위**에, 선택 탭과 패널이 붙어 있어야 한다 [S4].
- 각 탭 패널은 같은 레이아웃에 다른 데이터여야 한다 [S4]. 탭 안에 탭 금지 [S8].
- 패널 시작에 탭 라벨과 같은 제목을 두고, URL 프래그먼트로 탭 상태를 남긴다 [S16].
- 섹션이 많으면 세로로 쌓이는 아코디언이 낫고, 여러 섹션을 동시에 봐야 해도 아코디언 [S15][S16].

**Do**
- 상세 화면: "판정 | 매물 | 구역 | 기록" 처럼 성격이 다른 묶음에만 탭.
- 모바일에서는 탭 내용을 순차 노출하거나 세그먼트 컨트롤로 — GOV.UK는 작은 화면에서 전부 순차 표시 [S16].

**Don't**
- 비교해야 할 두 값(예: 좋은 사례 vs 나쁜 사례)을 서로 다른 탭에 — 비교는 한 화면 나란히 [S16].
- 탭 라벨에 긴 문장·건수 설명 — 건수는 라벨 옆 짧은 숫자 뱃지까지만.
- 탭을 7~8개 넘겨 캐러셀이 되게 하기 [S4][S8].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| GOV.UK Tabs | https://design-system.service.gov.uk/components/tabs/ | 첫 탭 기본 선택, 패널 제목 반복, 모바일 순차 노출 |
| Carbon Tabs | https://carbondesignsystem.com/components/tabs/usage/ | 라인/컨테인드 변형, 개수 상한 |

## 3. 툴팁 (Tooltip)

**언제 쓰나** — 아이콘 전용 버튼의 이름, 잘린 텍스트의 전체 문자열, 단축키 같은 **보조 설명**에만 [S2][S9]. 없어도 과제를 마칠 수 있어야 한다.

**규칙(측정 가능)**
- 과제 완료에 **필수인 정보 금지**(필드 요건, 비밀번호 규칙, 지시문) — 필요하면 화면에 상시 표시 [S2][S9][S18][S20].
- 길이: **한 줄 짧은 문장** [S9], 아이콘 라벨은 **1~2단어** [S6]. 툴팁 글자는 잘리면 안 된다 [S9]. 긴 설명이 필요하면 툴팁이 아니다 [S18].
- 안에 **상호작용 요소 금지**(링크·버튼·입력·이미지) [S6][S9][S19]. 필요하면 팝오버/토글팁(항목 4).
- 트리거: 마우스 호버 **와** 키보드 포커스 둘 다 [S2][S6]. `Esc`로 닫힘 [S6][S18].
- 비활성(disabled) 요소·비상호작용 텍스트에 툴팁 금지 [S9]. 포커스 가능한 요소에만 붙인다 [S19].
- 터치 기기에서는 동작하지 않는다 — 모바일에서 필요한 정보면 본문에 둔다 [S2][S20].
- 지연: Primer 기본 50ms, 중간 400ms, 긴 1200ms [S13]. 기본 위치는 트리거 아래 중앙, 화면 밖으로 나가지 않게 자동 재배치 [S13][S18].
- 주변에 요소가 붙어 있으면 화살표로 대상을 가리킨다 [S2]. 관련 내용을 가리지 않는 위치 [S2][S18].
- 같은 종류 요소에는 전부 일관되게 달거나 전부 빼라 — 절반만 달면 발견되지 않는다 [S2].
- 보이는 라벨을 그대로 반복하지 않는다 [S9][S18].
- 툴팁은 "숨겨져 있고 존재 신호가 거의 없으므로 **최후 수단**" [S13][S19]. 툴팁이 많아지면 라벨 자체가 불명확하다는 뜻 [S20].

**Do**
- 지표 이름 옆 (i) 아이콘 → 한 줄 정의. 계산식·출처처럼 긴 것은 접기/팝오버로.
- 잘린 주소·구역명은 툴팁으로 전체 문자열 [S21].

**Don't**
- 판정 근거·기준값처럼 결론을 이해하는 데 필요한 정보를 툴팁에만 두기.
- 3줄 넘는 설명을 툴팁에 — 접기(항목 1)나 팝오버(항목 4)로.
- 라벨이 있는 버튼에 같은 말 툴팁.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Carbon Tooltip | https://carbondesignsystem.com/components/tooltip/usage/ | 툴팁 / 정의 툴팁 / 토글팁 구분 |
| Primer Tooltip | https://primer.style/product/components/tooltip/ | label형 vs description형, 지연 옵션 |
| USWDS Tooltip | https://designsystem.digital.gov/components/tooltip/ | 위치 4종, 접근성 통과 항목 |

## 4. 팝오버 / 토글팁 (Popover)

**언제 쓰나** — 툴팁보다 많은 내용, 또는 **상호작용이 가능한 내용**(링크·버튼·작은 폼·선택지)을 제자리에서 보여줄 때 [S7][S10]. 작은 과제를 완료시키려면 모달 [S10]. 비상호작용 메시지면 툴팁 [S10].

**규칙(측정 가능)**
- 열기: 클릭/`Enter`. 닫기: 트리거 재클릭, 바깥 클릭, `Esc` [S6][S7][S10]. 바깥 클릭에 항상 닫히므로 **필수 입력을 넣지 않는다** [S10].
- 너비 상한: 그리드 **4칼럼 이하**, 넘으면 모달 [S7].
- 팝오버 **안에서 스크롤 금지** — 숨은 내용의 단서가 없다 [S10].
- 팝오버 안에 팝오버 중첩 금지 [S7][S10]. 팝오버 안 툴팁은 위치만 조심하면 허용 [S7].
- 트리거와 컨테이너 간격 4px(캐럿 있음/없음 동일), 탭형은 0px [S7].
- 배치는 `auto`(남는 공간 쪽) 기본, 화면 가장자리에서 자동 반전 [S10].
- 역할(`menu`/`dialog`)과 라벨을 지정한다 [S10].
- 페이지 로드 직후·로그인 직후·과제 중에 자동으로 뜨는 팝업은 쓰지 않는다 [S24].

**Do**
- 지도 마커 클릭 → 작은 카드(값 3~4개 + "상세 보기" 링크 1개). 전체 상세는 드로어(항목 5).
- 용어 정의 + "출처 보기" 링크처럼 링크가 필요한 설명은 툴팁 대신 토글팁.

**Don't**
- 지도 위에 큰 팝오버를 띄워 지도를 덮기 — "아이콘·카드가 커서 지도가 안 보인다"는 지적. 구석의 작은 카드 또는 드로어.
- 팝오버에 긴 설명문 여러 단락 — 2~3줄 넘으면 접기나 상세 화면.
- 호버로 열리는 팝오버에 버튼 넣기(커서가 이동하면 닫힌다).

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Carbon Popover | https://carbondesignsystem.com/components/popover/usage/ | 캐럿/탭팁 변형, 4칼럼 상한 |
| Atlassian Popup | https://atlassian.design/components/popup/usage | 팝업 vs 툴팁 vs 모달 선택표, 스크롤 금지 |

## 5. 드로어 / 사이드 패널 (Drawer)

**언제 쓰나** — 현재 페이지(지도·목록)를 떠나지 않고 **부차 과제**(상세 보기·편집·도움말)를 처리할 때 [S11][S23]. 전체 집중이 필요한 과제는 모달·별도 페이지.

**규칙(측정 가능)**
- 열리면 포커스는 드로어 첫 항목, 닫히면 트리거로 복귀 [S11]. `Esc`·닫기 버튼·배경 클릭으로 닫힘 [S11].
- 제목(라벨) 필수 [S11].
- 뒤 화면을 참조해야 하는 과제면 **전폭/확장 폭 드로어 금지** — 뒤가 안 보인다 [S11]. 지도 화면에서는 폭을 1/3 이하로, 지도가 계속 보이게. (권장, 근거 약함)
- 도움말 패널은 "짧은 UI 텍스트(바로 보임) → 패널(개념·판단 근거) → 외부 문서(새 탭)" 3단 중 가운데를 맡는다 [S23]. 페이지 수준 도움말은 패널 기본 내용으로, 닫았다 열어도 내용이 유지된다 [S23].
- UI 본문 텍스트는 "행동을 결정하는 데 필요한 정보만" — 설명은 패널로 [S23].

**Do**
- 목록 행 클릭 → 우측 드로어에 상세. 목록은 뒤에 남아 다음 행으로 바로 이동.
- 패널 상단에 결론·값 요약, 그 아래 접기로 근거.

**Don't**
- 드로어가 열리면서 지도가 아래로 밀리거나 가려지기 — 지도는 항상 보여야 한다.
- 드로어 안에 또 드로어·모달 쌓기.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Atlassian Drawer | https://atlassian.design/components/drawer/usage | 폭 5종, 포커스 이동 규칙, 전폭 주의 |
| Cloudscape Help system | https://cloudscape.design/patterns/general/help-system/ | 정보 링크 → 도움말 패널 3단 구조 |

## 6. 긴 텍스트 자르기와 "더 보기"

**언제 쓰나** — 설명·메모·주소처럼 길이가 가변인 텍스트를 카드·표 셀·목록에 넣을 때.

**규칙(측정 가능)**
- 설명 단락은 기본 **2~3줄**(`line-clamp`)까지 보이고 그 아래 "더 보기" 토글. 펼치면 "접기"로 라벨이 바뀐다 [S22]. (줄 수 자체는 권장, 근거 약함)
- 한 줄 값(주소·ID)은 말줄임으로 자르고 **툴팁으로 전체 문자열** 제공 [S21].
- 자를 때 최소 **4글자**는 보이게, 3글자 이상 생략될 때만 자른다 [S21]. 문장부호 바로 앞뒤에서 자르지 않는다 [S21].
- 자르는 위치: 끝(기본), 앞(끝이 중요할 때), 가운데(앞뒤가 같은 문자열이 많을 때) [S21].
- 내비게이션 항목·표 머리글은 자르지 않는다(셀 내용만) [S21].
- 잘린 텍스트가 링크면 말줄임도 링크 안에 포함 [S21].
- 자르기·숨기기는 "꼭 필요할 때만 아껴서" [S12].

**Do**
- 카드: 결론 1줄은 절대 자르지 않고, 설명은 2줄 클램프 + "더 보기".
- 표 셀: 긴 값은 말줄임 + 툴팁, 머리글은 그대로.

**Don't**
- 결론·값·상태를 자르기 — 자르는 건 설명 문장만.
- "더 보기"를 눌렀더니 다시 "더 보기"(2단계 초과) [S1].
- 아이콘만 있는 말줄임 토글 — 글자 라벨과 같이 [S12].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| PatternFly Truncate | https://www.patternfly.org/components/truncate/design-guidelines | 앞/가운데/끝 자르기, 툴팁으로 전체 표시 |
| PatternFly Expandable section | https://www.patternfly.org/components/expandable-section/design-guidelines | Show more / Show less 라벨 전환 |

## 출처
| # | 출처 | URL | 확인일 | 라이선스/비고 |
|---|---|---|---|---|
| S1 | NN/g, Progressive Disclosure | https://www.nngroup.com/articles/progressive-disclosure/ | 2026-10-08 | 저작권 유지(요약만) |
| S2 | NN/g, Tooltip Guidelines | https://www.nngroup.com/articles/tooltip-guidelines/ | 2026-10-08 | 저작권 유지(요약만) |
| S3 | NN/g, Accordions on Desktop | https://www.nngroup.com/articles/accordions-complex-content/ | 2026-10-08 | 저작권 유지(요약만) |
| S4 | NN/g, Tabs, Used Right | https://www.nngroup.com/articles/tabs-used-right/ | 2026-10-08 | 저작권 유지(요약만) |
| S5 | IBM Carbon, Accordion usage | https://carbondesignsystem.com/components/accordion/usage/ | 2026-10-08 | Apache-2.0 |
| S6 | IBM Carbon, Tooltip usage | https://carbondesignsystem.com/components/tooltip/usage/ | 2026-10-08 | Apache-2.0 |
| S7 | IBM Carbon, Popover usage | https://carbondesignsystem.com/components/popover/usage/ | 2026-10-08 | Apache-2.0 |
| S8 | IBM Carbon, Tabs usage | https://carbondesignsystem.com/components/tabs/usage/ | 2026-10-08 | Apache-2.0 |
| S9 | Atlassian, Tooltip usage | https://atlassian.design/components/tooltip/usage | 2026-10-08 | 미확인 |
| S10 | Atlassian, Popup usage | https://atlassian.design/components/popup/usage | 2026-10-08 | 미확인 |
| S11 | Atlassian, Drawer usage | https://atlassian.design/components/drawer/usage | 2026-10-08 | 미확인(Drawer는 폐기 예정, Modal 권장) |
| S12 | GitHub Primer, Progressive disclosure | https://primer.style/product/ui-patterns/progressive-disclosure/ | 2026-10-08 | MIT |
| S13 | GitHub Primer, Tooltip | https://primer.style/product/components/tooltip/ | 2026-10-08 | MIT |
| S14 | GOV.UK, Details | https://design-system.service.gov.uk/components/details/ | 2026-10-08 | MIT(GOV.UK Frontend) |
| S15 | GOV.UK, Accordion | https://design-system.service.gov.uk/components/accordion/ | 2026-10-08 | MIT(GOV.UK Frontend) |
| S16 | GOV.UK, Tabs | https://design-system.service.gov.uk/components/tabs/ | 2026-10-08 | MIT(GOV.UK Frontend) |
| S17 | USWDS, Accordion | https://designsystem.digital.gov/components/accordion/ | 2026-10-08 | 퍼블릭도메인/CC0 |
| S18 | USWDS, Tooltip | https://designsystem.digital.gov/components/tooltip/ | 2026-10-08 | 퍼블릭도메인/CC0 |
| S19 | Elastic EUI, Tooltip | https://eui.elastic.co/docs/components/display/tooltip/ | 2026-10-08 | 미확인 |
| S20 | Shopify Polaris(web components), Tooltip | https://shopify.dev/docs/api/app-home/polaris-web-components/overlays/tooltip | 2026-10-08 | 미확인(polaris.shopify.com 구 URL은 shopify.dev로 리다이렉트) |
| S21 | PatternFly, Truncate design guidelines | https://www.patternfly.org/components/truncate/design-guidelines | 2026-10-08 | 미확인 |
| S22 | PatternFly, Expandable section design guidelines | https://www.patternfly.org/components/expandable-section/design-guidelines | 2026-10-08 | 미확인 |
| S23 | AWS Cloudscape, Help system | https://cloudscape.design/patterns/general/help-system/ | 2026-10-08 | 미확인(코드는 Apache-2.0) |
| S24 | NN/g, Popups: 10 Problematic Trends | https://www.nngroup.com/articles/popups/ | 2026-10-08 | 저작권 유지(요약만) |

읽기 실패로 뺀 출처: Polaris 구 URL 5건(301 → shopify.dev 허브), Adobe Spectrum tooltip(404), Material 3 tooltips(JS 렌더, 본문 없음), SAP Fiori Expandable Text(403), PatternFly ux-writing/truncation(404), Cloudscape Expandable section(본문 미수신).
