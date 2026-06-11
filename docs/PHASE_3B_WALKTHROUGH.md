# Phase 3B — POPIA Protection and PostgreSQL Loader

## What this phase does

1. Reads job seeker CSV/XLSX files from `data/raw`
2. Validates records
3. Splits accepted and rejected outputs
4. Encrypts first name and last name
5. Hashes ID, mobile, email and WhatsApp values
6. Upserts `dim_location`
7. Upserts `dim_person`
8. Inserts `fact_employment_status`
9. Inserts `fact_job_seeker_survey`
10. Inserts raw JSON into `seip_staging.stg_job_seeker`
11. Logs the ETL run in `seip_audit.aud_etl_run_log`

## Commands

```powershell
python generate_dev_fernet_key.py
copy .env.example .env
docker compose up -d
powershell -ExecutionPolicy Bypass -File run_all_sql.ps1
python run_phase_3b_job_seeker_to_postgres.py
```

## Verify

```sql
SELECT * FROM seip_core.vw_person_safe;
SELECT * FROM seip_core.vw_unemployment_by_township;
SELECT * FROM seip_audit.aud_etl_run_log ORDER BY started_at DESC;
SELECT * FROM seip_staging.stg_job_seeker ORDER BY loaded_at DESC;
```
