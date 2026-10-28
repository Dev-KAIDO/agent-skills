#!/usr/bin/env python3
"""Enterprise GUI Testing skill runner."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "_skill-governance" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from project_intel import (  # noqa: E402
    append_jsonl,
    append_operation,
    collect_repo_files,
    ensure_project_intel,
    finding,
    load_json,
    replace_items_for_source,
    run_command,
    safe_read_text,
    update_progress_state,
    write_json,
)
from skill_governance import utc_now  # noqa: E402


SOURCE_SKILL = "pyqt-test-engine"
GUI_FAILURE_TYPES = {
    "widget failure",
    "event loop failure",
    "teardown/cleanup failure",
    "visual regression",
    "missing element",
    "timing/race condition",
    "startup failure",
    "interaction failure",
}


def load_request(args) -> dict:
    if args.input:
        payload = load_json(Path(args.input), {})
        if isinstance(payload, dict):
            return payload
    return {}


def repo_root_from_request(request: dict) -> Path:
    repo_path = str(request.get("repo_path", "")).strip()
    if not repo_path:
        raise SystemExit("repo_path is required.")
    repo_root = Path(repo_path).resolve()
    if not repo_root.exists():
        raise SystemExit(f"Repository path does not exist: {repo_root}")
    return repo_root


def as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_rel(value: str) -> str:
    return str(value).replace("\\", "/").strip()


def optional_tool_status() -> dict:
    return {
        "pytest_qt": importlib.util.find_spec("pytestqt") is not None,
        "pyautogui": importlib.util.find_spec("pyautogui") is not None,
        "pillow": importlib.util.find_spec("PIL") is not None,
    }


def detect_gui_stack(repo_root: Path) -> dict:
    files = collect_repo_files(repo_root)
    manifests = []
    for name in ("requirements.txt", "pyproject.toml", "setup.py", "package.json"):
        path = repo_root / name
        if path.exists():
            manifests.append(name)
    manifest_text = "\n".join(safe_read_text(repo_root / name) for name in manifests if (repo_root / name).exists()).lower()
    code_text = "\n".join(safe_read_text(repo_root / rel)[:4000] for rel in files if rel.suffix.lower() == ".py")[:200000].lower()
    combined = manifest_text + "\n" + code_text
    return {
        "manifests": manifests,
        "pyqt5": "pyqt5" in combined,
        "pyside": "pyside" in combined,
        "pytest_qt_declared": "pytest-qt" in combined or "pytestqt" in combined,
        "pyautogui_declared": "pyautogui" in combined,
        "pillow_declared": "pillow" in combined or "pil" in combined,
        "test_files": [rel.as_posix() for rel in files if "test" in rel.name.lower() or "tests" in rel.parts],
    }


def classify_failure(text: str, explicit: str = "") -> str:
    value = explicit.strip().lower()
    if value in GUI_FAILURE_TYPES:
        return value
    lowered = text.lower()
    if "delete" in lowered or "teardown" in lowered or "top-level" in lowered or "toplevel" in lowered:
        return "teardown/cleanup failure"
    if "event loop" in lowered or "qapplication" in lowered or "qcoreapplication" in lowered:
        return "event loop failure"
    if "timeout" in lowered or "waituntil" in lowered or "race" in lowered or "focus" in lowered:
        return "timing/race condition"
    if "screenshot" in lowered or "pixel" in lowered or "overlap" in lowered or "layout" in lowered:
        return "visual regression"
    if "not found" in lowered or "missing" in lowered or "no such element" in lowered:
        return "missing element"
    if "startup" in lowered or "launch" in lowered or "boot" in lowered:
        return "startup failure"
    if "click" in lowered or "type" in lowered or "keyboard" in lowered or "mouse" in lowered:
        return "interaction failure"
    return "widget failure"


def stable_failure_id(prefix: str, existing: list) -> str:
    return f"{prefix}-{len(existing) + 1:03d}"


def record_gui_failure(paths, failure: dict) -> dict:
    catalog = load_json(paths.gui_failure_catalog, {"artifact_type": "gui-failure-catalog", "repo_root": str(paths.repo_root), "failures": []})
    failures = [item for item in catalog.get("failures", []) if isinstance(item, dict)]
    if not failure.get("id"):
        failure["id"] = stable_failure_id("guifailure", failures)
    failure.setdefault("source_skill", SOURCE_SKILL)
    failure.setdefault("created_at", utc_now())
    failure.setdefault("updated_at", utc_now())
    failure.setdefault("status", "open")
    failure["failure_type"] = classify_failure(
        " ".join(str(failure.get(field, "")) for field in ("traceback", "exception", "title", "reproduction_steps")),
        str(failure.get("failure_type", "")),
    )
    required = {
        "test_name": str(failure.get("test_name", "unknown")),
        "window": str(failure.get("window", "")),
        "widget": str(failure.get("widget", "")),
        "traceback": str(failure.get("traceback", failure.get("exception", ""))),
        "screenshot_path": str(failure.get("screenshot_path", "")),
        "reproduction_steps": [str(item) for item in as_list(failure.get("reproduction_steps"))],
        "affected_files": [normalize_rel(item) for item in as_list(failure.get("affected_files")) if str(item).strip()],
        "severity": str(failure.get("severity", "medium")),
        "confidence": float(failure.get("confidence", 0.75)),
    }
    failure.update(required)
    failures = [item for item in failures if item.get("id") != failure["id"]] + [failure]
    catalog.update({"artifact_type": "gui-failure-catalog", "generated_at": utc_now(), "repo_root": str(paths.repo_root), "failures": failures})
    write_json(paths.gui_failure_catalog, catalog)
    append_jsonl(paths.gui_error_log, failure)
    diag = finding(
        failure["id"],
        f"GUI failure: {failure['test_name']}",
        "gui",
        failure["severity"],
        failure["confidence"],
        SOURCE_SKILL,
        [{"type": "gui_failure", "failure_type": failure["failure_type"], "traceback": failure["traceback"], "screenshot_path": failure["screenshot_path"]}],
        failure["affected_files"],
        "Route this GUI failure through gui-repair-runner with regression scope and the original verification command.",
        extra={"gui_failure_type": failure["failure_type"]},
    )
    replace_items_for_source(paths.diagnostic_findings, "diagnostic-findings", "findings", SOURCE_SKILL, [diag])
    return failure


def write_output(output_path: Path, artifact_type: str, artifacts: dict, extra: dict | None = None) -> None:
    payload = {"artifact_type": artifact_type, "generated_at": utc_now(), "artifacts": artifacts}
    if extra:
        payload.update(extra)
    write_json(output_path, payload)
    print(output_path)


def run_gui_test_orchestrator(repo_root: Path, request: dict, paths, output_path: Path) -> int:
    stack = detect_gui_stack(repo_root)
    tools = optional_tool_status()
    plan = [
        {"id": "gui-plan-001", "stage": "sandbox", "skill": "gui-test-data-sandbox", "reason": "Isolate GUI data and settings before automation."},
        {"id": "gui-plan-002", "stage": "widget", "skill": "pyqt-test-engine", "reason": "Use pytest-qt for internal Qt widget, dialog, and window behavior."},
        {"id": "gui-plan-003", "stage": "visual", "skill": "gui-visual-regression", "reason": "Capture visual evidence for layout, overlap, blank window, and missing element checks."},
        {"id": "gui-plan-004", "stage": "e2e", "skill": "desktop-e2e-automation", "reason": "Use PyAutoGUI only when a true desktop flow is required."},
        {"id": "gui-plan-005", "stage": "failure-recording", "skill": "gui-failure-recorder", "reason": "Record every failed GUI check with evidence."},
        {"id": "gui-plan-006", "stage": "repair-loop", "skill": "gui-repair-runner", "reason": "Repair only recorded failures and retest the original flow."},
    ]
    payload = {"artifact_type": "gui-test-plan", "generated_at": utc_now(), "repo_root": str(repo_root), "source_skill": SOURCE_SKILL, "stack": stack, "tool_status": tools, "test_plan": plan}
    write_json(paths.gui_test_plan, payload)
    append_operation(paths, SOURCE_SKILL, "plan-gui-testing", repo_root.name, "completed", {"steps": len(plan)})
    update_progress_state(paths, {"last_gui_test_plan": paths.gui_test_plan.as_posix()})
    write_output(output_path, "gui-test-orchestrator-output", {"gui_test_plan": str(paths.gui_test_plan)}, {"step_count": len(plan)})
    return 0


def run_pyqt_test_engine(repo_root: Path, request: dict, paths, output_path: Path) -> int:
    command = [str(item) for item in as_list(request.get("test_command"))]
    result = None
    failures = []
    if command and request.get("run_tests", False):
        result = run_command(command, repo_root, int(request.get("timeout", 120)))
        if result["returncode"] != 0:
            failure = record_gui_failure(
                paths,
                {
                    "test_name": " ".join(command),
                    "traceback": "\n".join([str(result.get("stdout", "")), str(result.get("stderr", ""))]).strip(),
                    "reproduction_steps": ["Run the captured pytest-qt command."],
                    "affected_files": request.get("affected_files", []),
                    "severity": "high",
                    "confidence": 0.9,
                    "failure_type": classify_failure(str(result)),
                },
            )
            failures.append(failure["id"])
    else:
        stack = detect_gui_stack(repo_root)
        result = {"status": "plan-only", "recommended_tests": stack["test_files"], "tool_status": optional_tool_status()}
    payload = {"artifact_type": "gui-test-results", "generated_at": utc_now(), "repo_root": str(repo_root), "source_skill": SOURCE_SKILL, "results": [{"mode": "pytest-qt", "result": result, "failure_ids": failures}]}
    write_json(paths.gui_test_results, payload)
    append_operation(paths, SOURCE_SKILL, "run-pyqt-test-engine", repo_root.name, "completed", {"failures": len(failures)})
    update_progress_state(paths, {"last_gui_test_results": paths.gui_test_results.as_posix()})
    write_output(output_path, "pyqt-test-engine-output", {"gui_test_results": str(paths.gui_test_results), "gui_failure_catalog": str(paths.gui_failure_catalog)}, {"failure_count": len(failures)})
    return 0


def run_desktop_e2e_automation(repo_root: Path, request: dict, paths, output_path: Path) -> int:
    tools = optional_tool_status()
    run = {
        "id": "e2e-run-001",
        "status": "planned" if not request.get("run_e2e", False) else "ready" if tools["pyautogui"] else "blocked-missing-pyautogui",
        "app_command": as_list(request.get("app_command")),
        "steps": [str(item) for item in as_list(request.get("steps"))],
        "screenshot_dir": str(paths.gui_screenshots_dir),
        "tool_status": tools,
        "assertions": [str(item) for item in as_list(request.get("assertions"))],
    }
    payload = {"artifact_type": "gui-e2e-run-log", "generated_at": utc_now(), "repo_root": str(repo_root), "source_skill": SOURCE_SKILL, "runs": [run]}
    write_json(paths.gui_e2e_run_log, payload)
    if run["status"].startswith("blocked"):
        record_gui_failure(paths, {"test_name": "desktop-e2e-automation", "failure_type": "interaction failure", "traceback": "PyAutoGUI is not available in the active interpreter.", "reproduction_steps": ["Install PyAutoGUI in the project interpreter or run plan-only."], "severity": "medium", "confidence": 0.85})
    append_operation(paths, SOURCE_SKILL, "prepare-desktop-e2e", repo_root.name, "completed", {"status": run["status"]})
    update_progress_state(paths, {"last_gui_e2e_run_log": paths.gui_e2e_run_log.as_posix()})
    write_output(output_path, "desktop-e2e-automation-output", {"e2e_run_log": str(paths.gui_e2e_run_log), "screenshots": str(paths.gui_screenshots_dir)}, {"status": run["status"]})
    return 0


def compare_images(baseline: Path, current: Path, threshold: float) -> dict:
    if importlib.util.find_spec("PIL") is None:
        return {"status": "blocked-missing-pillow", "difference_ratio": None}
    from PIL import Image, ImageChops  # type: ignore
    with Image.open(baseline).convert("RGB") as base, Image.open(current).convert("RGB") as new:
        if base.size != new.size:
            return {"status": "failed", "reason": "image-size-mismatch", "baseline_size": base.size, "current_size": new.size, "difference_ratio": 1.0}
        diff = ImageChops.difference(base, new)
        bbox = diff.getbbox()
        if bbox is None:
            ratio = 0.0
        else:
            changed = 0
            pixels = diff.load()
            width, height = diff.size
            for x in range(width):
                for y in range(height):
                    if pixels[x, y] != (0, 0, 0):
                        changed += 1
            ratio = changed / float(width * height)
        return {"status": "passed" if ratio <= threshold else "failed", "difference_ratio": ratio, "threshold": threshold}


def run_gui_visual_regression(repo_root: Path, request: dict, paths, output_path: Path) -> int:
    baseline = Path(str(request.get("baseline_image", "")))
    current = Path(str(request.get("current_image", "")))
    threshold = float(request.get("threshold", 0.01))
    if baseline and not baseline.is_absolute():
        baseline = repo_root / baseline
    if current and not current.is_absolute():
        current = repo_root / current
    if str(baseline) and str(current) and baseline.exists() and current.exists():
        comparison = compare_images(baseline, current, threshold)
    else:
        comparison = {"status": "planned", "reason": "baseline/current images not provided", "threshold": threshold}
    comparison.update({"id": "visual-comparison-001", "baseline_image": str(baseline) if str(baseline) else "", "current_image": str(current) if str(current) else ""})
    payload = {"artifact_type": "gui-visual-regression-report", "generated_at": utc_now(), "repo_root": str(repo_root), "source_skill": SOURCE_SKILL, "comparisons": [comparison]}
    write_json(paths.gui_visual_regression_report, payload)
    if comparison["status"] == "failed":
        record_gui_failure(paths, {"test_name": "visual-regression", "failure_type": "visual regression", "screenshot_path": str(current), "traceback": json.dumps(comparison), "reproduction_steps": ["Re-run visual comparison with the same baseline and current screenshots."], "severity": "medium", "confidence": 0.86})
    append_operation(paths, SOURCE_SKILL, "run-visual-regression", repo_root.name, "completed", {"status": comparison["status"]})
    update_progress_state(paths, {"last_gui_visual_regression_report": paths.gui_visual_regression_report.as_posix()})
    write_output(output_path, "gui-visual-regression-output", {"visual_regression_report": str(paths.gui_visual_regression_report), "gui_failure_catalog": str(paths.gui_failure_catalog)}, {"status": comparison["status"]})
    return 0


def run_gui_flake_stabilizer(repo_root: Path, request: dict, paths, output_path: Path) -> int:
    catalog = load_json(paths.gui_failure_catalog, {})
    failures = [item for item in catalog.get("failures", []) if isinstance(item, dict) and item.get("status") != "closed"]
    signals = []
    for failure in failures:
        failure_type = str(failure.get("failure_type", ""))
        if failure_type in {"event loop failure", "teardown/cleanup failure", "timing/race condition"}:
            signals.append(
                {
                    "failure_id": failure.get("id"),
                    "failure_type": failure_type,
                    "stabilization": "Use minimal failing slice, explicit event flushing, deterministic waits, and teardown cleanup before full-flow verification.",
                    "verification": failure.get("verification_command") or "Re-run the original GUI test or E2E flow.",
                }
            )
    payload = {"artifact_type": "gui-flake-report", "generated_at": utc_now(), "repo_root": str(repo_root), "source_skill": SOURCE_SKILL, "flake_signals": signals}
    write_json(paths.gui_flake_report, payload)
    append_operation(paths, SOURCE_SKILL, "analyze-gui-flakes", repo_root.name, "completed", {"signals": len(signals)})
    update_progress_state(paths, {"last_gui_flake_report": paths.gui_flake_report.as_posix()})
    write_output(output_path, "gui-flake-stabilizer-output", {"flake_report": str(paths.gui_flake_report)}, {"signal_count": len(signals)})
    return 0


def run_gui_test_data_sandbox(repo_root: Path, request: dict, paths, output_path: Path) -> int:
    sandbox_root = paths.gui_dir / "sandbox"
    sandbox_root.mkdir(parents=True, exist_ok=True)
    sandbox = {
        "id": "gui-sandbox-001",
        "sandbox_root": str(sandbox_root),
        "database_path": str(sandbox_root / "test_gui.sqlite3"),
        "settings_path": str(sandbox_root / "test_settings.json"),
        "config_path": str(sandbox_root / "test_config.json"),
        "cleanup_policy": "Only remove paths under the declared sandbox_root.",
        "status": "prepared",
    }
    current = load_json(paths.gui_test_plan, {"artifact_type": "gui-test-plan", "repo_root": str(repo_root), "test_plan": []})
    current["generated_at"] = utc_now()
    current.setdefault("test_plan", [])
    current["sandbox"] = sandbox
    write_json(paths.gui_test_plan, current)
    append_operation(paths, SOURCE_SKILL, "prepare-gui-sandbox", repo_root.name, "completed", {"sandbox_root": str(sandbox_root)})
    update_progress_state(paths, {"last_gui_sandbox": str(sandbox_root)})
    write_output(output_path, "gui-test-data-sandbox-output", {"gui_test_plan": str(paths.gui_test_plan)}, {"sandbox_root": str(sandbox_root)})
    return 0


def run_gui_failure_recorder(repo_root: Path, request: dict, paths, output_path: Path) -> int:
    failure = dict(request.get("failure", {}))
    if not failure:
        failure = {
            "test_name": request.get("test_name", "manual-gui-failure"),
            "window": request.get("window", ""),
            "widget": request.get("widget", ""),
            "traceback": request.get("traceback", request.get("exception", "")),
            "screenshot_path": request.get("screenshot_path", ""),
            "reproduction_steps": request.get("reproduction_steps", []),
            "affected_files": request.get("affected_files", []),
            "severity": request.get("severity", "medium"),
            "confidence": request.get("confidence", 0.75),
            "status": request.get("status", "open"),
            "failure_type": request.get("failure_type", ""),
            "verification_command": request.get("verification_command", ""),
        }
    recorded = record_gui_failure(paths, failure)
    append_operation(paths, SOURCE_SKILL, "record-gui-failure", repo_root.name, "completed", {"failure_id": recorded["id"]})
    update_progress_state(paths, {"last_gui_failure_id": recorded["id"]})
    write_output(output_path, "gui-failure-recorder-output", {"gui_failure_catalog": str(paths.gui_failure_catalog), "gui_error_log": str(paths.gui_error_log)}, {"failure_id": recorded["id"]})
    return 0


def run_gui_repair_runner(repo_root: Path, request: dict, paths, output_path: Path) -> int:
    catalog = load_json(paths.gui_failure_catalog, {})
    failures = [item for item in catalog.get("failures", []) if isinstance(item, dict) and item.get("status") != "closed"]
    repairs = []
    retests = []
    for index, failure in enumerate(failures, 1):
        affected = [normalize_rel(item) for item in as_list(failure.get("affected_files")) if str(item).strip()]
        reproduction = [str(item) for item in as_list(failure.get("reproduction_steps")) if str(item).strip()]
        verification_command = failure.get("verification_command") or request.get("verification_command")
        ready = bool(affected and reproduction and verification_command)
        repair = {
            "id": f"gui-repair-{index:03d}",
            "failure_id": failure.get("id"),
            "status": "planned" if ready else "blocked-missing-required-evidence",
            "target_files": affected,
            "required_prechecks": ["change-impact-mapper", "regression-guard"],
            "repair_tooling": ["defect-fixer"],
            "recommended_action": "Apply the smallest GUI fix tied to the recorded failure and retest the original flow.",
            "missing_requirements": [] if ready else [name for name, ok in {"affected_files": bool(affected), "reproduction_steps": bool(reproduction), "verification_command": bool(verification_command)}.items() if not ok],
        }
        repairs.append(repair)
        retest = {"id": f"gui-retest-{index:03d}", "failure_id": failure.get("id"), "verification_command": verification_command, "status": "planned" if ready else "blocked"}
        if ready and request.get("run_retest", False):
            command = [str(item) for item in as_list(verification_command)]
            result = run_command(command, repo_root, int(request.get("timeout", 120)))
            retest["result"] = result
            retest["status"] = "passed" if result["returncode"] == 0 else "failed"
            if result["returncode"] != 0:
                record_gui_failure(paths, {"test_name": "gui-retest", "failure_type": failure.get("failure_type", "widget failure"), "traceback": "\n".join([result.get("stdout", ""), result.get("stderr", "")]), "reproduction_steps": ["Re-run the GUI retest command."], "affected_files": affected, "severity": failure.get("severity", "medium"), "confidence": 0.84})
        retests.append(retest)
    write_json(paths.gui_repair_plan, {"artifact_type": "gui-repair-plan", "generated_at": utc_now(), "repo_root": str(repo_root), "source_skill": SOURCE_SKILL, "repairs": repairs})
    write_json(paths.gui_retest_report, {"artifact_type": "gui-retest-report", "generated_at": utc_now(), "repo_root": str(repo_root), "source_skill": SOURCE_SKILL, "retests": retests})
    write_json(paths.verification_report, {"artifact_type": "verification-report", "generated_at": utc_now(), "repo_root": str(repo_root), "source_skill": SOURCE_SKILL, "checks": retests, "status": "planned" if not request.get("run_retest", False) else "executed"})
    append_operation(paths, SOURCE_SKILL, "prepare-gui-repair-run", repo_root.name, "completed", {"repairs": len(repairs), "retests": len(retests)})
    update_progress_state(paths, {"last_gui_repair_plan": paths.gui_repair_plan.as_posix(), "last_gui_retest_report": paths.gui_retest_report.as_posix()})
    write_output(output_path, "gui-repair-runner-output", {"gui_repair_plan": str(paths.gui_repair_plan), "gui_retest_report": str(paths.gui_retest_report), "verification_report": str(paths.verification_report)}, {"repair_count": len(repairs)})
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=f"Run {SOURCE_SKILL}.")
    parser.add_argument("--input", help="JSON input")
    parser.add_argument("--output", default=f"{SOURCE_SKILL.replace('-', '_')}_output.json", help="Summary JSON output")
    args = parser.parse_args()
    request = load_request(args)
    repo_root = repo_root_from_request(request)
    paths = ensure_project_intel(repo_root)
    output_path = Path(args.output)
    if SOURCE_SKILL == "gui-test-orchestrator":
        return run_gui_test_orchestrator(repo_root, request, paths, output_path)
    if SOURCE_SKILL == "pyqt-test-engine":
        return run_pyqt_test_engine(repo_root, request, paths, output_path)
    if SOURCE_SKILL == "desktop-e2e-automation":
        return run_desktop_e2e_automation(repo_root, request, paths, output_path)
    if SOURCE_SKILL == "gui-visual-regression":
        return run_gui_visual_regression(repo_root, request, paths, output_path)
    if SOURCE_SKILL == "gui-flake-stabilizer":
        return run_gui_flake_stabilizer(repo_root, request, paths, output_path)
    if SOURCE_SKILL == "gui-test-data-sandbox":
        return run_gui_test_data_sandbox(repo_root, request, paths, output_path)
    if SOURCE_SKILL == "gui-failure-recorder":
        return run_gui_failure_recorder(repo_root, request, paths, output_path)
    if SOURCE_SKILL == "gui-repair-runner":
        return run_gui_repair_runner(repo_root, request, paths, output_path)
    raise SystemExit(f"Unsupported skill: {SOURCE_SKILL}")


if __name__ == "__main__":
    raise SystemExit(main())
