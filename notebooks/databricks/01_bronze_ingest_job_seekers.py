# Databricks notebook source
# SEIP Phase 4B — Notebook 01
# Bronze ingestion: raw CSV/XLSX style exports into Delta

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import *

RAW_PATH = "dbfs:/FileStore/seip/raw/job_seekers"
BRONZE_PATH = "dbfs:/FileStore/seip/delta/bronze/job_seekers"

# COMMAND ----------

schema = StructType([
    StructField("respondent_id", StringType(), True),
    StructField("consent_given", StringType(), True),
    StructField("consent_date", StringType(), True),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("id_number", StringType(), True),
    StructField("date_of_birth", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("nationality", StringType(), True),
    StructField("south_african_citizen", StringType(), True),
    StructField("mobile_number", StringType(), True),
    StructField("email", StringType(), True),
    StructField("whatsapp_number", StringType(), True),
    StructField("township", StringType(), True),
    StructField("ward_number", StringType(), True),
    StructField("suburb", StringType(), True),
    StructField("gps_latitude", StringType(), True),
    StructField("gps_longitude", StringType(), True),
    StructField("highest_qualification", StringType(), True),
    StructField("education_level_code", StringType(), True),
    StructField("field_of_study", StringType(), True),
    StructField("nqf_level", StringType(), True),
    StructField("digital_literacy_level", StringType(), True),
    StructField("currently_employed", StringType(), True),
    StructField("employment_status", StringType(), True),
    StructField("months_unemployed", StringType(), True),
    StructField("seeking_work", StringType(), True),
    StructField("previous_job_title", StringType(), True),
    StructField("previous_sector", StringType(), True),
    StructField("preferred_sector", StringType(), True),
    StructField("preferred_job_type", StringType(), True),
    StructField("has_smartphone", StringType(), True),
    StructField("has_internet_access", StringType(), True),
    StructField("transport_mode", StringType(), True),
    StructField("willing_to_relocate", StringType(), True),
    StructField("training_interest", StringType(), True),
    StructField("preferred_training_area", StringType(), True),
    StructField("household_size", StringType(), True),
    StructField("household_income_band", StringType(), True),
    StructField("grant_recipient", StringType(), True),
    StructField("disability_status", StringType(), True),
    StructField("disability_type", StringType(), True),
    StructField("available_start_date", StringType(), True),
    StructField("survey_date", StringType(), True),
    StructField("surveyor_name", StringType(), True),
    StructField("source_channel", StringType(), True),
])

# COMMAND ----------

bronze_df = (
    spark.read
    .option("header", "true")
    .schema(schema)
    .csv(RAW_PATH)
    .withColumn("_ingestion_timestamp", F.current_timestamp())
    .withColumn("_source_file", F.input_file_name())
    .withColumn("_bronze_load_date", F.current_date())
)

display(bronze_df.limit(10))

# COMMAND ----------

(
    bronze_df.write
    .format("delta")
    .mode("append")
    .partitionBy("_bronze_load_date")
    .save(BRONZE_PATH)
)

spark.sql("CREATE DATABASE IF NOT EXISTS seip_lakehouse")

spark.sql(f"""
CREATE TABLE IF NOT EXISTS seip_lakehouse.bronze_job_seekers
USING DELTA
LOCATION '{BRONZE_PATH}'
""")

print("Bronze job seeker ingestion complete.")
