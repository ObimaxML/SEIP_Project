# SEIP Implementation Roadmap

The implementation of this project is **phase by phase**, starting with the foundation. 

The blueprint defines the stack as **PostgreSQL, Python, Databricks, Spark, Power BI, Tableau, Airflow, Docker, and GitHub**, with POPIA/security as a cross-cutting requirement.

## SEIP Implementation Roadmap

### Phase 0 — Project Setup

Goal: create the working environment, Git repo, Docker stack, folder structure, and project standards.

Deliverables:

* GitHub repository
* Docker Compose environment
* PostgreSQL + PostGIS database
* Python project structure
* `.env` configuration
* Initial README
* Branching strategy

### Phase 1 — PostgreSQL Database Foundation

Goal: build the SEIP warehouse using schemas, reference tables, dimensions, staging, facts, audit tables, RBAC, and indexes.

Deliverables:

* `seip_core` schema
* `seip_staging` schema
* `seip_audit` schema
* Reference tables
* Core dimensions
* Staging tables
* Fact tables
* Audit logging tables

### Phase 2 — Data Collection Templates

Goal: prepare job seeker, business, training provider, and informal economy survey templates.

Deliverables:

* Excel/CSV templates
* Google Form / KoBoToolbox structure
* Data dictionary
* Field validation rules

### Phase 3 — Python ETL Pipeline

Goal: ingest Excel/CSV, validate, clean, hash/encrypt PII, geocode, and load PostgreSQL.

Deliverables:

* Extractor scripts
* Validator scripts
* POPIA utility scripts
* PostgreSQL loader
* Logging
* Rejected-record handling

### Phase 4 — Docker + Airflow Orchestration

Goal: run the full ETL pipeline automatically.

Deliverables:

* Airflow DAG
* Scheduled pipeline
* Dockerized services
* ETL monitoring logs

### Phase 5 — Databricks Lakehouse

Goal: implement Bronze, Silver, and Gold layers using Spark/Delta.

Deliverables:

* Bronze raw tables
* Silver cleaned tables
* Gold KPI tables
* ML-ready datasets

### Phase 6 — Analytics + BI

Goal: build dashboards in Power BI/Tableau.

Deliverables:

* Unemployment dashboard
* Skills gap dashboard
* Township/ward heatmap
* Training provider performance dashboard
* Informal economy dashboard

### Phase 7 — Machine Learning

Goal: build prediction and clustering models.

Deliverables:

* Employment probability model
* Skills gap prediction
* Risk-zone clustering
* Model evaluation report

---

# Phase 0 — Project Setup

Create this folder structure:

```bash
seip/
├── README.md
├── .env
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── sql/
│   ├── 00_extensions.sql
│   ├── 01_schemas.sql
│   ├── 02_reference_tables.sql
│   ├── 03_dimensions.sql
│   ├── 04_staging.sql
│   ├── 05_facts.sql
│   ├── 06_audit.sql
│   └── 07_views.sql
├── data/
│   ├── raw/
│   ├── processed/
│   ├── rejected/
│   └── templates/
├── src/
│   ├── config/
│   ├── extractors/
│   ├── validators/
│   ├── transformers/
│   ├── loaders/
│   └── utils/
├── notebooks/
│   ├── databricks/
│   └── exploration/
└── airflow/
    └── dags/
```

## Git setup

```bash
git init
git checkout -b develop

git add .
git commit -m "Initial SEIP project structure"

git branch feature/database-foundation
git branch feature/python-etl
git branch feature/databricks-lakehouse
git branch feature/powerbi-dashboards
```

## `.gitignore`

```gitignore
.env
__pycache__/
*.pyc
data/raw/
data/processed/
data/rejected/
*.xlsx
*.csv
.ipynb_checkpoints/
.venv/
```

## `requirements.txt`

```txt
pandas
numpy
sqlalchemy
psycopg2-binary
python-dotenv
openpyxl
cryptography
pydantic
geopy
pytest
```

## `.env`

```env
POSTGRES_DB=seip_db
POSTGRES_USER=seip_admin
POSTGRES_PASSWORD=change_me
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

POPIA_SECRET_KEY=replace_with_secure_key
ETL_BATCH_SIZE=1000
```

## `docker-compose.yml`

```yaml
version: "3.9"

services:
  postgres:
    image: postgis/postgis:16-3.4
    container_name: seip_postgres
    environment:
      POSTGRES_DB: seip_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: Krbgp012
    ports:
      - "5433:5432"
    volumes:
      - seip_pgdata:/var/lib/postgresql/data
      - ./sql:/docker-entrypoint-initdb.d

volumes:
  seip_pgdata:
```

Run it:

```bash
docker compose up -d
```

---

# Phase 1 — PostgreSQL Foundation

## `sql/00_extensions.sql`

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

## `sql/01_schemas.sql`

```sql
CREATE SCHEMA IF NOT EXISTS seip_core;
CREATE SCHEMA IF NOT EXISTS seip_staging;
CREATE SCHEMA IF NOT EXISTS seip_audit;
```

## Reference table example

```sql
CREATE TABLE seip_core.ref_township (
    township_code VARCHAR(30) PRIMARY KEY,
    township_name VARCHAR(100) NOT NULL,
    municipality VARCHAR(100),
    province VARCHAR(100) DEFAULT 'Gauteng'
);

INSERT INTO seip_core.ref_township 
(township_code, township_name, municipality)
VALUES
('SOWETO', 'Soweto', 'City of Johannesburg'),
('DIEPSLOOT', 'Diepsloot', 'City of Johannesburg'),
('ALEXANDRA', 'Alexandra', 'City of Johannesburg'),
('ORANGE_FARM', 'Orange Farm', 'City of Johannesburg'),
('TEMBISA', 'Tembisa', 'Ekurhuleni'),
('KATLEHONG', 'Katlehong', 'Ekurhuleni'),
('VOSLOORUS', 'Vosloorus', 'Ekurhuleni'),
('KAGISO', 'Kagiso', 'Mogale City'),
('PROTEA_GLEN', 'Protea Glen', 'City of Johannesburg');
```

## Location dimension

```sql
CREATE TABLE seip_core.dim_location (
    location_key BIGSERIAL PRIMARY KEY,
    location_id UUID DEFAULT uuid_generate_v4() UNIQUE,

    township_code VARCHAR(30) REFERENCES seip_core.ref_township(township_code),
    ward_number VARCHAR(30),
    suburb VARCHAR(100),

    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    geom GEOMETRY(Point, 4326),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Person dimension

```sql
CREATE TABLE seip_core.dim_person (
    person_key BIGSERIAL PRIMARY KEY,
    person_id UUID DEFAULT uuid_generate_v4() UNIQUE,

    first_name_encrypted BYTEA,
    last_name_encrypted BYTEA,
    id_number_hash VARCHAR(256),

    date_of_birth DATE,
    age INT GENERATED ALWAYS AS (
        DATE_PART('year', AGE(date_of_birth))
    ) STORED,

    gender_code VARCHAR(30),
    highest_qualification VARCHAR(150),
    nqf_level INT,

    employment_status_code VARCHAR(50),
    location_key BIGINT REFERENCES seip_core.dim_location(location_key),

    consent_given BOOLEAN NOT NULL DEFAULT FALSE,
    consent_date TIMESTAMP,
    consent_version VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Staging table

```sql
CREATE TABLE seip_staging.stg_job_seeker (
    staging_id BIGSERIAL PRIMARY KEY,
    source_file_name VARCHAR(255),
    raw_payload JSONB NOT NULL,
    validation_status VARCHAR(30) DEFAULT 'PENDING',
    validation_errors JSONB,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Employment fact table

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
```

## Audit table

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
```

---

**Next: Phase 1A — Complete PostgreSQL DDL.**

