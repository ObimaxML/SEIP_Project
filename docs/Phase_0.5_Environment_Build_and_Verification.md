# Phase 0.5 — Environment Build & Verification

Goal: make sure your machine is ready before we create the SEIP database.

## 0.5.1 Install Required Tools

Install these first:

| Tool                         | Purpose                                  |
| ---------------------------- | ---------------------------------------- |
| VS Code                      | Main development workspace               |
| Git                          | Version control                          |
| Docker Desktop               | Run PostgreSQL/PostGIS and later Airflow |
| PostgreSQL client tools      | Run `psql` commands                      |
| pgAdmin 4                    | Inspect database visually                |
| Python 3.11+                 | ETL scripts                              |
| Power BI Desktop             | Dashboards                               |
| Databricks Community Edition | Spark/lakehouse work                     |

Your blueprint stack includes PostgreSQL, Python, Databricks, Spark, Power BI, Tableau, Airflow, Docker and GitHub.

---

## 0.5.2 Create Project Folder

Open PowerShell:

```powershell
mkdir C:\Projects\SEIP
cd C:\Projects\SEIP
code .
```

Inside VS Code terminal:

```bash
mkdir sql src data airflow notebooks docs
mkdir data/raw data/processed data/rejected data/templates
mkdir src/config src/extractors src/validators src/transformers src/loaders src/utils
```

---

## 0.5.3 Initialize Git

```bash
git init
git checkout -b develop

echo ".env" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".venv/" >> .gitignore
echo "data/raw/" >> .gitignore
echo "data/processed/" >> .gitignore
echo "data/rejected/" >> .gitignore
echo "*.csv" >> .gitignore
echo "*.xlsx" >> .gitignore

git add .
git commit -m "Initial SEIP project structure"
```

---

## 0.5.4 Create Python Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

Create `requirements.txt`:

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

Install:

```bash
pip install -r requirements.txt
```

Verify:

```bash
python --version
pip list
```

---

## 0.5.5 Create `.env`

Create a file named `.env`:

```env
POSTGRES_DB=seip_db
POSTGRES_USER=seip_admin
POSTGRES_PASSWORD=change_me
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

POPIA_SECRET_KEY=replace_with_secure_key
ETL_BATCH_SIZE=1000
```

---

## 0.5.6 Create Docker Compose for PostgreSQL + PostGIS

Create `docker-compose.yml`:

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
      - "5432:5432"
    volumes:
      - seip_pgdata:/var/lib/postgresql/data
      - ./sql:/docker-entrypoint-initdb.d

volumes:
  seip_pgdata:
```

Start database:

```bash
docker compose up -d
```

Check container:

```bash
docker ps
```

Expected result:

```text
seip_postgres   postgis/postgis:16-3.4   Up
```

---

## 0.5.7 Test PostgreSQL Connection

Run:

```bash
docker exec -it seip_postgres_airflow psql -U postgres -d seip_db
```

Inside PostgreSQL:

```sql
SELECT version();
```

Then:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
SELECT PostGIS_Version();
```

Exit:

```sql
\q
```

If `PostGIS_Version()` returns a version number, your GIS setup is working.

---

## 0.5.8 Connect pgAdmin 4

Open pgAdmin 4.

Create new server:

```text
Name: SEIP Local PostgreSQL
Host: localhost
Port: 5432
Maintenance database: seip_db
Username: seip_admin
Password: change_me
```

Then confirm you can see:

```text
Servers
└── SEIP Local PostgreSQL
    └── Databases
        └── seip_db
```

---

## 0.5.9 Create First Test SQL Script

Create:

```text
sql/00_test_connection.sql
```

Add:

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

SELECT 
    uuid_generate_v4() AS test_uuid,
    PostGIS_Version() AS postgis_version;
```

Run it:

```bash
docker exec -i seip_postgres_airflow psql -U postgres -d seip_db < sql/00_test_connection.sql
```

Expected: you should see a UUID and PostGIS version.

---

## 0.5.10 Commit Phase 0.5

```bash
git add .
git commit -m "Complete Phase 0.5 environment setup"
```

Phase 0.5 is complete when:

```text
✅ VS Code project opened
✅ Git initialized
✅ Python venv working
✅ Docker running
✅ PostgreSQL container running
✅ PostGIS extension working
✅ pgAdmin connected
✅ SQL script executes successfully
```

Next: **Phase 1A — Complete PostgreSQL DDL in execution order.**
