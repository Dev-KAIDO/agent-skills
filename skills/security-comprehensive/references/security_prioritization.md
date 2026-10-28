# Security Prioritization

Use this reference when turning security findings into remediation plans.

## Evidence Priority

- KEV or actively exploited evidence: prioritize first and record the evidence source.
- Secure by Design: prefer root-cause removal and default-safe behavior over narrow symptom patches.
- Memory safety: when buffer overflow or unsafe memory patterns are implicated, prefer elimination over detection-only mitigations.
- GHSA: preserve ecosystem, package, vulnerable range, patched version, and advisory URL when present.
- NVD: prefer incremental polling or bounded vulnerability lookups over broad refreshes.
- ASVS: map verification to relevant control families when the finding affects application security behavior.

## Remediation Rules

- Require a confirmed finding or documented risk before planning work.
- Require change-impact and regression checks before executable fixes.
- Avoid broad dependency upgrades unless a fixed version or safe version range is explicit.
