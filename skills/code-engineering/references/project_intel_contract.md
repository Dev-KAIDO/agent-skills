# Project Intel Contract

- Always create `.codex-project-intel/` at the repository root.
- Treat `project_memory.md` as human-readable durable notes.
- Treat `project_intelligence.json` as the machine-readable summary of the repository.
- Keep `operations_log.jsonl` append-only.
- Keep `progress_state.json` as the current snapshot of completed and pending work.
- Keep `decision_log.md` readable and chronological.
- Downstream skills may replace only their own artifact slices, not the entire project-intel tree.
