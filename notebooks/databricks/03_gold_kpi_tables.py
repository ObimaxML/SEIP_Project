# Databricks notebook source
# SEIP Phase 4B — Notebook 03
# Gold layer: KPI-ready aggregated tables

# COMMAND ----------

from pyspark.sql import functions as F

SILVER_PATH = "dbfs:/FileStore/seip/delta/silver/job_seekers"
GOLD_PATH = "dbfs:/FileStore/seip/delta/gold"

silver_df = spark.read.format("delta").load(SILVER_PATH)
valid_df = silver_df.filter(F.col("validation_status") == "VALID")

# COMMAND ----------

gold_unemployment_by_township = (
    valid_df
    .groupBy("township")
    .agg(
        F.count("*").alias("total_job_seekers"),
        F.sum(F.when(F.col("currently_employed_bool") == False, 1).otherwise(0)).alias("unemployed_count"),
        F.sum(F.when(F.col("currently_employed_bool") == True, 1).otherwise(0)).alias("employed_count"),
        F.avg("months_unemployed_int").alias("avg_months_unemployed"),
        F.sum(F.when(F.col("age").between(15, 34), 1).otherwise(0)).alias("youth_count")
    )
    .withColumn(
        "unemployment_rate_pct",
        F.round(F.col("unemployed_count") / F.col("total_job_seekers") * 100, 2)
    )
)

display(gold_unemployment_by_township)

# COMMAND ----------

gold_skills_training_demand = (
    valid_df
    .groupBy("township", "preferred_training_area")
    .agg(
        F.count("*").alias("demand_count"),
        F.sum(F.when(F.col("training_interest_bool") == True, 1).otherwise(0)).alias("interested_count")
    )
    .withColumn(
        "training_interest_rate_pct",
        F.round(F.col("interested_count") / F.col("demand_count") * 100, 2)
    )
    .orderBy(F.desc("demand_count"))
)

display(gold_skills_training_demand)

# COMMAND ----------

gold_digital_access = (
    valid_df
    .groupBy("township")
    .agg(
        F.count("*").alias("total_job_seekers"),
        F.sum(F.when(F.col("has_smartphone_bool") == True, 1).otherwise(0)).alias("smartphone_users"),
        F.sum(F.when(F.col("has_internet_access_bool") == True, 1).otherwise(0)).alias("internet_users")
    )
    .withColumn("smartphone_access_pct", F.round(F.col("smartphone_users") / F.col("total_job_seekers") * 100, 2))
    .withColumn("internet_access_pct", F.round(F.col("internet_users") / F.col("total_job_seekers") * 100, 2))
)

display(gold_digital_access)

# COMMAND ----------

(
    gold_unemployment_by_township.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(f"{GOLD_PATH}/unemployment_by_township")
)

(
    gold_skills_training_demand.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(f"{GOLD_PATH}/skills_training_demand")
)

(
    gold_digital_access.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(f"{GOLD_PATH}/digital_access")
)

# COMMAND ----------

spark.sql(f"""
CREATE TABLE IF NOT EXISTS seip_lakehouse.gold_unemployment_by_township
USING DELTA
LOCATION '{GOLD_PATH}/unemployment_by_township'
""")

spark.sql(f"""
CREATE TABLE IF NOT EXISTS seip_lakehouse.gold_skills_training_demand
USING DELTA
LOCATION '{GOLD_PATH}/skills_training_demand'
""")

spark.sql(f"""
CREATE TABLE IF NOT EXISTS seip_lakehouse.gold_digital_access
USING DELTA
LOCATION '{GOLD_PATH}/digital_access'
""")

print("Gold KPI tables created.")
