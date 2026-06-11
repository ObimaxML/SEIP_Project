from pathlib import Path
import json
import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from ml.scripts.feature_engineering import add_employment_features

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "ml" / "data" / "employment_prediction_dataset.csv"
MLRUNS_PATH = PROJECT_ROOT / "mlruns"

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

def target_to_bool(series):
    return series.astype(str).str.lower().isin(["true", "1", "yes"])

def main():
    mlflow.set_tracking_uri(f"file:///{MLRUNS_PATH.as_posix()}")
    mlflow.set_experiment("SEIP Employment Prediction")

    df = pd.read_csv(DATA_PATH)
    df = add_employment_features(df)

    y = target_to_bool(df[TARGET])
    X = df.drop(columns=[c for c in ["person_key", TARGET] if c in df.columns])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y if y.value_counts().min() >= 2 else None
    )

    preprocessor = ColumnTransformer([
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), NUMERIC_FEATURES),
        ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), CATEGORICAL_FEATURES),
    ])

    params = {
        "n_estimators": 200,
        "max_depth": None,
        "class_weight": "balanced",
        "random_state": 42
    }

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", RandomForestClassifier(**params))
    ])

    with mlflow.start_run(run_name="random_forest_feature_engineered"):
        mlflow.log_params(params)
        mlflow.log_param("rows", len(df))
        mlflow.log_param("features_numeric", ",".join(NUMERIC_FEATURES))
        mlflow.log_param("features_categorical", ",".join(CATEGORICAL_FEATURES))

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1": f1_score(y_test, y_pred, zero_division=0),
            "roc_auc": roc_auc_score(y_test, y_prob) if y_test.nunique() == 2 else 0,
        }

        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(pipeline, "model")

        print("MLflow run complete.")
        print(json.dumps(metrics, indent=2))
        print(f"Tracking URI: file:///{MLRUNS_PATH.as_posix()}")

if __name__ == "__main__":
    main()
