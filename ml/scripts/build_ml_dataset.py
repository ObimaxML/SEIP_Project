from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from src.config.settings import DATABASE_URL

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = PROJECT_ROOT / "ml" / "data" / "employment_prediction_dataset.csv"

QUERY = """
SELECT
    p.person_key,
    p.gender_code,
    p.age,
    p.south_african_citizen,
    p.highest_qualification,
    p.education_level_code,
    p.field_of_study,
    p.nqf_level,
    l.township_code,
    l.ward_number,
    f.currently_employed,
    f.months_unemployed,
    f.seeking_work,
    f.preferred_sector,
    f.income_band,
    s.digital_literacy_level,
    s.has_smartphone,
    s.transport_mode,
    s.willing_to_relocate,
    s.training_interest,
    s.completeness_score,
    s.quality_score
FROM seip_core.vw_person_safe p
LEFT JOIN seip_core.dim_location l
    ON p.township_code = l.township_code
LEFT JOIN seip_core.fact_employment_status f
    ON p.person_key = f.person_key
LEFT JOIN seip_core.fact_job_seeker_survey s
    ON p.person_key = s.person_key
WHERE f.currently_employed IS NOT NULL
"""

def main():
    engine = create_engine(DATABASE_URL)
    df = pd.read_sql(QUERY, engine)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"ML dataset created: {OUTPUT_PATH}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

if __name__ == "__main__":
    main()
