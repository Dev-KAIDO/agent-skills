#!/usr/bin/env python3
"""Kaido agent-skills — automated library validator.

Runs a full health check over the skills library and exits non-zero on any
failure, so it can gate every push via GitHub Actions (see
.github/workflows/validate.yml) or be run locally:

    python tools/validate_skills.py

Checks
------
1.  Every skill dir has a valid frontmatter (name matches dir, description
    present, <= 1024 chars, safe name pattern).
2.  Skill dirs without SKILL.md are only allowed when explicitly exempted.
3.  Every `scripts/`, `references/`, `examples/` path mentioned in a SKILL.md
    exists on disk (no dead links).
4.  No SKILL.md is nested inside references/ (would confuse discovery).
5.  All Python files parse (ast) — syntax errors fail the build.
6.  All shell files pass `bash -n` when bash is available (skipped elsewhere).
7.  All JS files pass `node --check` when node is available (skipped elsewhere).
8.  All text files decode as strict UTF-8.
9.  No __pycache__ / *.pyc tracked by git.
10. No obvious secret material (tokens/keys) in tracked text files.

Stdlib only — no third-party dependencies.
"""

from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

# Directories under skills/ that are shared libraries, not skills.
NON_SKILL_EXEMPT = {"_skill-governance", "sdlc-system"}

TEXT_SUFFIXES = {".md", ".py", ".js", ".mjs", ".cjs", ".sh", ".json", ".yaml",
                 ".yml", ".txt", ".ts", ".tsx", ".css", ".html", ".svg", ".xml"}

FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---", re.S)
REF_RE = re.compile(r"(?:scripts|references|examples)/[A-Za-z0-9_\-./]+")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]

errors: list[str] = []
warnings: list[str] = []


def err(check: str, message: str) -> None:
    errors.append(f"[{check}] {message}")


def warn(check: str, message: str) -> None:
    warnings.append(f"[{check}] {message}")


def iter_files(base: Path, suffixes: set[str] | None = None):
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts:
            continue
        if suffixes is not None and path.suffix.lower() not in suffixes:
            continue
        yield path


def check_frontmatter() -> dict[str, dict]:
    skills: dict[str, dict] = {}
    if not SKILLS.is_dir():
        err("frontmatter", "skills/ directory not found")
        return skills
    for entry in sorted(SKILLS.iterdir()):
        if not entry.is_dir():
            continue
        skill_md = entry / "SKILL.md"
        if not skill_md.exists():
            if entry.name not in NON_SKILL_EXEMPT:
                err("frontmatter",
                    f"'{entry.name}' has no SKILL.md (add it, or exempt it in "
                    f"NON_SKILL_EXEMPT if it is a shared library)")
            continue
        try:
            text = skill_md.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError as exc:
            err("frontmatter", f"{entry.name}/SKILL.md is not valid UTF-8: {exc}")
            continue
        match = FRONTMATTER_RE.match(text)
        if not match:
            err("frontmatter", f"{entry.name}/SKILL.md has no frontmatter block")
            continue
        block = match.group(1)
        fields: dict[str, str] = {}
        for line in block.splitlines():
            if ":" in line and not line.startswith((" ", "\t")):
                key, _, value = line.partition(":")
                fields[key.strip()] = value.strip()
        name = fields.get("name", "")
        description = fields.get("description", "")
        if not name:
            err("frontmatter", f"{entry.name}: missing 'name'")
        elif name != entry.name:
            err("frontmatter", f"{entry.name}: name '{name}' != directory name")
        elif not NAME_RE.match(name):
            err("frontmatter", f"{entry.name}: name '{name}' is not lowercase-kebab")
        if not description:
            err("frontmatter", f"{entry.name}: missing 'description'")
        elif len(description) > 1024:
            err("frontmatter",
                f"{entry.name}: description is {len(description)} chars (max 1024)")
        skills[entry.name] = {"dir": entry, "description": description}
    return skills


def check_references(skills: dict[str, dict]) -> None:
    for name, meta in skills.items():
        skill_md = meta["dir"] / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8-sig", errors="replace")
        seen: set[str] = set()
        for match in REF_RE.finditer(text):
            rel = match.group(0).rstrip(".,);:")
            if rel in seen:
                continue
            seen.add(rel)
            if not (meta["dir"] / rel).exists():
                err("references", f"{name}: dead reference '{rel}'")


def check_nested_skill_md() -> None:
    for path in SKILLS.rglob("SKILL.md"):
        parts = path.relative_to(SKILLS).parts
        if len(parts) > 2 and "references" in parts:
            err("nested", f"nested SKILL.md discovered: "
                          f"{'/'.join(parts)} (rename to index.md)")


def check_python() -> None:
    count = 0
    for path in iter_files(SKILLS, {".py"}):
        count += 1
        try:
            ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except SyntaxError as exc:
            err("python", f"{path.relative_to(ROOT)}:{exc.lineno}: {exc.msg}")
        except UnicodeDecodeError as exc:
            err("python", f"{path.relative_to(ROOT)}: not UTF-8: {exc}")
    if count == 0:
        warn("python", "no Python files found")


def check_shell() -> None:
    if shutil.which("bash") is None:
        warn("shell", "bash not available — skipped")
        return
    probe = subprocess.run(["bash", "-c", "exit 0"],
                           capture_output=True, text=True)
    if probe.returncode != 0:
        warn("shell", "bash present but not functional in this environment "
                      "(e.g. WSL without a distro) — skipped")
        return
    for path in iter_files(SKILLS, {".sh"}):
        result = subprocess.run(["bash", "-n", str(path)],
                                capture_output=True, text=True)
        if result.returncode != 0:
            err("shell", f"{path.relative_to(ROOT)}: "
                         f"{(result.stderr or result.stdout).strip()[:300]}")


def check_javascript() -> None:
    if shutil.which("node") is None:
        warn("javascript", "node not available — skipped")
        return
    for path in iter_files(SKILLS, {".js", ".mjs", ".cjs"}):
        result = subprocess.run(["node", "--check", str(path)],
                                capture_output=True, text=True)
        if result.returncode != 0:
            err("javascript",
                f"{path.relative_to(ROOT)}: {result.stderr.strip()[:300]}")


def check_utf8() -> None:
    for path in iter_files(SKILLS, TEXT_SUFFIXES):
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            err("utf8", f"{path.relative_to(ROOT)}: {exc}")


def check_git_tracked_junk() -> None:
    if shutil.which("git") is None:
        warn("git", "git not available — skipped")
        return
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        warn("git", "git ls-files failed — skipped")
        return
    tracked = [line for line in result.stdout.splitlines() if line]
    junk = [f for f in tracked
            if "__pycache__" in f or f.endswith((".pyc", ".pyo"))]
    for item in junk:
        err("git-junk", f"tracked build artifact: {item}")
    for line in tracked:
        if not line.endswith(tuple(TEXT_SUFFIXES)):
            continue
        path = ROOT / line
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern in SECRET_PATTERNS:
            found = pattern.search(text)
            if found:
                err("secrets", f"{line}: possible secret material "
                               f"({found.group(0)[:12]}...)")


def check_json_files() -> None:
    for path in iter_files(ROOT, {".json"}):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            err("json", f"{path.relative_to(ROOT)}: {exc}")


def main() -> int:
    skills = check_frontmatter()
    if skills:
        check_references(skills)
    check_nested_skill_md()
    check_python()
    check_shell()
    check_javascript()
    check_utf8()
    check_git_tracked_junk()
    check_json_files()

    print("=" * 60)
    print(f"Kaido skills validation — {len(skills)} skills checked")
    print("=" * 60)
    for message in warnings:
        print(f"  WARN  {message}")
    for message in errors:
        print(f"  FAIL  {message}")
    print("-" * 60)
    if errors:
        print(f"RESULT: FAIL — {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"RESULT: PASS — 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
