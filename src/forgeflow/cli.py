#!/usr/bin/env python3
"""CLI for forgeflow."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import sys
from pathlib import Path

from forgeflow import __version__


PACKAGE_ROOT = Path(__file__).resolve().parent
SHARED_DIR = PACKAGE_ROOT / "shared"
TEMPLATES_DIR = SHARED_DIR / "templates"
RUNTIME_README = SHARED_DIR / "runtime" / "README.md"
CURSOR_SKILLS_DIR = PACKAGE_ROOT / "targets" / "cursor" / "skills"
CODEX_SKILLS_DIR = PACKAGE_ROOT / "targets" / "codex" / "skills"
TEMPLATE_FILES = ("IDEA.md", "PLAN.md", "PROGRESS.md", "REVIEW.md", "SUMMARY.md")
VALID_STATUSES = {"idea", "planned", "in_progress", "review", "done", "dropped"}
REQUIRED_FRONTMATTER_KEYS = ("id", "title", "slug", "status", "created_at", "updated_at")
PLAN_PHASE_FIELDS = (
    "Goal",
    "Scope",
    "Dependencies",
    "Parallelizable",
    "Success definition",
    "Checkpoint",
    "Reopen alignment if",
    "Notes",
)
PLACEHOLDER_TOKENS = {
    "",
    "none",
    "null",
    "tbd",
    "n/a",
    "what user value are we trying to create?",
    "what is painful, unclear, or missing today?",
    "state the original goal in one concise paragraph.",
    "summarize what was achieved.",
    "main behavior changes",
    "test coverage added or updated",
    "important design decisions",
    "none, or clearly scoped follow-up items",
}


def _today() -> str:
    return dt.date.today().isoformat()


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    if not value:
        raise ValueError("slug must not be empty")
    return value


def _project_root(path_str: str | None) -> Path:
    return Path(path_str).resolve() if path_str else Path.cwd().resolve()


def _runtime_dir(project_root: Path) -> Path:
    return project_root / ".ai-workflow"


def _ideas_dir(project_root: Path) -> Path:
    return _runtime_dir(project_root) / "ideas"


def _features_dir(project_root: Path) -> Path:
    return _runtime_dir(project_root) / "features"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _parse_frontmatter(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    text = _read(path)
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def _has_nonempty_bullet(text: str, label: str) -> bool:
    pattern = rf"(?m)^- {re.escape(label)}:[ \t]*([^\n]+?)?[ \t]*$"
    match = re.search(pattern, text)
    return bool(match and match.group(1) and not _looks_like_placeholder(match.group(1)))


def _has_header(text: str, header: str) -> bool:
    return re.search(rf"(?m)^#{{1,3}} {re.escape(header)}\s*$", text) is not None


def _extract_phase_blocks(plan_text: str) -> list[str]:
    matches = list(re.finditer(r"(?m)^## Phase .+$", plan_text))
    blocks: list[str] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(plan_text)
        blocks.append(plan_text[start:end])
    return blocks


def _looks_like_placeholder(value: str) -> bool:
    normalized = value.strip().lower()
    return normalized in PLACEHOLDER_TOKENS


def _validate_iso_date(value: str) -> bool:
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _render_template(name: str, slug: str, title: str, status: str) -> str:
    content = _read(TEMPLATES_DIR / name)
    today = _today()
    branch = f"codex/{slug}"
    return (
        content.replace("feature-example", f"feature-{slug}")
        .replace("Example Feature", title)
        .replace("example-feature", slug)
        .replace("2026-03-15", today)
        .replace("codex/example-feature", branch)
        .replace("status: idea", f"status: {status}", 1)
    )


def _ensure_runtime(project_root: Path) -> Path:
    runtime_dir = _runtime_dir(project_root)
    runtime_dir.mkdir(parents=True, exist_ok=True)
    _write(runtime_dir / "README.md", _read(RUNTIME_README))
    _write(runtime_dir / ".gitignore", "features/*/tmp/\n")
    _write(runtime_dir / "MANAGED_BY_FORGEFLOW", f"version={__version__}\n")
    _write(_ideas_dir(project_root) / ".gitkeep", "")
    _write(_features_dir(project_root) / ".gitkeep", "")
    return runtime_dir


def _print_next_steps(project_root: Path, export_cursor: bool) -> None:
    print("")
    print("Next steps:")
    print(f"  1. cd {project_root}")
    print("  2. forgeflow new-idea --slug <feature-name>")
    print("  3. forgeflow init-feature --slug <feature-name>")
    if export_cursor:
        print("  4. Open the project in Cursor or Codex and invoke the installed skills.")


def setup_project(args: argparse.Namespace) -> int:
    project_root = _project_root(args.project)
    runtime_dir = _ensure_runtime(project_root)
    if getattr(args, "export_cursor", False):
        export_cursor(argparse.Namespace(project=str(project_root), force=args.force))
    print(f"Initialized runtime at {runtime_dir}")
    _print_next_steps(project_root, getattr(args, "export_cursor", False))
    return 0


def new_idea(args: argparse.Namespace) -> int:
    project_root = _project_root(args.project)
    _ensure_runtime(project_root)
    slug = _slugify(args.slug)
    title = args.title or slug.replace("-", " ").title()
    path = _ideas_dir(project_root) / f"{_today()}-{slug}.md"
    if path.exists() and not args.force:
        print(f"idea file already exists: {path}")
        return 1
    _write(path, _render_template("IDEA.md", slug, title, "idea"))
    print(path)
    return 0


def init_feature(args: argparse.Namespace) -> int:
    project_root = _project_root(args.project)
    _ensure_runtime(project_root)
    slug = _slugify(args.slug)
    title = args.title or slug.replace("-", " ").title()
    feature_dir = _features_dir(project_root) / slug
    if feature_dir.exists() and not args.force:
        print(f"feature directory already exists: {feature_dir}")
        return 1
    feature_dir.mkdir(parents=True, exist_ok=True)
    status_by_file = {
        "IDEA.md": "idea",
        "PLAN.md": "planned",
        "PROGRESS.md": "in_progress",
        "REVIEW.md": "review",
        "SUMMARY.md": "done",
    }
    for name in TEMPLATE_FILES:
        _write(feature_dir / name, _render_template(name, slug, title, status_by_file[name]))
    print(feature_dir)
    return 0


def _feature_dir(project_root: Path, slug: str) -> Path:
    return _features_dir(project_root) / _slugify(slug)


def status(args: argparse.Namespace) -> int:
    project_root = _project_root(args.project)
    features_dir = _features_dir(project_root)
    if not features_dir.exists():
        print(f"features directory not found: {features_dir}")
        return 1
    if not args.slug:
        for path in sorted(p for p in features_dir.iterdir() if p.is_dir()):
            meta = _parse_frontmatter(path / "IDEA.md")
            print(f"{path.name}: {meta.get('status', 'unknown')}")
        return 0

    feature_dir = _feature_dir(project_root, args.slug)
    if not feature_dir.exists():
        print(f"feature not found: {feature_dir}")
        return 1

    idea = _parse_frontmatter(feature_dir / "IDEA.md")
    plan = _parse_frontmatter(feature_dir / "PLAN.md")
    print(f"feature: {feature_dir.name}")
    print(f"idea status: {idea.get('status', 'unknown')}")
    print(f"plan status: {plan.get('status', 'unknown')}")
    print(f"progress file: {'yes' if (feature_dir / 'PROGRESS.md').exists() else 'no'}")
    print(f"review file: {'yes' if (feature_dir / 'REVIEW.md').exists() else 'no'}")
    print(f"summary file: {'yes' if (feature_dir / 'SUMMARY.md').exists() else 'no'}")
    return 0


def _check_feature(feature_dir: Path) -> list[str]:
    findings: list[str] = []
    file_paths = {name: feature_dir / name for name in TEMPLATE_FILES}
    for name, path in file_paths.items():
        if not path.exists():
            findings.append(f"missing file: {name}")
    metas = {name: _parse_frontmatter(path) for name, path in file_paths.items()}
    texts = {name: _read(path) if path.exists() else "" for name, path in file_paths.items()}

    idea_meta = metas["IDEA.md"]
    idea_text = texts["IDEA.md"]
    plan_text = texts["PLAN.md"]
    progress_text = texts["PROGRESS.md"]
    review_text = texts["REVIEW.md"]
    summary_text = texts["SUMMARY.md"]
    progress_started = any(
        _has_nonempty_bullet(progress_text, label)
        for label in ("Active phase", "Last completed phase", "Next recommended action", "Handoff summary")
    )
    review_started = any(
        _has_nonempty_bullet(review_text, label)
        for label in ("Decision", "Blocking findings")
    ) or re.search(r"(?m)^## (Critical|Major|Minor)\n\n- (?!None\b).+", review_text) is not None
    summary_started = any(
        _has_nonempty_bullet(summary_text, label)
        for label in ("Final relevant test command(s)", "Final review status", "Merge or PR status")
    )

    for name, meta in metas.items():
        for key in REQUIRED_FRONTMATTER_KEYS:
            if key not in meta:
                findings.append(f"{name} missing frontmatter key: {key}")
        status = meta.get("status")
        if status and status not in VALID_STATUSES:
            findings.append(f"{name} has invalid status: {status}")
        for date_key in ("created_at", "updated_at"):
            if date_key in meta and not _validate_iso_date(meta[date_key]):
                findings.append(f"{name} has invalid {date_key}: {meta[date_key]}")

    if idea_meta.get("slug") and idea_meta.get("slug") != feature_dir.name:
        findings.append("IDEA.md slug does not match feature directory name")

    baseline = {key: idea_meta.get(key, "") for key in ("id", "title", "slug")}
    for name, meta in metas.items():
        for key in ("id", "title", "slug"):
            if meta.get(key) and baseline.get(key) and meta[key] != baseline[key]:
                findings.append(f"{name} {key} does not match IDEA.md")

    for header in ("Goal", "Success Signals", "Non-Goals", "Code Context", "Alignment Notes", "Decision Snapshot"):
        if not _has_header(idea_text, header):
            findings.append(f"IDEA.md missing {header} section")
    goal_match = re.search(r"(?s)# Goal\n\n(.+?)(?:\n# |\Z)", idea_text)
    if not goal_match or _looks_like_placeholder(goal_match.group(1).strip()):
        findings.append("IDEA.md goal is still placeholder or empty")
    success_signals = re.findall(r"(?m)^- .+\S$", idea_text.split("# Success Signals", 1)[1].split("#", 1)[0]) if "# Success Signals" in idea_text else []
    if len(success_signals) < 2:
        findings.append("IDEA.md success signals should contain at least two concrete bullets")
    non_goals = re.findall(r"(?m)^- .+\S$", idea_text.split("# Non-Goals", 1)[1].split("#", 1)[0]) if "# Non-Goals" in idea_text else []
    if len(non_goals) < 1:
        findings.append("IDEA.md should contain at least one non-goal bullet")
    for label in (
        "Initial interpretation",
        "User-confirmed intent",
        "Cost or complexity concerns raised during discussion",
        "Proposal",
        "Selected option",
        "Assumptions",
        "Reopen alignment if",
    ):
        if not _has_nonempty_bullet(idea_text, label):
            findings.append(f"IDEA.md missing alignment value for '{label}'")
    if "Question 1" in idea_text or "Question 2" in idea_text:
        findings.append("IDEA.md still contains template open questions")

    for header in ("Objective", "Success Criteria", "Alignment Loop", "Scope Contract", "Review Standard", "Execution Deltas", "Change Log"):
        if not _has_header(plan_text, header):
            findings.append(f"PLAN.md missing {header} section")
    objective_match = re.search(r"(?s)# Objective\n\n(.+?)(?:\n# |\Z)", plan_text)
    if not objective_match or _looks_like_placeholder(objective_match.group(1)):
        findings.append("PLAN.md objective is still placeholder or empty")
    success_bullets = re.findall(r"(?m)^- .+\S$", plan_text.split("# Success Criteria", 1)[1].split("#", 1)[0]) if "# Success Criteria" in plan_text else []
    if len(success_bullets) < 2:
        findings.append("PLAN.md success criteria should contain at least two concrete bullets")
    for label in (
        "Initial phase proposal",
        "User-confirmed success definition",
        "User-confirmed phase ordering",
        "Cost or scope tradeoffs discussed",
        "In scope",
        "Out of scope",
        "User-confirmed constraints",
        "Reopen alignment if",
    ):
        if not _has_nonempty_bullet(plan_text, label):
            findings.append(f"PLAN.md missing alignment value for '{label}'")

    phase_blocks = _extract_phase_blocks(plan_text)
    if not phase_blocks:
        findings.append("PLAN.md has no phase sections")
    for index, block in enumerate(phase_blocks, start=1):
        for field in PLAN_PHASE_FIELDS:
            if not _has_nonempty_bullet(block, field):
                findings.append(f"PLAN.md phase {index} is missing a non-empty '{field}' entry")

    if progress_started:
        for header in ("Current State", "Phase Journal"):
            if not _has_header(progress_text, header):
                findings.append(f"PROGRESS.md missing {header} section")
        for label in ("Active phase", "Last completed phase", "Next recommended action", "Handoff summary"):
            if not _has_nonempty_bullet(progress_text, label):
                findings.append(f"PROGRESS.md missing current state value for '{label}'")
        journal_matches = list(re.finditer(r"(?m)^## Phase \d+\s*$", progress_text))
        if not journal_matches:
            findings.append("PROGRESS.md phase journal headings should use '## Phase N'")
        for index, match in enumerate(journal_matches, start=1):
            start = match.start()
            end = journal_matches[index].start() if index < len(journal_matches) else len(progress_text)
            block = progress_text[start:end]
            for field in ("Started", "Completed", "Commit", "Tests", "Findings", "Plan updates", "Goal check", "Scope delta", "Handoff summary", "Next-phase impact"):
                if not _has_nonempty_bullet(block, field):
                    findings.append(f"PROGRESS.md phase journal {index} is missing a value for '{field}'")

    if review_started:
        if not _has_header(review_text, "Findings"):
            findings.append("REVIEW.md missing Findings section")
        if not _has_header(review_text, "Follow-up"):
            findings.append("REVIEW.md missing Follow-up section")
        if not _has_header(review_text, "Release Gate"):
            findings.append("REVIEW.md missing Release Gate section")
        for heading in ("Critical", "Major", "Minor"):
            if not _has_header(review_text, heading):
                findings.append(f"REVIEW.md missing {heading} subsection")
        for label in ("Additional phases needed", "Files to revisit", "Decision", "Ship ready"):
            if not _has_nonempty_bullet(review_text, label):
                findings.append(f"REVIEW.md missing follow-up value for '{label}'")
        if not re.search(r"(?m)^- Ship ready:\s*(yes|no)\s*$", review_text):
            findings.append("REVIEW.md release gate must mark ship readiness as 'yes' or 'no'")
        if re.search(r"(?m)^- Ship ready:\s*yes\s*$", review_text) and re.search(r"(?m)^## (Critical|Major)\n\n- (?!None\b).+", review_text):
            findings.append("REVIEW.md cannot be ship ready while critical or major findings remain")

    if summary_started:
        for header in ("Outcome", "Delivered", "Remaining Work", "Evidence"):
            if not _has_header(summary_text, header):
                findings.append(f"SUMMARY.md missing {header} section")
        outcome_match = re.search(r"(?s)# Outcome\n\n(.+?)(?:\n# |\Z)", summary_text)
        if not outcome_match or _looks_like_placeholder(outcome_match.group(1)):
            findings.append("SUMMARY.md outcome is still placeholder or empty")
        delivered_bullets = re.findall(r"(?m)^- .+\S$", summary_text.split("# Delivered", 1)[1].split("#", 1)[0]) if "# Delivered" in summary_text else []
        if len(delivered_bullets) < 2:
            findings.append("SUMMARY.md delivered section should contain at least two concrete bullets")
        for label in ("Final relevant test command(s)", "Final review status", "Merge or PR status"):
            if not _has_nonempty_bullet(summary_text, label):
                findings.append(f"SUMMARY.md missing evidence value for '{label}'")

    return findings


def doctor(args: argparse.Namespace) -> int:
    project_root = _project_root(args.project)
    features_dir = _features_dir(project_root)
    if not features_dir.exists():
        print(f"features directory not found: {features_dir}")
        return 1
    feature_dirs = [_feature_dir(project_root, args.slug)] if args.slug else sorted(p for p in features_dir.iterdir() if p.is_dir())
    has_error = False
    for feature_dir in feature_dirs:
        if not feature_dir.exists():
            print(f"feature not found: {feature_dir}")
            has_error = True
            continue
        findings = _check_feature(feature_dir)
        if findings:
            has_error = True
            print(f"[FAIL] {feature_dir.name}")
            for finding in findings:
                print(f"  - {finding}")
        else:
            print(f"[OK] {feature_dir.name}")
    return 1 if has_error else 0


def export_cursor(args: argparse.Namespace) -> int:
    project_root = _project_root(args.project)
    target_dir = project_root / ".cursor" / "skills"
    if target_dir.exists() and any(target_dir.iterdir()) and not args.force:
        print(f"cursor skills directory is not empty: {target_dir}")
        print("rerun with --force to replace forgeflow-managed skills")
        return 1
    target_dir.mkdir(parents=True, exist_ok=True)
    for skill_dir in CURSOR_SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        destination = target_dir / skill_dir.name
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(skill_dir, destination)
    _write(target_dir / ".forgeflow-managed", f"version={__version__}\n")
    print(f"Exported Cursor skills to {target_dir}")
    return 0


def install_codex(args: argparse.Namespace) -> int:
    codex_home = Path(args.codex_home or os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    skills_dir = codex_home / "skills"
    bin_dir = Path(args.bin_dir or Path.home() / ".local" / "bin").expanduser()
    skills_dir.mkdir(parents=True, exist_ok=True)

    for skill_dir in CODEX_SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        target = skills_dir / skill_dir.name
        if target.exists() or target.is_symlink():
            if not args.force:
                print(f"existing skill found: {target}")
                print("rerun with --force to replace forgeflow-managed skills")
                return 1
            if target.is_symlink() or target.is_file():
                target.unlink()
            else:
                shutil.rmtree(target)
        target.symlink_to(skill_dir)
        print(f"linked codex skill: {target}")

    existing_cli = shutil.which("forgeflow")
    if existing_cli:
        print(f"forgeflow CLI available at {existing_cli}")
        return 0

    bin_dir.mkdir(parents=True, exist_ok=True)
    launcher = bin_dir / "forgeflow"
    launcher.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                f'exec "{sys.executable}" "{PACKAGE_ROOT / "cli.py"}" "$@"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    launcher.chmod(0o755)
    print(f"installed fallback forgeflow CLI to {launcher}")
    if str(bin_dir) not in os.environ.get("PATH", ""):
        print(f"add {bin_dir} to PATH if needed")
    return 0


def version(_: argparse.Namespace) -> int:
    print(__version__)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="forgeflow workflow CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_codex_parser = subparsers.add_parser("install-codex", help="Install Codex skills and a forgeflow launcher")
    install_codex_parser.add_argument("--codex-home")
    install_codex_parser.add_argument("--bin-dir")
    install_codex_parser.add_argument("--force", action="store_true")
    install_codex_parser.set_defaults(func=install_codex)

    setup_parser = subparsers.add_parser("setup-project", help="Initialize .ai-workflow runtime in a project")
    setup_parser.add_argument("--project")
    setup_parser.add_argument("--export-cursor", action="store_true")
    setup_parser.add_argument("--force", action="store_true")
    setup_parser.set_defaults(func=setup_project)

    export_cursor_parser = subparsers.add_parser("export-cursor", help="Export Cursor skills into a project")
    export_cursor_parser.add_argument("--project")
    export_cursor_parser.add_argument("--force", action="store_true")
    export_cursor_parser.set_defaults(func=export_cursor)

    new_idea_parser = subparsers.add_parser("new-idea", help="Create an idea artifact")
    new_idea_parser.add_argument("--project")
    new_idea_parser.add_argument("--slug", required=True)
    new_idea_parser.add_argument("--title")
    new_idea_parser.add_argument("--force", action="store_true")
    new_idea_parser.set_defaults(func=new_idea)

    init_feature_parser = subparsers.add_parser("init-feature", help="Create a feature artifact scaffold")
    init_feature_parser.add_argument("--project")
    init_feature_parser.add_argument("--slug", required=True)
    init_feature_parser.add_argument("--title")
    init_feature_parser.add_argument("--force", action="store_true")
    init_feature_parser.set_defaults(func=init_feature)

    status_parser = subparsers.add_parser("status", help="Show workflow status")
    status_parser.add_argument("--project")
    status_parser.add_argument("--slug")
    status_parser.set_defaults(func=status)

    doctor_parser = subparsers.add_parser("doctor", help="Detect workflow gaps and stage-gate violations")
    doctor_parser.add_argument("--project")
    doctor_parser.add_argument("--slug")
    doctor_parser.set_defaults(func=doctor)

    version_parser = subparsers.add_parser("version", help="Print forgeflow version")
    version_parser.set_defaults(func=version)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
