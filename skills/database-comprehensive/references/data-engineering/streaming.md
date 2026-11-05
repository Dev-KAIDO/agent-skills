# Streaming & Events (البث وتصميم الأحداث)

## 1. Kafka Mental Model

```
topic → partitions (ordered, parallel) → consumer group (one consumer per partition)
```

- Order is guaranteed **per partition only** — the message key decides the partition.
- Consumers are independent: slow consumer = lag, not backpressure to others.
- Retention is time/size-based; consumers read at their own offset (replayable by design).

## 2. Design Rules

- **Key by the entity that must stay ordered** (`order_id`, not random). Wrong key = out-of-order state downstream.
- One event = one fact, past tense: `OrderPlaced`, `PaymentCaptured` — not `UpdateOrder`.
- Schema with **backward + forward compatibility** (Avro/Protobuf + registry). Never break readers: add optional fields first.
- Payload carries ids + minimal fields; heavy lookups happen in consumers via the source of truth (events are a log, not a database).
- Include `event_id` (idempotency), `event_time`, `producer`, `schema_version` in every envelope.

## 3. Consumer Patterns

| Pattern | Use |
|---------|-----|
| At-least-once + idempotent writes | **default** — dedupe on `event_id` or natural key |
| Exactly-once | only where truly required; costs (transactions/coordinator coupling) are real |
| Compacted topic | state tables (`user_id` → latest record) — log compaction keeps last per key |
| Dead-letter queue | poison messages parked with error, not blocking the partition |

**Consumer lag is the health metric:** alert on lag growth, not just errors. Lag + processing rate tells you time-to-recovery.

## 4. CDC (Change Data Capture)

- Debezium/managed CDC reads the DB transaction log → near-real-time events without touching app code.
- Schema changes propagate as events — test them (add column = fine, rename/reorder = break).
- Initial snapshot + tailing log: handle the cutover without duplicates or gaps (checkpoint the LSN).
- Outbox pattern when CDC isn't available: app writes event in the same transaction as the row, relay publishes it — never dual-write without a transaction.

## 5. Failure Checklist

| Symptom | Likely cause |
|---------|--------------|
| Repeated processing / dupes | no idempotency key, at-least-once + non-idempotent write |
| Skewed partitions (one hot) | bad key (nulls, one giant tenant) |
| Growing lag | consumer slower than producer — scale consumers (≤ partition count) or batch writes |
| Consumer group flapping | unstable broker/network, session.timeout tuning |
| Ordering bugs across entities | expecting global order — it doesn't exist; partition per entity |

## 6. When NOT to Stream

Dashboards on daily metrics, nightly aggregates, low-volume audit logs → batch. Streaming adds: operational surface (brokers, schema registry, lag monitoring) that must be justified by a freshness requirement.
