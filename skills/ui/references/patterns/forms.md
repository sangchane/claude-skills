# 폼·입력 (Forms / Input)

> 언제 읽나: 매물 기록·설정·로그인·조건 입력처럼 사용자가 값을 치고 저장하는 화면을 만들 때. 필터 바의 입력칸은 filter-search-sort.md와 같이 본다.
> 확인일 2026-10-08. 출처는 맨 아래. 수치 옆 [S1] 같은 표시는 출처 번호, 표시 없는 수치는 "권장(근거 약함)".

색·그림자·서체·모노 숫자 같은 하드룰은 SKILL.md·tokens.md에 있다. 여기선 "무엇을 어디에 몇 개, 무엇을 숨기나"만 쓴다.

## 1. 레이아웃 — 한 열, 라벨 위, 폭은 입력 길이

**언제 쓰나** — 필드 2개 이상인 모든 폼.

**규칙(측정 가능)**
- 한 열(single column)이 기본. 다열은 오독이 잦고 화면 확대 사용자가 둘째 열을 놓친다 [S1][S10][S13][S15][S25].
- 한 줄에 묶어도 되는 예외: 성/이름, 시·구·우편번호처럼 짧고 논리적으로 한 덩어리인 필드만 [S1][S10].
- 라벨은 필드 바로 위, 왼쪽 정렬 [S10][S13][S14][S25]. 라벨 끝에 콜론 금지, 문장형 대소문자 [S11][S21]. 라벨은 최대 3단어 [S15].
- 라벨-필드 간격 < 필드-필드 간격 — 가까운 것이 묶여 보인다 [S4]. 필드 사이 24~32px, 섹션 사이 32~40px [S10]. 마지막 필드와 버튼 사이 48px 이상 [S10].
- 필드 폭은 예상 입력 길이에 맞춘다 [S1][S11][S26]. 폭 단계 예: USWDS 5/9/13/20/30/40/50ex [S26], Atlassian 75/150/250/350/500px [S13], GOV.UK width-5/10/20 [S21].
- 짧은 값(우편번호·연도·호수)에 전체 폭 필드를 쓰지 않는다 — 폭이 "얼마나 쓰라"는 힌트 [S26].
- 선택지 2~3개는 드롭다운 대신 라디오 [S1]. 드롭다운은 5~15개일 때 (권장, 근거 약함).
- 설명이 긴 설정 폼은 "왼쪽 제목+설명 / 오른쪽 필드" 2단, 최대 폭 800px, 비율 1:1 또는 1:2 [S30]. 모바일에선 세로로 쌓인다 [S30].
- 필드 순서는 중요도순, 관련 필드는 인접, 가장 흔한 선택지를 먼저 [S1][S15].

**Do**
- 필드를 줄인다 — 필드 하나를 지울 때마다 전환율이 오른다 [S1]. 유도 가능·나중에 받을 수 있는 값은 빼라.
- 관련 필드를 `fieldset`+`legend`로 묶고 제목을 준다 [S25][S10].
- 스마트 기본값(사용자 지역·직전 입력)을 미리 채운다 [S13][S8].

**Don't**
- 15개 필드를 한 덩어리로 늘어놓지 않는다 — 3개 섹션으로 쪼개면 짧아 보인다 [S4]. 사용자 지적 "텍스트·정보를 한 페이지에 나열해 너무 많다".
- 세로 공간 아끼려고 2열로 접지 않는다 [S15].
- 라벨을 오른쪽 정렬하거나 필드에서 멀리 두지 않는다 [S4].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| IBM Carbon Forms | https://carbondesignsystem.com/patterns/forms-pattern/ | 한 열, 라벨 위, 간격 수치 |
| USWDS Text input | https://designsystem.digital.gov/components/text-input/ | 폭 7단계(ex 단위) |
| Elastic EUI Form layouts | https://eui.elastic.co/docs/components/forms/layouts/guidelines | 제목·설명 왼쪽 / 필드 오른쪽 2단 |

## 2. 필수/선택 표기·플레이스홀더·도움말 vs 툴팁

**언제 쓰나** — 필드마다 "꼭 써야 하나, 뭘 써야 하나"를 알려야 할 때.

**규칙(측정 가능)**
- 소수만 표기한다: 대부분 필수면 선택 필드에만 "(선택)", 대부분 선택이면 필수에만 "(필수)" [S10]. GOV.UK는 항상 "(optional)"만 붙이고 별표 금지 [S18][S22]. 한 제품 안에서 방식 하나로 통일 [S10].
- 별표를 쓰면 라벨 앞에, 빨간색, 폼 머리에 범례 1줄("* 표시는 필수") [S5][S13][S25]. "모든 항목 필수" 같은 상단 안내문만으로는 안 된다 — 안 읽는다 [S5].
- 로그인 폼(필드 2개)은 표기 생략 가능 [S5][S15].
- 플레이스홀더를 라벨 대신 쓰지 않는다 — 입력하면 사라져 기억에 의존하고, 채워진 것으로 오해한다 [S3][S1][S14][S26]. 예외: 검색창(아이콘+접근성 라벨 있을 때) [S13][S14].
- 플레이스홀더를 쓴다면 형식 예시만("YYYY-MM-DD") [S10][S30]. 기본은 "표시 안 함" [S11].
- 도움말(힌트)은 필드 아래(GOV.UK는 라벨 아래·필드 위) 항상 보이는 텍스트, 한 문장·최대 두 문장 [S21][S30]. 마침표·링크 없이 [S21].
- 과제 완료에 꼭 필요한 정보는 툴팁에 넣지 않는다 — "툴팁을 찾아야 과제를 끝낼 수 있으면 안 된다" [S6][S10]. 툴팁은 보충 정보만, i 아이콘, 마우스·키보드 모두로 열림 [S6][S10].
- 에러 메시지가 뜨면 같은 자리의 도움말은 치운다(중복 줄임) [S11][S15].

**Do**
- 형식 요구(비밀번호 규칙·전화번호 형식)는 도움말로 미리 보여 준다 [S1][S14].
- 도움말이 라벨과 같은 말이면 지운다 [S15].

**Don't**
- 필드마다 설명 문장을 2~3줄씩 상시 노출하지 않는다 — 사용자 지적 "설명은 궁금해서 클릭했을 때만". 한 줄 힌트 + 나머지는 툴팁/접기.
- 힌트에 긴 설명을 넣지 않는다 — 스크린리더가 전부 읽는다. 긴 설명은 본문 문단으로 [S18][S21].
- 툴팁을 어떤 필드엔 달고 어떤 필드엔 안 달지 않는다 — 일관성 [S6].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| GOV.UK Text input | https://design-system.service.gov.uk/components/text-input/ | 라벨·힌트·플레이스홀더 금지 이유 |
| NN/g 플레이스홀더 | https://www.nngroup.com/articles/form-design-placeholders/ | 라벨 대체 시 7가지 문제 |
| Carbon Forms | https://carbondesignsystem.com/patterns/forms-pattern/ | "소수만 표기" 규칙, 툴팁 제한 |

## 3. 검증 시점·에러 메시지·에러 요약

**언제 쓰나** — 제출 가능한 모든 폼.

**규칙(측정 가능)**
- 기본 시점은 제출 시(submit) [S15][S22]. 인라인 검증을 쓰면 **필드를 떠난 뒤(blur)**, 타이핑 중에는 띄우지 않는다 [S2][S10][S14][S30]. 첫 blur 이후부터만 인라인 [S15]. 상호작용 전 필드에 에러 표시 금지 [S26].
- 검증이 1초 넘게 걸리면 로딩 표시 [S15]. 서버 검증은 항상 별도로 [S22].
- 에러 메시지 위치: 해당 필드 바로 옆(GOV.UK: 힌트 뒤·입력 앞, 빨간 세로선으로 연결) [S2][S19]. 요약만 두고 필드 옆을 생략하지 않는다 [S2].
- 에러 3개 이상이면 폼 맨 위에 요약(각 항목이 필드로 링크) [S15]. GOV.UK는 1개여도 항상 요약, 제목 "There is a problem", 페이지 로드 시 요약으로 포커스, `<title>` 앞에 "Error: " [S20][S22].
- 요약의 문구와 필드 옆 문구는 글자 그대로 같게 [S19][S20].
- 메시지 내용: 무엇이 잘못됐고 어떻게 고치나 [S2][S19]. 형식 예: 비었음 "○○을 입력하세요" / 길이 "○○은 N자 이하여야 합니다" / 숫자 아님 "○○은 숫자여야 합니다(예: 30)" [S21][S23].
- 금지어: "유효하지 않은", "잘못된 요청", "please/sorry", 기술 용어, 유머 [S19]. "성을 입력하세요"가 "성은 필수 항목입니다"보다 낫다 [S19].
- 색 + 아이콘 + 테두리 세 가지로 표시(색만으로 구분 금지) [S2][S11]. 긴 폼에선 에러 필드 배경을 살짝 다르게 [S2].
- 사용자가 입력한 값은 에러 후에도 지우지 않는다 [S1][S19][S22].
- 제출 버튼을 비활성화하지 않는다 — 뭘 해야 할지 모른다, 탭 포커스도 안 된다 [S13][S15][S16][S28].
- 입력 형식은 관대하게 받는다(공백·하이픈 자동 제거, 애매하지 않으면 통과) [S22]. HTML5 `required`·브라우저 기본 검증은 끄고(`novalidate`) 직접 메시지 [S22].

**Do**
- 라디오·체크박스 그룹은 그룹당 에러 1개 [S15]. 요약에서 그룹은 첫 옵션으로 링크 [S20].
- 에러 아이콘에만 짧은 펄스 애니메이션(텍스트는 흔들지 않음) [S2].

**Don't**
- 타이핑 첫 글자에서 "형식이 틀렸습니다"를 띄우지 않는다 [S2][S22].
- 에러를 모달·토스트로만 알리지 않는다 — 필드 옆에 있어야 고치면서 본다 [S2].
- 제출 실패 시 폼을 초기화하지 않는다 [S15][S16].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| GOV.UK Error summary | https://design-system.service.gov.uk/components/error-summary/ | 위치·포커스·링크·제목 |
| GOV.UK Error message | https://design-system.service.gov.uk/components/error-message/ | 문구 규칙, 금지어 |
| GitHub Primer Forms | https://primer.style/ui-patterns/forms/overview | submit 기본, blur 후 인라인, 3개 이상 요약 |

## 4. 숫자·단위·글자수 입력

**언제 쓰나** — 가격·면적·지분·연식·전화번호처럼 숫자를 받을 때.

**규칙(측정 가능)**
- `<input type="number">`를 쓰지 않는다(스크롤로 값이 바뀌는 사고). 정수는 `inputmode="numeric"`, 소수는 `inputmode="decimal"`(음수 필요 시 제외) [S21].
- 증감(±) 버튼형 숫자 입력은 현재 값에서 몇 단계 조정할 때만. 넓은 범위(1~30 이상)·정확한 값(가격·거리)은 텍스트형 숫자 입력 [S12].
- 단위·통화는 접두/접미사로 입력칸 **밖**에 붙인다(원·만원·㎡·%) [S21][S27]. 접미사는 `aria-hidden`이므로 라벨이나 힌트에도 단위를 쓴다("면적(㎡)") [S21][S27].
- 접미사는 범용 기호·약어가 있을 때만. 답이 "환불" 같은 자유 서술일 수 있으면 금지 [S27].
- 천단위 구분·공백·하이픈은 입력 시 허용하고 저장 전 제거한다 [S22]. 표시할 때는 천단위 구분해 보여 준다 (권장, 근거 약함; 숫자 서체는 SKILL.md).
- 소수 자릿수가 정해진 값(원 단위 금액 123.45)은 에러 문구에 자릿수를 명시 [S21].
- `maxlength`로 잘라내지 않는다(잘렸는지 모른다). 글자수 제한은 카운터로 [S21][S23].
- 글자수 카운터는 법적·기술적 상한이 있거나 과잉 입력 증거가 있을 때만. 상한의 75% 같은 임계부터 표시 가능, 초과 입력 자체는 허용하고 메시지 [S23]. 카운터가 있는 Carbon 텍스트영역은 상한에서 입력을 막는다 [S11] — 둘 중 하나로 정해 통일.
- 참조번호·이름·코드는 `spellcheck="false"` [S21]. 복사·붙여넣기 막지 않는다 [S21].
- 숫자 필드 폭은 자릿수+단위에 맞춰 짧게(5~13ex) [S26].

**Do**
- 범위가 있으면 힌트에 최소·최대를 적는다 [S12].
- 기본값이 있으면 넣는다(수량 1 등) [S12].

**Don't**
- 가격을 슬라이더나 ± 버튼으로만 받지 않는다 [S12] (filter-search-sort.md 3절).
- 단위를 플레이스홀더에만 쓰지 않는다 — 입력하면 사라진다 [S3].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| GOV.UK Text input | https://design-system.service.gov.uk/components/text-input/ | inputmode, prefix/suffix, 에러 문구 서식 |
| USWDS Input prefix/suffix | https://designsystem.digital.gov/components/input-prefix-suffix/ | 단위를 라벨에도 쓰는 규칙 |
| Carbon Number input | https://carbondesignsystem.com/components/number-input/usage/ | ± 입력과 텍스트 입력의 경계 |
| GOV.UK Character count | https://design-system.service.gov.uk/components/character-count/ | 임계 % 표시, 초과 허용 |

## 5. 긴 폼 분할 — 섹션·단계·한 페이지 한 질문

**언제 쓰나** — 필드 8개를 넘거나, 주제가 2개 이상이거나, 앞 답에 따라 뒤 질문이 바뀔 때 (개수는 권장, 근거 약함).

**규칙(측정 가능)**
- 1단계: 같은 페이지 안에서 섹션 제목 + 간격(섹션 사이 32~40px)으로 나눈다 [S10][S30][S4].
- 2단계: 주제가 다르거나 앞 답이 뒤를 바꾸면 페이지(단계)로 나눈다. 한 화면에 한 주제(micro-topic) [S28]. GOV.UK는 한 페이지 한 질문, 질문을 h1으로 [S18].
- 단계가 있으면 진행 표시(현재 단계 강조, 짧은 라벨) [S8][S28]. 앞 단계를 끝내기 전에 뒤 단계로 못 건너뛰게 [S8].
- 각 단계는 다른 화면·이전 단계의 정보 없이 완결돼야 한다 [S8]. 도움말은 폼을 가리지 않는 옆 영역에 [S8].
- 중간 저장·나중에 이어하기를 둔다 [S8][S28]. 직전 입력값을 다음 사용 때 기본값으로 [S8].
- 제출 직전 "답변 확인" 페이지: 섹션별 요약 목록 + 섹션마다 "변경" 링크, 비어 있으면 "미입력" 표시, 제출 버튼은 "확인하고 보내기"처럼 구체 동사 [S24].
- 같은 정보를 두 번 묻지 않는다 — 미리 채우거나 이전 답을 보여 준다 [S18].
- 위저드는 초보·드문 작업(설정·온보딩)에만. 반복 작업·숙련자에겐 단일 폼 [S8].
- 쉬운 질문에서 어려운 질문 순으로 [S28].

**Do**
- 단계 버튼 라벨은 "다음" 대신 다음 단계 이름 또는 GOV.UK식 "계속" [S8][S18]. 왼쪽 정렬 [S18].
- 뒤로가기 링크를 페이지 상단에 두고, 돌아가면 입력값이 그대로 [S18].

**Don't**
- 한 페이지에 섹션 없이 질문 20개를 늘어놓지 않는다 — 사용자 지적 "한 페이지에 나열해 너무 많다".
- 폼 안에서 다른 페이지로 나가는 링크 뒤에 필수 정보를 숨기지 않는다 [S28].
- 입력 컨트롤을 disabled로 두지 않는다(대비·스크린리더 문제) [S28].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| GOV.UK Question pages | https://design-system.service.gov.uk/patterns/question-pages/ | 한 페이지 한 질문, h1=라벨, Continue |
| GOV.UK Check answers | https://design-system.service.gov.uk/patterns/check-answers/ | 요약 목록 + 변경 링크 |
| USWDS Progress easily | https://designsystem.digital.gov/patterns/complete-a-complex-form/progress-easily/ | 작은 덩어리·진행 표시·저장 후 재개 |
| NN/g Wizards | https://www.nngroup.com/articles/wizards/ | 언제 위저드를 쓰고 쓰지 않나 |

## 6. 저장/취소 버튼·기본 버튼·자동 저장

**언제 쓰나** — 폼의 마지막 줄. 버튼 위치와 저장 방식이 화면마다 다르면 사용자가 매번 찾는다.

**규칙(측정 가능)**
- 폼당 저장(제출) 버튼 1개 [S16]. 라벨은 "저장"·"만들기"·"보내기" 같은 동사, "제출/OK" 금지 [S13][S16][S7].
- 위치: 페이지 안 폼 = 왼쪽 정렬, 기본(primary) 버튼이 왼쪽·취소가 오른쪽 [S10][S16][S18]. 다이얼로그·사이드 패널 = 오른쪽 정렬, 취소 왼쪽·기본 오른쪽 [S10][S16]. 인라인 편집 = 입력칸 바로 옆 [S16]. 한 제품 안에서 한 규칙 [S7].
- 기본 버튼은 시각적으로 하나만 강조. 파괴적 동작은 기본 버튼으로 두지 않는다 [S7].
- 취소는 링크 스타일로 약하게 [S13][S1]. 리셋/초기화 버튼은 두지 않는다 — 실수로 지우는 위험이 더 크다 [S1][S9].
- 저장 버튼은 폼이 비어 있거나 틀려도 활성 [S16][S13]. 전송 중에는 스피너 [S13].
- 명시적 저장이 기본. 텍스트·체크박스·라디오·셀렉트는 저장 버튼 [S16]. 토글·세그먼트·단일 선택 드롭다운처럼 "즉시 효과" 컨트롤만 자동 저장 [S16]. 한 페이지에 두 방식을 섞지 않는다 [S16].
- 자동 저장이면 저장됨 표시를 컨트롤 옆에 두고, 결과가 화면 안에서 안 보이면 인라인 메시지/배너 [S16]. 파괴적 자동 저장에는 실행 취소 [S16].
- 저장 안 한 변경이 있으면 페이지 이탈 시 경고(`beforeunload`) [S16].
- 저장 실패 시 입력값 보존 + 실패 이유 표시, 필드와 버튼은 계속 활성 [S15][S16].

**Do**
- 저장 후 화면이 그대로면 "저장됨" 1줄, 다른 페이지로 가면 배너 [S16].
- 폼 일부만 저장하는 버튼은 secondary [S16].

**Don't**
- 긴 설정 페이지에 섹션마다 저장 버튼을 두면서 상단에도 전체 저장을 두지 않는다 — 저장 버튼 1개 [S16].
- 저장 버튼을 조건 충족 전까지 회색으로 잠그지 않는다 [S15][S16].
- 뒤로가기만으로 빠져나갈 수 있는 1페이지 폼에 큰 취소 버튼을 두지 않는다 [S9].

**실제 예시**
| 제품/시스템 | URL | 무엇을 볼 것 |
|---|---|---|
| GitHub Primer Saving | https://primer.style/product/ui-patterns/saving/ | 명시/자동 저장 구분, 버튼 위치 3가지, 비활성 금지 |
| Carbon Forms | https://carbondesignsystem.com/patterns/forms-pattern/ | 페이지 폼 왼쪽 / 다이얼로그 오른쪽 |
| NN/g OK-Cancel | https://www.nngroup.com/articles/ok-cancel-or-cancel-ok/ | 플랫폼 관례 우선, 기본 버튼 강조 |

## 출처
| # | 출처 | URL | 확인일 | 라이선스/비고 |
|---|---|---|---|---|
| S1 | NN/g, Website Forms Usability: Top 10 | https://www.nngroup.com/articles/web-form-design/ | 2026-10-08 | 저작권 유지, 요약만 |
| S2 | NN/g, Error-Message Guidelines (forms) | https://www.nngroup.com/articles/errors-forms-design-guidelines/ | 2026-10-08 | 저작권 유지, 요약만 |
| S3 | NN/g, Placeholders in Form Fields Are Harmful | https://www.nngroup.com/articles/form-design-placeholders/ | 2026-10-08 | 저작권 유지, 요약만 |
| S4 | NN/g, Form Design: White Space | https://www.nngroup.com/articles/form-design-white-space/ | 2026-10-08 | 저작권 유지, 요약만 |
| S5 | NN/g, Marking Required Fields | https://www.nngroup.com/articles/required-fields/ | 2026-10-08 | 저작권 유지, 요약만 |
| S6 | NN/g, Tooltip Guidelines | https://www.nngroup.com/articles/tooltip-guidelines/ | 2026-10-08 | 저작권 유지, 요약만 |
| S7 | NN/g, OK-Cancel or Cancel-OK | https://www.nngroup.com/articles/ok-cancel-or-cancel-ok/ | 2026-10-08 | 저작권 유지, 요약만 |
| S8 | NN/g, Wizards | https://www.nngroup.com/articles/wizards/ | 2026-10-08 | 저작권 유지, 요약만 |
| S9 | NN/g, Reset and Cancel Buttons | https://www.nngroup.com/articles/reset-and-cancel-buttons/ | 2026-10-08 | 저작권 유지, 요약만(2000년 글) |
| S10 | IBM Carbon, Forms pattern | https://carbondesignsystem.com/patterns/forms-pattern/ | 2026-10-08 | Apache-2.0(Carbon) |
| S11 | IBM Carbon, Text input usage | https://carbondesignsystem.com/components/text-input/usage/ | 2026-10-08 | Apache-2.0(Carbon) |
| S12 | IBM Carbon, Number input usage | https://carbondesignsystem.com/components/number-input/usage/ | 2026-10-08 | Apache-2.0(Carbon) |
| S13 | Atlassian, Form usage | https://atlassian.design/components/form/usage | 2026-10-08 | 미확인 |
| S14 | Atlassian, Text field usage | https://atlassian.design/components/textfield/usage | 2026-10-08 | 미확인 |
| S15 | GitHub Primer, Forms overview | https://primer.style/ui-patterns/forms/overview | 2026-10-08 | MIT(Primer) |
| S16 | GitHub Primer, Saving | https://primer.style/product/ui-patterns/saving/ | 2026-10-08 | MIT(Primer) |
| S17 | GitHub Primer, TextInput | https://primer.style/product/components/text-input/ | 2026-10-08 | MIT(Primer) — 선행/후행 비주얼 참고만 |
| S18 | GOV.UK, Question pages | https://design-system.service.gov.uk/patterns/question-pages/ | 2026-10-08 | MIT(GOV.UK Frontend) |
| S19 | GOV.UK, Error message | https://design-system.service.gov.uk/components/error-message/ | 2026-10-08 | MIT(GOV.UK Frontend) |
| S20 | GOV.UK, Error summary | https://design-system.service.gov.uk/components/error-summary/ | 2026-10-08 | MIT(GOV.UK Frontend) |
| S21 | GOV.UK, Text input | https://design-system.service.gov.uk/components/text-input/ | 2026-10-08 | MIT(GOV.UK Frontend) |
| S22 | GOV.UK, Validation pattern | https://design-system.service.gov.uk/patterns/validation/ | 2026-10-08 | MIT(GOV.UK Frontend) |
| S23 | GOV.UK, Character count | https://design-system.service.gov.uk/components/character-count/ | 2026-10-08 | MIT(GOV.UK Frontend) |
| S24 | GOV.UK, Check answers | https://design-system.service.gov.uk/patterns/check-answers/ | 2026-10-08 | MIT(GOV.UK Frontend) |
| S25 | USWDS, Form | https://designsystem.digital.gov/components/form/ | 2026-10-08 | 퍼블릭도메인/CC0(USWDS 문서) |
| S26 | USWDS, Text input | https://designsystem.digital.gov/components/text-input/ | 2026-10-08 | 퍼블릭도메인/CC0(USWDS 문서) |
| S27 | USWDS, Input prefix/suffix | https://designsystem.digital.gov/components/input-prefix-suffix/ | 2026-10-08 | 퍼블릭도메인/CC0(USWDS 문서) |
| S28 | USWDS, Complete a complex form: Progress easily | https://designsystem.digital.gov/patterns/complete-a-complex-form/progress-easily/ | 2026-10-08 | 퍼블릭도메인/CC0(USWDS 문서) |
| S29 | Ant Design, Form | https://ant.design/components/form | 2026-10-08 | 미확인 — 기본 검증 트리거 onChange, vertical 권장(모바일) 참고만 |
| S30 | Elastic EUI, Form layouts guidelines | https://eui.elastic.co/docs/components/forms/layouts/guidelines | 2026-10-08 | 미확인 |

읽기 실패(출처에서 제외): Adobe Spectrum text-field(404, s2 도메인도 리다이렉트 후 404), EUI /form-layouts/(404, /layouts/guidelines로 대체), Salesforce Lightning data-entry(제목만 렌더, 본문 없음), Polaris form-layout·help-content·app-settings-layout(shopify.dev 허브로 리다이렉트), NN/g number-formatting(404), NN/g autosave(404), USWDS complete-a-complex-form 상위 페이지(개요만, 하위 progress-easily로 대체).
