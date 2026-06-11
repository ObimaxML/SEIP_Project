# Phase 3C — Testing, Error Handling and Production-Ready ETL Improvements

## Objective

Phase 3C hardens the ETL so it behaves more like a real data engineering pipeline.

## Added files

```text
src/utils/exceptions.py
src/utils/data_quality_report.py
tests/test_popia.py
tests/test_validator.py
tests/test_extractor.py
run_phase_3c_smoke_tests.py
run_tests.ps1
reset_and_rebuild_db.ps1
```

## What this phase adds

1. Unit tests for encryption, hashing, SA ID validation, extraction and validation.
2. A data quality report generated during the ETL run.
3. Custom exception classes for cleaner production error handling.
4. A reset-and-rebuild script for local development.
5. A smoke-test runner.

## Implementation steps

### Step 1 — Open the project

```powershell
cd C:\Projects\SEIP_Project_Phase_0_to_3C
code .
```

### Step 2 — Activate environment

```powershell
.venv\Scripts\activate
```

### Step 3 — Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 4 — Run tests

```powershell
python -m pytest -q
```

Expected:

```text
9 passed
```

### Step 5 — Reset and rebuild database

```powershell
powershell -ExecutionPolicy Bypass -File reset_and_rebuild_db.ps1
```

### Step 6 — Run ETL

```powershell
python run_phase_3b_job_seeker_to_postgres.py
```

### Step 7 — Check outputs

```text
data/processed/job_seekers_accepted_*.csv
data/rejected/job_seekers_rejected_*.csv
data/processed/quality_report_*.csv
logs/seip_etl_*.log
```

### Step 8 — Verify in pgAdmin

```sql
SELECT * FROM seip_core.vw_person_safe;

SELECT * 
FROM seip_audit.aud_etl_run_log
ORDER BY started_at DESC;

SELECT *
FROM seip_staging.stg_job_seeker
ORDER BY loaded_at DESC;
```

## Why this matters

This prepares SEIP for:

- Airflow retries
- CI/CD testing
- GitHub Actions
- Better ETL observability
- Databricks Bronze/Silver/Gold ingestion
