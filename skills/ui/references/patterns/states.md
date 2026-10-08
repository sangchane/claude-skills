# 상태 (States: empty / loading / error / stale / partial)

> 언제 읽나: 데이터가 없거나·오는 중이거나·실패했거나·오래됐을 때 화면이 어떻게 보일지 정해야 할 때. 정상 상태만 그린 화면을 넘기기 전(Pre-Flight "빈/로딩/에러(+stale)" 항목)에 반드시.
> 확인일 2026-10-08. 출처는 맨 아래. 수치 옆 [S1] 같은 표시는 출처 번호, 표시 없는 수치는 "권장(근거 약함)".

공통 원칙(모든 항목에 적용)
- 응답 시간 3한계: **0.1초** 즉각(피드백 불필요), **1초** 사고 흐름 유지(지연은 느끼지만 특별 피드백 불필요), **10초** 주의 유지 한계(넘으면 진행률 + 중단 수단) [S1].
- 상태 표시는 **대체하는 내용과 같은 자리**에 둔다 — 전면 오버레이는 화면 전체가 멈출 때만 [S13][S7].
- 상태 문구는 "무엇이 일어났나 + 다음에 무엇을 하나" 두 줄 구조. 기술 용어(404·500·bad request)·"oops" 금지 [S15][S16][S4].
- 한 화면에 여러 상태가 동시에 뜰 때(타일 여러 개)는 아이콘·일러스트를 빼고 텍스트만 — 한 페이지에 일러스트는 1개 [S5][S17].

## 1. 빈 상태 (Empty)

**언제 쓰나** — 표·카드·목록·대시보드 타일에 보여줄 항목이 0개일 때 [S23]. 네 경우를 **구분**해서 다르게 쓴다.

**규칙(측정 가능)**
- 네 종류를 구분한다: ① 처음(아직 만든 것 없음) ② 검색 결과 없음 ③ 필터 때문에 0건 ④ 권한 없음. 에러는 빈 상태가 아니라 에러 상태(항목 3) [S5][S12][S17][S23].
- 구성: 제목(필수) + 설명(선택, "왜 비었는지" 설명할 때만) + 행동 버튼. 제목은 굵게·마침표 없음, 설명은 마침표 있음, 세 요소가 같은 말을 반복하지 않는다 [S23][S9].
- 다음 행동은 **1개**(primary) — 보조 행동은 텍스트 링크 1개까지 [S12][S17][S9]. "한 빈 상태에서 여러 선택지를 다루지 않는다" [S5].
- 필터 0건의 행동 버튼 문구는 "필터 지우기"(Clear filter) 고정 [S23]. 검색 0건은 검색어 수정 유도, 권한 없음은 관리자 연락, 처음은 "만들기" [S17].
- 처음 상태에만 아이콘/일러스트 + 옅은 배경, 결과 없음·권한 없음은 투명 배경에 아이콘 선택 [S17]. 작은 타일·여러 개 동시에는 텍스트만 [S5].
- 제목은 "무슨 일인가"에 답한다("No matches", "No distributions") [S17][S23]. 설명 단어 수는 최소로 [S9].
- 컨테이너 폭: 넓음 464px / 좁음 304px [S9]. 세로 레이아웃은 "제목 + 단락 2개"까지 [S17].
- 건수 카운터("0건")를 같이 보여 준다 [S23]. 값이 없는 셀은 빈칸이 아니라 "-" [S23].
- 동사형 명령문 버튼("만들기", "지우기") [S9]. 제품 전문 용어·다른 앱 참조 금지 [S5].
- 처음 상태는 "데이터가 차면 여기에 무엇이 보일지"를 구체적으로 쓴다 [S5].

**Do**
- 후보지 목록 필터 0건: "조건에 맞는 구역이 없습니다" + [필터 지우기].
- 매물 기록 처음: "아직 기록한 매물이 없습니다. 주소를 넣으면 판정과 손익이 여기에 쌓입니다" + [매물 추가].
- 대시보드 타일 비었을 때: 타일 제목은 유지하고 본문만 한 줄 텍스트.

**Don't**
- 네 경우를 하나의 "데이터 없음"으로 뭉개기 — 필터 때문인지 정말 없는지 알 수 없다.
- 버튼 없는 빈 상태(막다른 길) [S23][S19].
- 빈 상태에 긴 안내문 여러 단락 — 제목 1줄 + 설명 1~2줄.
- 권한 없음을 빈 목록처럼 보이게 하기 — "볼 권한이 없습니다"라고 쓴다.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Carbon Empty states pattern | https://carbondesignsystem.com/patterns/empty-states-pattern/ | 3분류(no data / user action / error management), 작은 타일 텍스트만 |
| Cloudscape Empty states | https://cloudscape.design/patterns/general/empty-states/ | 표 안 빈 상태 vs 필터 0건("Clear filter") |
| EUI EmptyPrompt | https://eui.elastic.co/docs/components/display/empty-prompt/ | 상황별 배경색·아이콘·행동 표 |
| Primer Blankslate | https://primer.style/product/ui-patterns/empty-states/ | 처음/일시 비어있음/에러 구분 |

## 2. 로딩 (Loading)

**언제 쓰나** — 데이터를 가져오는 동안. 어떤 표시를 쓸지는 **예상 시간**과 **범위**(전체 페이지 vs 타일 하나)로 정한다.

**규칙(측정 가능)**
- **1초 미만**: 아무 표시도 하지 않는다 — 깜빡임이 오히려 느려 보인다 [S2][S13][S10]. Carbon은 3초 초과부터 스피너 [S7].
- **1~3초**: 불확정 표시(스피너) [S13]. **2~10초**: 스피너 또는 스켈레톤 [S2][S3].
- **10초 이상**: 진행률 바(확정형) [S2][S3]. Primer는 3~10초부터 가능하면 확정형 [S13].
- 범위: **모듈 하나** = 그 자리에 작은 스피너, **페이지 전체** = 스켈레톤 [S2][S6][S7]. 전면 오버레이는 사용자 행동으로 앱 전체가 잠길 때만 [S6][S7].
- 스켈레톤은 **실제 콘텐츠의 크기·모양**을 따라야 한다(레이아웃 시프트 방지) [S11][S13]. 머리글·푸터만 있는 "프레임형" 스켈레톤은 고장으로 보여 금지 [S2].
- 스켈레톤은 컨테이너·데이터 컴포넌트(타일·표·카드)에만, 버튼·입력·토글·드롭다운·모달·토스트에는 쓰지 않는다 [S6].
- 스켈레톤 노출은 "몇 초"까지 [S6]. 콘텐츠가 오면 즉시 제거 [S11]. 아주 짧은 로딩에는 쉬머 애니메이션 생략, 빽빽한 반복 목록에도 쉬머 생략 [S11].
- 페이지당 스피너는 **1개** [S10]. 섹션별로 점진 로드할 때만 여러 개 허용, 한 번에 다 오면 큰 것 1개 [S18][S13].
- 점진 로드 순서: ① 컨테이너 뼈대 ② 비데이터 텍스트 + 데이터 텍스트 스켈레톤 ③ 이미지·상호작용 요소 [S6]. 이미지는 스켈레톤 없이 빈 공간이어도 된다 [S6].
- 로딩 중에는 관련 버튼(취소 등)을 비활성화하고, 스피너에는 "loading/submitting" 같은 라벨을 단다 [S7][S10]. `aria-busy` 전환, 완료 후 새 콘텐츠 첫 요소로 포커스 [S13].
- 재갱신(refresh)은 스켈레톤보다 **기존 데이터를 그대로 두고** 갱신 — 항목 5 [S22].

**Do**
- 지표 타일 8개 페이지: 첫 진입은 타일 모양 스켈레톤, 개별 타일 재계산은 타일 안 작은 스피너.
- 표 첫 로드는 열 구조를 유지한 스켈레톤 행 5~10개 [S22]. (행 수는 권장, 근거 약함)
- 버튼 제출은 버튼 안 스피너 + 버튼 비활성(LoadingButton) [S10].

**Don't**
- 전체 화면 흐림 오버레이로 타일 하나 로딩 — 지도까지 가려진다.
- 0.3초짜리 응답에 스피너 깜빡이기 [S2][S13].
- 콘텐츠와 모양이 다른 스켈레톤(회색 막대 3줄)을 모든 곳에 — 로드 후 레이아웃이 튄다 [S11].
- 스피너만 10초 넘게 — 진행률이나 예상 시간 없이는 사용자가 떠난다 [S1][S3].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Carbon Loading pattern | https://carbondesignsystem.com/patterns/loading-pattern/ | 상황별 선택표, 점진 로드 순서 |
| Primer Loading | https://primer.style/product/ui-patterns/loading/ | 1/3/10초 임계값, 스켈레톤 적용 범위 |
| Atlassian Skeleton | https://atlassian.design/components/skeleton/usage | 모양 일치, 쉬머 생략 조건 |
| Ant Design Skeleton | https://ant.design/components/skeleton | 아바타·제목·단락 조합 데모 |

## 3. 에러 (Error)

**언제 쓰나** — 요청 실패·검증 실패·서버 장애. **인라인**(문제가 난 자리)이 기본, **전면**(페이지 전체)은 페이지 자체를 못 그릴 때만.

**규칙(측정 가능)**
- 메시지는 **원인 + 해결** 두 부분 필수 [S8][S4]. "오류가 발생했습니다" 같은 일반 문구 금지 — "필수 항목이 비어 제출되지 않았습니다"처럼 구체적으로 [S12][S4].
- 위치: 문제가 난 요소 **바로 옆** [S4][S8][S24]. 폼 검증은 필드 옆 메시지 + 페이지 상단 에러 요약(h1 위, 포커스 이동) [S14]. 서버 측 검증 실패는 제출 버튼 위 페이지 알림 [S24].
- 에러 요약은 오류가 1개여도 띄우고, 각 항목은 해당 필드로 링크, 문구는 필드 옆과 동일 [S14]. 페이지 `<title>` 앞에 "Error: " [S14].
- 심각도 매칭: 모달은 되돌릴 수 없는 심각한 에러에만, 사소한 것은 배너·토스트 [S4][S8]. 모달은 한 번에 1개 [S8].
- 길이: 인라인 알림 **2줄 이하**, 토스트 **3줄 이하** [S8]. 행동이 있는 알림은 자동 닫힘 금지, 긴급 메시지는 타이머 금지 [S8].
- **재시도 버튼**: 로드 실패 빈 상태의 기본 행동은 "다시 시도" [S17]. 컴포넌트 단위 실패는 그 컴포넌트의 내장 에러 상태를 쓴다 [S24].
- 입력값은 보존한다 — 다시 치게 하지 않는다 [S4]. 사용자를 탓하는 단어("invalid", "illegal") 금지 [S4].
- 전면 에러 페이지: 제목 "서비스에 문제가 있습니다" + "나중에 다시 시도" + 저장된 입력 보존 여부·기간 + 연락처/대체 경로 [S16]. 404는 "주소를 확인하세요" 2가지 안내 + 연락처, 브레드크럼 없음 [S15]. 빨간 경고 텍스트 금지 [S15][S16].
- 사용자가 입력을 마치기 전에 에러를 미리 띄우지 않는다 [S4].
- 색만으로 에러를 표시하지 않는다(아이콘·텍스트 동반) [S4].

**Do**
- 타일 데이터 로드 실패: 타일 안에 "공시가격을 못 가져왔습니다(API 한도). [다시 시도]" — 타일 밖 화면은 그대로.
- 폼: 필드 옆 메시지 + 상단 요약, 요약 항목 클릭하면 필드로.
- 전체 페이지 실패(서버 다운)만 Result/전면 페이지 [S21].

**Don't**
- 에러를 빈 상태(항목 1)처럼 "데이터 없음"으로 보여주기 [S23].
- "오류 코드 500" 같은 기술 문구만 보여주고 다음 행동 없음 [S16].
- 에러 토스트를 3초 뒤 자동으로 지우기 — 읽기 전에 사라진다 [S8].
- 전면 모달로 사소한 실패 알리기 — 사용자 흐름을 끊는다 [S4][S8].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| GOV.UK Error summary | https://design-system.service.gov.uk/components/error-summary/ | 상단 요약 + 필드 링크 + 포커스 이동 |
| GOV.UK Problem with the service | https://design-system.service.gov.uk/patterns/problem-with-the-service-pages/ | 전면 에러 페이지의 최소 문구 |
| Carbon Notification pattern | https://carbondesignsystem.com/patterns/notification-pattern/ | 인라인/토스트/모달 선택, 줄 수 상한 |
| Ant Design Result | https://ant.design/components/result | 403/404/500 전면 결과 화면 구성 |

## 4. 대기 · 계산 중 (Progress)

**언제 쓰나** — 사용자가 시작한 작업(일괄 판정·동기화·내보내기)이 수 초~수 분 걸릴 때. 로딩(항목 2)과 달리 "얼마나 남았는지"가 핵심.

**규칙(측정 가능)**
- **2~10초**: 불확정 루프 애니메이션(스피너). **10초 이상**: 확정형(퍼센트) 진행률 [S3][S1]. 1~2초는 피드백만 주고 애니메이션 없음 [S3].
- 확정형이 가능하면(문서 N개 처리 등) 10초 미만이라도 확정형 [S3][S13].
- 진행률에는 **텍스트 설명**("주소 3/50 처리 중")과 **예상 시간**("약 3분 남음")을 붙인다 [S3]. 실제보다 빠르게 약속하지 않는다 [S3].
- 긴 작업에는 **취소** 버튼 [S3][S1]. 10초를 넘으면 사용자가 다른 일을 하게 되므로 백그라운드 처리 + 완료 알림을 고려한다 [S13][S1].
- 몇 분 이상 걸리면 전면 로더 옆에 알림(notification)도 같이 [S6].
- 정지 화면(움직임 없는 "처리 중" 텍스트) 금지 — 멈춘 것과 구분이 안 된다 [S3]. "클릭하지 마세요" 안내문 금지 [S3].
- 진행률 애니메이션은 처음 느리게, 끝으로 갈수록 빠르게 [S3].
- 진행률이 있으면 사용자는 평균 **3배** 더 기다린다 [S3].
- 상태 표시(pending)는 새로고침 버튼 옆, 지연 사유는 팝오버로 [S22].

**Do**
- 구역 일괄 계산: "구역 12/37 계산 중 · 약 40초 남음" + [취소]. 끝나면 결과 타일로 교체.
- 백그라운드 동기화: 헤더에 작은 상태 점 + "동기화 중 3/3개 구".

**Don't**
- 스피너만 돌리고 몇 분을 보내기 [S3].
- 진행률 바가 99%에서 멈춰 있기 — 예상 시간을 줄 수 없으면 불확정형으로 바꾼다.
- 취소 불가능한 긴 작업을 전면 오버레이로 잠그기 [S1][S3].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| NN/g Progress Indicators | https://www.nngroup.com/articles/progress-indicators/ | 루프 vs 퍼센트 선택 임계값, 예상 시간 문구 |
| Carbon Loading component | https://carbondesignsystem.com/components/loading/usage/ | 대형(오버레이) vs 소형(인라인) |
| Atlassian Spinner | https://atlassian.design/components/spinner/usage | 1초 이상일 때만, 페이지당 1개 |

## 5. 오래된 데이터 (Stale)

**언제 쓰나** — 실시간·주기 갱신 데이터(동기화된 참조 데이터, 외부 API 값, 관제 지표)를 보여줄 때. 값이 "언제 것"인지 모르면 신뢰할 수 없다.

**규칙(측정 가능)**
- 갱신에 성공하면 **마지막 갱신 시각**을 데이터 옆에 표시하고, 변경을 ARIA live region으로 알린다 [S22].
- 새로고침 버튼은 헤더 행동 영역에 1개 — 화면 곳곳에 흩뿌리지 않는다(부분 갱신이 꼭 필요한 곳만 예외) [S22].
- 자동 갱신 주기는 명시(예: 10초) [S22]. 수동 갱신은 여러 자원에 작업하는 큰 데이터셋에, 자동은 실시간 목록에 [S22].
- 갱신 중에도 **기존 데이터는 보이게** 두고 행동 가능하게 한다(스켈레톤으로 지우지 않는다) [S22].
- 갱신이 **1~10초** 넘게 걸리면 새로고침 버튼 옆에 pending 상태 표시 + 팝오버로 지연 사유 [S22].
- 경과 임계값 후 배지: 갱신 주기의 2배가 지나면 "N분 전" 배지를 경고색으로, 실시간 연결이 끊기면 "연결 끊김 · 마지막 HH:MM" 배지 + 재연결 중 표시. (권장, 근거 약함)
- 끊긴 동안 마지막 정상 값은 지우지 않고 흐리게 유지한다 — 값이 사라지는 것보다 오래된 값이 낫다. (권장, 근거 약함)
- 갱신 실패(부분·전체)는 경고 상태 표시 + 설명 + 복구 행동(재시도·영향 범위 필터) [S22].

**Do**
- 지표 헤더 구석에 "갱신 14:02" 작은 모노 글자. 임계 초과 시 같은 자리에 노란 배지 "32분 전".
- 외부 API 값(공시가격)은 수집일을 값 옆에 — 출처·수집일 규약과 같은 원칙.

**Don't**
- 갱신 시각 없는 실시간 지표 — 사용자는 끊긴 줄 모른다.
- 재갱신 때마다 화면을 스켈레톤으로 비우기 [S22].
- 큰 빨간 띠로 "연결 끊김"을 지도 위에 올리기 — 구석 작은 배지로, 지도는 보이게.

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Cloudscape Loading and refreshing | https://cloudscape.design/patterns/general/loading-and-refreshing/ | 마지막 갱신 시각, 수동/자동 갱신, pending 표시 |

## 6. 부분 실패 (Partial failure)

**언제 쓰나** — 대시보드 타일·표 열·지도 레이어 중 **일부만** 데이터를 못 받았을 때. 전체를 에러로 바꾸면 멀쩡한 정보까지 잃는다.

**규칙(측정 가능)**
- 실패한 **그 컴포넌트 안에서만** 에러 상태를 보인다(컴포넌트 내장 에러 상태) — 나머지는 정상 렌더 [S24][S13].
- 각 실패 타일에 원인 1줄 + "다시 시도" 1개 [S17][S8]. 여러 타일이 동시에 실패하면 아이콘 생략·텍스트만 [S5][S17].
- 페이지 상단에는 요약 1줄만("지표 2개를 불러오지 못했습니다") — 타일마다 긴 문장 반복 금지. (권장, 근거 약함)
- 갱신 중 일부 실패는 경고 상태 표시 + 영향 범위 설명 + 복구 행동 [S22].
- 섹션별 점진 로드에서는 섹션마다 로더가 있어도 된다 [S18] — 실패도 섹션 단위로.
- 값이 못 온 셀은 "-"(empty value) [S23]. 계산에 들어가지 않는 값은 결과에 "일부 지표 제외" 표시. (권장, 근거 약함)
- 자동 재시도는 백오프로 조용히, 사용자에게는 수동 재시도 버튼 하나. (권장, 근거 약함)

**Do**
- 지표 타일 8개 중 1개 실패: 그 타일만 "공시가격 조회 실패 · 하루 한도 초과 [다시 시도]", 나머지 7개 정상, 종합 판정에 "공시가격 제외" 꼬리표.
- 지도 레이어 하나 실패: 범례에 그 레이어만 회색 + 경고 아이콘, 지도는 그대로.

**Don't**
- 타일 하나 실패를 전면 에러 페이지로 [S24].
- 실패한 타일을 조용히 빼서 빈 자리로 두기 — 사용자가 "원래 없는 지표"로 오해한다.
- 실패 타일마다 일러스트 + 3줄 설명 — 한 화면에 에러 그림 여러 개 [S5][S17].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| Cloudscape Errors | https://cloudscape.design/patterns/general/errors/ | 컴포넌트 단위 기능 에러 vs 페이지 알림 구분 |
| EUI EmptyPrompt (error loading) | https://eui.elastic.co/docs/components/display/empty-prompt/ | 로드 에러 타일의 재시도 행동 |

## 출처
| # | 출처 | URL | 확인일 | 라이선스/비고 |
|---|---|---|---|---|
| S1 | NN/g, Response Times: The 3 Important Limits | https://www.nngroup.com/articles/response-times-3-important-limits/ | 2026-10-08 | 저작권 유지(요약만) |
| S2 | NN/g, Skeleton Screens 101 | https://www.nngroup.com/articles/skeleton-screens/ | 2026-10-08 | 저작권 유지(요약만) |
| S3 | NN/g, Progress Indicators | https://www.nngroup.com/articles/progress-indicators/ | 2026-10-08 | 저작권 유지(요약만) |
| S4 | NN/g, Error-Message Guidelines | https://www.nngroup.com/articles/error-message-guidelines/ | 2026-10-08 | 저작권 유지(요약만) |
| S5 | IBM Carbon, Empty states pattern | https://carbondesignsystem.com/patterns/empty-states-pattern/ | 2026-10-08 | Apache-2.0 |
| S6 | IBM Carbon, Loading pattern | https://carbondesignsystem.com/patterns/loading-pattern/ | 2026-10-08 | Apache-2.0 |
| S7 | IBM Carbon, Loading component usage | https://carbondesignsystem.com/components/loading/usage/ | 2026-10-08 | Apache-2.0 |
| S8 | IBM Carbon, Notification pattern | https://carbondesignsystem.com/patterns/notification-pattern/ | 2026-10-08 | Apache-2.0 |
| S9 | Atlassian, Empty state usage | https://atlassian.design/components/empty-state/usage | 2026-10-08 | 미확인 |
| S10 | Atlassian, Spinner usage | https://atlassian.design/components/spinner/usage | 2026-10-08 | 미확인 |
| S11 | Atlassian, Skeleton usage | https://atlassian.design/components/skeleton/usage | 2026-10-08 | 미확인 |
| S12 | GitHub Primer, Empty states | https://primer.style/product/ui-patterns/empty-states/ | 2026-10-08 | MIT |
| S13 | GitHub Primer, Loading | https://primer.style/product/ui-patterns/loading/ | 2026-10-08 | MIT |
| S14 | GOV.UK, Error summary | https://design-system.service.gov.uk/components/error-summary/ | 2026-10-08 | MIT(GOV.UK Frontend) |
| S15 | GOV.UK, Page not found pages | https://design-system.service.gov.uk/patterns/page-not-found-pages/ | 2026-10-08 | MIT(GOV.UK Frontend) |
| S16 | GOV.UK, Problem with the service pages | https://design-system.service.gov.uk/patterns/problem-with-the-service-pages/ | 2026-10-08 | MIT(GOV.UK Frontend) |
| S17 | Elastic EUI, EmptyPrompt | https://eui.elastic.co/docs/components/display/empty-prompt/ | 2026-10-08 | 미확인 |
| S18 | Elastic EUI, Loading | https://eui.elastic.co/docs/components/display/loading/ | 2026-10-08 | 미확인 |
| S19 | Ant Design, Empty | https://ant.design/components/empty | 2026-10-08 | MIT(코드) / 문서 미확인 |
| S20 | Ant Design, Skeleton | https://ant.design/components/skeleton | 2026-10-08 | MIT(코드) / 문서 미확인 |
| S21 | Ant Design, Result | https://ant.design/components/result | 2026-10-08 | MIT(코드) / 문서 미확인 |
| S22 | AWS Cloudscape, Loading and refreshing | https://cloudscape.design/patterns/general/loading-and-refreshing/ | 2026-10-08 | 미확인(코드는 Apache-2.0) |
| S23 | AWS Cloudscape, Empty states | https://cloudscape.design/patterns/general/empty-states/ | 2026-10-08 | 미확인(코드는 Apache-2.0) |
| S24 | AWS Cloudscape, Errors | https://cloudscape.design/patterns/general/errors/ | 2026-10-08 | 미확인(코드는 Apache-2.0) |

읽기 실패로 뺀 출처: Carbon Skeleton states usage(404), GOV.UK patterns/problem-pages(404 → 위 S15·S16으로 대체), Adobe Spectrum progress-circle·illustrated-message(404), Salesforce Lightning empty-state·loading(JS 렌더, 본문 없음), Polaris skeleton-page·empty-state(301 → shopify.dev 허브).
