import subprocess
import sys
from pathlib import Path
import shutil

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def run(script):
    print(f"\nRunning {script}...")
    subprocess.run([sys.executable, str(PROJECT_ROOT / script)], check=True)

def main():
    dataset = PROJECT_ROOT / "ml/data/employment_prediction_dataset.csv"
    sample = PROJECT_ROOT / "ml/data/sample_employment_prediction_dataset.csv"

    if not dataset.exists() and sample.exists():
        shutil.copy(sample, dataset)
        print("No ML dataset found. Copied sample dataset for demonstration.")

    run("ml/scripts/train_model_comparison.py")
    run("ml/scripts/fairness_check.py")
    run("ml/scripts/train_with_mlflow.py")

    print("\nPhase 6B pipeline complete.")

if __name__ == "__main__":
    main()
