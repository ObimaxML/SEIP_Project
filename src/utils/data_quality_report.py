import pandas as pd
from pathlib import Path
from datetime import datetime

def build_quality_summary(df: pd.DataFrame, accepted: pd.DataFrame, rejected: pd.DataFrame) -> pd.DataFrame:
    total = len(df)
    accepted_count = len(accepted)
    rejected_count = len(rejected)

    rows = [
        {"metric": "records_received", "value": total},
        {"metric": "records_accepted", "value": accepted_count},
        {"metric": "records_rejected", "value": rejected_count},
        {"metric": "acceptance_rate_pct", "value": round((accepted_count / total * 100), 2) if total else 0},
        {"metric": "rejection_rate_pct", "value": round((rejected_count / total * 100), 2) if total else 0},
    ]

    if not rejected.empty and "validation_errors" in rejected.columns:
        error_counts = {}
        for errors in rejected["validation_errors"]:
            for err in errors:
                error_counts[err] = error_counts.get(err, 0) + 1

        for error_code, count in sorted(error_counts.items()):
            rows.append({"metric": f"error_{error_code}", "value": count})

    return pd.DataFrame(rows)

def write_quality_report(df: pd.DataFrame, accepted: pd.DataFrame, rejected: pd.DataFrame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_quality_summary(df, accepted, rejected)
    path = output_dir / f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    report.to_csv(path, index=False)
    return path
