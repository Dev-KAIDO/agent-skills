#!/usr/bin/env python3
"""Run static and command-level diagnostics for a repository."""

from __future__ import annotations

import argparse
import importlib.util
import py_compile
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "_skill-governance" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from project_intel import (  # noqa: E402
    append_operation,
    build_failure_catalog,
    build_local_dependency_graph,
    collect_repo_files,
    ensure_project_intel,
    finding,
    load_json,
    parse_python_imports,
    project_intel_paths,
    python_module_index,
    replace_items_for_source,
    run_command,
    safe_read_text,
    write_json,
)
from skill_governance import utc_now  # noqa: E402


SOURCE_SKILL = "system-diagnostics"


def load_request(args) -> dict:
    if args.input:
        payload = load_json(Path(args.input), {})
        if isinstance(payload, dict):
            return payload
    return {}


def local_root_tokens(module_index: dict[str, Path]) -> set[str]:
    return {name.split(".", 1)[0] for name in module_index}


def detect_unresolved_imports(repo_root: Path, files: list[Path]) -> list[dict[str, object]]:
    module_index = python_module_index(files)
    local_tokens = local_root_tokens(module_index)
    findings = []
    counter = 0
    for rel in files:
        if rel.suffix.lower() != ".py":
            continue
        imports = parse_python_imports(safe_read_text(repo_root / rel))
        for module in imports:
            root_token = module.split(".", 1)[0]
            if module in module_index:
                continue
            if root_token in local_tokens or module.startswith("src."):
                counter += 1
                findings.append(
                    finding(
                        f"unresolvedimport-{counter:03d}",
                        f"Unresolved local import: {module}",
                        "imports",
                        "high",
                        0.93,
                        SOURCE_SKILL,
                        [{"type": "import", "file": rel.as_posix(), "module": module}],
                        [rel.as_posix()],
                        "Restore the missing local module or correct the import path before runtime checks continue.",
                    )
                )
            elif importlib.util.find_spec(root_token) is None and root_token not in {"typing"}:
                counter += 1
                findings.append(
                    finding(
                        f"missingmodule-{counter:03d}",
                        f"Import may depend on an unavailable module: {module}",
                        "imports",
                        "medium",
                        0.67,
                        SOURCE_SKILL,
                        [{"type": "import", "file": rel.as_posix(), "module": module}],
                        [rel.as_posix()],
                        "Confirm whether the dependency should be installed or whether the import path is stale.",
                    )
                )
    return findings


def detect_python_syntax(repo_root: Path, files: list[Path]) -> list[dict[str, object]]:
    findings = []
    counter = 0
    for rel in files:
        if rel.suffix.lower() != ".py":
            continue
        try:
            py_compile.compile(str(repo_root / rel), doraise=True)
        except py_compile.PyCompileError as exc:
            counter += 1
            findings.append(
                finding(
                    f"pythonsyntax-{counter:03d}",
                    f"Python syntax or compile failure in {rel.as_posix()}",
                    "syntax",
                    "high",
                    0.99,
                    SOURCE_SKILL,
                    [{"type": "compile", "file": rel.as_posix(), "error": str(exc)}],
                    [rel.as_posix()],
                    "Fix the syntax or compile error before any runtime or test execution.",
                )
            )
    return findings


def detect_config_gaps(repo_root: Path, request: dict) -> list[dict[str, object]]:
    findings = []
    required_runtime_files = [str(item) for item in request.get("required_runtime_files", [])]
    counter = 0
    for required in required_runtime_files:
        if not (repo_root / required).exists():
            counter += 1
            evidence = [{"type": "missing_file", "file": required}]
            if (repo_root / f"{required}.example").exists() or (repo_root / f"{required}.sample").exists():
                evidence.append({"type": "example_present", "file": f"{required}.example"})
            findings.append(
                finding(
                    f"missingconfig-{counter:03d}",
                    f"Missing runtime configuration file: {required}",
                    "config",
                    "medium",
                    0.84,
                    SOURCE_SKILL,
                    evidence,
                    [required],
                    "Create the runtime configuration file or document how the environment is injected during startup.",
                )
            )
    return findings


def detect_command_failures(repo_root: Path, request: dict) -> list[dict[str, object]]:
    findings = []
    counter = 0
    for command in request.get("commands", []):
        result = run_command([str(part) for part in command], repo_root)
        if result["returncode"] != 0:
            counter += 1
            findings.append(
                finding(
                    f"commandfailure-{counter:03d}",
                    f"Command failed: {' '.join(result['command'])}",
                    "commands",
                    "high",
                    0.97,
                    SOURCE_SKILL,
                    [
                        {
                            "type": "command",
                            "command": result["command"],
                            "returncode": result["returncode"],
                            "stdout": result["stdout"],
                            "stderr": result["stderr"],
                        }
                    ],
                    [],
                    "Repair the failing build or test command and keep the exact invocation for follow-up verification.",
                )
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose build, import, config, and runtime faults in a repository.")
    parser.add_argument("--input", help="JSON input describing repo_path and optional commands")
    parser.add_argument("--output", default="system_diagnostics_output.json", help="Summary JSON output")
    args = parser.parse_args()

    request = load_request(args)
    repo_path = str(request.get("repo_path", "")).strip()
    if not repo_path:
        raise SystemExit("repo_path is required.")

    repo_root = Path(repo_path).resolve()
    if not repo_root.exists():
        raise SystemExit(f"Repository path does not exist: {repo_root}")

    paths = ensure_project_intel(repo_root)
    files = collect_repo_files(repo_root)
    graph = build_local_dependency_graph(repo_root)

    findings = []
    findings.extend(detect_python_syntax(repo_root, files))
    findings.extend(detect_unresolved_imports(repo_root, files))
    findings.extend(detect_config_gaps(repo_root, request))
    findings.extend(detect_command_failures(repo_root, request))

    replace_items_for_source(paths.diagnostic_findings, "diagnostic-findings", "findings", SOURCE_SKILL, findings)
    failure_catalog = build_failure_catalog(findings)
    write_json(
        paths.failure_catalog,
        {
            "artifact_type": "failure-catalog",
            "generated_at": utc_now(),
            "repo_root": str(repo_root),
            "failures": failure_catalog,
        },
    )
    append_operation(
        paths,
        SOURCE_SKILL,
        "run-diagnostics",
        repo_root.name,
        "completed",
        {"finding_count": len(findings), "graph_nodes": len(graph)},
    )

    output = {
        "artifact_type": "system-diagnostics-output",
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "finding_count": len(findings),
        "failure_catalog_count": len(failure_catalog),
        "artifacts": {
            "diagnostic_findings": str(paths.diagnostic_findings),
            "failure_catalog": str(paths.failure_catalog),
        },
    }
    write_json(Path(args.output), output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
