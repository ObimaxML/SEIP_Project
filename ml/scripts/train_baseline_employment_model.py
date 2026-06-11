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
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "ml" / "data" / "employment_prediction_dataset.csv"
MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "baseline_employment_model.joblib"
REPORT_PATH = PROJECT_ROOT / "ml" / "reports" / "baseline_employment_model_report.json"
FEATURE_IMPORTANCE_PATH = PROJECT_ROOT / "ml" / "reports" / "baseline_feature_coefficients.csv"

TARGET = "currently_employed"

DROP_COLUMNS = [
    "person_key",
    TARGET
]

NUMERIC_FEATURES = [
    "age",
    "nqf_level",
    "months_unemployed",
    "completeness_score",
    "quality_score",
]

CATEGORICAL_FEATURES = [
    "gender_code",
    "south_african_citizen",
    "highest_qualification",
    "education_level_code",
    "field_of_study",
    "township_code",
    "ward_number",
    "seeking_work",
    "preferred_sector",
    "income_band",
    "digital_literacy_level",
    "has_smartphone",
    "transport_mode",
    "willing_to_relocate",
    "training_interest",
]

def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. "
            "Run: python ml/scripts/build_ml_dataset.py"
        )

    df = pd.read_csv(DATA_PATH)

    if df.empty:
        raise ValueError("ML dataset is empty. Load more survey records first.")

    return df

def prepare_target(df: pd.DataFrame) -> pd.Series:
    return df[TARGET].astype(str).str.lower().isin(["true", "1", "yes"])

def main():
    df = load_data()

    missing_cols = [c for c in NUMERIC_FEATURES + CATEGORICAL_FEATURES + [TARGET] if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing model columns: {missing_cols}")

    X = df.drop(columns=[c for c in DROP_COLUMNS if c in df.columns])
    y = prepare_target(df)

    if y.nunique() < 2:
        raise ValueError(
            "Target has only one class. Add both employed and unemployed examples "
            "before training a classifier."
        )

    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )

    model = LogisticRegression(max_iter=1000, class_weight="balanced")

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ])

    stratify = y if y.value_counts().min() >= 2 else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=42,
        stratify=stratify
    )

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "rows": int(len(df)),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1": float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_proba)) if y_test.nunique() == 2 else None,
        "classification_report": classification_report(y_test, y_pred, output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "target": TARGET,
        "positive_class": "currently_employed = TRUE",
        "model_type": "LogisticRegression baseline",
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(pipeline, MODEL_PATH)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # Coefficients for interpretability
    feature_names = (
        NUMERIC_FEATURES
        + list(
            pipeline.named_steps["preprocessor"]
            .named_transformers_["cat"]
            .named_steps["onehot"]
            .get_feature_names_out(CATEGORICAL_FEATURES)
        )
    )

    coefficients = pipeline.named_steps["model"].coef_[0]
    coef_df = pd.DataFrame({
        "feature": feature_names,
        "coefficient": coefficients,
        "absolute_coefficient": abs(coefficients)
    }).sort_values("absolute_coefficient", ascending=False)

    coef_df.to_csv(FEATURE_IMPORTANCE_PATH, index=False)

    print("Baseline employment model trained.")
    print(f"Model: {MODEL_PATH}")
    print(f"Report: {REPORT_PATH}")
    print(f"Feature coefficients: {FEATURE_IMPORTANCE_PATH}")
    print(json.dumps({k: v for k, v in metrics.items() if k not in ['classification_report', 'confusion_matrix']}, indent=2))

if __name__ == "__main__":
    main()
