# Feature Engineering (هندسة الخصائص)

## 1. Leakage First

**The #1 mistake.** A feature that encodes the target (or information unavailable at prediction time) gives fake accuracy that collapses in production.

Red flags: features computed over the full dataset (target encoding, global stats), timestamps after the decision point, IDs with high cardinality, "post-outcome" fields.

**Rule:** compute every feature strictly from data available **at the moment of prediction**, fitted on train only.

## 2. Numeric

| Situation | Transform |
|-----------|-----------|
| Right-skewed (income, prices, counts) | `log1p`, Box-Cox, Yeo-Johnson |
| Outliers | clip at train p1/p99, or robust scaler |
| Different scales for linear/SVM/kNN | StandardScaler (fit on train!) |
| Bounded ranges for trees | no scaling needed |

Tree models (XGBoost/RF) need no scaling; linear/kNN/neural do.

## 3. Categorical

| Cardinality | Encoding |
|-------------|----------|
| Binary | 0/1 |
| Low (< ~15) | one-hot (drop one) |
| High (user, product) | target/frequency encoding **with out-of-fold smoothing**, or embeddings |
| Ordinal (small < medium < large) | label map with real order |

- Never label-encode unordered categories for linear models (imposes fake order).
- Handle unseen categories explicitly (`"__unknown__"`).
- Frequency encoding is a safe high-cardinality baseline — often beats one-hot on trees.

## 4. Temporal Features

```python
df["dow"] = df.ts.dt.dayofweek
df["hour"] = df.ts.dt.hour
df["month"] = df.ts.dt.month
df["is_weekend"] = df.ts.dt.dayofweek >= 5
# cyclic encoding for smooth time-of-day:
df["hour_sin"] = np.sin(2 * np.pi * df.hour / 24)
```

- **Lag/rolling features** (last-7d mean, t-1, t-7) must be shifted to avoid peeking at the future.
- Fit scalers/encoders on train window only; time series never uses random CV — use walk-forward splits.

## 5. Text & Embeddings

- Classic baseline: TF-IDF (1–2 grams, min_df) — strong for classification.
- Pretrained embeddings (sentence-transformers) for semantic search/similarity; fine-tune only with enough labeled data.
- Normalize vectors (`normalize=True`) if using cosine similarity via dot product.

## 6. Selection

1. Drop: near-zero variance, > ~60% missing (or make missingness a feature), constant duplicates.
2. Importance-based: tree importances, permutation importance on validation.
3. Correlation filter: drop one of each pair |r| > 0.9.
4. Verify each addition lifts a **held-out** metric — features are kept by evidence, not hope.
