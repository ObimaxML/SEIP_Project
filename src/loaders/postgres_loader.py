import json
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

class PostgresLoader:
    def __init__(self, database_url: str, popia_protector):
        self.engine = create_engine(database_url)
        self.popia = popia_protector

    def parse_bool(self, value):
        if isinstance(value, bool):
            return value
        if pd.isna(value):
            return False
        return str(value).strip().lower() in ["true", "yes", "y", "1"]

    def clean_date(self, value):
        if pd.isna(value) or value == "":
            return None
        try:
            return pd.to_datetime(value).date()
        except Exception:
            return None

    def start_etl_run(self, pipeline_name, source_file_name, records_received):
        sql = text("""
            INSERT INTO seip_audit.aud_etl_run_log
            (pipeline_name, source_file_name, status, records_received)
            VALUES (:pipeline_name, :source_file_name, 'RUNNING', :records_received)
            RETURNING etl_run_id
        """)
        with self.engine.begin() as conn:
            return conn.execute(sql, {
                "pipeline_name": pipeline_name,
                "source_file_name": source_file_name,
                "records_received": records_received
            }).scalar()

    def finish_etl_run(self, etl_run_id, status, loaded, rejected, error_message=None):
        sql = text("""
            UPDATE seip_audit.aud_etl_run_log
            SET status=:status, records_loaded=:loaded,
                records_rejected=:rejected, error_message=:error_message,
                completed_at=CURRENT_TIMESTAMP
            WHERE etl_run_id=:etl_run_id
        """)
        with self.engine.begin() as conn:
            conn.execute(sql, {
                "etl_run_id": etl_run_id, "status": status,
                "loaded": loaded, "rejected": rejected,
                "error_message": error_message
            })

    def insert_staging(self, conn, row, status, errors):
        payload = row.where(pd.notna(row), None).to_dict()
        sql = text("""
            INSERT INTO seip_staging.stg_job_seeker
            (source_file_name, raw_payload, validation_status, validation_errors)
            VALUES (:source_file_name, CAST(:raw_payload AS jsonb), :status, CAST(:errors AS jsonb))
        """)
        conn.execute(sql, {
            "source_file_name": payload.get("source_file_name", "unknown"),
            "raw_payload": json.dumps(payload, default=str),
            "status": status,
            "errors": json.dumps(errors or [], default=str)
        })

    def upsert_location(self, conn, row):
        township = str(row.get("township", "")).strip().upper()
        ward = row.get("ward_number")
        # Ensure ward is None if it is NaN or empty, otherwise force to int
        if pd.isna(ward) or ward == "":
            ward = None
        else:
            ward = str(ward).strip()

        suburb = row.get("suburb")
        if pd.isna(suburb) or suburb == "":
            suburb = None

        existing = conn.execute(text("""
            SELECT location_key FROM seip_core.dim_location
            WHERE township_code=:township
              AND ward_number IS NOT DISTINCT FROM :ward
              AND suburb IS NOT DISTINCT FROM :suburb
            LIMIT 1
        """), {"township": township, "ward": ward, "suburb": suburb}).scalar()

        if existing:
            return existing

        lat = None if pd.isna(row.get("gps_latitude")) else float(row.get("gps_latitude"))
        lon = None if pd.isna(row.get("gps_longitude")) else float(row.get("gps_longitude"))

        return conn.execute(text("""
            INSERT INTO seip_core.dim_location
            (township_code, ward_number, suburb, municipality, province, latitude, longitude, geom)
            VALUES (:township, :ward, :suburb, 'City of Johannesburg', 'Gauteng',
                    :lat, :lon,
                    CASE WHEN :lat IS NULL OR :lon IS NULL
                         THEN NULL
                         ELSE ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
                    END)
            RETURNING location_key
        """), {"township": township, "ward": ward, "suburb": suburb, "lat": lat, "lon": lon}).scalar()

    def upsert_person(self, conn, row, location_key):
        id_hash = self.popia.hash_value(row.get("id_number"))
        existing = conn.execute(
            text("SELECT person_key FROM seip_core.dim_person WHERE id_number_hash=:id_hash"),
            {"id_hash": id_hash}
        ).scalar()

        params = {
            "first_name_encrypted": self.popia.encrypt_text(row.get("first_name")),
            "last_name_encrypted": self.popia.encrypt_text(row.get("last_name")),
            "id_number_hash": id_hash,
            "gender_code": row.get("gender"),
            "date_of_birth": self.clean_date(row.get("date_of_birth")),
            "nationality": row.get("nationality"),
            "south_african_citizen": self.parse_bool(row.get("south_african_citizen")),
            "highest_qualification": row.get("highest_qualification"),
            "education_level_code": row.get("education_level_code"),
            "field_of_study": row.get("field_of_study"),
            "nqf_level": None if pd.isna(row.get("nqf_level")) else int(row.get("nqf_level")),
            "employment_status_code": row.get("employment_status"),
            "location_key": location_key,
            "mobile_number_hash": self.popia.hash_value(row.get("mobile_number")),
            "email_hash": self.popia.hash_value(row.get("email")),
            "whatsapp_number_hash": self.popia.hash_value(row.get("whatsapp_number")),
            "consent_given": self.parse_bool(row.get("consent_given")),
            "consent_date": self.clean_date(row.get("consent_date")),
            "consent_version": "v1.0"
        }

        if existing:
            conn.execute(text("""
                UPDATE seip_core.dim_person
                SET gender_code=:gender_code,
                    date_of_birth=:date_of_birth,
                    nationality=:nationality,
                    south_african_citizen=:south_african_citizen,
                    highest_qualification=:highest_qualification,
                    education_level_code=:education_level_code,
                    field_of_study=:field_of_study,
                    nqf_level=:nqf_level,
                    employment_status_code=:employment_status_code,
                    location_key=:location_key,
                    mobile_number_hash=:mobile_number_hash,
                    email_hash=:email_hash,
                    whatsapp_number_hash=:whatsapp_number_hash,
                    consent_given=:consent_given,
                    consent_date=:consent_date,
                    updated_at=CURRENT_TIMESTAMP
                WHERE person_key=:person_key
            """), {**params, "person_key": existing})
            return existing

        return conn.execute(text("""
            INSERT INTO seip_core.dim_person (
                first_name_encrypted, last_name_encrypted, id_number_hash,
                gender_code, date_of_birth, nationality, south_african_citizen,
                highest_qualification, education_level_code, field_of_study, nqf_level,
                employment_status_code, location_key, mobile_number_hash, email_hash,
                whatsapp_number_hash, consent_given, consent_date, consent_version
            )
            VALUES (
                :first_name_encrypted, :last_name_encrypted, :id_number_hash,
                :gender_code, :date_of_birth, :nationality, :south_african_citizen,
                :highest_qualification, :education_level_code, :field_of_study, :nqf_level,
                :employment_status_code, :location_key, :mobile_number_hash, :email_hash,
                :whatsapp_number_hash, :consent_given, :consent_date, :consent_version
            )
            RETURNING person_key
        """), params).scalar()

    def insert_facts(self, conn, row, person_key, location_key):
        survey_date = self.clean_date(row.get("survey_date")) or datetime.now().date()
        conn.execute(text("""
            INSERT INTO seip_core.fact_employment_status
            (person_key, location_key, survey_date, currently_employed,
             months_unemployed, seeking_work, preferred_sector, income_band)
            VALUES (:person_key, :location_key, :survey_date, :currently_employed,
                    :months_unemployed, :seeking_work, :preferred_sector, :income_band)
        """), {
            "person_key": person_key,
            "location_key": location_key,
            "survey_date": survey_date,
            "currently_employed": self.parse_bool(row.get("currently_employed")),
            "months_unemployed": None if pd.isna(row.get("months_unemployed")) else int(row.get("months_unemployed")),
            "seeking_work": self.parse_bool(row.get("seeking_work")),
            "preferred_sector": row.get("preferred_sector"),
            "income_band": row.get("household_income_band")
        })

        conn.execute(text("""
            INSERT INTO seip_core.fact_job_seeker_survey
            (person_key, location_key, survey_date, digital_literacy_level,
             has_smartphone, transport_mode, willing_to_relocate,
             training_interest, completeness_score, quality_score)
            VALUES (:person_key, :location_key, :survey_date, :digital_literacy_level,
                    :has_smartphone, :transport_mode, :willing_to_relocate,
                    :training_interest, 90.0, 90.0)
        """), {
            "person_key": person_key,
            "location_key": location_key,
            "survey_date": survey_date,
            "digital_literacy_level": row.get("digital_literacy_level"),
            "has_smartphone": self.parse_bool(row.get("has_smartphone")),
            "transport_mode": row.get("transport_mode"),
            "willing_to_relocate": self.parse_bool(row.get("willing_to_relocate")),
            "training_interest": self.parse_bool(row.get("training_interest"))
        })

    def load_job_seekers(self, accepted_df, rejected_df):
        total = len(accepted_df) + len(rejected_df)
        etl_run_id = self.start_etl_run("job_seeker_csv_to_postgres", "data/raw", total)
        loaded = 0

        try:
            with self.engine.begin() as conn:
                for _, row in accepted_df.iterrows():
                    self.insert_staging(conn, row, "VALID", [])
                    location_key = self.upsert_location(conn, row)
                    person_key = self.upsert_person(conn, row, location_key)
                    self.insert_facts(conn, row, person_key, location_key)
                    loaded += 1

                for _, row in rejected_df.iterrows():
                    self.insert_staging(conn, row, "REJECTED", row.get("validation_errors", []))

            self.finish_etl_run(etl_run_id, "SUCCESS", loaded, len(rejected_df))
            return {"etl_run_id": str(etl_run_id), "status": "SUCCESS", "loaded": loaded, "rejected": len(rejected_df)}

        except Exception as exc:
            self.finish_etl_run(etl_run_id, "FAILED", loaded, len(rejected_df), str(exc))
            raise
