import subprocess
import sys

def main():
    result = subprocess.run([sys.executable, "-m", "pytest", "-q"])
    raise SystemExit(result.returncode)

if __name__ == "__main__":
    main()
