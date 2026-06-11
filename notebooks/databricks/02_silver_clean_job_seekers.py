# Databricks notebook source
# SEIP Phase 4B — Notebook 02
# Silver transformation: clean, type-cast, mask PII, deduplicate

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

BRONZE_PATH = "dbfs:/FileStore/seip/delta/bronze/job_seekers"
SILVER_PATH = "dbfs:/FileStore/seip/delta/silver/job_seekers"

# COMMAND ----------

bronze_df = spark.read.format("delta").load(BRONZE_PATH)

# COMMAND ----------

def to_bool(col_name):
    return (
        F.when(F.lower(F.col(col_name)).isin("true", "yes", "y", "1"), F.lit(True))
         .when(F.lower(F.col(col_name)).isin("false", "no", "n", "0"), F.lit(False))
         .otherwise(F.lit(None).cast("boolean"))
    )

silver_df = (
    bronze_df
    .withColumn("respondent_id", F.trim(F.col("respondent_id")))
    .withColumn("township", F.upper(F.trim(F.col("township"))))
    .withColumn("gender", F.initcap(F.trim(F.col("gender"))))
    .withColumn("consent_given_bool", to_bool("consent_given"))
    .withColumn("south_african_citizen_bool", to_bool("south_african_citizen"))
    .withColumn("currently_employed_bool", to_bool("currently_employed"))
    .withColumn("seeking_work_bool", to_bool("seeking_work"))
    .withColumn("has_smartphone_bool", to_bool("has_smartphone"))
    .withColumn("has_internet_access_bool", to_bool("has_internet_access"))
    .withColumn("willing_to_relocate_bool", to_bool("willing_to_relocate"))
    .withColumn("training_interest_bool", to_bool("training_interest"))
    .withColumn("grant_recipient_bool", to_bool("grant_recipient"))
    .withColumn("disability_status_bool", to_bool("disability_status"))
    .withColumn("date_of_birth_date", F.to_date("date_of_birth"))
    .withColumn("survey_date_date", F.to_date("survey_date"))
    .withColumn("consent_date_date", F.to_date("consent_date"))
    .withColumn("age", F.floor(F.months_between(F.current_date(), F.col("date_of_birth_date")) / 12))
    .withColumn("nqf_level_int", F.col("nqf_level").cast("int"))
    .withColumn("months_unemployed_int", F.col("months_unemployed").cast("int"))
    .withColumn("gps_latitude_decimal", F.col("gps_latitude").cast("double"))
    .withColumn("gps_longitude_decimal", F.col("gps_longitude").cast("double"))
    .withColumn("id_number_hash", F.sha2(F.lower(F.trim(F.col("id_number"))), 256))
    .withColumn("mobile_number_hash", F.sha2(F.lower(F.trim(F.col("mobile_number"))), 256))
    .withColumn("email_hash", F.sha2(F.lower(F.trim(F.col("email"))), 256))
    .withColumn("whatsapp_number_hash", F.sha2(F.lower(F.trim(F.col("whatsapp_number"))), 256))
    .withColumn("first_name_masked", F.concat(F.substring("first_name", 1, 1), F.lit("***")))
    .withColumn("last_name_masked", F.concat(F.substring("last_name", 1, 1), F.lit("***")))
)

# COMMAND ----------

silver_df = (
    silver_df
    .withColumn(
        "validation_status",
        F.when(F.col("consent_given_bool") != True, "REJECTED")
         .when((F.col("age") < 14) | (F.col("age") > 80), "REJECTED")
         .when(~F.col("township").isin("SOWETO", "DIEPSLOOT", "ALEXANDRA", "ORANGE_FARM", "TEMBISA", "KATLEHONG", "VOSLOORUS", "KAGISO", "PROTEA_GLEN"), "REJECTED")
         .when((F.col("nqf_level_int") < 1) | (F.col("nqf_level_int") > 10), "REJECTED")
         .otherwise("VALID")
    )
)

# COMMAND ----------

window_spec = Window.partitionBy("id_number_hash").orderBy(F.col("_ingestion_timestamp").desc())

deduped_df = (
    silver_df
    .withColumn("_row_number", F.row_number().over(window_spec))
    .filter(F.col("_row_number") == 1)
    .drop("_row_number")
)

# COMMAND ----------

safe_cols = [
    "respondent_id",
    "consent_given_bool",
    "consent_date_date",
    "first_name_masked",
    "last_name_masked",
    "id_number_hash",
    "date_of_birth_date",
    "age",
    "gender",
    "nationality",
    "south_african_citizen_bool",
    "mobile_number_hash",
    "email_hash",
    "whatsapp_number_hash",
    "township",
    "ward_number",
    "suburb",
    "gps_latitude_decimal",
    "gps_longitude_decimal",
    "highest_qualification",
    "education_level_code",
    "field_of_study",
    "nqf_level_int",
    "digital_literacy_level",
    "currently_employed_bool",
    "employment_status",
    "months_unemployed_int",
    "seeking_work_bool",
    "previous_job_title",
    "previous_sector",
    "preferred_sector",
    "preferred_job_type",
    "has_smartphone_bool",
    "has_internet_access_bool",
    "transport_mode",
    "willing_to_relocate_bool",
    "training_interest_bool",
    "preferred_training_area",
    "household_size",
    "household_income_band",
    "grant_recipient_bool",
    "disability_status_bool",
    "disability_type",
    "available_start_date",
    "survey_date_date",
    "source_channel",
    "validation_status",
    "_ingestion_timestamp",
    "_source_file"
]

final_silver_df = deduped_df.select(*safe_cols)

display(final_silver_df.limit(10))

# COMMAND ----------

(
    final_silver_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(SILVER_PATH)
)

spark.sql(f"""
CREATE TABLE IF NOT EXISTS seip_lakehouse.silver_job_seekers
USING DELTA
LOCATION '{SILVER_PATH}'
""")

print("Silver job seeker cleaning complete.")
