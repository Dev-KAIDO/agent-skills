# Data Quality (جودة البيانات)

## 1. The Contract

A **data contract** between producer and consumer: schema (types, nullability), semantics (what `status=active` means), SLA (freshness, completeness), owner, change process.

- Versioned (schema registry or docs-as-code). Breaking change = new major version + deprecation window.
- Producer's CI runs the same checks consumers rely on — quality moves **left**.

## 2. The Four Checks (run every load)

| Check | Example | Tooling |
|-------|---------|---------|
| **Schema** | types, required columns, no unexpected drift | dbt tests, Great Expectations, pandera |
| **Uniqueness** | natural key not duplicated | `group by key having count > 1` |
| **Range/domain** | amount ≥ 0, status in enum, no future dates | expectation suites |
| **Freshness** | max(updated_at) within SLA | orchestrator freshness check |

Plus row-count sanity vs. trailing baseline (−30% overnight = investigate before downstream uses it).

## 3. Anomaly Detection

- Baseline per metric/day-of-week (z-score or MAD on trailing 28 days); alert on deviation, not absolute value.
- Distinguish **pipeline broken** (0 rows, all-null column) from **real world changed** (business event) — first is page-worthy, second is a dashboard note.
- Alert to the **owner with a runbook**, not a generic channel.

## 4. Lineage

- Table → column → upstream tables/models → pipeline → dashboard. Needed to answer "if this breaks, who is impacted?"
- Generate automatically where possible (dbt parse, OpenLineage) — manual lineage rots within weeks.
- Lineage is the prerequisite for impact analysis on every schema change.

## 5. Recovery Order

```
1. Stop the bleeding   (quarantine bad partition, don't let it flow downstream)
2. Notify consumers    (which models/dashboards are affected)
3. Fix + backfill      (reprocess from raw — raw layer makes this cheap)
4. Postmortem          (add the check that would have caught it, to CI)
```

**Rule:** every incident ends with a new test. Quality without a feedback loop decays.
