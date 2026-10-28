# Wave 2 Contract: CI Failure Analyzer

This skill participates in the Enterprise Skills Wave 2 operating layer.

## Contract

- Reads existing `.codex-project-intel` artifacts before producing new output.
- Writes only its declared primary artifacts unless the workflow explicitly updates diagnostics, remediation, verification, progress, or decisions.
- Keeps source evidence, confidence, status, and affected files visible.
- Defers live external sync to the existing delivery and release skills.

## Integration

- Use `change-impact-mapper` before remediation or hardening work.
- Use `regression-guard` before any code-changing repair.
- Use `evidence-sync` after verification to prepare docs, release, and tracker handoffs.
