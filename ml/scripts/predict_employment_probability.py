from pathlib import Path
import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "baseline_employment_model.joblib"
INPUT_PATH = PROJECT_ROOT / "ml" / "data" / "employment_prediction_dataset.csv"
OUTPUT_PATH = PROJECT_ROOT / "ml" / "reports" / "employment_probability_scores.csv"

def main():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not found. Run train_baseline_employment_model.py first.")

    model = joblib.load(MODEL_PATH)
    df = pd.read_csv(INPUT_PATH)

    scoring_df = df.drop(columns=[c for c in ["person_key", "currently_employed"] if c in df.columns])
    probabilities = model.predict_proba(scoring_df)[:, 1]
    predictions = model.predict(scoring_df)

    output = df.copy()
    output["employment_probability"] = probabilities
    output["employment_prediction"] = predictions

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(OUTPUT_PATH, index=False)

    print(f"Scores written to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
