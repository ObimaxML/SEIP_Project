# Phase 1B — Sample Data, Test Inserts & Foreign Key Validation

Goal: prove the database works before we build Python ETL. This phase adds test data across the SEIP star schema and validates relationships, audit triggers, views and PostGIS. The blueprint expects reference data, dimensional tables, fact tables, audit logging and analytics views as part of the PostgreSQL foundation.

## Create this file

```text
sql/11_sample_data_tests.sql
```

## 1. Insert sample locations

```sql
INSERT INTO seip_core.dim_location (
    township_code,
    ward_number,
    suburb,
    municipality,
    province,
    latitude,
    longitude,
    geom
)
VALUES
(
    'SOWETO',
    'WARD_001',
    'Orlando East',
    'City of Johannesburg',
    'Gauteng',
    -26.2311,
    27.9226,
    ST_SetSRID(ST_MakePoint(27.9226, -26.2311), 4326)
),
(
    'ALEXANDRA',
    'WARD_002',
    'Alexandra',
    'City of Johannesburg',
    'Gauteng',
    -26.1039,
    28.0989,
    ST_SetSRID(ST_MakePoint(28.0989, -26.1039), 4326)
),
(
    'DIEPSLOOT',
    'WARD_003',
    'Diepsloot',
    'City of Johannesburg',
    'Gauteng',
    -25.9333,
    28.0167,
    ST_SetSRID(ST_MakePoint(28.0167, -25.9333), 4326)
);
```

## 2. Insert sample people

```sql
INSERT INTO seip_core.dim_person (
    first_name_encrypted,
    last_name_encrypted,
    id_number_hash,
    gender_code,
    date_of_birth,
    nationality,
    south_african_citizen,
    highest_qualification,
    education_level_code,
    field_of_study,
    nqf_level,
    employment_status_code,
    location_key,
    mobile_number_hash,
    email_hash,
    whatsapp_number_hash,
    consent_given,
    consent_date,
    consent_version
)
SELECT
    convert_to('encrypted_thabo', 'UTF8'),
    convert_to('encrypted_mokoena', 'UTF8'),
    'hash_9001015009087',
    'Male',
    DATE '1998-01-15',
    'South African',
    TRUE,
    'Matric',
    'GRADE_12',
    'General',
    4,
    'UNEMPLOYED',
    l.location_key,
    'hash_mobile_001',
    'hash_email_001',
    'hash_whatsapp_001',
    TRUE,
    CURRENT_TIMESTAMP,
    'v1.0'
FROM seip_core.dim_location l
WHERE l.township_code = 'SOWETO'
LIMIT 1;

INSERT INTO seip_core.dim_person (
    first_name_encrypted,
    last_name_encrypted,
    id_number_hash,
    gender_code,
    date_of_birth,
    nationality,
    south_african_citizen,
    highest_qualification,
    education_level_code,
    field_of_study,
    nqf_level,
    employment_status_code,
    location_key,
    mobile_number_hash,
    email_hash,
    whatsapp_number_hash,
    consent_given,
    consent_date,
    consent_version
)
SELECT
    convert_to('encrypted_ayanda', 'UTF8'),
    convert_to('encrypted_dlamini', 'UTF8'),
    'hash_9502026009088',
    'Female',
    DATE '2001-06-20',
    'South African',
    TRUE,
    'Diploma',
    'DIPLOMA',
    'Information Technology',
    6,
    'EMPLOYED',
    l.location_key,
    'hash_mobile_002',
    'hash_email_002',
    'hash_whatsapp_002',
    TRUE,
    CURRENT_TIMESTAMP,
    'v1.0'
FROM seip_core.dim_location l
WHERE l.township_code = 'ALEXANDRA'
LIMIT 1;
```

## 3. Insert sample skills

```sql
INSERT INTO seip_core.dim_skill (
    skill_name,
    skill_category_code,
    skill_type,
    nqf_level,
    demand_level
)
VALUES
('Microsoft Excel', 'DIGITAL', 'Technical', 4, 'High'),
('SQL', 'DIGITAL', 'Technical', 5, 'High'),
('Python', 'DIGITAL', 'Technical', 6, 'High'),
('Customer Service', 'SOFT', 'Soft Skill', 3, 'Medium'),
('Plumbing', 'TRADE', 'Trade', 4, 'Medium');
```

## 4. Link people to skills

```sql
INSERT INTO seip_core.bridge_person_skill (
    person_key,
    skill_key,
    proficiency_level,
    years_experience,
    verified
)
SELECT
    p.person_key,
    s.skill_key,
    'Intermediate',
    2.0,
    FALSE
FROM seip_core.dim_person p
JOIN seip_core.dim_skill s
    ON s.skill_name = 'Microsoft Excel'
WHERE p.id_number_hash = 'hash_9001015009087';

INSERT INTO seip_core.bridge_person_skill (
    person_key,
    skill_key,
    proficiency_level,
    years_experience,
    verified
)
SELECT
    p.person_key,
    s.skill_key,
    'Beginner',
    1.0,
    FALSE
FROM seip_core.dim_person p
JOIN seip_core.dim_skill s
    ON s.skill_name = 'SQL'
WHERE p.id_number_hash = 'hash_9502026009088';
```

## 5. Insert company and job demand

```sql
INSERT INTO seip_core.dim_company (
    company_name,
    sector_code,
    company_size,
    township_code,
    contact_email_hash,
    contact_number_hash
)
VALUES
(
    'Soweto Retail Market',
    'RETAIL',
    'Small',
    'SOWETO',
    'hash_company_email_001',
    'hash_company_number_001'
);

INSERT INTO seip_core.dim_job (
    job_title,
    sector_code,
    job_level,
    minimum_qualification,
    salary_band
)
VALUES
(
    'Junior Data Capturer',
    'ICT',
    'Entry Level',
    'Matric',
    'R4,000 - R7,000'
);
```

## 6. Link job to required skills

```sql
INSERT INTO seip_core.bridge_job_skill (
    job_key,
    skill_key,
    required_level,
    mandatory
)
SELECT
    j.job_key,
    s.skill_key,
    'Intermediate',
    TRUE
FROM seip_core.dim_job j
JOIN seip_core.dim_skill s
    ON s.skill_name = 'Microsoft Excel'
WHERE j.job_title = 'Junior Data Capturer';

INSERT INTO seip_core.bridge_job_skill (
    job_key,
    skill_key,
    required_level,
    mandatory
)
SELECT
    j.job_key,
    s.skill_key,
    'Beginner',
    TRUE
FROM seip_core.dim_job j
JOIN seip_core.dim_skill s
    ON s.skill_name = 'SQL'
WHERE j.job_title = 'Junior Data Capturer';
```

## 7. Insert fact records

```sql
INSERT INTO seip_core.fact_employment_status (
    person_key,
    location_key,
    survey_date,
    currently_employed,
    months_unemployed,
    seeking_work,
    preferred_sector,
    income_band
)
SELECT
    p.person_key,
    p.location_key,
    CURRENT_DATE,
    FALSE,
    18,
    TRUE,
    'ICT',
    'No income'
FROM seip_core.dim_person p
WHERE p.id_number_hash = 'hash_9001015009087';

INSERT INTO seip_core.fact_employment_status (
    person_key,
    location_key,
    survey_date,
    currently_employed,
    months_unemployed,
    seeking_work,
    preferred_sector,
    income_band
)
SELECT
    p.person_key,
    p.location_key,
    CURRENT_DATE,
    TRUE,
    0,
    FALSE,
    'ICT',
    'R4,000 - R7,000'
FROM seip_core.dim_person p
WHERE p.id_number_hash = 'hash_9502026009088';

INSERT INTO seip_core.fact_job_seeker_survey (
    person_key,
    location_key,
    survey_date,
    digital_literacy_level,
    has_smartphone,
    transport_mode,
    willing_to_relocate,
    training_interest,
    completeness_score,
    quality_score
)
SELECT
    p.person_key,
    p.location_key,
    CURRENT_DATE,
    'Intermediate',
    TRUE,
    'Taxi',
    TRUE,
    TRUE,
    92.50,
    88.00
FROM seip_core.dim_person p
WHERE p.id_number_hash = 'hash_9001015009087';

INSERT INTO seip_core.fact_business_vacancy (
    company_key,
    job_key,
    location_key,
    vacancy_count,
    salary_band,
    experience_required_years,
    vacancy_status,
    survey_date
)
SELECT
    c.company_key,
    j.job_key,
    l.location_key,
    3,
    'R4,000 - R7,000',
    1.0,
    'OPEN',
    CURRENT_DATE
FROM seip_core.dim_company c
JOIN seip_core.dim_job j
    ON j.job_title = 'Junior Data Capturer'
JOIN seip_core.dim_location l
    ON l.township_code = c.township_code
WHERE c.company_name = 'Soweto Retail Market'
LIMIT 1;
```

## 8. Insert staging test record

```sql
INSERT INTO seip_staging.stg_job_seeker (
    source_file_name,
    raw_payload,
    validation_status,
    validation_errors
)
VALUES (
    'sample_job_seekers.csv',
    '{
        "first_name": "Test",
        "last_name": "Respondent",
        "township": "Soweto",
        "currently_employed": false,
        "consent_given": true
    }'::jsonb,
    'VALID',
    NULL
);
```

## 9. Run the script

```bash
docker exec -i seip_postgres psql -U seip_admin -d seip_db < sql/11_sample_data_tests.sql
```

## 10. Validate tables

```sql
SELECT COUNT(*) AS total_locations
FROM seip_core.dim_location;

SELECT COUNT(*) AS total_people
FROM seip_core.dim_person;

SELECT COUNT(*) AS total_skills
FROM seip_core.dim_skill;

SELECT COUNT(*) AS total_employment_facts
FROM seip_core.fact_employment_status;
```

## 11. Validate views

```sql
SELECT *
FROM seip_core.vw_person_safe;

SELECT *
FROM seip_core.vw_unemployment_by_township;

SELECT *
FROM seip_core.vw_skills_gap;
```

## 12. Validate PostGIS

```sql
SELECT
    township_code,
    suburb,
    ST_AsText(geom) AS point_geometry
FROM seip_core.dim_location;
```

Expected example:

```text
POINT(27.9226 -26.2311)
```

## 13. Validate audit trigger

Run:

```sql
UPDATE seip_core.dim_person
SET employment_status_code = 'SEEKING_WORK',
    updated_at = CURRENT_TIMESTAMP
WHERE id_number_hash = 'hash_9001015009087';
```

Then check:

```sql
SELECT
    action_type,
    changed_by,
    changed_at
FROM seip_audit.aud_person_changes
ORDER BY changed_at DESC;
```

Expected:

```text
INSERT
INSERT
UPDATE
```

## 14. Validate foreign keys

This should fail because township does not exist:

```sql
INSERT INTO seip_core.dim_location (
    township_code,
    ward_number,
    suburb
)
VALUES (
    'UNKNOWN_TOWNSHIP',
    'WARD_999',
    'Test Area'
);
```

Expected error:

```text
violates foreign key constraint
```

That is good. It proves your reference table relationship is working.

## 15. Commit Phase 1B

```bash
git add .
git commit -m "Add Phase 1B sample data and database validation tests"
```

Phase 1B is complete when:

```text
✅ Sample townships/locations inserted
✅ Sample people inserted
✅ Skills inserted
✅ Person-skill bridge working
✅ Company/job demand inserted
✅ Fact tables populated
✅ Views return results
✅ PostGIS geometry works
✅ Audit trigger logs changes
✅ Foreign keys reject bad data
```

Next: **Phase 1C — Database hardening: constraints, quality checks, seed scripts, rollback scripts and cleaner execution commands.**
