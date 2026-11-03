# Vector Stores (مخازن المتجهات)

## 1. Choice Matrix

| Store | Best for | Notes |
|-------|----------|-------|
| **pgvector** | already on Postgres, <10M vectors | one DB for data + vectors; HNSW supported |
| **Qdrant** | self-hosted, filters-heavy | strong payload filtering, Rust |
| **Pinecone** | zero-ops, serverless | cost grows with replicas |
| **Redis (Search)** | <1M vectors, sub-ms, live updates | also cache |
| **Chroma / LanceDB** | local, prototypes, embedded | not for multi-node prod |
| **Elastic / OpenSearch** | already have it | hybrid BM25+vector built in |

**Default:** pgvector if Postgres is already in the stack — a second datastore is an operational tax.

## 2. Index Types

| Index | When |
|-------|------|
| Flat (exact) | < ~50k vectors — exact beats ANN |
| HNSW | default ANN: high recall, fast, memory-heavy (graph in RAM) |
| IVF | very large sets, memory-constrained; train on sample first |

HNSW knobs: `m` (16–48 links/node) ↑ recall/memory · `ef_construction` (100–400) ↑ build quality/time · `ef_search` (64–200) ↑ query recall/latency. Tune against a labeled set, not by feel.

## 3. Sizing Rules

- Memory ≈ `n_vectors × dims × 4B` (+ HNSW graph overhead ~1.3–2×). 10M × 1536-dim float32 ≈ 61 GB before graph.
- Keep dimensions fixed; PCA-dimensionality-reduction only after measuring recall loss.
- Store metadata in the same row (pgvector) or payload (Qdrant) — round-trips to a second store kill latency.

## 4. Filtered Search Correctness

- ANN + hard filters can return **fewer than k** results even when matches exist.
- Pattern: over-fetch (k×5) → apply filter → top-k; or use exact scan when filter selectivity < ~1% of the corpus.
- Put high-selectivity filters (tenant!) in the index structure where supported.

## 5. Ops

- **Delete/update is the hard part:** soft-delete flag + periodic compaction, or collection versioning (write to `v2`, swap alias).
- Track index build time and recall@k on a golden query set per tuning change.
- Multi-tenant: one collection with `tenant_id` filter for small tenants; separate collections when one tenant > ~30% of data.
