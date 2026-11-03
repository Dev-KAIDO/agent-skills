# ML Basics (أساسيات التعلّم الآلي) — scikit-learn

## 1. Canonical Workflow

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

pre = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                      ("sc", StandardScaler())]), num_cols),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                      ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat_cols),
])
model = Pipeline([("pre", pre), ("clf", XGBClassifier())])

model.fit(X_train, y_train)
```

**Everything inside the pipeline** — preprocessing outside it is the classic leakage bug (scaler fitted on test data).

## 2. Splits

| Data | Split |
|------|-------|
| IID rows | stratified K-fold (keep class ratios) |
| Time series | walk-forward / TimeSeriesSplit — **never** random shuffle |
| Groups (users, patients) | GroupKFold — no group in both train and test |
| Tiny data | repeated stratified K-fold + report variance |

Hold out a final test set **once**; tune only on train/val.

## 3. Model Pick

| Situation | Start with |
|-----------|-----------|
| Tabular, mixed types, mid-size | **CatBoost / XGBoost** |
| Need explainability, small data | logistic regression + clear features |
| Text | TF-IDF + linear baseline, then embeddings |
| Images/audio | pretrained backbone + fine-tune |
| Pure kNN-like retrieval | embeddings + ANN |

Always ship the **simple baseline first**; a complex model must beat it by a margin worth the maintenance.

## 4. Metrics

| Problem | Metric |
|---------|--------|
| Balanced classes | accuracy |
| Imbalanced (fraud, churn) | precision/recall, F1, **PR-AUC** (not ROC-AUC) |
| Ranking / recommendations | MAP, NDCG, hit@k |
| Regression, outliers present | MAE (median-based) |
| Regression, large errors costly | RMSE |
| Probabilities used for decisions | log loss, calibration curve |

Pick the metric **from the business cost of errors** (false negative = missed fraud), not by habit.

## 5. Imbalanced Data

1. Correct metric first (PR-AUC).
2. `class_weight="balanced"` / sample weights.
3. Resampling (SMOTE) only inside CV folds — never before splitting.
4. Threshold tuning on validation (0.5 is rarely optimal).

## 6. Over/Underfitting

| Symptom | Action |
|---------|--------|
| High train error | more features, bigger model, better labels |
| Low train, high val (overfit) | regularize, early stop, more data, simpler model |
| Both high (underfit) | more capacity / richer features |

## 7. Ship Checklist

- [ ] Pipeline contains all preprocessing (no leakage)
- [ ] Split strategy matches data (time/group-aware)
- [ ] Metric matches business cost
- [ ] Model + training code + data version pinned (MLflow/git)
- [ ] Inference latency and size budget measured
- [ ] Drift monitoring planned (input + prediction distribution)
