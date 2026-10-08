# KPI·지표 타일·대시보드 레이아웃 (KPI tiles & dashboard layout)

> 언제 읽나: 요약 숫자(지표 타일)·차트·표가 한 화면에 같이 놓이는 대시보드·관제·분석 홈·판정 결과 화면을 만들 때.
> 확인일 2026-10-08. 출처는 맨 아래. 수치 옆 [S1] 같은 표시는 출처 번호, 표시 없는 수치는 "권장(근거 약함)".

색·그림자·서체·모노 숫자는 SKILL.md·tokens.md가 정한다. 여기서는 "무엇을 어디에 몇 개, 무엇을 접나"만 다룬다.
차트 자체의 형태·색 규칙은 `dataviz` 스킬이 담당한다.

## 1. 화면 위계 — 요약 타일 → 차트 → 표

**언제 쓰나** — 한 화면에 요약 숫자·시계열·목록이 함께 있는 모든 대시보드. 사용자가 "지금 상태가 어떤가"를 3초 안에 알아야 할 때.

**규칙(측정 가능)**
- 세로 순서는 고정: 1줄 요약 타일(KPI) → 차트(추세·분포) → 표(상세 목록). 위에서 아래로 "전체 → 세부" [S4][S15]
- 가장 중요한 지표가 맨 위, 나머지는 F-패턴(왼쪽 위 → 오른쪽 → 아래)으로 배치 [S1]
- "가장 중요한 데이터가 가장 높은 대비와 가장 큰 면적을 차지한다" [S1] → 최상단-좌측 타일이 가장 크다
- 요약 타일 줄은 1줄이 기본. 2줄이 되면 첫 줄만 "요약", 둘째 줄은 접힘 섹션이나 차트 영역으로 내린다 (권장, 근거 약함)
- 그리드 열은 모두 같은 폭·같은 거터. 데스크톱(1200~1400px)에서는 3열 또는 4열이 가장 흔하고 전체 폭을 채운다 [S15]
- 카드 크기는 소(정적 목록 4개 항목)·중(필터 가능한 목록)·대(차트) 세 단계만 [S15]
- 카드 하나는 "지표 하나, 지표 묶음 하나, 또는 중요한 정보의 요약 하나"만 담는다 [S15]
- 반응형에서 1열로 접힐 때도 "가장 중요한 정보가 맨 위" 순서를 유지한다 [S15]
- 차트는 서비스·주제별로 1줄(row)씩, 줄 순서는 데이터 흐름(요청 → 오류 → 지연처럼 좌→우) [S4]

**Do**
- 시작 전에 "이 화면에서 제일 먼저 봐야 할 숫자 1개"를 정하고 그것을 좌상단 최대 타일로 둔다.
- 타일 줄 → 차트 → 표 순서를 wireframe 단계에서 고정하고, 나중에 끼어드는 요소는 그 아래 섹션에 넣는다.
- 지도·캔버스 같은 "핵심 화면"이 있으면 그것을 차트 자리(두 번째 블록)가 아니라 요약 타일과 같은 첫 블록 높이에서 시작시킨다.
- 상세는 표로 내리고, 표는 기본 5~10행만 보여 준 뒤 "모두 보기"로 연다 [S10].

**Don't**
- 화면을 숫자·문장으로 가득 채우지 않는다. "복잡함을 줄이기 위해 주의를 흩트릴 것을 걷어낸다" [S1] — 설명 문장은 타일 밖(툴팁·접힘)으로.
- 중요한 화면(지도·메인 차트)을 배너·필터·안내 띠 아래로 밀지 않는다 (6절).
- 타일을 같은 크기로 균등 분할해 "무엇이 중요한지" 지우지 않는다. 최대 면적 = 최대 중요도 [S1].
- 파이·도넛을 요약 영역에 쓰지 않는다. "길이와 2D 위치"가 가장 빨리 읽히고 파이·도넛은 대부분의 과제에서 나쁘다 [S5].
- 3D 차트를 쓰지 않는다 [S5].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Cloudflare Account Analytics | https://developers.cloudflare.com/analytics/account-and-zone-analytics/account-analytics/ | HTTP Traffic 패널이 맨 위, 스파크라인 4개 → 지도 → 국가별 표 순서 [S9] |
| PatternFly Dashboard | https://www.patternfly.org/patterns/dashboard/design-guidelines | Details → Performance → Inventory → Health 순 카드 우선순위, 3열·4열 그리드 [S15] |
| GitHub Traffic | https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository | 14일 그래프 위, 아래에 referring sites·popular content 표 [S12] |
| GA4 Reports snapshot | https://support.google.com/analytics/answer/10668965 | 요약 카드 나열, 카드 추가·삭제·재배치 가능 [S13] |

## 2. KPI 타일 한 개의 구성 요소

**언제 쓰나** — 숫자 하나로 상태를 말하는 타일(매출·방문자·판정 점수·충족 항목 수 등).

**규칙(측정 가능)**
- 필수 2개: 값(value) + 라벨(title/description). 그 외는 선택 [S2][S7][S8]
- 선택 요소는 최대 3개까지: 비교값(델타), 추세(스파크라인), 상태(임계값 색·배지). 4개 이상이면 타일이 아니라 카드다 (권장, 근거 약함)
- 값에는 접두·접미(통화·단위·%)를 붙이고 자릿수(precision)·천 단위 구분자를 고정한다 [S2]
- 값이 임계값을 넘으면 값 또는 배경 색으로 상태를 표시한다. 색 모드는 없음·값만·배경 중 하나로 통일 [S3][S7]
- 상태 변형은 success·warning·danger·info·neutral 다섯 가지 이내 [S8]
- 라벨이 길면 1줄로 자르고 툴팁으로 전체를 보여 준다 [S8]
- 로딩 중에는 값 자리를 자리표시(대시 2개 깜빡임 등)로 대신하고 레이아웃을 흔들지 않는다 [S6]
- 같은 주제의 지표 여러 개는 나란히(side-by-side) 한 줄에 둔다 [S8]
- 같은 지표의 시간 변화를 보이려면 타일이 아니라 차트를 쓴다 [S8]

**Do**
- 값은 라벨보다 크게, 라벨은 값 위 또는 아래 한 곳으로 통일한다(화면마다 바꾸지 않는다).
- 타일 폭이 좁으면 값·라벨이 세로로, 넓으면 가로로 — 자동 전환 규칙을 하나 정한다 [S7].
- "무엇을 충족했나"가 핵심이면 숫자 대신 `18 of 43` + 기준선 막대처럼 "기준 대비 위치"를 타일 안에 넣는다 (3절).
- 타일을 클릭하면 해당 상세 표·차트로 이동(드릴다운)하게 한다 [S14].

**Don't**
- 타일 안에 설명 문장을 넣지 않는다. 설명은 아이콘 툴팁·접힘(details)으로, "궁금해서 클릭했을 때만" 보이게.
- 숫자만 늘어놓고 "충족/미달"을 사용자가 계산하게 두지 않는다. 임계값 색·배지·기준선 중 하나는 반드시 붙인다.
- 한 타일에 지표 두 개를 섞지 않는다 [S15].
- 아이콘·값 글씨를 키워서 옆의 지도·차트를 가리지 않는다. 타일은 작게, 핵심 화면은 크게.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Ant Design Statistic | https://ant.design/components/statistic | title·value·prefix/suffix·precision·groupSeparator·추세 색 [S2] |
| Grafana Stat | https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/stat/ | value·name·배경 스파크라인·color mode·thresholds·orientation 자동 [S7] |
| Datadog Query Value | https://docs.datadoghq.com/dashboards/widgets/query_value/ | 단일 값 + 단위 자동 포맷 + 조건부 색 + 이전 기간 대비 변화 [S3] |
| GitLab Pajamas Single stat | https://design.gitlab.com/data-visualization/single-stat | value·title·meta 배지·description 툴팁·5가지 variant [S8] |
| Elastic EuiStat | https://eui.elastic.co/docs/components/display/stat/ | title/description 2요소, titleSize 6단계, 로딩 대시 [S6] |

## 3. 비교값 — 전기 대비 델타와 목표(기준선) 대비

**언제 쓰나** — 숫자 하나만으로는 "좋은지 나쁜지" 알 수 없을 때. 거의 모든 KPI 타일.

**규칙(측정 가능)**
- 비교 기준은 둘 중 하나를 타일마다 명시: (a) 이전 동일 기간, (b) 목표·임계값. 둘 다 있으면 (b)를 주, (a)를 보조로 [S3][S9]
- 전기 대비는 "이전 기간 대비 % 변화"를 값 바로 아래에 둔다 [S9]. 표기는 상대(%)·절대값·둘 다 중 하나로 화면 전체 통일 [S3]
- 델타에는 방향(▲▼ 또는 +/−)과 색(좋음/나쁨)을 함께 쓴다 — 색만으로 구분하지 않는다(남성 약 8% 색각 이상) [S5]
- "증가 = 좋음"이 아닌 지표(오류율·이탈률)는 색 매핑을 지표별로 뒤집는다 (권장, 근거 약함)
- 목표 대비는 기준선이 있는 막대(진행률) 또는 "현재 / 기준" 두 숫자로. 기준선 위치는 막대 위에 표시 (권장, 근거 약함)
- 기간 선택기는 화면 우상단 1곳. 바꾸면 모든 타일·차트·표가 같이 바뀐다 [S9][S10][S11]
- 비교 기간이 없는 타일(누적값·정적 속성)은 델타 자리를 비워 두지 않고 요소 자체를 뺀다 (권장, 근거 약함)

**Do**
- 델타 옆에 비교 기준을 짧게 적는다(`vs 지난 7일`, `목표 70`).
- 판정형 화면(체크리스트 충족)은 "충족 n / 전체 N"을 값으로, 기준선 막대를 추세 자리에 둔다.
- 델타 숫자는 값보다 작게, 값과 같은 줄 또는 바로 아래 1곳으로 통일한다.

**Don't**
- 비교값 없이 절대값만 나열하지 않는다 — "뭐가 부족하고 뭐가 강점인지" 안 보인다.
- 델타의 의미(어느 기간 대비인지)를 화면마다 다르게 두지 않는다.
- 색만으로 좋음/나쁨을 전하지 않는다 [S5].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Cloudflare Account Analytics | https://developers.cloudflare.com/analytics/account-and-zone-analytics/account-analytics/ | 각 지표에 "previous period 대비 % 변화" [S9] |
| Datadog Query Value | https://docs.datadoghq.com/dashboards/widgets/query_value/ | 변화 지표를 상대%·절대값·둘 다로 선택, 값 아래 표시 [S3] |
| Grafana Stat | https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/stat/ | 값·이름·percent-change 글자 크기를 따로 조절 [S7] |

## 4. 추세 — 스파크라인

**언제 쓰나** — 타일 값이 "오르는 중인지 내리는 중인지"를 숫자 없이 보여 줄 때.

**규칙(측정 가능)**
- 스파크라인은 축·눈금·범례 없이 선 또는 면 하나. 타일 배경이나 값 옆 한 자리 [S7][S15]
- 기간은 상단 기간 선택기와 같다. 타일마다 다른 기간을 쓰지 않는다 [S9]
- 스케일은 "최소~최대"와 "0 포함" 중 하나를 화면 전체에서 통일 [S3]
- 추세 카드 = "현재 값 + 과거 스파크라인" 조합이 표준 [S15]
- 스파크라인에 상태색을 입히려면 값과 같은 색 모드를 따른다 [S7]
- 데이터 포인트가 2개 이하면 스파크라인을 그리지 않고 델타 텍스트만 둔다 (권장, 근거 약함)

**Do**
- 선 굵기·높이를 타일 전체에서 하나로 고정한다(폰트 크기처럼 토큰화).
- 마지막 점만 강조(점 하나)해 "지금"이 어디인지 보이게 한다.
- 호버 시 날짜·값 툴팁을 띄운다 [S12].

**Don't**
- 스파크라인에 축 라벨·격자선을 넣지 않는다 — 차트가 된다.
- 스파크라인만으로 수치를 전하지 않는다. 값·델타 텍스트가 반드시 같이 있다.
- 비율 지표에 "0 포함" 스케일을 써서 변화가 안 보이게 만들지 않는다.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Cloudflare Account Analytics | https://developers.cloudflare.com/analytics/account-and-zone-analytics/account-analytics/ | Requests·Bandwidth·Page views·Visitors 스파크라인 + % 변화 [S9] |
| Grafana Stat | https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/stat/ | Graph mode None/Area, 배경 스파크라인 [S7] |
| PatternFly Dashboard | https://www.patternfly.org/patterns/dashboard/design-guidelines | Trend card = 현재 값 + 과거 스파크라인 [S15] |

## 5. 타일 개수 상한과 밀도

**언제 쓰나** — "지표를 더 넣자"는 요청이 올 때마다.

**규칙(측정 가능)**
- 요약 타일 줄은 데스크톱 기준 3~6개, 폰에서는 2열 접힘. 6개를 넘으면 두 그룹으로 나누고 둘째 그룹은 아래 섹션으로 [S15] (개수 자체는 권장, 근거 약함)
- 실제 제품의 최상단 지표 수: Cloudflare HTTP Traffic 4개(Requests·Bandwidth·Page views·Visitors) [S9], Vercel 3탭(Visitors·Page views·Bounce rate) [S11], GitHub Traffic 2종(clones·visitors) [S12]
- 타일 추가는 사용자가 하게 한다(Add/Edit 위젯) — 기본값은 적게 [S10][S13]
- 한 주제(topic)에 overview는 1개 [S14]
- 그리드 거터·마진 16px 기준 [S15]
- 밀도 dial이 높아도(Cockpit) 타일 수를 늘리지 않는다. 타일 크기·패딩을 줄인다 (권장, 근거 약함)

**Do**
- 지표 후보를 "결정에 쓰이는 것"만 남기고, 나머지는 표의 열로 내린다.
- 타일 줄을 화면 폭에 맞춰 1줄로 끝낸다. 넘치면 가로 스크롤이 아니라 개수를 줄인다.

**Don't**
- 가능한 지표를 전부 타일로 만들지 않는다. "복잡함을 줄이기 위해 걷어낸다" [S1].
- 같은 값을 타일·차트·표에 세 번 반복하지 않는다. 타일은 요약, 표는 상세.
- 텍스트·정보를 한 페이지에 다 펼치지 않는다 — 이미지(스파크라인·막대)로 바꾸거나 접는다.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Stripe Dashboard Home | https://docs.stripe.com/dashboard/basics | "Your overview" 위젯을 Add/Edit로 추가·삭제 [S10] |
| Vercel Web Analytics | https://vercel.com/docs/analytics | Visitors·Page views·Bounce rate 3개 + 패널은 상위 항목만, "View All"로 확장 [S11] |
| GA4 Overview report | https://support.google.com/analytics/answer/10659551 | 요약 카드 = 지표 + 차트 + 상위 항목, 카드 추가·삭제 [S14] |

## 6. 덜 중요한 띠(배너·필터·알림)가 핵심 화면을 밀어내지 않게

**언제 쓰나** — 안내 배너·필터 바·알림·기간 선택기·탭이 요약 타일이나 지도 위에 쌓일 때.

**규칙(측정 가능)**
- 핵심 화면(요약 타일 줄 또는 지도·메인 차트)의 상단은 뷰포트 위에서 1~2줄(헤더 + 도구 줄 1줄) 안에 시작한다. 폰(844px 높이)에서도 스크롤 없이 핵심 화면의 윗부분이 보여야 한다 (권장, 근거 약함)
- 기간 선택기·필터는 우상단 1줄에 모은다. 별도 띠를 만들지 않는다 [S9][S11]
- 알림(미해결 분쟁·검증 요청 등)은 요약 영역과 분리된 자리에 둔다 [S10] — 요약 타일 안이나 위가 아니라 옆 또는 아래
- 안내 배너는 한 번에 1개, 닫기 가능, 닫은 상태를 기억한다 (권장, 근거 약함)
- 지도·캔버스 위에 올리는 정보(범례·요약 태그)는 모서리 1곳에 작은 카드 1개. 폰에서는 화면 폭의 1/2 이하 (권장, 근거 약함)
- 탭·세그먼트 전환은 핵심 화면 위 한 줄만 차지한다. 2줄이 되면 드롭다운으로 바꾼다 (권장, 근거 약함)

**Do**
- 레이아웃 wireframe에 "핵심 화면 시작 y 좌표"를 적어 두고 띠를 추가할 때마다 확인한다.
- 필터는 접힌 상태가 기본, 적용 중이면 적용 개수 배지만 보인다(데이터 표 패턴 3절과 같은 규칙).
- 지도 위 태그는 작은 카드 하나로 모으고, 상세는 클릭 시 패널로.

**Don't**
- 지도·메인 차트를 안내 문장·필터 띠·배너 때문에 아래로 밀지 않는다.
- 아이콘·글씨를 크게 키워 지도를 가리지 않는다 — 구석의 작은 카드 태그로.
- 기간 선택기를 타일마다 따로 두지 않는다.
- 빈 상태·로딩 상태에서 띠만 남고 핵심 화면이 비는 레이아웃을 만들지 않는다 — 자리표시 타일을 같은 크기로 둔다.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Stripe Dashboard Home | https://docs.stripe.com/dashboard/basics | 분석·차트가 본문, 알림은 별도 표면 [S10] |
| Cloudflare Zone Analytics | https://developers.cloudflare.com/analytics/account-and-zone-analytics/zone-analytics/ | 탭(Traffic·Security·Cache…) 1줄 + 그래프 위 우측 기간 드롭다운 [S16] |
| Vercel Web Analytics | https://vercel.com/docs/analytics | 기간 드롭다운 우상단 1곳, 패널은 상위 항목만 [S11] |

## 출처
| # | 출처 | URL | 확인일 | 라이선스/비고 |
|---|---|---|---|---|
| S1 | IBM Carbon — Data visualization: Dashboards | https://carbondesignsystem.com/data-visualization/dashboards/ | 2026-10-08 | 페이지에 표기 없음(© IBM) · 코드는 Apache-2.0 |
| S2 | Ant Design — Statistic | https://ant.design/components/statistic | 2026-10-08 | MIT(코드) · 문서 미확인 |
| S3 | Datadog Docs — Query Value widget | https://docs.datadoghq.com/dashboards/widgets/query_value/ | 2026-10-08 | 미확인(제품 도움말, 요약만) |
| S4 | Grafana Docs — Dashboard best practices | https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/ | 2026-10-08 | 미확인(제품 문서, 요약만) |
| S5 | NN/g — Dashboards: Making Charts and Graphs Easier to Understand | https://www.nngroup.com/articles/dashboards-preattentive/ | 2026-10-08 | 저작권 유지(NN/g, 요약만) |
| S6 | Elastic EUI — Stat | https://eui.elastic.co/docs/components/display/stat/ | 2026-10-08 | 미확인 |
| S7 | Grafana Docs — Stat visualization | https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/stat/ | 2026-10-08 | 미확인(제품 문서, 요약만) |
| S8 | GitLab Pajamas — Single stat | https://design.gitlab.com/data-visualization/single-stat | 2026-10-08 | 미확인 |
| S9 | Cloudflare Docs — Account analytics | https://developers.cloudflare.com/analytics/account-and-zone-analytics/account-analytics/ | 2026-10-08 | 미확인(제품 도움말, 요약만) |
| S10 | Stripe Docs — Web Dashboard basics | https://docs.stripe.com/dashboard/basics | 2026-10-08 | 미확인(제품 도움말, 요약만) |
| S11 | Vercel Docs — Web Analytics | https://vercel.com/docs/analytics | 2026-10-08 | 미확인(제품 도움말, 요약만) |
| S12 | GitHub Docs — Viewing traffic to a repository | https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository | 2026-10-08 | 미확인(제품 도움말, 요약만) |
| S13 | Google Analytics Help — [GA4] Reports snapshot | https://support.google.com/analytics/answer/10668965 | 2026-10-08 | 미확인(제품 도움말, 요약만) |
| S14 | Google Analytics Help — [GA4] Overview report | https://support.google.com/analytics/answer/10659551 | 2026-10-08 | 미확인(제품 도움말, 요약만) |
| S15 | PatternFly — Dashboard design guidelines | https://www.patternfly.org/patterns/dashboard/design-guidelines | 2026-10-08 | 미확인(코드는 MIT) |
| S16 | Cloudflare Docs — Zone analytics | https://developers.cloudflare.com/analytics/account-and-zone-analytics/zone-analytics/ | 2026-10-08 | 미확인(제품 도움말, 요약만) |

읽기 실패(출처로 쓰지 않음): Carbon `patterns/dashboard` 404 · Datadog dashboard best-practices 404 · GA Home 도움말(9212670)은 홈 카드 설명 없음 · Material 3(대시보드 패턴 없음, 시도 안 함).