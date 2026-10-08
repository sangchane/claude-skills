# 알림·배너·배지 (Notification, Banner & Badge)

> 언제 읽나: 시스템 공지 띠·페이지 경고·저장 완료 토스트·상태 태그·미확인 개수 배지를 화면에 넣을 때. "이 메시지를 어디에 어떤 모양으로, 얼마나 오래"를 정한다.
> 확인일 2026-10-08. 출처는 맨 아래. 수치 옆 [S1] 같은 표시는 출처 번호, 표시 없는 수치는 "권장(근거 약함)".

상태색(정보·성공·경고·위험) 토큰과 아이콘 크기는 tokens.md에 있으므로 반복하지 않는다. 여기서는 종류 선택·위치·개수·시간·문구 구조만 정한다.

## 1. 무엇을 언제: 배너 · 인라인 알림 · 토스트 · 배지 선택

**언제 쓰나** — 메시지를 넣기 전에 반드시 먼저. 범위·긴급도·지속성 세 축으로 종류를 고른다.

**규칙(측정 가능)**
- 범위로 고른다: 시스템 전체 → 전폭 배너 [S1][S2][S4][S17] · 페이지·섹션 → 인라인 알림(section message·callout·message bar) [S2][S8][S12][S22] · 한 항목·필드 → 인라인 메시지·배지 [S12][S25] · 사용자 행동 결과(저장·삭제) → 토스트 [S1][S19][S23].
- 트리거로 고른다: 사용자가 한 일에 대한 응답 = 인라인·토스트. 시스템이 먼저 보내는 것 = 배너 [S2][S17]. "Use site alerts for critical system notifications... not in response to an action" [S17].
- 지속성으로 고른다: 사라져도 되는 것(정보를 다른 곳에서 다시 볼 수 있음) = 토스트 자동 닫힘 [S23][S26]. 사용자가 해결해야 하는 것 = 배너·인라인, 해결될 때까지 유지 [S2][S4][S22].
- 긴급도로 고른다: 즉시 결정이 필요하면 모달 [S2][S5]. 데이터 손실·기능 상실 경고 = 배너 [S4][S5]. 그 외는 모달·배너를 쓰지 않는다.
- 표시(indicator) ≠ 검증(validation) ≠ 알림(notification). 입력 오류는 필드 옆 검증 메시지로, 토스트로 보내지 않는다 — "toasts for errors miss critical information" [S25].
- 심각도 우선순위로 쌓는다: 오류 → 경고 → 성공 → 정보 [S20][S22]. 같은 자리에 둘 이상이면 가장 심각한 것만 펼치고 나머지는 접는다 [S22].
- 종류를 잘못 고르면 효과가 사라진다: 검증을 알림으로 보내면 무시되고, 오류를 토스트로 보내면 놓친다 [S25].

**Do**
- 한 화면에 알림 종류는 2가지 이하(예: 배너 1 + 토스트)로 제한한다 (권장, 근거 약함).
- 메시지마다 "범위·트리거·지속성"을 한 줄로 적어두고 종류를 고른다.
- 성공 알림은 아낀다 — 콜아웃·배너는 "broken"에 쓰는 것이지 성공에 쓰는 것이 아니다 [S12][S20].

**Don't**
- 같은 사실을 배너와 토스트로 두 번 알리지 않는다 ("Cross device, not duplicative" [S28]).
- 필드 오류를 페이지 상단 배너로만 보여 주지 않는다 — 필드 옆이 우선, 상단은 요약 [S12][S22].
- 알림이 많아지면 전부 무시된다 — "Too many notifications will either overwhelm or annoy the user" [S16].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Carbon notification 패턴 | https://carbondesignsystem.com/patterns/notification-pattern/ | 7종(inline·toast·actionable·callout·banner·panel·modal) 비교표 |
| Primer notification messaging | https://primer.style/product/ui-patterns/notification-messaging/ | 메시지 유형 × 컴포넌트 × 위치 표 |
| NN/g indicators/validations/notifications | https://www.nngroup.com/articles/indicators-validations-notifications/ | 세 가지의 구분 |

## 2. 전폭 배너(시스템·페이지)

**언제 쓰나** — 서비스 전체 또는 페이지 전체에 걸린 상태(점검·데이터 지연·필수 조치)를 알릴 때.

**규칙(측정 가능)**
- 페이지당 1개 [S2][S4][S13][S17]. 메시지가 둘이면 한 배너 안에 합치거나 링크 목록으로 [S13][S17].
- 위치: 헤더·내비게이션 바로 아래, 본문 콘텐츠 위 [S2][S12]. GOV.UK는 `h1` 바로 앞 [S13]. 사이트 알림은 헤더 위 전폭 [S17].
- 높이: 기본 1줄(아이콘 + 한 문장 + 링크), 최대 2줄. 넘치면 "자세히" 링크로 보낸다 (권장, 근거 약함). Atlassian 배너는 화면 폭을 넘으면 잘리고 펼칠 수 없다 [S4] — 그래서 짧게.
- 고정(sticky) 아님. 아래 콘텐츠를 밀어내며 삽입되고 스크롤과 함께 올라간다 [S4]. 화면 상단에 붙여 두지 않는다.
- 닫기: 시스템 상태 배너(점검·장애)는 닫기 없음, 상태가 끝나면 사라진다 [S4]. 안내·업셀 배너는 닫기 버튼을 두고, 닫으면 세션 동안 다시 띄우지 않는다 (권장). 경고·오류는 조치 없이 닫으면 다음 세션에 다시 뜬다 [S22].
- 문구 구조: `[무엇이 일어났나] + [무엇을 하면 되나]`. 제목(선택) + 본문 한두 문장 + 액션 1~2개 [S8][S9][S12]. 경고·오류 배너는 액션(버튼·링크)이 필수 [S22]. 액션 라벨은 동사 1~2단어 [S2][S22].
- 색만으로 심각도를 전하지 않는다 — 아이콘 + 글자 [S4][S7][S8].
- 접근성: 긴급은 `role="alert"`, 상태 안내는 `role="status"`, 비긴급은 `role="region"` [S13][S16]. `alert`은 보조기기에 시끄러우니 정말 중요할 때만 [S4].
- 사람들은 배너를 자주 놓친다 — 아껴 쓴다 [S13].

**Do**
- 슬림 변형(아이콘 + 1줄, 제목 없음)을 기본으로 [S16][S17].
- 배너가 뜨면 핵심 화면(지도·표)이 여전히 첫 화면에 보이는지 폰(390×844)에서 확인한다.
- 다이얼로그 안의 오류는 다이얼로그 헤더 아래 배너로, 페이지로 빠져나가지 않는다 [S12].

**Don't**
- "중요한 화면(지도)이 덜 중요한 띠 때문에 밑으로 밀린다" — 안내·마케팅 띠로 콘텐츠를 밀지 않는다. 띠는 높이 상한(2줄)과 닫기를 지킨다.
- 배너를 2개 이상 쌓지 않는다 [S2][S17].
- 배너를 `position: fixed`로 붙이지 않는다 [S4].
- 공포색(강한 빨강 전폭)을 비긴급 안내에 쓰지 않는다 — "fear or panic" [S17].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| GOV.UK notification banner | https://design-system.service.gov.uk/components/notification-banner/ | `h1` 앞 1개·성공 변형·합치기 |
| USWDS site alert | https://designsystem.digital.gov/components/site-alert/ | 헤더 위 전폭·슬림·쌓지 않기 |
| Atlassian banner | https://atlassian.design/components/banner/usage | 닫기 없음·한 번에 하나·밀어내기 |

## 3. 인라인 알림·콜아웃(섹션·항목)

**언제 쓰나** — 특정 섹션·카드·폼에 붙는 상태: 이 구역은 데이터가 오래됐다, 이 매물은 조건 미충족이다, 저장하려면 X가 필요하다.

**규칙(측정 가능)**
- 위치: 관련 섹션 **바로 위**(섹션 제목 아래, 콘텐츠 위) [S2][S22]. 카드면 카드 제목 아래 [S22]. 폼이면 폼 상단(요약) + 필드 옆(개별) [S12][S22].
- 본문 2줄 이내 [S1][S2]. 콜아웃은 제목 필수 [S20]. 제목은 마침표 없이 짧게 [S1].
- 액션: 주 액션 1개, 보조 1개까지 [S20]. 경고·오류는 액션 필수 [S22].
- 지속성: 해결될 때까지 유지. 콜아웃은 닫기 없음(페이지와 함께 로드) [S2]. 인라인은 닫기 선택 [S1].
- 페이지당 콜아웃 수를 최소화 [S20]. 한 섹션에 1개, 페이지에 3개 넘으면 설계를 다시 본다 (권장, 근거 약함).
- 크기: 항상 자리 잡는 콜아웃은 작은 크기(`s`) [S20].
- 인용·보충 설명 띠(inset text)는 중요한 내용에 쓰지 않는다 — 복잡한 페이지에서 눈에 안 띈다 [S15]. 아주 드물게만 [S15].
- 문구: 무엇이 문제인지 + 해결 방법, 능동 동사, 비난하지 않기 [S8]. 링크 텍스트는 목적지를 말한다 [S8].

**Do**
- 판정 결과(통과·미달)는 항목 옆 배지(항목 5)로, 왜 미달인지는 클릭 시 펼치는 인라인 설명으로 — "설명 문장은 궁금해서 클릭했을 때만".
- 데이터가 오래됐으면(stale) 해당 표·지도 위에 1줄 인라인 경고 + "새로고침" 액션.
- 여러 섹션에 같은 경고가 걸리면 페이지 상단 배너 1개로 묶는다 [S13].

**Don't**
- 설명 문단을 콜아웃에 담아 세로 길이를 늘리지 않는다 — 2줄 넘으면 접기.
- 성공 콜아웃을 상시 띄우지 않는다 [S20].
- 한 카드에 인라인 알림을 2개 이상 두지 않는다. 심각한 것 하나 + 배지.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Atlassian section message | https://atlassian.design/components/section-message/usage | 섹션 위 배치·제목/본문/액션 구조 |
| Fluent message bar | https://fluent2.microsoft.design/components/web/react/core/messagebar/usage | 페이지·컨테이너·탭·카드·폼별 위치, 심각도 정렬, 아코디언 묶기 |
| EUI callout | https://eui.elastic.co/docs/components/display/callout/ | 제목 필수·액션 1+1·크기 s |

## 4. 토스트

**언제 쓰나** — 사용자가 방금 한 일의 결과(저장됨·3건 삭제됨·동기화 완료)를 짧게 확인시킬 때. 정보가 사라져도 다른 곳에서 다시 볼 수 있을 때만.

**규칙(측정 가능)**
- 표시 시간: 5초가 접근성 하한 [S26]. 기본 5~7초 [S1][S23][S27], 읽기 시간 6~7초 기준 10초까지 [S19]. Ant Design 기본 4.5초(notification)·3초(message) [S29][S30]는 하한 아래이므로 5초 이상으로 올린다.
- 액션이 있는 토스트는 자동으로 닫지 않는다 [S2][S26]. 호버·포커스 중에는 타이머를 멈춘다 [S23][S26].
- 성공·링크 없음 = 3~5초 자동 닫힘, 그 외(오류·경고·링크 있음) = 닫을 때까지 유지 [S27]. 닫기 버튼은 항상 둔다 [S27].
- 위치: 한 앱에서 한 곳으로 고정. 우상 또는 우하(콘텐츠를 가장 덜 가리는 곳) [S1][S19][S23]. Atlassian은 좌하 [S5], Spectrum 기본 하단 중앙 [S26], LDS는 상단 중앙 고정 [S27] — 어느 쪽이든 **하나만**.
- 동시 개수: 1개씩이 이상적 [S19]. 최대 4개, 간격 16px [S23]. 넘치면 가장 오래된 것부터 지운다 [S29]. 새 것이 위 [S2][S5].
- 같은 종류가 연달아 오면 묶는다: "4 visualizations were deleted" [S19][S27].
- 본문 길이: 1줄, 최대 60자(영문) [S23] / 3줄 이하 [S2] / 1~2문장 [S27]. 한국어는 25자 안팎 1줄 (권장, 근거 약함).
- 액션: 최대 2개(링크 2 [S5], 버튼 1+1 [S19]). 버튼 글자 1~2단어·36자 이하 [S23].
- 폰에서는 폭 90%, 아이콘·설명 생략 [S27].
- 포커스를 토스트로 옮기지 않는다 [S23][S27].
- 오류·필수 조치는 토스트로 보내지 않는다 — 모달·필드 오류·메시지 바로 [S23][S25].

**Do**
- "저장됨"처럼 동사 과거형 한 토막. "successfully"는 뺀다 [S19].
- 되돌리기(Undo)가 가능하면 액션 1개로 넣고 자동 닫힘을 끈다 [S26].
- 긴 오류는 토스트에 요약 + "자세히" 버튼으로 패널 열기 [S19].

**Don't**
- 토스트를 3개 이상 겹쳐 띄우지 않는다 [S19][S23].
- 토스트에만 있는 정보로 상태를 알리지 않는다 — 사라지면 끝이다 [S26].
- 폰에서 토스트가 하단 시트·지도 컨트롤을 덮지 않게 한다. 하단 고정 UI가 있으면 토스트는 상단.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Fluent toast | https://fluent2.microsoft.design/components/web/react/core/toast/usage | 7초·최대 4개·16px·60자 |
| EUI toast | https://eui.elastic.co/docs/components/display/toast/ | 10초·한 번에 하나·묶기 |
| React Spectrum Toast | https://react-spectrum.adobe.com/react-spectrum/Toast.html | 5초 하한·액션 있으면 유지·호버 정지 |
| LDS(spring-21) toasts | http://spring-21.lightningdesignsystem.com/guidelines/messaging/components/toasts/ | 성공 3~5초·그 외 sticky·폰 90% |

## 5. 상태 배지(태그·로젠지)

**언제 쓰나** — 항목(매물·구역)의 상태·판정·등급을 한 단어로 붙일 때: `통과`, `미달`, `검토중`, `신규`.

**규칙(측정 가능)**
- 글자 수: 1~2단어 [S24], 20자 이하 [S3]. 한국어 2~4자(`통과`, `조건부`, `미달`) (권장). 잘리는 라벨은 쓰지 않는다 [S7][S24].
- 한 줄, 줄바꿈 없음, 넘치면 말줄임 + 툴팁 [S3][S21]. Atlassian 로젠지 최대 폭 200px [S7].
- 문장형 대소문자(첫 글자만), 전부 대문자 금지 [S7][S14][S24].
- 형용사(상태)로 쓴다, 동사(행동) 금지 [S14]. 배지는 링크·버튼이 아니다 — 비상호작용이면 hover·focus 스타일을 끈다 [S14][S18].
- 색 = 뜻 하나. 성공·경고·위험·정보·중립 같은 의미색만 상태에 쓴다 [S6][S7]. GOV.UK 예: 회색 비활성·초록 신규·파랑 대기·빨강 긴급/반려·노랑 지연 [S14]. 사용자 생성 라벨(카테고리)은 의미색이 아닌 강조색 [S7].
- 색만으로 뜻을 주지 않는다 — 글자가 뜻을 담고, 아이콘은 뜻이 확립된 것만 [S7][S24]. 작은 배지에는 아이콘을 넣지 않는다 [S3].
- 상태 종류 수: 가능한 최소로 시작한다 — 많을수록 못 외운다 [S14]. 한 화면의 상태 어휘 5개 이하 (권장, 근거 약함).
- 항목당 배지 1개(상태) + 보조 1개(등급)까지. 태그 묶음은 5줄 넘게 감싸지 않는다 [S3]. 섞어 쓰지 않는다(상호작용 태그 + 정적 태그) [S18].
- 숫자(개수·지표)에는 배지 대신 카운트 배지(항목 6) [S6].
- 심각한 상태 강조(채운 아이콘·진한 배경)는 아껴야 효과가 남는다 [S7].

**Do**
- 판정 결과는 표·카드 행 맨 앞 또는 제목 오른쪽에 배지 1개 — "숫자만 늘어놓아 뭐가 강점이고 부족한지 안 보인다"의 해법.
- 같은 뜻은 앱 전체에서 같은 글자·같은 색 [S13].
- 배지 옆 `i` 아이콘 또는 클릭으로 "왜 이 상태인가"를 펼친다(항목 3).

**Don't**
- `상태: 통과` 같은 라벨+값 중복 금지. 배지 글자만.
- 배지를 많이 달아 주목 효과를 죽이지 않는다 — "Don't overdo it" [S18].
- 사용자가 배지를 버튼으로 오해하게 두지 않는다 [S18].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| GOV.UK tag | https://design-system.service.gov.uk/components/tag/ | 9색 뜻·형용사·비상호작용 |
| Atlassian lozenge | https://atlassian.design/components/lozenge/usage | 200px 상한·의미색 vs 강조색 |
| Carbon tag | https://carbondesignsystem.com/components/tag/usage/ | 20자·말줄임+툴팁·4변형 |

## 6. 카운트 배지(미확인 개수)

**언제 쓰나** — 아이콘·탭·내비 항목 옆에 "몇 개"를 붙일 때: 새 매물 12, 미확인 알림 3.

**규칙(측정 가능)**
- 상한 표기: 99 초과 → `99+` [S31]. 더 큰 단위는 축약(`1K`, `5M`) [S6].
- 0이면 숨긴다(기본) [S31]. 꼭 보여야 하면 `showZero`처럼 명시적으로만.
- 숫자 없이 "있음"만 알리면 점(dot) 배지 [S31]. 점은 아이콘 우상단에 겹친다.
- 위치: 설명하는 대상 위·옆에 붙여 시각적으로 연결 [S24]. 내비·버튼 안에서는 라벨 오른쪽 [S11].
- 크기 섞지 않기: 한 맥락에 한 크기 [S24]. 작은 크기 2단계(small·medium) [S31].
- 아이콘만 있는 배지는 aria-label로 뜻을 준다 [S24].
- 변형 2가지면 충분: 기본(옅은 배경) · 강조(진한 배경·반전 글자) [S11].
- 높은 주목이 필요한 개수에 쓰고, 상태 글자에는 로젠지(항목 5) [S6].

**Do**
- 읽으면(열면) 즉시 0으로 내리고 숨긴다.
- 탭 라벨 옆 개수는 모노 숫자(토큰 규칙) 2~3자리까지만 보이게 설계한다.

**Don't**
- `123456` 같은 원값을 그대로 쓰지 않는다 — `99+` [S31].
- 개수 배지를 상태색(빨강)으로만 구분하지 않는다 — 숫자가 있어야 한다 [S24].
- 핵심 화면(지도·표) 위에 떠다니는 카운트 배지를 두지 않는다 — 내비·탭에 붙인다.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Ant Design badge | https://ant.design/components/badge | `overflowCount` 기본 99·dot·0 숨김 |
| Primer counter label | https://primer.style/product/components/counter-label/ | 내비·버튼 옆 개수, 기본/강조 2변형 |
| Atlassian badge | https://atlassian.design/components/badge/usage | 숫자 전용, 로젠지와의 구분 |

## 출처
| # | 출처 | URL | 확인일 | 라이선스/비고 |
|---|---|---|---|---|
| S1 | IBM Carbon — Notification usage | https://carbondesignsystem.com/components/notification/usage/ | 2026-10-08 | Apache-2.0(Carbon) |
| S2 | IBM Carbon — Notification pattern | https://carbondesignsystem.com/patterns/notification-pattern/ | 2026-10-08 | Apache-2.0(Carbon) |
| S3 | IBM Carbon — Tag usage | https://carbondesignsystem.com/components/tag/usage/ | 2026-10-08 | Apache-2.0(Carbon) |
| S4 | Atlassian — Banner usage | https://atlassian.design/components/banner/usage | 2026-10-08 | 미확인 |
| S5 | Atlassian — Flag usage | https://atlassian.design/components/flag/usage | 2026-10-08 | 미확인 |
| S6 | Atlassian — Badge usage | https://atlassian.design/components/badge/usage | 2026-10-08 | 미확인 |
| S7 | Atlassian — Lozenge usage | https://atlassian.design/components/lozenge/usage | 2026-10-08 | 미확인 |
| S8 | Atlassian — Section message usage | https://atlassian.design/components/section-message/usage | 2026-10-08 | 미확인 |
| S9 | GitHub Primer — Banner | https://primer.style/product/components/banner/ | 2026-10-08 | MIT(Primer) |
| S10 | GitHub Primer — Label | https://primer.style/product/components/label/ | 2026-10-08 | MIT(Primer) |
| S11 | GitHub Primer — CounterLabel | https://primer.style/product/components/counter-label/ | 2026-10-08 | MIT(Primer) |
| S12 | GitHub Primer — Notification messaging | https://primer.style/product/ui-patterns/notification-messaging/ | 2026-10-08 | MIT(Primer) |
| S13 | GOV.UK — Notification banner | https://design-system.service.gov.uk/components/notification-banner/ | 2026-10-08 | MIT(GOV.UK Frontend), 문서 라이선스 미확인 |
| S14 | GOV.UK — Tag | https://design-system.service.gov.uk/components/tag/ | 2026-10-08 | MIT(GOV.UK Frontend), 문서 라이선스 미확인 |
| S15 | GOV.UK — Inset text | https://design-system.service.gov.uk/components/inset-text/ | 2026-10-08 | MIT(GOV.UK Frontend), 문서 라이선스 미확인 |
| S16 | USWDS — Alert | https://designsystem.digital.gov/components/alert/ | 2026-10-08 | 퍼블릭도메인/CC0(USWDS 문서) |
| S17 | USWDS — Site alert | https://designsystem.digital.gov/components/site-alert/ | 2026-10-08 | 퍼블릭도메인/CC0(USWDS 문서) |
| S18 | USWDS — Tag | https://designsystem.digital.gov/components/tag/ | 2026-10-08 | 퍼블릭도메인/CC0(USWDS 문서) |
| S19 | Elastic EUI — Toast | https://eui.elastic.co/docs/components/display/toast/ | 2026-10-08 | 미확인(EUI 코드는 Elastic/SSPL 이중) |
| S20 | Elastic EUI — Callout | https://eui.elastic.co/docs/components/display/callout/ | 2026-10-08 | 미확인 |
| S21 | Elastic EUI — Badge | https://eui.elastic.co/docs/components/display/badge/ | 2026-10-08 | 미확인 |
| S22 | Microsoft Fluent 2 — Message bar | https://fluent2.microsoft.design/components/web/react/core/messagebar/usage | 2026-10-08 | 미확인 |
| S23 | Microsoft Fluent 2 — Toast | https://fluent2.microsoft.design/components/web/react/core/toast/usage | 2026-10-08 | 미확인 |
| S24 | Microsoft Fluent 2 — Badge | https://fluent2.microsoft.design/components/web/react/core/badge/usage | 2026-10-08 | 미확인 |
| S25 | NN/g — Indicators, validations, notifications | https://www.nngroup.com/articles/indicators-validations-notifications/ | 2026-10-08 | 저작권 유지, 요약만 |
| S26 | Adobe React Spectrum — Toast | https://react-spectrum.adobe.com/react-spectrum/Toast.html | 2026-10-08 | Apache-2.0(react-spectrum) |
| S27 | Salesforce LDS(spring-21) — Toasts | http://spring-21.lightningdesignsystem.com/guidelines/messaging/components/toasts/ | 2026-10-08 | 미확인(구 버전 아카이브) |
| S28 | Salesforce LDS(spring-21) — Messaging overview | http://spring-21.lightningdesignsystem.com/guidelines/messaging/overview/ | 2026-10-08 | 미확인(구 버전 아카이브) |
| S29 | Ant Design — Notification | https://ant.design/components/notification | 2026-10-08 | MIT(antd) |
| S30 | Ant Design — Message | https://ant.design/components/message | 2026-10-08 | MIT(antd) |
| S31 | Ant Design — Badge | https://ant.design/components/badge | 2026-10-08 | MIT(antd) |

읽기 실패(출처로 쓰지 않음): Shopify Polaris banner·badge·toast(shopify.dev로 리다이렉트 후 404), Adobe Spectrum toast·badge·alert-banner·in-line-alert(404), Primer flash(랜딩만 반환), LDS 현행 messaging overview·toasts·banners(404/본문 없음)·spring-21 banners(404), NN/g toasts(404), Material 3 snackbar·badges(JS 렌더, 제목만).
