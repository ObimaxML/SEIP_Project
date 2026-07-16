# SEIP Development Environment Setup

For **SEIP**, we run the development environment primarily in **VS Code**, with **pgAdmin 4** used as a database administration and query tool.

## Recommended Setup

| Tool                         | Purpose                      |
| ---------------------------- | ---------------------------- |
| VS Code                      | Main development environment |
| PostgreSQL 16                | Database engine              |
| PostGIS                      | GIS capabilities             |
| pgAdmin 4                    | Database administration      |
| Docker Desktop               | Container management         |
| Git + GitHub                 | Version control              |
| Python venv                  | Python environment           |
| Databricks Community Edition | Lakehouse & Spark            |
| Power BI Desktop             | Reporting                    |
| Tableau Public               | Portfolio dashboards         |

---

# Why VS Code?

Because SEIP is not just a database project.

We will be building:

✅ PostgreSQL database

✅ Python ETL pipelines

✅ Airflow DAGs

✅ Docker containers

✅ Databricks notebooks

✅ GitHub repository

✅ Power BI datasets

✅ ML models

Trying to manage all that directly from pgAdmin would be painful.

VS Code becomes the central workspace.

---

# The Actual Development Workflow

## VS Code

Project folder:

```text
C:\Projects\SEIP
```

Open entire project:

```bash
code C:\Projects\SEIP
```

Inside VS Code:

```text
SEIP
│
├── sql
├── src
├── airflow
├── docker
├── notebooks
├── data
└── docs
```

---

## pgAdmin 4

Connect to:

```text
localhost
Port: 5432

Database:
seip_db
```

Use pgAdmin for:

* Visual table browsing
* ERD inspection
* Running ad-hoc SQL
* Viewing indexes
* Checking execution plans
* Monitoring queries

Not for source control.

---

## SQL Development

Create scripts in VS Code:

```text
sql/
├── 00_extensions.sql
├── 01_schema.sql
├── 02_reference_tables.sql
├── 03_dimensions.sql
├── 04_fact_tables.sql
```

Commit to Git:

```bash
git add .
git commit -m "Added dimensional model"
```

Run against PostgreSQL:

```bash
psql -U seip_admin -d seip_db -f 03_dimensions.sql
```

or

Execute from pgAdmin Query Tool.

---

# What I Would Do If This Were My Portfolio Project

## Option A (Recommended)

```text
VS Code
+
Docker
+
PostgreSQL
+
pgAdmin
+
GitHub
+
Databricks
```

This is what a Data Engineer/Data Analyst would actually use in industry.

---

## Option B

```text
PostgreSQL
+
pgAdmin only
```

Possible.

Not recommended.

We lose:

* Git integration
* Python development
* Airflow development
* Docker development
* Project structure
* Reproducibility

---

# Recommendation

Given our goal of becoming a stronger:

* Data Analyst
* Data Engineer
* Data Scientist

and using SEIP as a flagship portfolio project,

We would build the entire solution in:

```text
VS Code
├── PostgreSQL 16
├── PostGIS
├── Python
├── Docker
├── Airflow
├── GitHub
├── Databricks
├── Power BI
└── Tableau
```

and use pgAdmin 4 as a companion tool for database inspection and troubleshooting.

That setup aligns closely with the stack described in the blueprint's architecture, database, and data engineering sections.

Before Phase 1A, we would actually add a **Phase 0.5 — Environment Build & Verification**, where we install and test every component (VS Code, PostgreSQL/PostGIS, Docker, Git, Python, pgAdmin, Databricks connectivity) and verify that all tools can talk to each other before writing a single table. This saves a huge amount of troubleshooting later.
