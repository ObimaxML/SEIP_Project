import pandas as pd
from datetime import date
from src.utils.popia import valid_sa_id_luhn

class JobSeekerValidator:
    def __init__(self, required_columns, valid_townships):
        self.required_columns = required_columns
        self.valid_townships = valid_townships

    def validate_required_columns(self, df):
        missing = [c for c in self.required_columns if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    def parse_bool(self, value):
        if isinstance(value, bool):
            return value
        if pd.isna(value):
            return False
        return str(value).strip().lower() in ["true", "yes", "y", "1"]

    def calculate_age(self, dob):
        dob = pd.to_datetime(dob, errors="coerce")
        if pd.isna(dob):
            return None
        today = pd.Timestamp(date.today())
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    def validate_row(self, row):
        errors = []

        if not self.parse_bool(row.get("consent_given")):
            errors.append("CONSENT_REQUIRED")

        age = self.calculate_age(row.get("date_of_birth"))
        if age is None or age < 14 or age > 80:
            errors.append("AGE_RANGE_VALID")

        if str(row.get("township", "")).strip().upper() not in self.valid_townships:
            errors.append("TOWNSHIP_VALID")

        if not valid_sa_id_luhn(str(row.get("id_number", ""))):
            errors.append("SA_ID_LUHN_VALID")

        nqf = row.get("nqf_level")
        if pd.notna(nqf):
            try:
                nqf = int(nqf)
                if nqf < 1 or nqf > 10:
                    errors.append("NQF_LEVEL_VALID")
            except Exception:
                errors.append("NQF_LEVEL_VALID")

        lat, lon = row.get("gps_latitude"), row.get("gps_longitude")
        if pd.notna(lat) and pd.notna(lon):
            try:
                lat, lon = float(lat), float(lon)
                if not (-27.5 <= lat <= -25.0 and 27.0 <= lon <= 29.5):
                    errors.append("GPS_IN_GAUTENG")
            except Exception:
                errors.append("GPS_IN_GAUTENG")

        return errors

    def validate(self, df):
        self.validate_required_columns(df)
        df = df.copy()
        df["validation_errors"] = df.apply(self.validate_row, axis=1)
        df["validation_status"] = df["validation_errors"].apply(
            lambda e: "VALID" if len(e) == 0 else "REJECTED"
        )
        return (
            df[df["validation_status"] == "VALID"].copy(),
            df[df["validation_status"] == "REJECTED"].copy()
        )
