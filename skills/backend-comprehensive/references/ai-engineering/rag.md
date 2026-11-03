# RAG — Retrieval-Augmented Generation (التوليد المعزّز بالاسترجاع)

End-to-end pipeline for answering from **your** documents.

## 1. Pipeline

```
ingest → chunk → embed → index          (offline / on change)
query  → embed → search → rerank → pack → generate   (online)
```

## 2. Chunking

| Strategy | When |
|----------|------|
| By structure (heading, paragraph, function) | docs, code, markdown — **default** |
| Fixed tokens (256–1024, 10–20% overlap) | unstructured blobs |
| Parent-child (small chunks retrieve, parent supplies context) | any — best quality when affordable |

**Rules:**
- Chunk **with** metadata: source, title, section, date, access-control tags — filter before search, not after.
- Never split mid-table or mid-code-block.
- Embed headings with their body; a heading alone is an orphan.

## 3. Embeddings & Search

- One embedding model per index — mixing models corrupts the space.
- **Hybrid search** (BM25 keyword + vector) wins for names, codes, SKUs; pure vector loses exact tokens.
- Filter with metadata (tenant, lang, ACL) **before** ANN search — never post-filter and hope for enough hits.

## 4. Reranking

First-stage recall (top 50–100) → cross-encoder rerank → top 4–8 into the prompt.
Costs ~10–50 ms; large gains on ambiguous queries. Skip only when latency budget < 100 ms.

## 5. Prompt Assembly

```
[system] Answer ONLY from the context below. Cite [n]. If not present, say "not in documents".
[context] [1] … [2] … (deduplicated, ordered by rank)
[question] …
```

- Deduplicate near-identical chunks; 8 copies of one paragraph crowd out signal.
- Budget: keep context ≤ ~50% of window — the model degrades past ~70% full ("lost in the middle": put best chunks first **and** last).

## 6. Failure Modes

| Symptom | Fix |
|---------|-----|
| Answers ignore docs | stronger "only from context" instruction; verify citations actually exist |
| Wrong but confident | require citation per claim; refuse when citation missing |
| Misses exact matches | add hybrid search / synonyms |
| Stale answers | re-index on document change; store content hash |
| Contradictory chunks | surface both with sources instead of picking silently |

## 7. Evaluation

- **Retrieval:** hit@k, MRR on a labeled query→doc set — measure **before** touching the prompt.
- **Answer:** golden Q&A set scored by exact match / LLM-as-judge (`evals.md`).
- Log every query with retrieved ids → offline analysis of misses.

## 8. Ties

- Vector index choice → `vector-stores.md`
- Generation quality/cost → `llm-apis.md`
