# Databricks notebook source
# SEIP Phase 4B — Notebook 00
# Mount and configuration layer

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import *

# For Databricks Community Edition, DBFS paths are enough.
# For Azure Databricks production, replace these with ADLS Gen2 mount paths.

RAW_PATH = "dbfs:/FileStore/seip/raw/job_seekers"
BRONZE_PATH = "dbfs:/FileStore/seip/delta/bronze/job_seekers"
SILVER_PATH = "dbfs:/FileStore/seip/delta/silver/job_seekers"
GOLD_PATH = "dbfs:/FileStore/seip/delta/gold"

DATABASE_NAME = "seip_lakehouse"

spark.sql(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
spark.sql(f"USE {DATABASE_NAME}")

print("SEIP Databricks configuration loaded.")
print(f"RAW_PATH    = {RAW_PATH}")
print(f"BRONZE_PATH = {BRONZE_PATH}")
print(f"SILVER_PATH = {SILVER_PATH}")
print(f"GOLD_PATH   = {GOLD_PATH}")
