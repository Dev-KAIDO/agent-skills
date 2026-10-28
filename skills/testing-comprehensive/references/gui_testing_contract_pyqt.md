# GUI Testing Contract: PyQt Test Engine

This skill belongs to the Enterprise GUI Testing wave.

## Required Behavior

- Keep GUI artifacts under `.codex-project-intel/gui/`.
- Prefer `pytest-qt` for PyQt/PySide widget, dialog, and window tests.
- Use PyAutoGUI only for true desktop E2E flows that need external window control.
- Use Pillow or equivalent image tooling for visual comparison when screenshots are supplied.
- Record every GUI failure before repair work begins.

## Repair Loop

- `gui-failure-recorder` stores failures.
- `gui-repair-runner` reads failures and prepares scoped repair batches.
- `regression-guard` maps blast radius before edits.
- `defect-fixer` applies scoped fixes only when evidence and verification commands exist.
- The original failing test or E2E flow must be rerun before closure.
