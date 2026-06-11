# Phase 6B — Feature Engineering, Model Improvement, Fairness Checks and MLflow

## Objective

Phase 6B improves the baseline ML workflow from Phase 6A.

It adds:

- Feature engineering
- Model comparison
- Best-model selection
- Fairness diagnostics
- MLflow tracking
- A single Phase 6B pipeline runner

## Files added

```text
ml/scripts/feature_engineering.py
ml/scripts/train_model_comparison.py
ml/scripts/fairness_check.py
ml/scripts/train_with_mlflow.py
ml/scripts/run_phase_6b_pipeline.py
```

## New engineered features

```text
age_band
youth_flag
long_term_unemployed_flag
very_long_term_unemployed_flag
matric_or_higher_flag
post_school_flag
digital_access_score
mobility_score
work_readiness_score
```

## Models compared

```text
Logistic Regression
Random Forest
Gradient Boosting
```

The selected best model is saved as:

```text
ml/models/best_employment_model.joblib
```

## Step 1 — Install updated requirements

```powershell
pip install -r requirements.txt
```

Phase 6B adds:

```text
mlflow
imbalanced-learn
```

## Step 2 — Build or provide ML dataset

Preferred:

```powershell
python ml/scripts/build_ml_dataset.py
```

Demo option:

```powershell
python ml/scripts/train_from_sample_dataset.py
```

## Step 3 — Run full Phase 6B pipeline

```powershell
python ml/scripts/run_phase_6b_pipeline.py
```

This runs:

```text
train_model_comparison.py
fairness_check.py
train_with_mlflow.py
```

## Outputs

```text
ml/reports/model_comparison_report.json
ml/models/best_employment_model.joblib
ml/reports/fairness_check_report.json
mlruns/
```

## Step 4 — View MLflow UI

Run:

```powershell
mlflow ui --backend-store-uri .\mlruns
```

Open:

```text
http://127.0.0.1:5000
```

You should see:

```text
SEIP Employment Prediction
```

## Step 5 — Interpret fairness report

Open:

```text
ml/reports/fairness_check_report.json
```

It compares performance across:

```text
gender_code
township_code
age_band
```

Look for major gaps in:

```text
predicted_positive_rate
accuracy
precision
recall
f1
```

## Critical governance note

This model must be used to identify support needs, not to deny people access to opportunities.

Avoid harmful use such as:

```text
Rejecting job seekers
Ranking people for exclusion
Denying training access
Denying placement support
```

Appropriate use:

```text
Identify high-risk cohorts
Prioritise outreach
Improve training design
Guide township-level intervention planning
```

## Git commit

```powershell
git add .
git commit -m "Implement Phase 6B model improvement fairness checks and MLflow tracking"
```

## Next phase

```text
Phase 7A — GIS mapping, township risk zones and spatial analytics
```
