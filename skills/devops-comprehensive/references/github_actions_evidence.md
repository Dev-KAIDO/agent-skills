# GitHub Actions Evidence

Use this reference when CI evidence comes from GitHub Actions logs, summaries, or workflow metadata.

## Evidence To Preserve

- Debug toggles: `ACTIONS_RUNNER_DEBUG`, `ACTIONS_STEP_DEBUG`, and runner diagnostic logs.
- Workflow commands: `::group::`, `::endgroup::`, `::error`, `::warning`, and `::notice`.
- Step summaries: `GITHUB_STEP_SUMMARY` content or mentions.
- Reusable workflows: `workflow_call`, local `.github/workflows/*.yml` references, and `uses:` workflow references.
- Artifact attestations: provenance evidence, never proof that an artifact is safe or vulnerability-free.

## Routing Rules

- Prefer local reproduction commands before repair.
- Preserve caller and callee workflow paths separately when reusable workflows are involved.
- Flag missing debug data as a diagnostic gap, not as an application defect.
