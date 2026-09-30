# dev 규칙(rules.md)과 스킬을 Codex·Antigravity 전역 설정(또는 --project <폴더>면 그 저장소)으로 내보낸다. 다시 실행하면 최신본으로 덮어쓴다.
import os, re, shutil, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = ["ui", "setup"]  # design·build는 Claude 전용 절차(superpowers·서브에이전트)가 많아 규칙만 쓴다. guide는 Claude 플러그인 목록용
REMOVED = ["design", "build"]  # 예전 버전이 복사한 것은 지운다
MARK = ".dev-sangchane"  # 이 파일이 있는 스킬 폴더만 덮어쓴다
START, END = "<!-- dev:start -->", "<!-- dev:end -->"

TOOL = {
    "codex": """## 모델·effort·위임
- 모델과 reasoning effort는 사용자가 `/model`로 고른다. 나는 바꾸지 못한다. 모델 기본 effort로 시작하고, L 작업만 한 단계 올리는 게 맞다. L 작업을 기본보다 낮게 하고 있을 때만 `/model`로 올리라고 한 줄로 권한다.
- 스킬은 `$ui`, `$setup`으로 부르거나 요청에 맞으면 스스로 쓴다.""",
    "antigravity": """## 모델·모드·위임
- 모델과 사고 수준(Fast·Low·Medium·High)은 사용자가 모델 선택기에서 고른다. 나는 바꾸지 못한다. 모델 기본 수준으로 시작하고, L 작업만 한 단계 올리는 게 맞다. L 작업을 Fast나 Low로 하고 있을 때만 올리라고 한 줄로 권한다.
- 스킬 ui, setup은 요청에 맞으면 스스로 쓴다.""",
}
COMMON = "- `build`·`design`은 이 도구에 스킬로 없다. 그 등급의 괄호 안 단계를 직접 수행하고, design은 요구사항·아키텍처·API·테스트 설계를 문서로 먼저 쓰는 단계로 한다. 스킬 본문의 `dev:X`는 스킬 `X`다. 본문이 없는 다른 이름(`superpowers:*`, `ponytail:*`, `ecc:*`, `reviewer`·`deep`·`quick` 에이전트)을 가리키면, 그 이름이 뜻하는 단계를 직접 수행한다. 리뷰는 구현을 마친 뒤 diff만 다시 읽는 별도 단계로 한다."


def rules_for(tool):
    t = (REPO / "rules.md").read_text(encoding="utf-8")
    t = re.sub(r"<!--.*?-->\n*", "", t, flags=re.S)
    t = t.split("## 모델·effort·위임")[0]
    t = t.replace("(dev 플러그인 세션 시작 훅이 이미 넣어 둔다)", "").replace("`dev:", "`")
    t = re.sub(r"- superpowers 스킬은.*\n", "", t)
    return t.rstrip() + "\n\n" + TOOL[tool] + "\n" + COMMON + "\n"


def write_block(path, body):
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    block = f"{START}\n{body}{END}\n"
    if START in old and END in old:
        new = old[: old.index(START)] + block + old[old.index(END) + len(END) :].lstrip("\n")
    else:
        new = (old.rstrip() + "\n\n" if old.strip() else "") + block
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new, encoding="utf-8")


def copy_skills(dest):
    for name in REMOVED:
        if (dest / name / MARK).exists():
            shutil.rmtree(dest / name)
            print(f"  지움(예전 복사본): {dest / name}")
    for name in SKILLS:
        d = dest / name
        if d.exists() and not (d / MARK).exists():
            print(f"  건너뜀: {d} (같은 이름의 다른 스킬이 있음)")
            continue
        shutil.rmtree(d, ignore_errors=True)
        shutil.copytree(REPO / "skills" / name, d, ignore=shutil.ignore_patterns("eval", "evals", "__pycache__"))
        (d / MARK).write_text("dev@sangchane에서 복사됨. tools/export.py가 덮어쓴다.\n", encoding="utf-8")
        print(f"  스킬: {d}")


def main(tools, project=None):
    home = Path.home()
    for tool in tools:
        print(tool)
        if project:  # 원격·클라우드 에이전트용: 저장소 안에 넣어 커밋하면 매 작업 컨테이너에서 읽힌다
            if tool == "codex":
                write_block(project / "AGENTS.md", rules_for(tool))
                print(f"  규칙: {project / 'AGENTS.md'}")
            elif tool == "antigravity":
                p = project / ".agents" / "rules" / "dev.md"
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("---\ntrigger: always_on\n---\n\n" + rules_for(tool), encoding="utf-8")
                print(f"  규칙: {p}")
            else:
                sys.exit(f"알 수 없는 도구: {tool} (codex, antigravity 중에서)")
            copy_skills(project / ".agents" / "skills")
        elif tool == "codex":
            codex = Path(os.environ.get("CODEX_HOME", home / ".codex"))
            write_block(codex / "AGENTS.md", rules_for(tool))
            print(f"  규칙: {codex / 'AGENTS.md'}")
            copy_skills(home / ".agents" / "skills")
        elif tool == "antigravity":
            p = home / ".gemini" / "config" / "rules" / "dev.md"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("---\ntrigger: always_on\n---\n\n" + rules_for(tool), encoding="utf-8")
            print(f"  규칙: {p}")
            copy_skills(home / ".gemini" / "config" / "skills")
        else:
            sys.exit(f"알 수 없는 도구: {tool} (codex, antigravity 중에서)")


if __name__ == "__main__":
    args = sys.argv[1:]
    project = None
    if "--project" in args:
        i = args.index("--project")
        project = Path(args[i + 1]).resolve()
        del args[i:i + 2]
    main(args or ["codex", "antigravity"], project)
