# Databricks notebook source
# SEIP Phase 4B — Notebook 05
# Export Gold tables to CSV for Power BI/Tableau portfolio use

# COMMAND ----------

EXPORT_PATH = "dbfs:/FileStore/seip/exports"

tables = [
    "gold_unemployment_by_township",
    "gold_skills_training_demand",
    "gold_digital_access"
]

for table in tables:
    df = spark.table(f"seip_lakehouse.{table}")
    output_path = f"{EXPORT_PATH}/{table}"
    (
        df.coalesce(1)
        .write
        .mode("overwrite")
        .option("header", "true")
        .csv(output_path)
    )
    print(f"Exported {table} to {output_path}")
