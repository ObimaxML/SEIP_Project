# SEIP Phase 5A — Power BI Semantic Model Specification

## Objective

Build a Power BI semantic model for the Soweto Employment Intelligence Platform using either:

1. PostgreSQL warehouse views/tables, or
2. Databricks Gold CSV exports.

Recommended portfolio path:

```text
Databricks Gold exports → Power BI Desktop
```

Recommended enterprise path:

```text
PostgreSQL / Databricks SQL Warehouse → Power BI Service
```

## Core entities

### Fact tables

| Table | Grain | Purpose |
|---|---|---|
| fact_employment_status | One employment observation per person per survey date | Employment, unemployment and job-seeking metrics |
| fact_job_seeker_survey | One survey per person per date | Digital access, transport, relocation and training interest |
| gold_unemployment_by_township | One row per township | Executive unemployment KPI summary |
| gold_skills_training_demand | One row per township and training area | Training demand analysis |
| gold_digital_access | One row per township | Smartphone and internet access KPIs |

### Dimension tables

| Table | Purpose |
|---|---|
| dim_person / vw_person_safe | Safe demographic profile without raw PII |
| dim_location | Township, ward, suburb and GIS location |
| ref_township | Township reference values |
| dim_skill | Skills reference |
| dim_date | Date filtering and time intelligence |

## Recommended model relationships

```text
dim_location[location_key] 1 ── * fact_employment_status[location_key]
dim_location[location_key] 1 ── * fact_job_seeker_survey[location_key]

vw_person_safe[person_key] 1 ── * fact_employment_status[person_key]
vw_person_safe[person_key] 1 ── * fact_job_seeker_survey[person_key]

dim_date[full_date] 1 ── * fact_employment_status[survey_date]
dim_date[full_date] 1 ── * fact_job_seeker_survey[survey_date]
```

## Recommended import mode

For portfolio:

```text
Import mode
```

For production:

```text
DirectQuery for large fact tables
Import/Dual for dimensions
Incremental refresh for survey facts
```

## Security note

Use `vw_person_safe`, not `dim_person`, for analytics users. Raw PII columns must not be imported into Power BI.
