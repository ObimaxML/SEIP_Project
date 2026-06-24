# SEIP Phase 5A — Power BI Connection Guide

## Option 1 — Connect to PostgreSQL

Use this when you want Power BI connected directly to your local SEIP PostgreSQL warehouse.

### Steps

1. Open Power BI Desktop.
2. Click **Get Data**.
3. Select **PostgreSQL database**.
4. Server:

```text
localhost
```

5. Database:

```text
seip_db
```

6. Authentication:

```text
Database
Username: postgres
Password: Krbgp012
```

7. Select these tables/views:

```text
seip_core.vw_person_safe
seip_core.dim_location
seip_core.ref_township
seip_core.fact_employment_status
seip_core.fact_job_seeker_survey
```

8. Click **Transform Data**.
9. Confirm data types.
10. Load.

## Option 2 — Import Databricks Gold CSV exports

Use this when you export Gold tables from Databricks.

Import:

```text
gold_unemployment_by_township
gold_skills_training_demand
gold_digital_access
```

Then use:

```text
bi/powerbi/dax/SEIP_Gold_CSV_DAX_Measures.dax
```

## Option 3 — Connect to Databricks SQL Warehouse

Use this in a more enterprise-style implementation.

1. In Databricks, create SQL Warehouse.
2. Get server hostname and HTTP path.
3. In Power BI, select **Azure Databricks** connector.
4. Paste server hostname and HTTP path.
5. Select Gold tables and SQL views.

## Recommended for you now

Start with:

```text
Option 1 — PostgreSQL
```

Then later use:

```text
Option 2 — Databricks Gold CSV exports
```

This gives you both a local working dashboard and a lakehouse-backed portfolio story.
