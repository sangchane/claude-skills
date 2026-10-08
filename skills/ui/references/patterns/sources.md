# UI 레퍼런스 출처 (무료) — 화면 만들기 전에 실제 사례 2~3개 보고 패턴 빌리기

확인일 2026-10-08 (표의 "확인일"도 같음). Mobbin(유료)은 쓰지 않는다. `design-md.md`의 awesome-design-md(색·서체 토큰)와 겹치지 않게 **화면 구성·흐름·상태 처리** 출처만 모았다.

규칙
- 확인용 페이지 접속만 한다. 대량 수집·스크래핑·스크린샷 일괄 저장은 하지 않는다.
- 남의 화면은 **패턴(배치·정보 위계·상태 처리)만 빌린다.** 브랜드·문구·이미지는 가져오지 않고, 스크린샷을 우리 저장소·공개물에 넣지 않는다. 인용은 URL + 한 줄 요약으로.
- "약관 미확인" = 약관 페이지를 읽지 못했다는 뜻. 허용으로 해석하지 않는다(보수적으로 "사람이 열어 보기"만).
- 표기: 실제 = 출시된 제품 화면 / 컨셉 = 시안(실제 아님) / 문서 = 가이드·코드.

## A. 에이전트가 작업 중 바로 쓸 추천 10곳

| # | 출처 | 왜 | 쓰는 법 |
|---|---|---|---|
| 1 | SaaSUI.design | 실제 SaaS 화면 3,500+, 유형별(대시보드·설정·온보딩·빈 상태·표·폼) 분류. **인증 없는 무료 MCP/API.** 인용 허용 | MCP 또는 `llms.txt`로 검색 → 해당 페이지 URL을 WebFetch로 읽고 요약·인용 |
| 2 | Component Gallery | 95개 디자인 시스템에서 60개 컴포넌트 2,671 예시. 컴포넌트 이름으로 "다른 시스템은 어떻게 만들었나" 비교 | WebFetch로 컴포넌트 페이지 읽기 |
| 3 | Carbon Design System (데이터 시각화·대시보드) | 차트 32종 선택 기준, 축·범례·색, 대시보드, 빈 상태·로딩 | WebFetch로 읽기, 규칙 인용 |
| 4 | Primer UI patterns (GitHub) | 데이터 시각화·빈 상태·폼·로딩·저하된 경험(degraded)·점진적 공개 | WebFetch로 읽기 |
| 5 | shadcn/ui Blocks | 대시보드·사이드바·로그인 코드 블록(MIT), 우리 스택(React·Tailwind)에 바로 맞음 | 코드 구조·배치 참고 |
| 6 | Tremor Blocks | KPI 카드 29, 필터바, 빈 상태, 표, 청구·사용량 페이지 등 300+ (무료·오픈소스) | 코드 구조·배치 참고 |
| 7 | Plausible 라이브 데모 `plausible.io/plausible.io` | 가입 없이 보는 **실제 분석 대시보드**(공개 데모) | 사람이 열어 보기 |
| 8 | Empty States (emptystat.es) | 실제 앱의 빈 상태 갤러리 | 사람이 열어 보기 / WebFetch |
| 9 | Pencil & Paper 아티클 | 대시보드·데이터 표·필터·빈 상태·로딩 UX 글(무료) | WebFetch로 읽고 요약 |
| 10 | Baymard 무료 글·예시 | 목록·필터·검색·상세 페이지 연구(이커머스 중심이나 "목록+필터" 판정 근거로 유용). 일부 유료 | WebFetch로 무료 글만, 요약·출처 표기 |

보조: GOV.UK Design System(폼·오류·확인 페이지, OGL), Ant Design 스펙(시각화 페이지·빈 상태, MIT), Page Flows 무료 둘러보기.

## B. 화면 유형별 어디서 찾나

| 화면 | 먼저 | 다음 |
|---|---|---|
| 대시보드 | SaaSUI `pattern/dashboard`(144장·80제품), Plausible 데모 | Carbon 대시보드·dataviz, Tremor KPI·차트 블록, Ant 시각화 페이지 |
| 리포트·판정 결과 | SaaSUI `pattern/analytics`, Carbon dataviz(게이지·미터·불릿) | Primer 데이터 시각화, Dashboard Design Patterns(학술 정리) |
| 목록+지도 | 사람이 직접: 호갱노노·직방·Zillow·Redfin·Airbnb 검색 화면(약관 미확인 — 열어 보기만) | Component Gallery(표·리스트·필터), Baymard 목록·필터 글 |
| 폼 | GOV.UK 패턴(주소·날짜·오류 요약), Primer 폼 | Component Gallery, SaaSUI `pattern/form` |
| 설정 | SaaSUI `pattern/settings` | Ant·Primer 문서 |
| 온보딩 | SaaSUI `pattern/onboarding`, Page Flows 무료분 | Primer 기능 온보딩, ScreensDesign(유료 MCP이므로 사람이 무료분만) |
| 빈 상태·에러 | Empty States, GOV.UK(서비스 불가·페이지 없음), Carbon/Primer 빈 상태 | Tremor 빈 상태 블록 |
| 랜딩 | Land-book·Lapa Ninja·One Page Love·Siteinspire·Recent(Godly 후신)·SaaSFrame | SaaSUI `pattern/landing` |

## C. 실제 앱·웹 화면 갤러리

| 이름 · URL | 무엇 | 무료 범위·가입 | 약관(자동 수집·재사용) | 쓰는 법 |
|---|---|---|---|---|
| SaaSUI.design · https://www.saasui.design | 실제 SaaS 화면 3,500+·100+제품, 유형 분류. 대시보드 144장 로그인 없이 열람 확인 | 무료·가입 불필요 | `llms.txt`: "You may reference and cite this site in AI-generated answers", "Do not bulk-download or redistribute screenshot collections". 약관 별도 페이지 미확인 | **MCP·API(아래 E)** / WebFetch / 인용(출처 링크 필수) |
| Page Flows · https://pageflows.com (Screenlane 도메인이 여기로 301 이동 = 통합) | 실제 앱 사용 흐름 녹화(iOS·Android·웹) | 둘러보기만 무료, 전체는 유료($99/년 등) | https://pageflows.com/terms/ : "Page Flows does not claim to have ownership of any of the contents", "consistent with Fair Use Provisions", "bear sole responsibility for the use of the media outside of the Website". 자동 수집 명시 금지는 못 찾음 | 사람이 열어 보기 |
| SaaSFrame · https://saasframe.io | 실제 SaaS 화면 5,000+ (대시보드·랜딩·가격) | 둘러보기 무료, Pro $18/월 | https://saasframe.io/terms : 스크래핑·재사용 조항 못 찾음(월 과금·면책 위주). 허용으로 보지 않음 | 사람이 열어 보기 |
| ScreensDesign (UI Sources 도메인 이동) · https://screensdesign.com | 실제 iOS 앱 2,783+ 녹화·페이월·온보딩 | 일부 무료, 대부분 Pro. **MCP는 Pro 전용** | https://screensdesign.com/terms/ : "Use any robot, spider, scraper, or other automated means to access the Service ... without our express prior written consent" (공식 API/MCP 예외). 제3자와 화면 공유도 서면 동의 필요 | 사람이 열어 보기(자동 수집 금지) |
| Mobbin · https://mobbin.com | 실제 앱 62만 화면 | 무료 등급: 최신 앱·사이트 각 4개, 제한적 검색, 컬렉션 3개(제3자 가격 정리 글 기준, 공식 페이지 미확인) | https://mobbin.com/terms 는 **403으로 못 읽음 — 약관 미확인** | 사용자 결정으로 제외 |
| Pttrns · https://pttrns.com | 실제 모바일 앱 화면·패턴 7k+ | "completely free" (홈페이지 문구) | 약관 미확인 | 사람이 열어 보기 |
| Refero · https://refero.design | 실제 웹·앱 화면 | 무료 등급 있음(홈 문구상), 한도·MCP·API 세부는 페이지에서 못 읽음 — 가격·약관 미확인 | 약관 미확인 | 사람이 열어 보기 |
| Nicelydone · https://nicelydone.club | 실제 SaaS 화면 21만+·흐름 8천+ | 라이브러리 가입 후 무료 열람, **MCP는 유료** | 약관 미확인 | MCP 쓰지 않음 |
| Navbar Gallery · https://www.navbar.gallery | 실제 사이트 내비게이션 예시 | 무료·가입 불필요(사이트에 유료 언급 없음) | 약관 미확인 | 사람이 열어 보기 |
| SaaS Pages · https://saaspages.xyz | 실제 SaaS 랜딩 섹션(헤더·가격·후기) | 무료 열람으로 보임 | 약관 미확인 | 사람이 열어 보기 |
| Landingfolio · https://www.landingfolio.com | 실제 랜딩 961+·컴포넌트 | 갤러리 무료, 템플릿 유료 | 푸터에 Terms·Licensing Agreement 있음, `/terms`는 404 → 약관 미확인 | 사람이 열어 보기 |
| One Page Love · https://onepagelove.com | 실제 원페이지 사이트 9천+·섹션 예시 9천+ (2008~) | 무료 열람 | 약관 미확인 | 사람이 열어 보기 |
| Siteinspire · https://www.siteinspire.com | 실제 웹사이트 갤러리 | 무료 열람 | 푸터에 개인정보 정책만 확인, 약관 미확인 | 사람이 열어 보기 |
| Recent.design (Godly가 여기로 301) · http://recent.design | 웹·브랜딩·모션 등 큐레이션(웹 UI 포함) | 무료 열람 | 약관 미확인 | 사람이 열어 보기 |
| Httpster · https://httpster.net | 실제 사이트 3,116 | 무료 열람 | 개인정보 정책만, 약관 미확인 | 사람이 열어 보기 |
| Dark Mode Design · https://www.darkmodedesign.com | 다크 모드 사이트 큐레이션 | 무료로 보임 | 약관 미확인 | 사람이 열어 보기(다크 테마 참고) |
| Collect UI · https://collectui.com | 사이트·인터페이스 큐레이션(일일), 컨셉/실제 구분 페이지에 없음 | 구독 옵션 있음, 무료 범위 미확인 | 약관 미확인 | 사람이 열어 보기 |
| Awwwards · https://www.awwwards.com | 수상 웹사이트(마케팅·인터랙션 중심, 대시보드 거의 없음) | 열람 무료, Pro 유료 | 약관 미확인 | 랜딩 참고용으로만 |
| UXArchive · https://uxarchive.com | **403으로 접속 실패** — 생존·내용 미확인 | - | 약관 미확인 | 제외 |
| Land-book · https://www.land-book.com | **403 접속 실패** — 미확인 | - | 약관 미확인 | 제외(사람이 브라우저로 열어 확인 가능) |
| Lapa Ninja · https://www.lapa.ninja | **403 접속 실패** — 미확인 | - | 약관 미확인 | 제외(사람이 브라우저로) |
| Screenlane | 독립 사이트 없음 (Page Flows로 이동) | - | Page Flows 항목 참조 | - |
| Dribbble · https://dribbble.com | **컨셉 시안 다수(실제 아님)** | 열람 무료 | https://www.dribbble.com/terms : "Copying, distributing, or disclosing any part of the Website ... by any automated or non-automated 'scraping'" 금지 | 레퍼런스로 쓰지 않음 |

## D. 대시보드·데이터·패턴 특화

| 이름 · URL | 무엇 | 무료·가입 | 약관·라이선스 | 쓰는 법 |
|---|---|---|---|---|
| Plausible 라이브 데모 · https://plausible.io/plausible.io | 실제 제품(분석)의 공개 대시보드 | 무료·가입 불필요 | 약관 미확인 | 사람이 열어 보기 |
| Grafana Play · https://play.grafana.org | 공개 데모로 알려졌으나 접속 시 "Error loading Grafana" — 지금 열리는지 미확인 | - | 약관 미확인 | 사람이 브라우저로 재확인 |
| Dashboard Design Patterns · https://dashboarddesignpatterns.github.io | 학술(IEEE TVCG 2023) 대시보드 패턴 정리, 치트시트. 실제 화면 아닌 분류 | 무료 | 라이선스 표기 못 찾음(약관 미확인) | WebFetch로 읽고 인용(출처 표기) |
| Tremor Blocks · https://blocks.tremor.so | KPI 카드·차트·필터바·빈 상태·표 300+ 코드 블록 | "free and open-source" | 저장소 `tremorlabs/tremor-blocks` MIT (GitHub API) | 코드·배치 참고 |
| shadcn/ui Blocks · https://ui.shadcn.com/blocks | 대시보드·사이드바·로그인 블록 | 무료 | MIT (`shadcn-ui/ui` LICENSE.md) | 코드·배치 참고 |
| From Data to Viz · https://www.data-to-viz.com | 데이터 형태별 차트 선택 의사결정 트리 | 무료 | 라이선스 미표기 | 사람이 열어 보기 / 차트 선택 근거 |
| Pencil & Paper 아티클 · https://www.pencilandpaper.io/articles | 대시보드·데이터 표·필터·빈 상태·로딩 UX | 무료 | 약관 미확인 | WebFetch 요약 |
| Empty States · https://emptystat.es | 실제 앱 빈 상태 갤러리(Gmail·Figma·Monzo 등) | 무료 | 약관 미확인 | 사람이 열어 보기 |

## E. 공개 디자인 시스템 (데이터 시각화·대시보드·폼·빈 상태 가이드 유무)

| 이름 · URL | 가이드 확인 | 라이선스 (확인 근거) | 쓰는 법 |
|---|---|---|---|
| IBM Carbon · https://carbondesignsystem.com | **데이터 시각화 32종**, 축·범례·색, 대시보드, 빈 상태·로딩 (`/data-visualization/getting-started/`). 대시보드 패턴 URL은 404 | 코드 Apache-2.0 (GitHub API). 문서 푸터 "Copyright © 2026 IBM" + IBM 이용약관 링크 — 문서 텍스트 재사용 조건 약관 미확인 | WebFetch, 규칙 요약·링크 |
| GitHub Primer · https://primer.style/product/ui-patterns/ | 데이터 시각화·빈 상태·폼·로딩·저하 경험·알림·점진적 공개·저장 | `primer/design` 저장소 MIT이나 **보관(archived)됨**; 문서 사이트는 열림 | WebFetch |
| GOV.UK · https://design-system.service.gov.uk/patterns/ | 폼 패턴(주소·날짜 등 10), 오류 복구, 확인·서비스 불가 페이지. 차트 가이드 없음 | 콘텐츠 "Open Government Licence v3.0, except where otherwise stated" | WebFetch, 인용 가능(출처 표기) |
| US Web Design System · https://designsystem.digital.gov | 복잡한 폼·프로필 패턴, 컴포넌트. 차트 가이드는 확인 못 함 | CC0 1.0 (공개 도메인, 폰트·일부 코드는 OFL·Apache·MIT) — `LICENSE.md` | WebFetch, 자유 인용 |
| Ant Design · https://ant.design/docs/spec/introduce | 데이터 표시, "Visualization Page" 템플릿, 폼 페이지, 빈 상태(Empty Status) | 코드 MIT (GitHub API); 문서 텍스트 조건은 약관 미확인 | WebFetch |
| Shopify Polaris · https://shopify.dev/docs/api/polaris | 접속한 페이지는 API 인덱스뿐 — 패턴 가이드 위치 미확인. 옛 `polaris-react.shopify.com/patterns`는 이 주소로 이동 | 저장소 라이선스 조회 실패 — 미확인 | 사람이 확인 |
| Atlassian · https://atlassian.design/foundations/ | 토큰·간격·색 위주. 접속한 페이지에 빈 상태·폼·시각화 언급 없음 | `/license` 링크만 있고 내용 미확인 | 보조 |
| Material 3 · https://m3.material.io | 접속은 됐으나 내용 못 읽음(레이아웃·빈 상태 가이드 유무 미확인) | 약관 미확인 | 사람이 열어 보기 |
| Microsoft Fluent 2 · https://fluent2.microsoft.design | 컴포넌트·Figma 키트·접근성 도구. 데이터 시각화·빈 상태 가이드는 확인 못 함 | `microsoft/fluentui` GitHub API가 NOASSERTION(라이선스 미판별), 사이트는 Microsoft 이용약관 링크 | 보조 |
| Adobe Spectrum · https://spectrum.adobe.com | "foundations, tokens, patterns, guidance" 언급만, 세부 미확인 | `spectrum-web-components` Apache-2.0(코드). 문서 약관 미확인 | 사람이 열어 보기 |
| Salesforce Lightning (SLDS 2) · https://www.lightningdesignsystem.com | 데이터 시각화·빈 상태·폼 가이드 언급 확인 (세부는 못 읽음) | `salesforce-ux/design-system` 저장소 보관됨, 라이선스 NOASSERTION | 사람이 열어 보기 |
| Elastic EUI · https://eui.elastic.co | Patterns 섹션 있음(내용 미확인) | Elastic License 2.0 + SSPL 이중 — **복사해 쓰지 말고 참고만** | 참고 |
| Grafana Saga · https://grafana.com/developers/saga/ | 접속했으나 내용 거의 안 읽힘 — 미확인 | 약관 미확인 | 사람이 열어 보기 |
| Base Web (Uber) · https://baseweb.design | 문서 내용 못 읽음 | 저장소 MIT (GitHub API), 마지막 푸시 2026-09 | 보조 |
| Radix · https://www.radix-ui.com | 접근성 프리미티브(패턴 가이드 아님) | `radix-ui/primitives` MIT | 접근성 동작 참고 |
| Awesome Design Systems · https://github.com/alexpate/awesome-design-systems | 200+ 디자인 시스템 목록 | Unlicense (GitHub API) | 새 시스템 찾을 때 |

## F. 패턴·UX 연구 아카이브

| 이름 · URL | 무엇 | 무료 범위 | 약관·재사용 | 쓰는 법 |
|---|---|---|---|---|
| UI-Patterns · https://ui-patterns.com | 입력·내비·데이터·온보딩 패턴 라이브러리 (2026-03 글 있음, 살아 있음) | 무료 | 푸터 © Learning Loop ApS, 콘텐츠 라이선스 미표기 | 요약·링크 인용 |
| Baymard Institute · https://baymard.com/blog | 이커머스·목록·검색 UX 연구, 무료 글 450+·예시 | 일부 무료, 벤치마크·도구는 유료 | 인용 정책 약관 미확인 | 무료 글만, 짧은 인용 + 출처 |
| Laws of UX · https://lawsofux.com | UX 원칙 30+ | 무료 | 라이선스 미표기(`/llms.txt`·`/about/`에 있을 수 있음, 미확인) | 원칙 이름 인용 |
| NN/g · https://www.nngroup.com | `/terms/`가 404라 약관 미확인. 접속 확인 못 함 | - | 약관 미확인 | 요약·링크만, 본문 복사 금지 |
| Component Gallery · https://component.gallery | 디자인 시스템 95개의 컴포넌트 2,671 예시 (changelog 있음, 살아 있음) | 무료 | 사이트 about에 콘텐츠 라이선스 없음 → 약관 미확인 | WebFetch로 비교, 링크 인용 |

## G. 에이전트용 MCP·API

| 이름 | 상태 | 설치 | 비고 |
|---|---|---|---|
| **SaaSUI.design MCP (무료, 인증 없음)** | `POST https://www.saasui.design/api/mcp` 호출해 응답 확인함(도구 `search_saas_designs` `list_applications` `get_application` `list_categories` `list_screen_types` `lookup_glossary`). `analytics dashboard`처럼 긴 질의는 0건, `dashboard`는 결과 있음 → **한 단어로 검색** | `claude mcp add --transport http saasui https://www.saasui.design/api/mcp` (HTTP 전송이라 이 형식 — 이 명령 자체는 실행해 보지 않음) | API: `https://www.saasui.design/api/agent/search?q=dashboard` (curl로 응답 확인). 마크다운 미러 `/markdown/*.md`, `/llms.txt` |
| UIZZE MCP | 무료 프리뷰 `https://uizze.com/mcp/preview`는 410 Gone(내려감, 글로 소개된 설치법은 stale). 전체 라이브러리는 토큰 필요 | - | 무료 레퍼런스 검색 용도로는 못 씀 |
| ScreensDesign MCP | Pro 전용 | - | 사용 안 함 |
| Nicelydone MCP | 유료 | - | 사용 안 함 |
| Mobbin MCP | 유료(제외) | - | - |
| Refero MCP | 검색 결과에서만 확인(비공식 `fidgetcoding-refero-mcp`, 사이트 색·서체 추출용으로 awesome-design-md와 겹침). 직접 확인 못 함 | - | 쓰지 않음 |

## H. 스킬에 넣을 때 쓰는 법 (제안)

1. 화면 유형을 정하고 B표에서 출처 2~3개를 고른다.
2. SaaSUI MCP/API로 `dashboard`·`settings`·`onboarding` 등 한 단어 검색 → 반환된 URL 2~3개를 WebFetch로 읽어 **배치·위계·상태 처리**를 3줄로 정리한다. 이미지는 저장하지 않는다.
3. 디자인 시스템 문서(Carbon·Primer·GOV.UK)는 규칙(차트 선택, 빈 상태 문구, 오류 요약)을 인용하고 URL을 남긴다.
4. 빌려 온 패턴은 `DESIGN.md` 토큰으로 다시 입히고, 출처 URL과 확인일을 화면 PR이나 DESIGN.md에 한 줄 남긴다.
5. 약관 미확인 출처는 에이전트가 읽지 말고 사람이 열어 본 뒤 말로 옮긴다.
