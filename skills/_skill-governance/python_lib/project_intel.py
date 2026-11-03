#!/usr/bin/env python3
"""Shared helpers for enterprise Wave 1 skills."""

from __future__ import annotations

import json
import os
import re
import subprocess
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

from skill_governance import utc_now


PROJECT_INTEL_DIRNAME = ".codex-project-intel"
IGNORED_PARTS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".idea",
    ".vscode",
    "dist",
    "build",
    PROJECT_INTEL_DIRNAME,
}
PYTHON_EXTENSIONS = {".py"}
JS_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
TEXT_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".json",
    ".toml",
    ".yml",
    ".yaml",
    ".md",
    ".txt",
    ".ini",
    ".cfg",
}


@dataclass(frozen=True)
class ProjectIntelPaths:
    repo_root: Path
    intel_root: Path
    project_memory: Path
    project_intelligence: Path
    diagnostics_dir: Path
    diagnostic_findings: Path
    failure_catalog: Path
    impact_dir: Path
    change_impact_map: Path
    ci_dir: Path
    ci_failure_report: Path
    security_dir: Path
    security_remediation_plan: Path
    incidents_dir: Path
    incident_report: Path
    stability_dir: Path
    hardening_plan: Path
    evidence_dir: Path
    evidence_bundle: Path
    gui_dir: Path
    gui_test_plan: Path
    gui_test_results: Path
    gui_screenshots_dir: Path
    gui_visual_regression_report: Path
    gui_flake_report: Path
    gui_e2e_run_log: Path
    gui_failure_catalog: Path
    gui_error_log: Path
    gui_repair_plan: Path
    gui_retest_report: Path
    risks_dir: Path
    risk_register: Path
    remediation_dir: Path
    repair_plan: Path
    verification_dir: Path
    verification_report: Path
    progress_dir: Path
    operations_log: Path
    progress_state: Path
    decisions_dir: Path
    decision_log: Path


def project_intel_paths(repo_path: Path | str) -> ProjectIntelPaths:
    repo_root = Path(repo_path).resolve()
    intel_root = repo_root / PROJECT_INTEL_DIRNAME
    return ProjectIntelPaths(
        repo_root=repo_root,
        intel_root=intel_root,
        project_memory=intel_root / "project_memory.md",
        project_intelligence=intel_root / "project_intelligence.json",
        diagnostics_dir=intel_root / "diagnostics",
        diagnostic_findings=intel_root / "diagnostics" / "diagnostic_findings.json",
        failure_catalog=intel_root / "diagnostics" / "failure_catalog.json",
        impact_dir=intel_root / "impact",
        change_impact_map=intel_root / "impact" / "change_impact_map.json",
        ci_dir=intel_root / "ci",
        ci_failure_report=intel_root / "ci" / "ci_failure_report.json",
        security_dir=intel_root / "security",
        security_remediation_plan=intel_root / "security" / "security_remediation_plan.json",
        incidents_dir=intel_root / "incidents",
        incident_report=intel_root / "incidents" / "incident_report.json",
        stability_dir=intel_root / "stability",
        hardening_plan=intel_root / "stability" / "hardening_plan.json",
        evidence_dir=intel_root / "evidence",
        evidence_bundle=intel_root / "evidence" / "evidence_bundle.json",
        gui_dir=intel_root / "gui",
        gui_test_plan=intel_root / "gui" / "gui_test_plan.json",
        gui_test_results=intel_root / "gui" / "gui_test_results.json",
        gui_screenshots_dir=intel_root / "gui" / "screenshots",
        gui_visual_regression_report=intel_root / "gui" / "visual_regression_report.json",
        gui_flake_report=intel_root / "gui" / "flake_report.json",
        gui_e2e_run_log=intel_root / "gui" / "e2e_run_log.json",
        gui_failure_catalog=intel_root / "gui" / "gui_failure_catalog.json",
        gui_error_log=intel_root / "gui" / "gui_error_log.jsonl",
        gui_repair_plan=intel_root / "gui" / "gui_repair_plan.json",
        gui_retest_report=intel_root / "gui" / "gui_retest_report.json",
        risks_dir=intel_root / "risks",
        risk_register=intel_root / "risks" / "risk_register.json",
        remediation_dir=intel_root / "remediation",
        repair_plan=intel_root / "remediation" / "repair_plan.json",
        verification_dir=intel_root / "verification",
        verification_report=intel_root / "verification" / "verification_report.json",
        progress_dir=intel_root / "progress",
        operations_log=intel_root / "progress" / "operations_log.jsonl",
        progress_state=intel_root / "progress" / "progress_state.json",
        decisions_dir=intel_root / "decisions",
        decision_log=intel_root / "decisions" / "decision_log.md",
    )


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def append_jsonl(path: Path, payload) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return path


def safe_read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="ignore")


def is_ignored(path: Path) -> bool:
    return any(part in IGNORED_PARTS for part in path.parts)


def collect_repo_files(repo_root: Path | str) -> List[Path]:
    root = Path(repo_root).resolve()
    files = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if is_ignored(rel):
            continue
        files.append(rel)
    return sorted(files)


def detect_languages(files: Sequence[Path]) -> Dict[str, int]:
    counters = Counter()
    for rel in files:
        suffix = rel.suffix.lower()
        if suffix == ".py":
            counters["python"] += 1
        elif suffix in {".js", ".jsx"}:
            counters["javascript"] += 1
        elif suffix in {".ts", ".tsx"}:
            counters["typescript"] += 1
        elif suffix == ".go":
            counters["go"] += 1
        elif suffix == ".rs":
            counters["rust"] += 1
        elif suffix == ".java":
            counters["java"] += 1
        elif suffix == ".cs":
            counters["csharp"] += 1
        elif suffix == ".rb":
            counters["ruby"] += 1
    return dict(counters)


def detect_manifests(repo_root: Path | str) -> List[str]:
    root = Path(repo_root).resolve()
    candidates = [
        "requirements.txt",
        "pyproject.toml",
        "setup.py",
        "package.json",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "Cargo.toml",
        "go.mod",
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
    ]
    return [item for item in candidates if (root / item).exists()]


def ensure_project_intel(repo_root: Path | str) -> ProjectIntelPaths:
    paths = project_intel_paths(repo_root)
    for directory in (
        paths.intel_root,
        paths.diagnostics_dir,
        paths.impact_dir,
        paths.ci_dir,
        paths.security_dir,
        paths.incidents_dir,
        paths.stability_dir,
        paths.evidence_dir,
        paths.gui_dir,
        paths.gui_screenshots_dir,
        paths.risks_dir,
        paths.remediation_dir,
        paths.verification_dir,
        paths.progress_dir,
        paths.decisions_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    if not paths.project_memory.exists():
        paths.project_memory.write_text(
            "\n".join(
                [
                    "# Project Memory",
                    "",
                    f"- Repository: `{paths.repo_root}`",
                    f"- Initialized: `{utc_now()}`",
                    "- Purpose: Durable analysis memory for enterprise Wave 1 skills.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    if not paths.project_intelligence.exists():
        write_json(
            paths.project_intelligence,
            {
                "artifact_type": "project-intelligence",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "languages": {},
                "manifests": [],
                "notes": [],
            },
        )
    if not paths.diagnostic_findings.exists():
        write_json(
            paths.diagnostic_findings,
            {
                "artifact_type": "diagnostic-findings",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "findings": [],
            },
        )
    if not paths.failure_catalog.exists():
        write_json(
            paths.failure_catalog,
            {
                "artifact_type": "failure-catalog",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "failures": [],
            },
        )
    if not paths.change_impact_map.exists():
        write_json(
            paths.change_impact_map,
            {
                "artifact_type": "change-impact-map",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "changes": [],
            },
        )
    if not paths.ci_failure_report.exists():
        write_json(
            paths.ci_failure_report,
            {
                "artifact_type": "ci-failure-report",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "failures": [],
            },
        )
    if not paths.security_remediation_plan.exists():
        write_json(
            paths.security_remediation_plan,
            {
                "artifact_type": "security-remediation-plan",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "remediations": [],
            },
        )
    if not paths.incident_report.exists():
        write_json(
            paths.incident_report,
            {
                "artifact_type": "incident-report",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "incidents": [],
            },
        )
    if not paths.hardening_plan.exists():
        write_json(
            paths.hardening_plan,
            {
                "artifact_type": "hardening-plan",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "hardening_items": [],
            },
        )
    if not paths.evidence_bundle.exists():
        write_json(
            paths.evidence_bundle,
            {
                "artifact_type": "evidence-bundle",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "evidence": [],
                "handoffs": {},
            },
        )
    if not paths.gui_test_plan.exists():
        write_json(
            paths.gui_test_plan,
            {
                "artifact_type": "gui-test-plan",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "test_plan": [],
            },
        )
    if not paths.gui_test_results.exists():
        write_json(
            paths.gui_test_results,
            {
                "artifact_type": "gui-test-results",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "results": [],
            },
        )
    if not paths.gui_visual_regression_report.exists():
        write_json(
            paths.gui_visual_regression_report,
            {
                "artifact_type": "gui-visual-regression-report",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "comparisons": [],
            },
        )
    if not paths.gui_flake_report.exists():
        write_json(
            paths.gui_flake_report,
            {
                "artifact_type": "gui-flake-report",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "flake_signals": [],
            },
        )
    if not paths.gui_e2e_run_log.exists():
        write_json(
            paths.gui_e2e_run_log,
            {
                "artifact_type": "gui-e2e-run-log",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "runs": [],
            },
        )
    if not paths.gui_failure_catalog.exists():
        write_json(
            paths.gui_failure_catalog,
            {
                "artifact_type": "gui-failure-catalog",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "failures": [],
            },
        )
    if not paths.gui_repair_plan.exists():
        write_json(
            paths.gui_repair_plan,
            {
                "artifact_type": "gui-repair-plan",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "repairs": [],
            },
        )
    if not paths.gui_retest_report.exists():
        write_json(
            paths.gui_retest_report,
            {
                "artifact_type": "gui-retest-report",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "retests": [],
            },
        )
    if not paths.gui_error_log.exists():
        paths.gui_error_log.touch()
    if not paths.risk_register.exists():
        write_json(
            paths.risk_register,
            {
                "artifact_type": "risk-register",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "risks": [],
            },
        )
    if not paths.repair_plan.exists():
        write_json(
            paths.repair_plan,
            {
                "artifact_type": "repair-plan",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "repairs": [],
            },
        )
    if not paths.verification_report.exists():
        write_json(
            paths.verification_report,
            {
                "artifact_type": "verification-report",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "checks": [],
            },
        )
    if not paths.progress_state.exists():
        write_json(
            paths.progress_state,
            {
                "artifact_type": "progress-state",
                "generated_at": utc_now(),
                "repo_root": str(paths.repo_root),
                "completed": [],
                "pending": [],
                "notes": [],
            },
        )
    if not paths.operations_log.exists():
        paths.operations_log.touch()
    if not paths.decision_log.exists():
        paths.decision_log.write_text("# Decision Log\n\n", encoding="utf-8")
    return paths


def append_operation(
    paths: ProjectIntelPaths,
    actor: str,
    action: str,
    target: str,
    status: str,
    details: Dict[str, object] | None = None,
) -> None:
    append_jsonl(
        paths.operations_log,
        {
            "timestamp": utc_now(),
            "actor": actor,
            "action": action,
            "target": target,
            "status": status,
            "details": details or {},
        },
    )


def append_decision(paths: ProjectIntelPaths, title: str, body: str) -> None:
    with paths.decision_log.open("a", encoding="utf-8") as handle:
        handle.write(f"## {title}\n\n{body.strip()}\n\n")


def update_progress_state(paths: ProjectIntelPaths, payload: Dict[str, object]) -> Path:
    current = load_json(paths.progress_state, {})
    current.update(payload)
    current["generated_at"] = utc_now()
    return write_json(paths.progress_state, current)


def module_aliases(rel_path: Path) -> List[str]:
    stem = rel_path.with_suffix("")
    parts = list(stem.parts)
    aliases = {".".join(parts)}
    if parts and parts[0] in {"src", "app", "lib"} and len(parts) > 1:
        aliases.add(".".join(parts[1:]))
    return sorted(alias for alias in aliases if alias)


def python_module_index(files: Sequence[Path]) -> Dict[str, Path]:
    index: Dict[str, Path] = {}
    for rel in files:
        if rel.suffix.lower() not in PYTHON_EXTENSIONS:
            continue
        for alias in module_aliases(rel):
            index.setdefault(alias, rel)
    return index


def parse_python_imports(text: str) -> List[str]:
    imports: List[str] = []
    import_pattern = re.compile(r"^\s*import\s+([a-zA-Z0-9_., ]+)", re.MULTILINE)
    from_pattern = re.compile(r"^\s*from\s+([a-zA-Z0-9_\.]+)\s+import\s+", re.MULTILINE)
    for match in import_pattern.findall(text):
        parts = [item.strip() for item in match.split(",") if item.strip()]
        imports.extend(parts)
    imports.extend(match.strip() for match in from_pattern.findall(text) if not match.startswith("."))
    return imports


def resolve_js_import(current: Path, raw_target: str, files: Sequence[Path]) -> Path | None:
    if not raw_target.startswith((".", "/")):
        return None
    repo_files = {str(rel).replace("\\", "/"): rel for rel in files}
    candidates = []
    current_parent = current.parent
    base = (current_parent / raw_target).as_posix()
    for suffix in ("", ".js", ".jsx", ".ts", ".tsx", "/index.js", "/index.ts"):
        candidates.append((base + suffix).replace("//", "/"))
    for candidate in candidates:
        rel = repo_files.get(candidate)
        if rel is not None:
            return rel
    return None


def build_local_dependency_graph(repo_root: Path | str) -> Dict[str, List[str]]:
    root = Path(repo_root).resolve()
    files = collect_repo_files(root)
    module_index = python_module_index(files)
    graph: Dict[str, set[str]] = defaultdict(set)
    for rel in files:
        rel_text = rel.as_posix()
        graph.setdefault(rel_text, set())
        suffix = rel.suffix.lower()
        if suffix in PYTHON_EXTENSIONS:
            text = safe_read_text(root / rel)
            for module in parse_python_imports(text):
                if module in module_index:
                    graph[rel_text].add(module_index[module].as_posix())
        elif suffix in JS_EXTENSIONS:
            text = safe_read_text(root / rel)
            for match in re.findall(r"""(?:from|require\()\s*['"]([^'"]+)['"]""", text):
                target = resolve_js_import(rel, match, files)
                if target is not None:
                    graph[rel_text].add(target.as_posix())
    return {key: sorted(value) for key, value in graph.items()}


def reverse_graph(graph: Dict[str, List[str]]) -> Dict[str, List[str]]:
    reversed_graph: Dict[str, set[str]] = defaultdict(set)
    for source, targets in graph.items():
        reversed_graph.setdefault(source, set())
        for target in targets:
            reversed_graph[target].add(source)
    return {key: sorted(value) for key, value in reversed_graph.items()}


def find_cycles(graph: Dict[str, List[str]]) -> List[List[str]]:
    visited: set[str] = set()
    stack: List[str] = []
    cycles: List[List[str]] = []
    seen_signatures: set[tuple[str, ...]] = set()

    def visit(node: str) -> None:
        visited.add(node)
        stack.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visit(neighbor)
            elif neighbor in stack:
                start = stack.index(neighbor)
                cycle = stack[start:] + [neighbor]
                signature = tuple(cycle)
                if signature not in seen_signatures:
                    cycles.append(cycle)
                    seen_signatures.add(signature)
        stack.pop()

    for node in sorted(graph):
        if node not in visited:
            visit(node)
    return cycles


def fan_in_out(graph: Dict[str, List[str]]) -> Dict[str, Dict[str, int]]:
    incoming = Counter()
    outgoing = Counter()
    for source, targets in graph.items():
        outgoing[source] = len(targets)
        for target in targets:
            incoming[target] += 1
    nodes = set(graph)
    nodes.update(incoming)
    return {
        node: {"fan_in": incoming[node], "fan_out": outgoing[node]}
        for node in sorted(nodes)
    }


def matching_tests(repo_root: Path | str, targets: Sequence[str]) -> List[str]:
    root = Path(repo_root).resolve()
    files = collect_repo_files(root)
    test_files = [rel for rel in files if "test" in rel.name.lower() or "tests" in rel.parts]
    matched = []
    target_tokens = {Path(item).stem.lower() for item in targets}
    target_parts = {Path(item).parent.name.lower() for item in targets if Path(item).parent.name}
    for rel in test_files:
        text = safe_read_text(root / rel).lower()
        haystack = f"{rel.as_posix().lower()} {text}"
        if any(token and token in haystack for token in target_tokens | target_parts):
            matched.append(rel.as_posix())
    return sorted(set(matched))


def count_todo_markers(repo_root: Path | str) -> Dict[str, int]:
    root = Path(repo_root).resolve()
    counts: Dict[str, int] = {}
    for rel in collect_repo_files(root):
        if rel.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        text = safe_read_text(root / rel)
        marker_count = len(re.findall(r"\b(TODO|FIXME|HACK)\b", text, flags=re.IGNORECASE))
        if marker_count:
            counts[rel.as_posix()] = marker_count
    return counts


def parse_dependency_files(repo_root: Path | str) -> List[Dict[str, str]]:
    root = Path(repo_root).resolve()
    items: List[Dict[str, str]] = []
    requirements = root / "requirements.txt"
    if requirements.exists():
        for raw in safe_read_text(requirements).splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            name, version = split_dependency_line(line)
            items.append({"ecosystem": "python", "file": "requirements.txt", "name": name, "version": version})
    package_json = root / "package.json"
    if package_json.exists():
        data = load_json(package_json, {})
        for section in ("dependencies", "devDependencies"):
            for name, version in data.get(section, {}).items():
                items.append({"ecosystem": "node", "file": "package.json", "name": name, "version": str(version)})
    return items


def split_dependency_line(line: str) -> tuple[str, str]:
    for token in ("==", ">=", "<=", "~=", "!=", ">", "<"):
        if token in line:
            name, version = line.split(token, 1)
            return name.strip(), version.strip()
    return line.strip(), ""


def semantic_major(version: str) -> int | None:
    match = re.search(r"(\d+)", version)
    return int(match.group(1)) if match else None


def semantic_minor(version: str) -> int | None:
    match = re.search(r"\d+\.(\d+)", version)
    return int(match.group(1)) if match else None


def run_command(command: Sequence[str], cwd: Path | str, timeout: int = 45) -> Dict[str, object]:
    start = time.perf_counter()
    completed = subprocess.run(
        list(command),
        cwd=str(cwd),
        text=True,
        capture_output=True,
        timeout=timeout,
        env=os.environ.copy(),
    )
    duration = round(time.perf_counter() - start, 3)
    return {
        "command": list(command),
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "duration_seconds": duration,
    }


def git_file_churn(repo_root: Path | str, max_commits: int = 200) -> Dict[str, int]:
    root = Path(repo_root).resolve()
    if not (root / ".git").exists():
        return {}
    completed = subprocess.run(
        ["git", "-C", str(root), "log", f"--max-count={max_commits}", "--name-only", "--pretty=format:"],
        text=True,
        capture_output=True,
        env=os.environ.copy(),
    )
    if completed.returncode != 0:
        return {}
    counts = Counter()
    for raw in completed.stdout.splitlines():
        line = raw.strip()
        if line:
            counts[line.replace("\\", "/")] += 1
    return dict(counts)


def make_item_id(prefix: str, index: int) -> str:
    return f"{prefix}-{index:03d}"


def finding(
    item_id: str,
    title: str,
    finding_type: str,
    severity: str,
    confidence: float,
    source_skill: str,
    evidence: List[Dict[str, object]],
    affected_files: List[str],
    recommended_action: str,
    status: str = "open",
    extra: Dict[str, object] | None = None,
) -> Dict[str, object]:
    payload = {
        "id": item_id,
        "title": title,
        "type": finding_type,
        "severity": severity,
        "confidence": confidence,
        "status": status,
        "source_skill": source_skill,
        "evidence": evidence,
        "affected_files": sorted(set(affected_files)),
        "recommended_action": recommended_action,
    }
    if extra:
        payload.update(extra)
    return payload


def risk(
    item_id: str,
    title: str,
    risk_type: str,
    severity: str,
    confidence: float,
    source_skill: str,
    affected_area: List[str],
    mitigation: str,
    time_horizon: str,
    trigger_signals: List[str],
    status: str = "open",
    extra: Dict[str, object] | None = None,
) -> Dict[str, object]:
    payload = {
        "id": item_id,
        "title": title,
        "risk_type": risk_type,
        "severity": severity,
        "confidence": confidence,
        "status": status,
        "source_skill": source_skill,
        "affected_area": sorted(set(affected_area)),
        "mitigation": mitigation,
        "time_horizon": time_horizon,
        "trigger_signals": trigger_signals,
    }
    if extra:
        payload.update(extra)
    return payload


def replace_items_for_source(path: Path, artifact_type: str, key: str, source_skill: str, items: List[Dict[str, object]]) -> Path:
    payload = load_json(path, {"artifact_type": artifact_type, "generated_at": utc_now(), key: []})
    existing = [item for item in payload.get(key, []) if item.get("source_skill") != source_skill]
    payload[key] = existing + items
    payload["generated_at"] = utc_now()
    return write_json(path, payload)


def build_failure_catalog(findings: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    grouped: Dict[str, Dict[str, object]] = {}
    for item in findings:
        code = str(item["id"]).split("-", 1)[0]
        entry = grouped.setdefault(
            code,
            {
                "code": code,
                "count": 0,
                "severity": item.get("severity", "medium"),
                "titles": set(),
                "affected_files": set(),
            },
        )
        entry["count"] += 1
        entry["titles"].add(item.get("title", code))
        entry["affected_files"].update(item.get("affected_files", []))
    failures = []
    for code, entry in sorted(grouped.items()):
        failures.append(
            {
                "code": code,
                "count": entry["count"],
                "severity": entry["severity"],
                "titles": sorted(entry["titles"]),
                "affected_files": sorted(entry["affected_files"]),
            }
        )
    return failures
