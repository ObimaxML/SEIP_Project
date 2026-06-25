# Phase 6A — Machine Learning Dataset and Baseline Employment Model

## Objective

Phase 6A introduces the first SEIP machine-learning component.

The goal is to create a baseline model that predicts whether a job seeker is likely to be currently employed based on demographic, education, location, digital access and survey features.

This is not yet the final production model. It is a baseline to prove the ML workflow.

The statement is highly plausible and describes a common starting point for labor market analysis, economic research, or the development of HR technology.

Creating a baseline model using these specific features is a standard practice for several reasons:

## Feature Relevance
The features mentioned—demographics, education, location, digital access, and survey responses—are all well-documented predictors of employment status. For instance, education level typically correlates with employment rates, while digital access is a critical barrier or enabler in the modern job market.

## Defining a "Baseline"
In machine learning, a baseline model provides a simple benchmark (often using a basic algorithm like Logistic Regression or a Random Forest) to compare against more complex models later. The goal is to see how much predictive power these fundamental variables have before moving to more advanced transformations.

## Predictive Validity
While survey data can sometimes have biases, combining it with objective data like location and education allows a model to capture both the structural environment and the individual’s specific situation.

## Practical Use Cases
Such a model could be used by NGOs to identify vulnerable populations who need job-seeking support or by government agencies to understand which "digital access" gaps are most strongly linked to unemployment in specific regions.

In summary, the statement describes a logically sound and technically standard objective for a data science project in the social or economic domain.

## Files added

```text
ml/scripts/build_ml_dataset.py
ml/scripts/train_baseline_employment_model.py
ml/scripts/predict_employment_probability.py
ml/data/
ml/models/
ml/reports/
notebooks/ml/01_baseline_employment_model.ipynb.md
```

## ML target

```text
currently_employed
```

The model predicts:

```text
TRUE  = currently employed
FALSE = currently not employed
```

## Features used

### Numeric features

```text
age
nqf_level
months_unemployed
completeness_score
quality_score
```

### Categorical features

```text
gender_code
south_african_citizen
highest_qualification
education_level_code
field_of_study
township_code
ward_number
seeking_work
preferred_sector
income_band
digital_literacy_level
has_smartphone
transport_mode
willing_to_relocate
training_interest
```

## Model used

```text
Logistic Regression
```

Why this model first?

- Easy to explain
- Good baseline
- Fast to train
- Coefficients are interpretable
- Suitable for portfolio demonstration

Later phases can add:

```text
Random Forest
XGBoost
LightGBM
Clustering
MLflow tracking
Databricks feature tables
```

---

# Implementation Steps

## Step 1 — Install updated dependencies

```powershell
pip install -r requirements.txt
```

Phase 6A adds:

```text
scikit-learn
joblib
matplotlib
```

## Step 2 — Ensure database has data

Run:

```powershell
docker compose up -d
python run_phase_3b_job_seeker_to_postgres.py
```

Important: the baseline classifier needs both classes:

```text
currently_employed = TRUE
currently_employed = FALSE
```

If your data only has one class, training will fail correctly.

## Step 3 — Build ML dataset

```powershell
python ml/scripts/build_ml_dataset.py
```

Output:

```text
ml/data/employment_prediction_dataset.csv
```

## Step 4 — Train baseline model

```powershell
python ml/scripts/train_baseline_employment_model.py
```

Outputs:

```text
ml/models/baseline_employment_model.joblib
ml/reports/baseline_employment_model_report.json
ml/reports/baseline_feature_coefficients.csv
```

## Step 5 — Generate employment probability scores

```powershell
python ml/scripts/predict_employment_probability.py
```

Output:

```text
ml/reports/employment_probability_scores.csv
```

## Step 6 — Review model performance

Open:

```text
ml/reports/baseline_employment_model_report.json
```

Look at:

```text
accuracy
precision
recall
f1
roc_auc
confusion_matrix
```

## Step 7 — Review feature coefficients

Open:

```text
ml/reports/baseline_feature_coefficients.csv
```

Large positive coefficients indicate features associated with higher employment probability.

Large negative coefficients indicate features associated with lower employment probability.

## Step 8 — Use scores in Power BI

Import:

```text
ml/reports/employment_probability_scores.csv
```

Create visuals:

```text
Employment probability by township
Employment probability by qualification
Employment probability by digital literacy level
High-risk unemployed cohort
```

---

# Important Model Governance Notes

## 1. Do not use this to deny services

This model must not be used to exclude job seekers from support, training or opportunities.

It should be used to identify where support is needed.

## 2. Watch for bias

Sensitive and proxy variables may introduce bias.

Examples:

```text
gender
location
education
transport access
digital access
```

Always evaluate model fairness before operational use.

## 3. Keep PII out of ML

The ML dataset should not contain:

```text
first_name
last_name
raw ID number
mobile number
email
physical address
```

## 4. Prefer explainable models first

For a public-sector employment platform, explainability matters.

Start with logistic regression, then compare with stronger models later.

---

# Git Commit

```powershell
git add .
git commit -m "Implement Phase 6A baseline employment prediction model"
```

## Next phase

```text
Phase 6B — Model improvement, feature engineering, fairness checks and MLflow tracking
```
