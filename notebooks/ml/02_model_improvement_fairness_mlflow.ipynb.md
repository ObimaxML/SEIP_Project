# SEIP ML Notebook 02 — Model Improvement, Fairness and MLflow

## Run Phase 6B pipeline

```python
!python ml/scripts/run_phase_6b_pipeline.py
```

## Load model comparison

```python
import json

with open("ml/reports/model_comparison_report.json") as f:
    comparison = json.load(f)

comparison
```

## Load fairness report

```python
with open("ml/reports/fairness_check_report.json") as f:
    fairness = json.load(f)

fairness
```

## Start MLflow UI

In terminal:

```bash
mlflow ui --backend-store-uri ./mlruns
```

Open:

```text
http://127.0.0.1:5000
```
