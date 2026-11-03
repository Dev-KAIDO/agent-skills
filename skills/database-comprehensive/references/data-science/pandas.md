# pandas (معالجة البيانات)

## 1. Loading

```python
df = pd.read_csv(path, parse_dates=["date"], dtype={"zip": "string"})
# big files: usecols=[...], dtype={...}, chunksize=1_000_000
# parquet > csv: typed, compressed, faster (pyarrow)
```

- Set `dtype` explicitly on load — silent `object` columns (ids read as floats, leading zeros lost) are a classic corruption source.
- `string` (not `object`) for text; `category` for low-cardinality repeats.

## 2. Cleaning Checklist

```python
df = df.drop_duplicates(subset=["id"])
df["date"] = pd.to_datetime(df["date"], errors="coerce")   # NaT = bad rows
df = df[df["amount"].notna() & (df["amount"] >= 0)]
df["status"] = df["status"].str.strip().str.lower()
```

- **Never** silently `fillna(0)` — choose: drop, impute with a stated rule, or keep NaN and let the model handle it.
- Audit after cleaning: row count delta, NaN counts per column, value ranges. Print it; don't assume.

## 3. Core Operations

```python
# joins — always validate cardinality
df.merge(orders, on="user_id", how="left", validate="many_to_one")

# groupby
df.groupby("country", observed=True).agg(
    revenue=("amount", "sum"), n=("id", "count"), avg=("amount", "mean"))

# windows
df["share"] = df["amount"] / df.groupby("country")["amount"].transform("sum")
```

- Pass `validate=` to every merge — a silent many-to-many explodes row counts and every downstream number.
- `inplace=True` is banned (hidden mutations, chaining bugs): reassign.
- `SettingWithCopyWarning` = your update may not have landed: use `.loc[mask, col] = value`.

## 4. Performance

| Do | Instead of |
|----|------------|
| vectorized ops, `.str`/`.dt` accessors | `df.apply(row_fn, axis=1)` |
| `category` dtype for repeated strings | `object` |
| read selected columns/chunks | whole file |
| `merge` on indexes (`left_index=True`) | repeated key sorting |
| Polars/DuckDB for > RAM | more RAM |

`apply(axis=1)` is 10–100× slower than vectorized — profile before reaching for it.

## 5. Pitfalls

- **Chained assignment** (`df[a][b] = v`) doesn't propagate — always `.loc`.
- **Inplace myths:** `sort_values(inplace=True)` on a slice is undefined; reassign.
- **Silent alignment:** arithmetic between DataFrames aligns on index and inserts NaNs — check shapes.
- **Categorical groupby misses unseen labels:** pass `observed=True`.
- **Time zones:** keep everything tz-aware UTC; localize only at display.
