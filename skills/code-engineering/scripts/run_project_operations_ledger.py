#!/usr/bin/env python3
"""Initialize and update the shared project-intelligence workspace for a repository."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "_skill-governance" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from project_intel import (  # noqa: E402
    append_decision,
    append_operation,
    collect_repo_files,
    detect_languages,
    detect_manifests,
    ensure_project_intel,
    load_json,
    safe_read_text,
    update_progress_state,
    write_json,
)
from skill_governance import utc_now  # noqa: E402


def load_request(args) -> dict:
    if args.input:
        payload = load_json(Path(args.input), {})
        if isinstance(payload, dict):
            return payload
    return {}


def append_memory_notes(memory_path: Path, notes: list[str]) -> None:
    if not notes:
        return
    with memory_path.open("a", encoding="utf-8") as handle:
        handle.write("## Notes\n\n")
        for note in notes:
            handle.write(f"- {note}\n")
        handle.write("\n")


def refresh_project_intelligence(paths, repo_root: Path) -> dict:
    files = collect_repo_files(repo_root)
    intelligence = {
        "artifact_type": "project-intelligence",
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "file_count": len(files),
        "languages": detect_languages(files),
        "manifests": detect_manifests(repo_root),
        "top_level_paths": sorted({rel.parts[0] for rel in files if rel.parts}),
    }
    write_json(paths.project_intelligence, intelligence)
    return intelligence


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize or refresh .codex-project-intel artifacts.")
    parser.add_argument("--input", help="JSON input describing repo_path and operations")
    parser.add_argument("--output", default="project_operations_ledger_output.json", help="Summary JSON output")
    args = parser.parse_args()

    request = load_request(args)
    repo_path = str(request.get("repo_path", "")).strip()
    if not repo_path:
        raise SystemExit("repo_path is required.")

    repo_root = Path(repo_path).resolve()
    if not repo_root.exists():
        raise SystemExit(f"Repository path does not exist: {repo_root}")

    paths = ensure_project_intel(repo_root)
    intelligence = refresh_project_intelligence(paths, repo_root)
    append_memory_notes(paths.project_memory, list(request.get("memory_notes", [])))

    for event in request.get("events", []):
        append_operation(
            paths,
            "project-operations-ledger",
            str(event.get("action", "update-project-intel")),
            str(event.get("target", repo_root.name)),
            str(event.get("status", "completed")),
            dict(event.get("details", {})),
        )

    if request.get("progress_update"):
        update_progress_state(paths, dict(request["progress_update"]))

    for decision in request.get("decisions", []):
        append_decision(paths, str(decision.get("title", "Decision")), str(decision.get("body", "")).strip())

    output = {
        "artifact_type": "project-operations-ledger-output",
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "intel_root": str(paths.intel_root),
        "project_intelligence": intelligence,
        "artifacts": {
            "project_memory": str(paths.project_memory),
            "project_intelligence": str(paths.project_intelligence),
            "operations_log": str(paths.operations_log),
            "progress_state": str(paths.progress_state),
            "decision_log": str(paths.decision_log),
        },
    }
    write_json(Path(args.output), output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
