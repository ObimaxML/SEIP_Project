# SEIP ML Notebook 01 — Baseline Employment Model

This notebook version is provided as markdown for easy conversion into Jupyter or Databricks.

## 1. Build dataset

```python
!python ml/scripts/build_ml_dataset.py
```

## 2. Train baseline model

```python
!python ml/scripts/train_baseline_employment_model.py
```

## 3. Score records

```python
!python ml/scripts/predict_employment_probability.py
```

## 4. Inspect model report

```python
import json
from pathlib import Path

report_path = Path("ml/reports/baseline_employment_model_report.json")

with open(report_path, "r") as f:
    report = json.load(f)

report
```

## 5. Inspect feature coefficients

```python
import pandas as pd

coef = pd.read_csv("ml/reports/baseline_feature_coefficients.csv")
coef.head(20)
```

## 6. Inspect employment probability scores

```python
scores = pd.read_csv("ml/reports/employment_probability_scores.csv")
scores.head()
```
