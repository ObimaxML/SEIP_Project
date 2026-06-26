# Phase 1A — PostgreSQL DDL Execution Order

This phase builds the **SEIP PostgreSQL foundation**: extensions, schemas, reference tables, dimensions, staging, facts, audit tables, indexes, views and roles. This aligns with the blueprint's PostgreSQL layer: **28 tables, star schema, PostGIS, RBAC, audit triggers and analytics views**.

## 1. Create These SQL Files

Inside VS Code:

```text
sql/
├── 00_extensions.sql
├── 01_schemas.sql
├── 02_reference_tables.sql
├── 03_dimensions.sql
├── 04_bridge_tables.sql
├── 05_staging_tables.sql
├── 06_fact_tables.sql
├── 07_audit_tables.sql
├── 08_indexes.sql
├── 09_views.sql
└── 10_rbac.sql
```

---

# `00_extensions.sql`

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

---

# `01_schemas.sql`

```sql
CREATE SCHEMA IF NOT EXISTS seip_core;
CREATE SCHEMA IF NOT EXISTS seip_staging;
CREATE SCHEMA IF NOT EXISTS seip_audit;
```

---

# `02_reference_tables.sql`

```sql
CREATE TABLE seip_core.ref_township (
    township_code VARCHAR(30) PRIMARY KEY,
    township_name VARCHAR(100) NOT NULL,
    municipality VARCHAR(100),
    province VARCHAR(100) DEFAULT 'Gauteng'
);

INSERT INTO seip_core.ref_township VALUES
('SOWETO', 'Soweto', 'City of Johannesburg', 'Gauteng'),
('DIEPSLOOT', 'Diepsloot', 'City of Johannesburg', 'Gauteng'),
('ALEXANDRA', 'Alexandra', 'City of Johannesburg', 'Gauteng'),
('ORANGE_FARM', 'Orange Farm', 'City of Johannesburg', 'Gauteng'),
('TEMBISA', 'Tembisa', 'Ekurhuleni', 'Gauteng'),
('KATLEHONG', 'Katlehong', 'Ekurhuleni', 'Gauteng'),
('VOSLOORUS', 'Vosloorus', 'Ekurhuleni', 'Gauteng'),
('KAGISO', 'Kagiso', 'Mogale City', 'Gauteng'),
('PROTEA_GLEN', 'Protea Glen', 'City of Johannesburg', 'Gauteng');

CREATE TABLE seip_core.ref_skill_category (
    skill_category_code VARCHAR(30) PRIMARY KEY,
    skill_category_name VARCHAR(100) NOT NULL
);

INSERT INTO seip_core.ref_skill_category VALUES
('DIGITAL', 'Digital Skills'),
('TECHNICAL', 'Technical Skills'),
('SOFT', 'Soft Skills'),
('BUSINESS', 'Business Skills'),
('TRADE', 'Trade Skills');

CREATE TABLE seip_core.ref_industry_sector (
    sector_code VARCHAR(30) PRIMARY KEY,
    sector_name VARCHAR(150) NOT NULL
);

INSERT INTO seip_core.ref_industry_sector VALUES
('RETAIL', 'Retail'),
('ICT', 'Information and Communication Technology'),
('CONSTRUCTION', 'Construction'),
('MANUFACTURING', 'Manufacturing'),
('HOSPITALITY', 'Hospitality'),
('TRANSPORT', 'Transport and Logistics'),
('FINANCE', 'Financial Services'),
('EDUCATION', 'Education and Training'),
('HEALTH', 'Healthcare'),
('INFORMAL', 'Informal Economy');
```

---

# `03_dimensions.sql`

```sql
CREATE TABLE seip_core.dim_location (
    location_key BIGSERIAL PRIMARY KEY,
    location_id UUID DEFAULT uuid_generate_v4() UNIQUE,

    township_code VARCHAR(30)
        REFERENCES seip_core.ref_township(township_code),

    ward_number VARCHAR(30),
    suburb VARCHAR(100),
    municipality VARCHAR(100),
    province VARCHAR(100) DEFAULT 'Gauteng',

    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    geom GEOMETRY(Point, 4326),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_core.dim_person (
    person_key BIGSERIAL PRIMARY KEY,
    person_id UUID DEFAULT uuid_generate_v4() UNIQUE,

    first_name_encrypted BYTEA,
    last_name_encrypted BYTEA,
    id_number_hash VARCHAR(256) UNIQUE,

    gender_code VARCHAR(30),
    date_of_birth DATE,

    age INT GENERATED ALWAYS AS (
        DATE_PART('year', AGE(date_of_birth))
    ) STORED,

    nationality VARCHAR(100),
    south_african_citizen BOOLEAN,

    highest_qualification VARCHAR(150),
    education_level_code VARCHAR(50),
    field_of_study VARCHAR(150),
    nqf_level INT,

    employment_status_code VARCHAR(50),
    location_key BIGINT REFERENCES seip_core.dim_location(location_key),

    mobile_number_hash VARCHAR(256),
    email_hash VARCHAR(256),
    whatsapp_number_hash VARCHAR(256),

    consent_given BOOLEAN NOT NULL DEFAULT FALSE,
    consent_date TIMESTAMP,
    consent_version VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_core.dim_skill (
    skill_key BIGSERIAL PRIMARY KEY,
    skill_id UUID DEFAULT uuid_generate_v4() UNIQUE,

    skill_name VARCHAR(150) NOT NULL,
    skill_category_code VARCHAR(30)
        REFERENCES seip_core.ref_skill_category(skill_category_code),

    skill_type VARCHAR(50),
    nqf_level INT,
    demand_level VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_core.dim_company (
    company_key BIGSERIAL PRIMARY KEY,
    company_id UUID DEFAULT uuid_generate_v4() UNIQUE,

    company_name VARCHAR(200) NOT NULL,
    sector_code VARCHAR(30)
        REFERENCES seip_core.ref_industry_sector(sector_code),

    company_size VARCHAR(50),
    township_code VARCHAR(30)
        REFERENCES seip_core.ref_township(township_code),

    contact_email_hash VARCHAR(256),
    contact_number_hash VARCHAR(256),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_core.dim_training_provider (
    provider_key BIGSERIAL PRIMARY KEY,
    provider_id UUID DEFAULT uuid_generate_v4() UNIQUE,

    provider_name VARCHAR(200) NOT NULL,
    provider_type VARCHAR(100),
    accredited BOOLEAN DEFAULT FALSE,
    accreditation_body VARCHAR(100),

    township_code VARCHAR(30)
        REFERENCES seip_core.ref_township(township_code),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_core.dim_job (
    job_key BIGSERIAL PRIMARY KEY,
    job_id UUID DEFAULT uuid_generate_v4() UNIQUE,

    job_title VARCHAR(200) NOT NULL,
    sector_code VARCHAR(30)
        REFERENCES seip_core.ref_industry_sector(sector_code),

    job_level VARCHAR(100),
    minimum_qualification VARCHAR(150),
    salary_band VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_core.dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    week_of_year INT,
    day_of_month INT,
    day_name VARCHAR(20)
);
```

---

# `04_bridge_tables.sql`

```sql
CREATE TABLE seip_core.bridge_person_skill (
    person_skill_key BIGSERIAL PRIMARY KEY,
    person_key BIGINT REFERENCES seip_core.dim_person(person_key),
    skill_key BIGINT REFERENCES seip_core.dim_skill(skill_key),
    proficiency_level VARCHAR(50),
    years_experience DECIMAL(4,1),
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_core.bridge_job_skill (
    job_skill_key BIGSERIAL PRIMARY KEY,
    job_key BIGINT REFERENCES seip_core.dim_job(job_key),
    skill_key BIGINT REFERENCES seip_core.dim_skill(skill_key),
    required_level VARCHAR(50),
    mandatory BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_core.bridge_provider_programme (
    provider_programme_key BIGSERIAL PRIMARY KEY,
    provider_key BIGINT REFERENCES seip_core.dim_training_provider(provider_key),
    programme_name VARCHAR(200),
    nqf_level INT,
    duration_weeks INT,
    placement_support BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

# `05_staging_tables.sql`

```sql
CREATE TABLE seip_staging.stg_job_seeker (
    staging_id BIGSERIAL PRIMARY KEY,
    source_file_name VARCHAR(255),
    raw_payload JSONB NOT NULL,
    validation_status VARCHAR(30) DEFAULT 'PENDING',
    validation_errors JSONB,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_staging.stg_business (
    staging_id BIGSERIAL PRIMARY KEY,
    source_file_name VARCHAR(255),
    raw_payload JSONB NOT NULL,
    validation_status VARCHAR(30) DEFAULT 'PENDING',
    validation_errors JSONB,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_staging.stg_training_provider (
    staging_id BIGSERIAL PRIMARY KEY,
    source_file_name VARCHAR(255),
    raw_payload JSONB NOT NULL,
    validation_status VARCHAR(30) DEFAULT 'PENDING',
    validation_errors JSONB,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_staging.stg_informal_biz (
    staging_id BIGSERIAL PRIMARY KEY,
    source_file_name VARCHAR(255),
    raw_payload JSONB NOT NULL,
    validation_status VARCHAR(30) DEFAULT 'PENDING',
    validation_errors JSONB,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

# `06_fact_tables.sql`

```sql
CREATE TABLE seip_core.fact_employment_status (
    employment_status_key BIGSERIAL PRIMARY KEY,

    person_key BIGINT REFERENCES seip_core.dim_person(person_key),
    location_key BIGINT REFERENCES seip_core.dim_location(location_key),

    survey_date DATE NOT NULL,
    currently_employed BOOLEAN,
    months_unemployed INT,
    seeking_work BOOLEAN,
    preferred_sector VARCHAR(100),
    income_band VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_core.fact_job_seeker_survey (
    survey_key BIGSERIAL PRIMARY KEY,

    person_key BIGINT REFERENCES seip_core.dim_person(person_key),
    location_key BIGINT REFERENCES seip_core.dim_location(location_key),

    survey_date DATE NOT NULL,
    digital_literacy_level VARCHAR(50),
    has_smartphone BOOLEAN,
    transport_mode VARCHAR(50),
    willing_to_relocate BOOLEAN,
    training_interest BOOLEAN,

    completeness_score DECIMAL(5,2),
    quality_score DECIMAL(5,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_core.fact_business_vacancy (
    vacancy_key BIGSERIAL PRIMARY KEY,

    company_key BIGINT REFERENCES seip_core.dim_company(company_key),
    job_key BIGINT REFERENCES seip_core.dim_job(job_key),
    location_key BIGINT REFERENCES seip_core.dim_location(location_key),

    vacancy_count INT DEFAULT 0,
    salary_band VARCHAR(100),
    experience_required_years DECIMAL(4,1),
    vacancy_status VARCHAR(50),

    survey_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_core.fact_training_outcome (
    training_outcome_key BIGSERIAL PRIMARY KEY,

    provider_key BIGINT REFERENCES seip_core.dim_training_provider(provider_key),
    programme_name VARCHAR(200),

    enrolled_count INT DEFAULT 0,
    completed_count INT DEFAULT 0,
    placed_count INT DEFAULT 0,

    completion_rate DECIMAL(5,2),
    placement_rate DECIMAL(5,2),

    reporting_period DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seip_core.fact_informal_business (
    informal_business_key BIGSERIAL PRIMARY KEY,

    location_key BIGINT REFERENCES seip_core.dim_location(location_key),

    business_type VARCHAR(150),
    owner_person_key BIGINT REFERENCES seip_core.dim_person(person_key),

    employee_count INT DEFAULT 0,
    monthly_revenue_band VARCHAR(100),
    access_to_finance BOOLEAN,
    growth_intent BOOLEAN,

    survey_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

# `07_audit_tables.sql`

```sql
CREATE TABLE seip_audit.aud_etl_run_log (
    etl_run_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,

    pipeline_name VARCHAR(100),
    source_file_name VARCHAR(255),

    status VARCHAR(30),
    records_received INT DEFAULT 0,
    records_loaded INT DEFAULT 0,
    records_rejected INT DEFAULT 0,

    error_message TEXT,

    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE TABLE seip_audit.aud_data_access_log (
    access_log_id BIGSERIAL PRIMARY KEY,

    username VARCHAR(100),
    accessed_object VARCHAR(150),
    access_type VARCHAR(50),
    access_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    client_ip VARCHAR(100)
);

CREATE TABLE seip_audit.aud_person_changes (
    change_id BIGSERIAL PRIMARY KEY,

    person_key BIGINT,
    action_type VARCHAR(20),
    changed_by VARCHAR(100) DEFAULT CURRENT_USER,
    old_record JSONB,
    new_record JSONB,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION seip_audit.fn_audit_person_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO seip_audit.aud_person_changes
        (person_key, action_type, new_record)
        VALUES (NEW.person_key, TG_OP, row_to_json(NEW)::jsonb);
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO seip_audit.aud_person_changes
        (person_key, action_type, old_record, new_record)
        VALUES (NEW.person_key, TG_OP, row_to_json(OLD)::jsonb, row_to_json(NEW)::jsonb);
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO seip_audit.aud_person_changes
        (person_key, action_type, old_record)
        VALUES (OLD.person_key, TG_OP, row_to_json(OLD)::jsonb);
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_audit_person_changes
AFTER INSERT OR UPDATE OR DELETE
ON seip_core.dim_person
FOR EACH ROW
EXECUTE FUNCTION seip_audit.fn_audit_person_changes();
```

---

# `08_indexes.sql`

```sql
CREATE INDEX idx_dim_location_township
ON seip_core.dim_location(township_code);

CREATE INDEX idx_dim_location_geom
ON seip_core.dim_location
USING GIST (geom);

CREATE INDEX idx_dim_person_location
ON seip_core.dim_person(location_key);

CREATE INDEX idx_dim_person_id_hash
ON seip_core.dim_person(id_number_hash);

CREATE INDEX idx_dim_skill_category
ON seip_core.dim_skill(skill_category_code);

CREATE INDEX idx_dim_company_name_trgm
ON seip_core.dim_company
USING GIN (company_name gin_trgm_ops);

CREATE INDEX idx_fact_employment_person
ON seip_core.fact_employment_status(person_key);

CREATE INDEX idx_fact_employment_location
ON seip_core.fact_employment_status(location_key);

CREATE INDEX idx_fact_employment_survey_date
ON seip_core.fact_employment_status(survey_date);

CREATE INDEX idx_fact_survey_person
ON seip_core.fact_job_seeker_survey(person_key);

CREATE INDEX idx_fact_vacancy_company
ON seip_core.fact_business_vacancy(company_key);

CREATE INDEX idx_fact_training_provider
ON seip_core.fact_training_outcome(provider_key);
```

---

# `09_views.sql`

```sql
CREATE OR REPLACE VIEW seip_core.vw_person_safe AS
SELECT
    p.person_key,
    p.person_id,
    p.gender_code,
    p.age,
    p.nationality,
    p.south_african_citizen,
    p.highest_qualification,
    p.education_level_code,
    p.field_of_study,
    p.nqf_level,
    p.employment_status_code,
    l.township_code,
    t.township_name,
    l.ward_number,
    p.created_at
FROM seip_core.dim_person p
LEFT JOIN seip_core.dim_location l
    ON p.location_key = l.location_key
LEFT JOIN seip_core.ref_township t
    ON l.township_code = t.township_code;

CREATE OR REPLACE VIEW seip_core.vw_unemployment_by_township AS
SELECT
    t.township_name,
    COUNT(*) AS total_people,
    COUNT(*) FILTER (WHERE f.currently_employed = FALSE) AS unemployed_count,
    ROUND(
        COUNT(*) FILTER (WHERE f.currently_employed = FALSE)::NUMERIC
        / NULLIF(COUNT(*), 0) * 100,
        2
    ) AS unemployment_rate
FROM seip_core.fact_employment_status f
JOIN seip_core.dim_location l
    ON f.location_key = l.location_key
JOIN seip_core.ref_township t
    ON l.township_code = t.township_code
GROUP BY t.township_name;

CREATE OR REPLACE VIEW seip_core.vw_skills_gap AS
SELECT
    s.skill_name,
    s.skill_category_code,
    COUNT(DISTINCT ps.person_key) AS people_with_skill,
    COUNT(DISTINCT js.job_key) AS jobs_requiring_skill,
    COUNT(DISTINCT js.job_key) - COUNT(DISTINCT ps.person_key) AS estimated_gap
FROM seip_core.dim_skill s
LEFT JOIN seip_core.bridge_person_skill ps
    ON s.skill_key = ps.skill_key
LEFT JOIN seip_core.bridge_job_skill js
    ON s.skill_key = js.skill_key
GROUP BY s.skill_name, s.skill_category_code;
```

---

# `10_rbac.sql`

```sql
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'seip_admin') THEN
        CREATE ROLE seip_admin;
    END IF;

    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'seip_engineer') THEN
        CREATE ROLE seip_engineer;
    END IF;

    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'seip_analyst') THEN
        CREATE ROLE seip_analyst;
    END IF;

    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'seip_viewer') THEN
        CREATE ROLE seip_viewer;
    END IF;
END $$;

GRANT USAGE ON SCHEMA seip_core TO seip_admin, seip_engineer, seip_analyst, seip_viewer;
GRANT USAGE ON SCHEMA seip_staging TO seip_admin, seip_engineer;
GRANT USAGE ON SCHEMA seip_audit TO seip_admin;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA seip_core TO seip_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA seip_staging TO seip_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA seip_audit TO seip_admin;

GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA seip_staging TO seip_engineer;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA seip_core TO seip_engineer;

GRANT SELECT ON seip_core.vw_person_safe TO seip_analyst, seip_viewer;
GRANT SELECT ON seip_core.vw_unemployment_by_township TO seip_analyst, seip_viewer;
GRANT SELECT ON seip_core.vw_skills_gap TO seip_analyst, seip_viewer;
```

---

# Run All Scripts

From VS Code terminal:

```bash
docker exec -i seip_postgres psql -U seip_admin -d seip_db < sql/00_extensions.sql
docker exec -i seip_postgres psql -U seip_admin -d seip_db < sql/01_schemas.sql
docker exec -i seip_postgres psql -U seip_admin -d seip_db < sql/02_reference_tables.sql
docker exec -i seip_postgres psql -U seip_admin -d seip_db < sql/03_dimensions.sql
docker exec -i seip_postgres psql -U seip_admin -d seip_db < sql/04_bridge_tables.sql
docker exec -i seip_postgres psql -U seip_admin -d seip_db < sql/05_staging_tables.sql
docker exec -i seip_postgres psql -U seip_admin -d seip_db < sql/06_fact_tables.sql
docker exec -i seip_postgres psql -U seip_admin -d seip_db < sql/07_audit_tables.sql
docker exec -i seip_postgres psql -U seip_admin -d seip_db < sql/08_indexes.sql
docker exec -i seip_postgres psql -U seip_admin -d seip_db < sql/09_views.sql
docker exec -i seip_postgres psql -U seip_admin -d seip_db < sql/10_rbac.sql
```

---

# Verification Query

Run this in pgAdmin or VS Code:

```sql
SELECT 
    schemaname,
    tablename
FROM pg_tables
WHERE schemaname IN ('seip_core', 'seip_staging', 'seip_audit')
ORDER BY schemaname, tablename;
```

Expected result: you should see your reference, dimension, bridge, staging, fact, and audit tables.

Then check PostGIS:

```sql
SELECT PostGIS_Version();
```

Commit:

```bash
git add .
git commit -m "Add Phase 1A PostgreSQL DDL foundation"
```

Next: **Phase 1B — Add sample data, test inserts, and validate foreign keys.**
