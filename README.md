# SEIP — Soweto Employment Intelligence Platform

This package contains the working implementation from Phase 0.5 to Phase 3B.

## Included

- Docker PostgreSQL/PostGIS environment
- PostgreSQL DDL scripts
- Reference, dimension, staging, fact and audit tables
- Quality constraints and validation scripts
- Job seeker data collection template
- Python extractor and validator
- POPIA encryption and HMAC hashing utilities
- PostgreSQL loader
- ETL audit logging

## Quick start

```powershell
cd SEIP_Project_Phase_0_to_3B
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python generate_dev_fernet_key.py
```

Paste the generated key into `.env` as `POPIA_SECRET_KEY`.

Then run:

```powershell
docker compose up -d
powershell -ExecutionPolicy Bypass -File run_all_sql.ps1
python run_phase_3b_job_seeker_to_postgres.py
```

## Verify

```sql
SELECT * FROM seip_core.vw_person_safe;
SELECT * FROM seip_core.vw_unemployment_by_township;
SELECT * FROM seip_audit.aud_etl_run_log ORDER BY started_at DESC;
```


## Phase 3C additions

Run tests:

```powershell
python -m pytest -q
```

Reset and rebuild database:

```powershell
powershell -ExecutionPolicy Bypass -File reset_and_rebuild_db.ps1
```

Read:

```text
docs/PHASE_3C_TESTING_AND_HARDENING.md
```


## Phase 4B additions

Databricks Lakehouse notebooks added:

```text
notebooks/databricks/00_mount_and_config.py
notebooks/databricks/01_bronze_ingest_job_seekers.py
notebooks/databricks/02_silver_clean_job_seekers.py
notebooks/databricks/03_gold_kpi_tables.py
notebooks/databricks/04_gold_sql_views.py
notebooks/databricks/05_export_gold_to_csv.py
```

Read:

```text
docs/PHASE_4B_DATABRICKS_LAKEHOUSE.md
```


## Phase 5A additions

Power BI model, DAX and dashboard design files added:

```text
docs/PHASE_5A_POWERBI_DASHBOARD_MODEL.md
bi/powerbi/dax/SEIP_DAX_Measures.dax
bi/powerbi/dashboard_specs/SEIP_Dashboard_Page_Specs.md
bi/powerbi/rls/SEIP_RLS_Rules.md
```


## Phase 5B additions

Power BI page-by-page build walkthrough added:

```text
docs/PHASE_5B_POWERBI_VISUAL_BUILD_WALKTHROUGH.md
bi/powerbi/dashboard_specs/SEIP_Page_1_Executive_Overview.md
bi/powerbi/dashboard_specs/SEIP_Page_2_Township_Profile.md
bi/powerbi/dashboard_specs/SEIP_Page_3_Youth_Skills.md
bi/powerbi/dashboard_specs/SEIP_Page_4_Digital_Access.md
bi/powerbi/dashboard_specs/SEIP_Page_5_Data_Quality.md
```


## Phase 6A additions

Machine learning baseline added:

```text
docs/PHASE_6A_MACHINE_LEARNING_BASELINE_MODEL.md
ml/scripts/build_ml_dataset.py
ml/scripts/train_baseline_employment_model.py
ml/scripts/predict_employment_probability.py
ml/scripts/train_from_sample_dataset.py
```

To test ML without PostgreSQL data:

```powershell
python ml/scripts/train_from_sample_dataset.py
```


## Phase 6B additions

Model improvement, fairness and MLflow tracking added:

```text
docs/PHASE_6B_MODEL_IMPROVEMENT_FAIRNESS_MLFLOW.md
ml/scripts/run_phase_6b_pipeline.py
```

Run:

```powershell
python ml/scripts/run_phase_6b_pipeline.py
```


## Phase 7B additions

Predictive spatial intelligence added:

```text
docs/PHASE_7B_PREDICTIVE_SPATIAL_INTELLIGENCE.md
gis/scripts/run_phase_7b_spatial_pipeline.py
```

Run:

```powershell
python gis/scripts/run_phase_7b_spatial_pipeline.py
```
