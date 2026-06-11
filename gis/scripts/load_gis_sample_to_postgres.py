from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from src.config.settings import DATABASE_URL

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_PATH = PROJECT_ROOT / "gis" / "sample_data" / "job_seeker_points_sample.csv"

def parse_bool(value):
    return str(value).strip().lower() in ["true", "1", "yes", "y"]

def main():
    engine = create_engine(DATABASE_URL)
    df = pd.read_csv(SAMPLE_PATH)

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO seip_gis.fact_job_seeker_location (
                    person_key, survey_date, township_code, ward_number,
                    latitude, longitude, currently_employed, age,
                    training_interest, preferred_training_area,
                    has_smartphone, transport_mode, geom
                )
                VALUES (
                    :person_key, CURRENT_DATE, :township_code, :ward_number,
                    :latitude, :longitude, :currently_employed, :age,
                    :training_interest, :preferred_training_area,
                    :has_smartphone, :transport_mode,
                    ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)
                )
            """), {
                "person_key": int(row["person_key"]),
                "township_code": row["township_code"],
                "ward_number": row["ward_number"],
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
                "currently_employed": parse_bool(row["currently_employed"]),
                "age": int(row["age"]),
                "training_interest": parse_bool(row["training_interest"]),
                "preferred_training_area": row["preferred_training_area"],
                "has_smartphone": parse_bool(row["has_smartphone"]),
                "transport_mode": row["transport_mode"],
            })

    print(f"Loaded GIS sample data from {SAMPLE_PATH}")

if __name__ == "__main__":
    main()
