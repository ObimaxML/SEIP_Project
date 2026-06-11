# Phase 4B — Databricks Bronze, Silver and Gold Lakehouse

## Objective

Phase 4B adds the SEIP Lakehouse layer using Databricks and Delta-style Bronze, Silver and Gold zones.

This extends the PostgreSQL warehouse with a scalable analytics layer for:

- Large survey files
- Historical snapshots
- Cleaned analytics datasets
- Power BI/Tableau-ready KPI tables
- Future ML datasets

## Architecture

```text
Raw CSV files
    ↓
Bronze Delta
Raw append-only data with ingestion metadata
    ↓
Silver Delta
Cleaned, typed, deduplicated, PII-masked records
    ↓
Gold Delta
KPI tables for dashboards and ML
```

## Notebook execution order

Run these notebooks in this order:

```text
00_mount_and_config.py
01_bronze_ingest_job_seekers.py
02_silver_clean_job_seekers.py
03_gold_kpi_tables.py
04_gold_sql_views.py
05_export_gold_to_csv.py
```

## Step 1 — Create Databricks workspace

Use one of these:

### Option A — Databricks Community Edition

Good for portfolio and learning.

### Option B — Azure Databricks

Better for enterprise-style implementation.

For now, use Community Edition unless you already have Azure access.

## Step 2 — Upload raw sample file

Upload this file into Databricks:

```text
notebooks/databricks/sample_upload_job_seekers.csv
```

Target DBFS path:

```text
dbfs:/FileStore/seip/raw/job_seekers/sample_job_seekers.csv
```

In Databricks UI:

```text
Data
Add Data
Upload File
```

Then move/copy it to the expected path if needed.

## Step 3 — Upload notebooks

Upload these notebooks from:

```text
notebooks/databricks/
```

Import them into your Databricks workspace.

## Step 4 — Run Notebook 00

Notebook:

```text
00_mount_and_config.py
```

This creates the working database:

```sql
seip_lakehouse
```

and confirms the DBFS paths:

```text
dbfs:/FileStore/seip/raw/job_seekers
dbfs:/FileStore/seip/delta/bronze/job_seekers
dbfs:/FileStore/seip/delta/silver/job_seekers
dbfs:/FileStore/seip/delta/gold
```

## Step 5 — Run Notebook 01: Bronze

Notebook:

```text
01_bronze_ingest_job_seekers.py
```

This reads raw CSV data and writes:

```text
seip_lakehouse.bronze_job_seekers
```

Bronze is raw and append-only.

It adds:

```text
_ingestion_timestamp
_source_file
_bronze_load_date
```

## Step 6 — Run Notebook 02: Silver

Notebook:

```text
02_silver_clean_job_seekers.py
```

This creates:

```text
seip_lakehouse.silver_job_seekers
```

Silver performs:

- String trimming
- Township standardisation
- Boolean conversion
- Date conversion
- Numeric conversion
- Age calculation
- SHA-256 hashing
- PII masking
- Validation status assignment
- Deduplication by ID hash

## Step 7 — Run Notebook 03: Gold

Notebook:

```text
03_gold_kpi_tables.py
```

This creates:

```text
seip_lakehouse.gold_unemployment_by_township
seip_lakehouse.gold_skills_training_demand
seip_lakehouse.gold_digital_access
```

These are BI-ready KPI tables.

## Step 8 — Run Notebook 04: BI Views

Notebook:

```text
04_gold_sql_views.py
```

This creates:

```text
vw_executive_unemployment_summary
vw_training_demand_summary
vw_digital_access_summary
```

## Step 9 — Run Notebook 05: Export to CSV

Notebook:

```text
05_export_gold_to_csv.py
```

This exports Gold datasets to:

```text
dbfs:/FileStore/seip/exports/
```

You can download these CSVs and import them into Power BI or Tableau.

## Gold KPIs created

### Unemployment by township

```text
township
total_job_seekers
employed_count
unemployed_count
unemployment_rate_pct
avg_months_unemployed
youth_count
```

### Skills/training demand

```text
township
preferred_training_area
demand_count
interested_count
training_interest_rate_pct
```

### Digital access

```text
township
total_job_seekers
smartphone_users
internet_users
smartphone_access_pct
internet_access_pct
```

## Verification queries

Run in Databricks SQL cell:

```sql
USE seip_lakehouse;

SHOW TABLES;
```

```sql
SELECT *
FROM gold_unemployment_by_township;
```

```sql
SELECT *
FROM vw_executive_unemployment_summary;
```

## Important design note

The PostgreSQL layer remains your relational warehouse and POPIA-controlled operational data store.

Databricks becomes your scalable analytical lakehouse layer.

For portfolio purposes:

```text
PostgreSQL = structured warehouse and audit layer
Databricks = scalable analytics and ML feature layer
Power BI/Tableau = reporting and presentation layer
```

## Git commit

```powershell
git add .
git commit -m "Implement Phase 4B Databricks lakehouse Bronze Silver Gold"
```
