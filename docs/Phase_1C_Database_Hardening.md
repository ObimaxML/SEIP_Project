# Phase 1C — Database Hardening

Goal: make the SEIP database safer, cleaner, repeatable, and harder to break before Python ETL starts. This supports the blueprint's requirements for POPIA compliance, auditability, RBAC, quality controls, and Git-controlled database development.

## Create These Files

```text
sql/
├── 12_constraints.sql
├── 13_quality_checks.sql
├── 14_seed_validation.sql
├── 15_rollback_dev.sql
└── run_all_sql.ps1
```

---

# `12_constraints.sql`

```sql
ALTER TABLE seip_core.dim_person
ADD CONSTRAINT chk_person_nqf_level
CHECK (nqf_level IS NULL OR nqf_level BETWEEN 1 AND 10);

ALTER TABLE seip_core.dim_person
ADD CONSTRAINT chk_person_consent_date
CHECK (
    consent_given = FALSE
    OR consent_date IS NOT NULL
);

ALTER TABLE seip_core.dim_person
ADD CONSTRAINT chk_person_birth_date
CHECK (
    date_of_birth IS NULL
    OR date_of_birth <= CURRENT_DATE
);

ALTER TABLE seip_core.fact_employment_status
ADD CONSTRAINT chk_months_unemployed
CHECK (
    months_unemployed IS NULL
    OR months_unemployed >= 0
);

ALTER TABLE seip_core.fact_job_seeker_survey
ADD CONSTRAINT chk_completeness_score
CHECK (
    completeness_score IS NULL
    OR completeness_score BETWEEN 0 AND 100
);

ALTER TABLE seip_core.fact_job_seeker_survey
ADD CONSTRAINT chk_quality_score
CHECK (
    quality_score IS NULL
    OR quality_score BETWEEN 0 AND 100
);

ALTER TABLE seip_core.fact_business_vacancy
ADD CONSTRAINT chk_vacancy_count
CHECK (vacancy_count >= 0);

ALTER TABLE seip_core.fact_training_outcome
ADD CONSTRAINT chk_training_counts
CHECK (
    completed_count <= enrolled_count
    AND placed_count <= completed_count
);

ALTER TABLE seip_core.fact_training_outcome
ADD CONSTRAINT chk_training_rates
CHECK (
    completion_rate BETWEEN 0 AND 100
    AND placement_rate BETWEEN 0 AND 100
);
```

---

# `13_quality_checks.sql`

```sql
-- 1. People without consent
SELECT *
FROM seip_core.dim_person
WHERE consent_given = FALSE;

-- 2. People with invalid age
SELECT *
FROM seip_core.dim_person
WHERE age < 14 OR age > 80;

-- 3. People without location
SELECT *
FROM seip_core.dim_person
WHERE location_key IS NULL;

-- 4. Employment facts without matching person
SELECT f.*
FROM seip_core.fact_employment_status f
LEFT JOIN seip_core.dim_person p
    ON f.person_key = p.person_key
WHERE p.person_key IS NULL;

-- 5. Location records without geometry
SELECT *
FROM seip_core.dim_location
WHERE geom IS NULL;

-- 6. Duplicate ID hashes
SELECT
    id_number_hash,
    COUNT(*) AS duplicate_count
FROM seip_core.dim_person
WHERE id_number_hash IS NOT NULL
GROUP BY id_number_hash
HAVING COUNT(*) > 1;

-- 7. Township-level unemployment sanity check
SELECT *
FROM seip_core.vw_unemployment_by_township
ORDER BY unemployment_rate DESC;
```

---

# `14_seed_validation.sql`

```sql
SELECT 'ref_township' AS table_name, COUNT(*) AS record_count
FROM seip_core.ref_township

UNION ALL

SELECT 'ref_skill_category', COUNT(*)
FROM seip_core.ref_skill_category

UNION ALL

SELECT 'ref_industry_sector', COUNT(*)
FROM seip_core.ref_industry_sector

UNION ALL

SELECT 'dim_location', COUNT(*)
FROM seip_core.dim_location

UNION ALL

SELECT 'dim_person', COUNT(*)
FROM seip_core.dim_person

UNION ALL

SELECT 'dim_skill', COUNT(*)
FROM seip_core.dim_skill

UNION ALL

SELECT 'fact_employment_status', COUNT(*)
FROM seip_core.fact_employment_status

UNION ALL

SELECT 'fact_job_seeker_survey', COUNT(*)
FROM seip_core.fact_job_seeker_survey;
```

---

# `15_rollback_dev.sql`

Use this only in development when you want to reset everything.

```sql
DROP SCHEMA IF EXISTS seip_audit CASCADE;
DROP SCHEMA IF EXISTS seip_staging CASCADE;
DROP SCHEMA IF EXISTS seip_core CASCADE;

DROP EXTENSION IF EXISTS pg_trgm;
DROP EXTENSION IF EXISTS postgis;
DROP EXTENSION IF EXISTS "uuid-ossp";
```

---

# `run_all_sql.ps1`

Create this PowerShell script in the project root:

```powershell
$container = "seip_postgres"
$db = "seip_db"
$user = "seip_admin"

$sqlFiles = @(
    "sql/00_extensions.sql",
    "sql/01_schemas.sql",
    "sql/02_reference_tables.sql",
    "sql/03_dimensions.sql",
    "sql/04_bridge_tables.sql",
    "sql/05_staging_tables.sql",
    "sql/06_fact_tables.sql",
    "sql/07_audit_tables.sql",
    "sql/08_indexes.sql",
    "sql/09_views.sql",
    "sql/10_rbac.sql",
    "sql/11_sample_data_tests.sql",
    "sql/12_constraints.sql",
    "sql/13_quality_checks.sql",
    "sql/14_seed_validation.sql"
)

foreach ($file in $sqlFiles) {
    Write-Host "Running $file ..."
    Get-Content $file | docker exec -i $container psql -U $user -d $db

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed on $file"
        exit 1
    }
}

Write-Host "All SEIP SQL scripts completed successfully."
```

Run:

```powershell
.\run_all_sql.ps1
```

---

# Important Fix Before Running Again

Because Phase 1B inserted sample rows, rerunning some inserts may create duplicates.

For development, either reset first:

```bash
docker exec -i seip_postgres psql -U seip_admin -d seip_db < sql/15_rollback_dev.sql
```

Then rerun:

```powershell
.\run_all_sql.ps1
```

Or change sample inserts later to use `ON CONFLICT DO NOTHING`.

---

# Recommended Improvement to Reference Inserts

Update your reference inserts like this:

```sql
INSERT INTO seip_core.ref_township 
(township_code, township_name, municipality, province)
VALUES
('SOWETO', 'Soweto', 'City of Johannesburg', 'Gauteng'),
('DIEPSLOOT', 'Diepsloot', 'City of Johannesburg', 'Gauteng'),
('ALEXANDRA', 'Alexandra', 'City of Johannesburg', 'Gauteng')
ON CONFLICT (township_code) DO NOTHING;
```

Do this for all reference tables so your scripts are repeatable.

---

# Verification

Run:

```sql
SELECT *
FROM seip_core.vw_unemployment_by_township;
```

Run:

```sql
SELECT *
FROM seip_core.vw_skills_gap;
```

Run:

```sql
SELECT *
FROM seip_audit.aud_person_changes
ORDER BY changed_at DESC;
```

Commit:

```bash
git add .
git commit -m "Add Phase 1C database hardening and validation scripts"
```

Phase 1C is complete when:

```text
✅ Check constraints added
✅ Data quality queries created
✅ Seed validation works
✅ Rollback script available
✅ SQL execution automated
✅ Database can be reset and rebuilt
```

Next: **Phase 2A — Data collection templates and data dictionary.**
