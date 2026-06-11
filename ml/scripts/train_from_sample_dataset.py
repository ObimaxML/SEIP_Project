from pathlib import Path
import shutil
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sample = PROJECT_ROOT / "ml" / "data" / "sample_employment_prediction_dataset.csv"
target = PROJECT_ROOT / "ml" / "data" / "employment_prediction_dataset.csv"

shutil.copy(sample, target)
print(f"Copied sample dataset to {target}")

subprocess.run([sys.executable, str(PROJECT_ROOT / "ml" / "scripts" / "train_baseline_employment_model.py")], check=True)
subprocess.run([sys.executable, str(PROJECT_ROOT / "ml" / "scripts" / "predict_employment_probability.py")], check=True)
