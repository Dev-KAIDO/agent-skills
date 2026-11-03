#!/usr/bin/env python3
"""Shared artifact I/O and CONFIG-driven runner for the sdlc-* skill scripts.

This library restores the `sdlc-system/python_lib` contract expected by the
skill scripts (they do ``sys.path.insert(0, parents[2] / "sdlc-system" /
"python_lib")`` before importing from this module).

Public API
----------
- ``load_artifact(path)``            read a JSON / YAML / JSONL artifact.
- ``write_artifact(data, path, fmt)`` write an artifact and return its path.
- ``list_from_payload(payload, keys)`` first list found under ``keys``.
- ``flatten_text(payload)``          recursive payload -> plain text.
- ``keyword_set(payload)``           lowercase word tokens of the payload.
- ``parse_simple_yaml(text)``        minimal indentation-based YAML parser.
- ``execute_configured_script(config)`` generic CLI runner driven by the
  per-script ``CONFIG`` dict (modes: analysis, tests, tracking, validate,
  document, scaffold, code-review, ...).

Exit codes: 0 = success, 1 = validation findings of severity high/critical,
2 = unusable input (missing/invalid artifact or arguments).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

__all__ = [
    "load_artifact",
    "write_artifact",
    "list_from_payload",
    "flatten_text",
    "keyword_set",
    "parse_simple_yaml",
    "execute_configured_script",
]

SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}


# --------------------------------------------------------------------------
# YAML (minimal, dependency free)
# --------------------------------------------------------------------------
def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
        return value[1:-1]
    lowered = value.lower()
    if lowered in {"true", "yes"}:
        return True
    if lowered in {"false", "no"}:
        return False
    if lowered in {"null", "none", "~"}:
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def parse_simple_yaml(text: str) -> Dict[str, Any]:
    """Parse the simple block-style YAML used by skill config files."""
    root: Dict[str, Any] = {}
    stack: List[tuple] = [(-1, root)]
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if ":" not in stripped:
            raise ValueError("Unsupported YAML structure: missing ':' separator")
        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not isinstance(parent, dict):
            raise ValueError("Unsupported YAML structure: scalar under non-mapping")
        if raw_value == "":
            node: Dict[str, Any] = {}
            parent[key] = node
            stack.append((indent, node))
            continue
        if raw_value.startswith(("[", "{")):
            try:
                parent[key] = json.loads(raw_value.replace("'", '"'))
                continue
            except json.JSONDecodeError:
                pass
        if raw_value.startswith(("[",)) and raw_value.endswith("]"):
            items = [parse_scalar(item) for item in raw_value[1:-1].split(",") if item.strip()]
            parent[key] = items
            continue
        parent[key] = parse_scalar(raw_value)
    return root


# --------------------------------------------------------------------------
# Artifact I/O
# --------------------------------------------------------------------------
def _die(message: str) -> None:
    raise SystemExit(message)


def load_artifact(path: Any) -> Any:
    """Load an artifact from JSON, YAML or JSONL based on the file suffix."""
    file_path = Path(path)
    if not file_path.exists():
        _die(f"Input artifact not found: {file_path}")
    try:
        text = file_path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        _die(f"Cannot read input artifact {file_path}: {exc}")

    suffix = file_path.suffix.lower()
    try:
        if suffix in {".yaml", ".yml"}:
            return parse_simple_yaml(text)
        if suffix == ".jsonl":
            return [json.loads(line) for line in text.splitlines() if line.strip()]
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return parse_simple_yaml(text)
    except (ValueError, json.JSONDecodeError) as exc:
        _die(f"Invalid artifact {file_path}: {exc}")


def write_artifact(data: Any, path: Any, fmt: str = "json") -> str:
    """Write ``data`` to ``path`` (creating parents) and return the path."""
    file_path = Path(path)
    if file_path.parent and not file_path.parent.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
    fmt = (fmt or "json").lower()
    try:
        if fmt == "json":
            payload = data if isinstance(data, str) else json.dumps(data, indent=2, ensure_ascii=False)
        elif fmt in {"md", "markdown", "txt", "text"}:
            payload = data if isinstance(data, str) else json.dumps(data, indent=2, ensure_ascii=False)
        elif fmt == "yaml":
            payload = _dump_yaml(data)
        else:
            payload = json.dumps(data, indent=2, ensure_ascii=False)
        file_path.write_text(payload.rstrip() + "\n", encoding="utf-8")
    except OSError as exc:
        _die(f"Cannot write artifact {file_path}: {exc}")
    return str(file_path)


def _dump_yaml(data: Any, indent: int = 0) -> str:
    pad = "  " * indent
    if isinstance(data, dict):
        lines = []
        for key, value in data.items():
            if isinstance(value, (dict, list)) and value:
                lines.append(f"{pad}{key}:")
                lines.append(_dump_yaml(value, indent + 1).rstrip("\n"))
            else:
                lines.append(f"{pad}{key}: {_yaml_scalar(value)}")
        return "\n".join(lines) + "\n"
    if isinstance(data, list):
        lines = [f"{pad}- {_yaml_scalar(item)}" if not isinstance(item, (dict, list)) else f"{pad}-" for item in data]
        out = []
        for item in data:
            if isinstance(item, (dict, list)):
                body = _dump_yaml(item, indent + 1).rstrip("\n")
                out.append(f"{pad}-" + ("\n" + body if body else ""))
            else:
                out.append(f"{pad}- {_yaml_scalar(item)}")
        return "\n".join(out) + "\n"
    return f"{pad}{_yaml_scalar(data)}\n"


def _yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "" or text != text.strip() or any(ch in text for ch in ":#{}[]\"'\n"):
        return json.dumps(text, ensure_ascii=False)
    return text


# --------------------------------------------------------------------------
# Payload helpers
# --------------------------------------------------------------------------
def list_from_payload(payload: Any, keys: Sequence[str]) -> List[Any]:
    """Return the first list found in ``payload`` under any of ``keys``."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in keys:
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, (dict, str, int, float))]
        # nested one level (e.g. {"report": {"findings": [...]}})
        for value in payload.values():
            if isinstance(value, dict):
                for key in keys:
                    nested = value.get(key)
                    if isinstance(nested, list):
                        return nested
    return []


def flatten_text(payload: Any) -> str:
    """Recursively flatten a payload into searchable plain text."""
    chunks: List[str] = []

    def walk(node: Any) -> None:
        if node is None:
            return
        if isinstance(node, dict):
            for key, value in node.items():
                chunks.append(str(key))
                walk(value)
        elif isinstance(node, (list, tuple, set)):
            for item in node:
                walk(item)
        else:
            chunks.append(str(node))

    walk(payload)
    return " ".join(chunks)


def keyword_set(payload: Any) -> set:
    """Lowercase word tokens contained in the payload."""
    return {token.lower() for token in re.findall(r"[A-Za-z0-9_\-]+", flatten_text(payload))}


# --------------------------------------------------------------------------
# CONFIG-driven runner
# --------------------------------------------------------------------------
def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Configured sdlc skill runner")
    parser.add_argument("--input", help="Path to the input artifact (json/yaml/jsonl)")
    parser.add_argument("--output", help="Output path (defaults to CONFIG['default_output'])")
    parser.add_argument("--repo", dest="repo_path", help="Optional repository root")
    return parser.parse_args(list(argv) if argv is not None else None)


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        return "\n".join(f"- {_stringify(item)}" for item in value)
    if isinstance(value, dict):
        return "\n".join(f"- **{key}:** {_stringify(val)}" for key, val in value.items())
    return str(value)


def _finding(message: str, severity: str = "medium", source: str = "rules") -> Dict[str, Any]:
    return {
        "message": message,
        "severity": severity if severity in SEVERITY_ORDER else "medium",
        "source": source,
    }


def _collect_findings(config: Dict[str, Any], payload: Any, text: str) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []

    # required top-level fields
    for field in config.get("required_fields", []) or []:
        present = isinstance(payload, dict) and field in payload and payload.get(field) not in (None, "", [], {})
        if not present:
            findings.append(_finding(f"Missing required field: {field}", "high", "required_fields"))

    # rules / checklist: finding when the keyword is ABSENT
    for rule in config.get("rules", []) or config.get("checklist", []) or []:
        keyword = str(rule.get("keyword", "")).lower()
        message = rule.get("message", f"Expected keyword not found: {keyword}")
        severity = rule.get("severity", "medium")
        if keyword and keyword not in text.lower():
            findings.append(_finding(str(message), str(severity), "rules"))

    # keyword_findings: advisory when the keyword IS present
    keyword_findings = config.get("keyword_findings", {}) or {}
    if isinstance(keyword_findings, dict):
        for keyword, message in keyword_findings.items():
            if str(keyword).lower() in text.lower():
                findings.append(_finding(str(message), "medium", "keyword_findings"))

    return findings


def _extract_items(config: Dict[str, Any], payload: Any) -> List[Any]:
    keys = config.get("preferred_item_keys", []) or config.get("item_keys", []) or [
        "items", "tasks", "stories", "functions", "findings"
    ]
    items = list_from_payload(payload, keys)
    if items:
        return items
    fallback = config.get("fallback_items", []) or []
    return list(fallback)


def _render_markdown(config: Dict[str, Any], payload: Any) -> str:
    lines: List[str] = [f"# {config.get('title', 'Document')}", ""]
    summary = config.get("summary")
    if summary:
        lines += [f"> {summary}", ""]
    for section in config.get("sections", []) or []:
        title = section.get("title", "Section")
        lines.append(f"## {title}")
        body = ""
        for field in section.get("fields", []) or []:
            if isinstance(payload, dict) and payload.get(field) not in (None, "", [], {}):
                body = _stringify(payload.get(field))
                break
        if not body:
            body = section.get("fallback", "")
        lines += [body or "_To be defined._", ""]
    if not config.get("sections"):
        body = _stringify(payload)
        lines += [body or "_No input provided._", ""]
    return "\n".join(lines).rstrip() + "\n"


def _build_tree(config: Dict[str, Any], payload: Any) -> List[str]:
    trees = config.get("trees", {}) or {}
    language = "default"
    if isinstance(payload, dict):
        language = str(payload.get("language") or config.get("default_language") or "default").lower()
    return list(trees.get(language) or trees.get("default") or trees.get(config.get("default_language", ""), []) or ["src/", "tests/"])


def execute_configured_script(config: Dict[str, Any], argv: Sequence[str] | None = None) -> int:
    """Run a skill script described entirely by ``config`` (see module docs)."""
    args = _parse_args(argv)

    payload: Any = {}
    if args.input:
        payload = load_artifact(args.input)

    text = flatten_text(payload)
    findings = _collect_findings(config, payload, text)

    output = args.output or config.get("default_output") or "output.json"
    mode = str(config.get("mode", "analysis"))
    is_markdown = str(output).lower().endswith((".md", ".markdown"))

    if is_markdown:
        document = _render_markdown(config, payload)
        path = write_artifact(document, output, "md")
        print(path)
        return _exit_code(findings)

    report: Dict[str, Any] = {
        "artifact_type": mode,
        "title": config.get("title", config.get("file", "report")),
        "summary": config.get("summary", ""),
        "source_script": config.get("file", ""),
        "input_provided": bool(args.input),
        "findings": findings,
        "recommended_actions": [
            "Review each finding and update the input artifact where needed.",
            "Re-run this script after updating the artifact to refresh the report.",
        ],
    }
    if args.repo_path:
        report["repo_path"] = str(args.repo_path)

    if "trees" in config:
        report["language"] = (
            str(payload.get("language")) if isinstance(payload, dict) and payload.get("language")
            else config.get("default_language", "default")
        )
        report["structure"] = _build_tree(config, payload)

    if config.get("preferred_item_keys") or config.get("fallback_items"):
        report["items"] = _extract_items(config, payload)

    if isinstance(payload, dict) and payload:
        report["input_summary"] = text[:500]
        report["inputs"] = {key: payload[key] for key in list(payload)[:20]}

    path = write_artifact(report, output, "json")
    print(path)
    return _exit_code(findings)


def _exit_code(findings: Iterable[Dict[str, Any]]) -> int:
    worst = max((SEVERITY_ORDER.get(str(f.get("severity", "medium")), 2) for f in findings), default=0)
    return 1 if worst >= SEVERITY_ORDER["high"] else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(execute_configured_script({"file": "sdlc_common.py", "mode": "analysis"}))
