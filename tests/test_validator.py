import pandas as pd
from src.validators.survey_validator import JobSeekerValidator

REQUIRED = [
    "respondent_id", "consent_given", "first_name", "last_name",
    "id_number", "date_of_birth", "gender", "township", "survey_date"
]
TOWNSHIPS = {"SOWETO", "ALEXANDRA"}

def base_row():
    return {
        "respondent_id": "JS001",
        "consent_given": True,
        "first_name": "Thabo",
        "last_name": "Mokoena",
        "id_number": "9001015009081",
        "date_of_birth": "1990-01-01",
        "gender": "Male",
        "township": "SOWETO",
        "survey_date": "2026-06-10",
        "nqf_level": 4,
        "gps_latitude": -26.2311,
        "gps_longitude": 27.9226,
    }

def test_valid_record_is_accepted():
    validator = JobSeekerValidator(REQUIRED, TOWNSHIPS)
    accepted, rejected = validator.validate(pd.DataFrame([base_row()]))
    assert len(accepted) == 1
    assert len(rejected) == 0

def test_missing_consent_is_rejected():
    validator = JobSeekerValidator(REQUIRED, TOWNSHIPS)
    row = base_row()
    row["consent_given"] = False
    accepted, rejected = validator.validate(pd.DataFrame([row]))
    assert len(accepted) == 0
    assert "CONSENT_REQUIRED" in rejected.iloc[0]["validation_errors"]

def test_invalid_township_is_rejected():
    validator = JobSeekerValidator(REQUIRED, TOWNSHIPS)
    row = base_row()
    row["township"] = "UNKNOWN"
    accepted, rejected = validator.validate(pd.DataFrame([row]))
    assert "TOWNSHIP_VALID" in rejected.iloc[0]["validation_errors"]

def test_missing_required_column_raises_error():
    validator = JobSeekerValidator(REQUIRED, TOWNSHIPS)
    row = base_row()
    row.pop("first_name")
    try:
        validator.validate(pd.DataFrame([row]))
        assert False
    except ValueError as exc:
        assert "Missing required columns" in str(exc)
