# Phase 5A — Power BI Dashboard Model and Measures

## Objective

Phase 5A turns SEIP data into an analytics-ready Power BI model.

You will build:

- Power BI semantic model
- Core DAX measures
- Dashboard page structure
- Row-level security rules
- PostgreSQL/Databricks connection approach
- Field mapping
- Dashboard design blueprint

## Files added

```text
bi/powerbi/model/SEIP_PowerBI_Model_Spec.md
bi/powerbi/model/PowerBI_Connection_Guide.md
bi/powerbi/model/PowerBI_Field_Mapping.csv
bi/powerbi/dax/SEIP_DAX_Measures.dax
bi/powerbi/dax/SEIP_Gold_CSV_DAX_Measures.dax
bi/powerbi/dashboard_specs/SEIP_Dashboard_Page_Specs.md
bi/powerbi/rls/SEIP_RLS_Rules.md
bi/powerbi/rls/security_user_access_sample.csv
sql/16_powerbi_views.sql
```

## Step 1 — Run Power BI views in PostgreSQL

From VS Code:

```powershell
Get-Content sql/16_powerbi_views.sql | docker exec -i seip_postgres_airflow psql -U postgres -d seip_db
```

This creates cleaner Power BI-facing views:

```text
vw_powerbi_employment_fact
vw_powerbi_job_seeker_survey
vw_powerbi_location
```

## Step 2 — Open Power BI Desktop

Click:

```text
Get Data → PostgreSQL database
```

Connection:

```text
Server: localhost
Database: seip_db
Username: seip_admin
Password: change_me
```

Import:

```text
seip_core.vw_person_safe
seip_core.vw_powerbi_location
seip_core.vw_powerbi_employment_fact
seip_core.vw_powerbi_job_seeker_survey
```

## Step 3 — Create relationships

Create these relationships:

```text
vw_person_safe[person_key] 1 → * vw_powerbi_employment_fact[person_key]
vw_person_safe[person_key] 1 → * vw_powerbi_job_seeker_survey[person_key]

vw_powerbi_location[location_key] 1 → * vw_powerbi_employment_fact[location_key]
vw_powerbi_location[location_key] 1 → * vw_powerbi_job_seeker_survey[location_key]
```

Set cross-filter direction to:

```text
Single
```

## Step 4 — Create measures table

In Power BI:

```text
Home → Enter Data
```

Create a blank table called:

```text
_Measures
```

Then paste measures from:

```text
bi/powerbi/dax/SEIP_DAX_Measures.dax
```

## Step 5 — Build dashboard pages

Use:

```text
bi/powerbi/dashboard_specs/SEIP_Dashboard_Page_Specs.md
```

Recommended pages:

1. Executive Overview
2. Township Employment Profile
3. Youth and Skills Gap
4. Digital Access and Readiness
5. Data Quality Monitor

## Step 6 — Add slicers

Add slicers for:

```text
Township
Ward
Gender
Age
Highest Qualification
Survey Date
Digital Literacy Level
```

## Step 7 — Add RLS

Import:

```text
bi/powerbi/rls/security_user_access_sample.csv
```

Then follow:

```text
bi/powerbi/rls/SEIP_RLS_Rules.md
```

## Step 8 — Save report

Save as:

```text
SEIP_Employment_Intelligence_Dashboard.pbix
```

## Step 9 — Git commit

```powershell
git add .
git commit -m "Implement Phase 5A Power BI semantic model and DAX measures"
```

## Recommended visual theme

Use a clean public-sector style:

```text
Background: light
Cards: high contrast
Maps: township/ward focused
Tables: minimal, executive-friendly
```

## Important POPIA reminder

Do not import:

```text
first_name_encrypted
last_name_encrypted
id_number_hash
mobile_number_hash
email_hash
whatsapp_number_hash
```

unless there is a legitimate analytics reason.

For dashboards, use:

```text
vw_person_safe
aggregated Gold tables
masked/anonymous fields only
```
