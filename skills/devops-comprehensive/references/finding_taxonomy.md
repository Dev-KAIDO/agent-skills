# Finding Taxonomy

- `syntax`: parser or compilation failures that block startup or test execution.
- `imports`: unresolved local dependencies, circular module hazards, or missing dependency entrypoints.
- `config`: missing runtime files, `.env.example` without a real runtime file, or startup-sensitive settings gaps.
- `commands`: build or test commands that return non-zero exit status.
- `runtime`: obvious startup hazards that are visible from repository evidence.

Every finding must include evidence and affected files, and the skill must stay read-only.
