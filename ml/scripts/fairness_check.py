from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from ml.scripts.feature_engineering import add_employment_features

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "ml" / "data" / "employment_prediction_dataset.csv"
MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "best_employment_model.joblib"
REPORT_PATH = PROJECT_ROOT / "ml" / "reports" / "fairness_check_report.json"

TARGET = "currently_employed"
GROUP_COLUMNS = ["gender_code", "township_code", "age_band"]

def target_to_bool(series):
    return series.astype(str).str.lower().isin(["true", "1", "yes"])

def group_metrics(df, group_col):
    rows = []
    for group_value, g in df.groupby(group_col, dropna=False):
        if len(g) < 2:
            continue
        y_true = g["actual"]
        y_pred = g["predicted"]
        rows.append({
            "group_column": group_col,
            "group_value": str(group_value),
            "records": int(len(g)),
            "actual_positive_rate": float(y_true.mean()),
            "predicted_positive_rate": float(y_pred.mean()),
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "precision": float(precision_score(y_true, y_pred, zero_division=0)),
            "recall": float(recall_score(y_true, y_pred, zero_division=0)),
            "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        })
    return rows

def main():
    df = pd.read_csv(DATA_PATH)
    df = add_employment_features(df)
    model = joblib.load(MODEL_PATH)

    y = target_to_bool(df[TARGET])
    X = df.drop(columns=[c for c in ["person_key", TARGET] if c in df.columns])

    df["actual"] = y
    df["predicted"] = model.predict(X)
    df["employment_probability"] = model.predict_proba(X)[:, 1]

    fairness_rows = []
    for group_col in GROUP_COLUMNS:
        if group_col in df.columns:
            fairness_rows.extend(group_metrics(df, group_col))

    report = {
        "note": "This is a basic fairness diagnostic. It does not prove fairness or remove bias.",
        "group_metrics": fairness_rows
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Fairness report written to: {REPORT_PATH}")

if __name__ == "__main__":
    main()
