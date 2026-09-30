# Godot 모바일 게임 UI

Godot 4 Control 노드로 폰 게임 UI를 만들 때 읽는다. 웹용 규칙(SKILL.md 3절의 Tailwind·React)은 적용하지 않고, dial과 "AI 티 안 나게"의 취지만 가져온다.
투박해지는 주원인은 결과를 보지 않고 노드를 쓰는 것이므로, 4절의 스크린샷 확인을 반드시 거친다.

## 1. 방향 먼저 (화면을 만들기 전에 한 번)

장르와 분위기(캐주얼·하드코어·귀여움·다크 판타지 등)를 한 줄로 정하고, 그에 맞춰 아래를 **Theme 리소스 하나**(`res://ui/theme.tres`)로 만든다.
프로젝트 설정 `gui/theme/custom`에 지정해 모든 Control이 따르게 한다.

- 색 5개: 배경 · 표면(패널) · 강조(주요 버튼) · 위험/경고 · 글자. 강조색은 한 화면에 한 곳.
- 폰트 1~2개: 한글이 들어가면 한글 글리프가 있는 폰트(Pretendard, Noto Sans KR 등)를 `res://`에 넣고 Theme 기본 폰트로. 숫자(점수·재화)는 굵게.
- 간격 단위 8px(기준 해상도 기준). 여백·간격은 8의 배수만.
- 버튼 StyleBoxFlat: 모서리 반경, 눌림(pressed)·비활성(disabled) 상태를 따로. 기본 회색 버튼을 그대로 두지 않는다.

노드마다 `theme_override_*`로 꾸미지 않는다. 한 곳을 바꾸면 전체가 따라와야 톤이 맞는다.

## 2. 하드룰

- **늘이기 설정**: `display/window/stretch/mode = canvas_items`, `aspect = expand`. 세로 게임이면 기준 해상도 720×1280(가로 게임은 1280×720)과 `display/window/handheld/orientation`을 맞춘다.
  expand여야 20:9 폰과 4:3 태블릿에서 검은 띠 없이 UI가 넓어진다.
- **배치는 컨테이너와 앵커로**: 좌표를 직접 넣은 `layout_mode = 0` + offset 배치를 쓰지 않는다. 화면 비율이 바뀌면 어긋난다.
  화면 가장자리 UI는 앵커 프리셋, 묶음은 VBox/HBox/Grid/MarginContainer.
- **노치·홈 바(안전 영역)**: 화면 가장자리에 붙는 UI는 전부 아래 SafeArea를 붙인 MarginContainer 안에 둔다. 배경 그림만 가장자리까지 채운다.
- **터치 크기**: 누르는 것은 최소 48dp. 기준 폭 720이면 1dp ≈ 2px이므로 `custom_minimum_size` 96×96 이상. 버튼끼리는 16px 이상 띄운다.
- **글자 크기**(기준 폭 720): 본문 32px 이상, 보조 26px 이상, 제목·점수 44px 이상. 폰에서 이보다 작으면 읽히지 않는다.
- **엄지 영역**: 자주 누르는 버튼(공격·확인·다음)은 화면 아래 1/3. 위쪽은 정보(재화·점수·일시정지).
- **반응감**: 누르면 반드시 반응한다. 눌림 크기 0.95 → 1.0 Tween(0.08초), 효과음, 중요한 동작은 `Input.vibrate_handheld(20)`. 화면 전환은 0.15~0.25초 페이드나 슬라이드.

```gdscript
# res://ui/safe_area.gd — 가장자리 UI를 감싸는 MarginContainer에 붙여 노치·홈 바만큼 여백을 준다.
extends MarginContainer

func _ready() -> void:
	_apply()
	get_viewport().size_changed.connect(_apply)

func _apply() -> void:
	var screen := Vector2(DisplayServer.screen_get_size())
	var safe := Rect2(DisplayServer.get_display_safe_area())
	if Engine.has_meta("safe_area_preview"):  # dev:ui 스크린샷 스크립트가 넣는 가짜 노치
		var p: Dictionary = Engine.get_meta("safe_area_preview")
		screen = p.screen
		safe = Rect2(0, p.top, screen.x, screen.y - p.top - p.bottom)
	var k := get_viewport_rect().size / screen  # 화면 픽셀 → UI 좌표
	add_theme_constant_override("margin_left", int(safe.position.x * k.x))
	add_theme_constant_override("margin_top", int(safe.position.y * k.y))
	add_theme_constant_override("margin_right", int((screen.x - safe.end.x) * k.x))
	add_theme_constant_override("margin_bottom", int((screen.y - safe.end.y) * k.y))
```

## 3. 흔한 투박함과 고치는 법

| 보이는 것 | 원인 | 고침 |
|---|---|---|
| 회색 기본 버튼, 기본 폰트 | Theme 없음 | 1절 Theme |
| 글자가 작고 흐림 | 기준 해상도 대비 폰트 크기 부족 | 2절 글자 크기 |
| 태블릿에서 UI가 한쪽에 몰림 | 좌표 배치, aspect keep | 컨테이너·앵커, aspect expand |
| 상단 재화가 노치에 가림 | 안전 영역 무시 | SafeArea |
| 누르는 게 헷갈림 | 상태별 스타일·반응 없음 | pressed 스타일, Tween, 소리 |
| 정보가 한 줄로 늘어섬 | 위계 없음 | 크기·굵기·색 3단계, 강조 한 곳 |

## 4. 화면 확인 (고칠 때마다)

스킬 폴더의 `scripts/godot_shots.gd`로 폰 두 종과 태블릿 한 종을 찍어 Read로 본다. 명령은 SKILL.md "Godot 모바일" 절에 있다.

- 빨간 띠(노치·홈 바) 아래에 글자나 버튼이 있으면 SafeArea가 빠졌거나 예전 버전이다(스크립트가 넣는 `safe_area_preview` 메타를 읽는 위 코드여야 한다).
- 세 장을 나란히 보고 겹침, 잘림, 한쪽 쏠림, 너무 작은 글자·버튼을 찾는다.
- 고치고 다시 찍는다. 세 번 돌려도 같은 문제가 남으면 사용자에게 화면을 보여 주고 방향을 묻는다.
- 스크립트는 `--script`로 돌아서 autoload를 직접 붙인다. 게임 진행 상태가 필요한 화면(결과창 등)은 그 상태를 만드는 테스트용 씬을 따로 두고 `scene=`으로 찍는다.
- 창이 뜨는 환경이 필요하다(`--headless`는 그리지 않는다). 실제 기기의 노치 위치는 기종마다 다르므로 마지막 확인은 실기기로 한다.
