# ETL / ELT & Orchestration (خطوط البيانات)

## 1. ETL vs ELT

| | ETL | ELT |
|---|-----|-----|
| Transform | before load | after load (in the warehouse) |
| Use when | strict schemas, small data, legacy targets | modern warehouse (Snowflake/BigQuery/Postgres) — **default today** |
| Advantage | clean boundary | raw data preserved, re-transformable |

**Rule:** always land **raw** first (immutable bronze layer), then transform to cleaned (silver), then aggregates (silver/gold). Re-running a broken transform must never require re-extracting.

## 2. Batch vs Streaming

- **Batch** (hourly/daily cron): default — simpler, replayable, cheaper.
- **Streaming** (Kafka/Flink): only when freshness < ~1 min is a real business need (fraud, live dashboards, bidding).
- Many "streaming" needs are satisfied by micro-batch every 1–5 min. Prove the requirement first.

## 3. Orchestration

| Tool | Style |
|------|-------|
| **Airflow** | Python DAGs, largest ecosystem, ops-heavy |
| **Dagster** | software-defined assets, lineage-first — good default for new stacks |
| **Prefect** | dynamic, Pythonic, low ceremony |
| **dbt** | SQL transformations + tests + docs (transform layer, not orchestrator) |
| **n8n / Zapier** | no-code SaaS glue, not for core data |

**DAG rules:**
- Tasks idempotent: re-run from any point produces the same result (write to `ds=` partitions, upsert on key).
- Explicit dependencies — no "runs at 03:00 so the other job must be done".
- Retries with backoff only on transient errors; alerts on 3rd failure, not page-on-first.
- SLA per pipeline: freshness target + owner + runbook link.

## 4. Late & Bad Data

- **Event time vs processing time:** partition by event time, tolerate late arrivals with a watermark (e.g., accept 48h late, then recompute the partition).
- **Idempotency keys:** every record has a natural key; loads are upserts/merges, not blind appends.
- **Backfills:** partitioned re-runs must be reproducible — keep transformation code versioned with the data run.

## 5. Incremental Loads

| Pattern | When |
|---------|------|
| Timestamp watermark (`updated_at > last`) | source has reliable updated_at (watch timezone!) |
| CDC (change data capture) | low-lag, full history, no updated_at |
| Snapshot diff | small tables, nightly |
| Full reload | tiny tables — don't over-engineer |

Watermark pitfalls: rows updated **during** the load window (overlap windows by a few minutes), clock skew, and NULL updated_at rows (route them to a fallback path).

## 6. Cost Control

- Cluster by date + high-filter column; prune partitions in every query.
- Materialize only what's queried repeatedly; expire intermediates (TTL on raw after silver lands).
- Downstream contract: consumers read **models**, never raw tables — raw layout stays free to change.
