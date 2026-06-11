from pathlib import Path
import json
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from ml.scripts.feature_engineering import add_employment_features

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "ml" / "data" / "employment_prediction_dataset.csv"
REPORT_PATH = PROJECT_ROOT / "ml" / "reports" / "model_comparison_report.json"
BEST_MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "best_employment_model.joblib"

TARGET = "currently_employed"

NUMERIC_FEATURES = [
    "age", "nqf_level", "months_unemployed", "completeness_score", "quality_score",
    "digital_access_score", "mobility_score", "work_readiness_score"
]

CATEGORICAL_FEATURES = [
    "gender_code", "south_african_citizen", "highest_qualification", "education_level_code",
    "field_of_study", "township_code", "ward_number", "seeking_work", "preferred_sector",
    "income_band", "digital_literacy_level", "has_smartphone", "transport_mode",
    "willing_to_relocate", "training_interest", "age_band", "youth_flag",
    "long_term_unemployed_flag", "very_long_term_unemployed_flag",
    "matric_or_higher_flag", "post_school_flag"
]

MODELS = {
    "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "random_forest": RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced"),
    "gradient_boosting": GradientBoostingClassifier(random_state=42),
}

def target_to_bool(series):
    return series.astype(str).str.lower().isin(["true", "1", "yes"])

def evaluate_model(name, pipeline, X_train, X_test, y_train, y_test):
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    if hasattr(pipeline.named_steps["model"], "predict_proba"):
        y_proba = pipeline.predict_proba(X_test)[:, 1]
        roc_auc = roc_auc_score(y_test, y_proba) if y_test.nunique() == 2 else None
    else:
        roc_auc = None

    return {
        "model_name": name,
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1": float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc) if roc_auc is not None else None,
        "pipeline": pipeline,
    }

def main():
    df = pd.read_csv(DATA_PATH)
    df = add_employment_features(df)

    y = target_to_bool(df[TARGET])
    if y.nunique() < 2:
        raise ValueError("Target has only one class. Use data with both employed and unemployed examples.")

    X = df.drop(columns=[c for c in ["person_key", TARGET] if c in df.columns])

    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_transformer, NUMERIC_FEATURES),
        ("cat", categorical_transformer, CATEGORICAL_FEATURES)
    ])

    stratify = y if y.value_counts().min() >= 2 else None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=stratify
    )

    results = []
    best_result = None

    for name, model in MODELS.items():
        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("model", model)
        ])
        result = evaluate_model(name, pipeline, X_train, X_test, y_train, y_test)
        results.append({k: v for k, v in result.items() if k != "pipeline"})

        if best_result is None or (result["roc_auc"] or 0) > (best_result["roc_auc"] or 0):
            best_result = result

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    BEST_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "rows": len(df),
            "models": results,
            "best_model": {k: v for k, v in best_result.items() if k != "pipeline"}
        }, f, indent=2)

    joblib.dump(best_result["pipeline"], BEST_MODEL_PATH)

    print("Model comparison complete.")
    print(f"Report: {REPORT_PATH}")
    print(f"Best model: {BEST_MODEL_PATH}")
    print(json.dumps({k: v for k, v in best_result.items() if k != "pipeline"}, indent=2))

if __name__ == "__main__":
    main()
