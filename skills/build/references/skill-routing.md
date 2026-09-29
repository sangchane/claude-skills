# 스킬 배선과 충돌 우선순위

단계별로 붙이는 스킬은 `SKILL.md` "단계별로 붙이는 것" 표가 정본이다. 이 파일은 그 표가 담지 못하는 배선 세부와 충돌 규칙만 둔다.
구현 쪽은 superpowers·ponytail·Claude Code 번들 명령(`/code-review`, `/security-review`, `/verify`)만 쓴다. ecc 플러그인은 평소 꺼 두고
dev:design(L 신규 설계)에서만 켠다 — 언어별 패턴·리뷰어 변형은 superpowers·번들 명령과 겹쳐 구현 라우팅에서 뺐다(2026-09-29).
설치 여부·미배정은 `python ../../tools/skill_catalog.py`(이 스킬 폴더 기준)가 검사한다.

## PLAN 순서 규칙 (`superpowers:writing-plans`가 주지 않는 것)

1. 첫 작업 3개는 버티컬 슬라이스 — 핵심 여정 하나를 입력 → 저장 → 조회까지 얇게 끝까지.
2. 그다음은 Impact × Uncertainty가 큰 작업부터. 로그인·화면 다듬기는 보통 마지막.
3. 작업의 "됐다" = 빈/에러 상태 있음 + 저장 후 재조회 됨 + 다음 화면 스텁 있음.
로그인까지만 예쁘고 그 뒤에서 막히는 패턴은 1·2를 어겨서 생긴다.

## ponytail 배선 (BUILD·REVIEW)

- **설치**: dev 플러그인의 의존성이라 dev를 설치하면 같이 설치된다(`ponytail@sangchane`).
  훅이 매 세션·매 서브에이전트에 사다리를 주입하고 `/ponytail lite|full|ultra|off`로 강도를 바꾼다. 기본 full.
- **BUILD**: 문제를 다 읽은 뒤, 코드를 쓰기 전에 사다리를 탄다. 사다리는 해법을 줄이지 읽기를 줄이지 않는다.
- **REVIEW**: `/code-review`로 정확성을 본 뒤, 원하면 `ponytail:ponytail-review`로 삭제 후보만 받는다 (`net: -N lines`).
- **사다리 (플러그인 미설치 시 같은 기준)**: 1 필요한가(YAGNI) → 2 이 코드베이스에 이미 있나 → 3 표준 라이브러리 → 4 플랫폼 네이티브
  (`<input type="date">`, CSS, DB 제약) → 5 이미 설치된 의존성 → 6 한 줄로 되나 → 7 그제야 최소 코드. 첫 번째로 성립하는 단에서 멈춘다.
  줄이지 않는 것: 신뢰 경계의 입력 검증, 데이터 손실을 막는 에러 처리, 보안, 접근성, 명시 요청. 의도적 단순화에는 상한과 업그레이드 경로를 주석으로 남긴다.
  출처: DietrichGebert/ponytail v4.9.0 (MIT), `evidence.md`.

## 알려진 충돌과 우선순위

- **brainstorming 이중 트리거**: `superpowers:using-superpowers` 훅의 "만들자 → brainstorming 먼저"는 dev 규칙(`rules.md`)의 경계 규칙이 우선한다
  (superpowers 자신이 "사용자 지시 > 스킬"). M은 FRAME 3줄, L 신규는 design이 brainstorming을 대신한다.
- **질문 방식**: superpowers "한 번에 하나 + 구현 전 승인" vs design "배치 1회 ≤5" vs ponytail "기본값으로 진행하고 같은 응답에서 묻는다".
  → design 안에서는 배치. 그 밖에서는 dev 규칙대로 해석이 크게 갈릴 때만, 한 번에 하나씩.
- **테스트 양**: ponytail "검증 하나면 충분" vs superpowers TDD. → SPEC의 완료 기준·테스트 계획이 정한다. 사소한 한 줄은 테스트 없음.
- **리뷰 횟수**: `superpowers:requesting-code-review`·`/code-review`는 둘 다 리뷰어를 띄운다. → 정확성 1회는 둘 중 하나, 복잡도는 `ponytail:ponytail-review` 선택.
  돈·안전·법 고위험은 `/security-review` + dev:reviewer 에이전트 1명을 생성 모델과 다른 등급으로 더한다.
- **서브에이전트 과다**: `superpowers:subagent-driven-development`는 작업 1개에 서브에이전트 3개. → BUILD 기본은 `superpowers:executing-plans`(같은 세션), 상한은 `model-routing.md`.
- **판정자 편향**: ponytail 훅은 모든 서브에이전트에 사다리를 넣어 REVIEW·GATE 판정자가 "짧은 쪽 선호"를 가질 수 있다.
  판정 프롬프트에 "길이는 품질이 아니다"를 둔다(design `judge-prompt.md`). 코딩 에이전트로 한정하려면 `PONYTAIL_SUBAGENT_MATCHER`.
- **Karpathy 가이드라인 플러그인**: dev 규칙의 작업 원칙이 같은 내용의 Opus 5.5판이다. 프로젝트에 andrej-karpathy-skills 플러그인이 설치돼 있으면 끈다.

## 갱신 절차

1. `python ../../tools/skill_catalog.py`(이 스킬 폴더 기준) — 참조 스킬 미설치·미배정 확인.
2. 배선 변경 시 `evals/evals.json` 케이스로 확인.
3. 외부 스킬 채택 기준은 저장소 README "외부 스킬 흡수 기준".
