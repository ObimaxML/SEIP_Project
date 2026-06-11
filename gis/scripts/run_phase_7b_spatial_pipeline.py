import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

scripts = [
    "gis/scripts/spatial_clustering.py",
    "gis/scripts/opportunity_access_score.py",
    "gis/scripts/training_centre_optimisation.py",
    "gis/scripts/create_interactive_gis_map.py",
]

def run(script):
    print(f"\nRunning {script}...")
    subprocess.run([sys.executable, str(PROJECT_ROOT / script)], check=True)

def main():
    for script in scripts:
        run(script)
    print("\nPhase 7B spatial intelligence pipeline complete.")

if __name__ == "__main__":
    main()
