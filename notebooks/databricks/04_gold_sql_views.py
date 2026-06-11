# Databricks notebook source
# SEIP Phase 4B — Notebook 04
# SQL views for BI consumption

# COMMAND ----------

spark.sql("USE seip_lakehouse")

# COMMAND ----------

spark.sql("""
CREATE OR REPLACE VIEW vw_executive_unemployment_summary AS
SELECT
    township,
    total_job_seekers,
    employed_count,
    unemployed_count,
    unemployment_rate_pct,
    avg_months_unemployed,
    youth_count
FROM gold_unemployment_by_township
ORDER BY unemployment_rate_pct DESC
""")

# COMMAND ----------

spark.sql("""
CREATE OR REPLACE VIEW vw_training_demand_summary AS
SELECT
    township,
    preferred_training_area,
    demand_count,
    interested_count,
    training_interest_rate_pct
FROM gold_skills_training_demand
ORDER BY demand_count DESC
""")

# COMMAND ----------

spark.sql("""
CREATE OR REPLACE VIEW vw_digital_access_summary AS
SELECT
    township,
    total_job_seekers,
    smartphone_users,
    internet_users,
    smartphone_access_pct,
    internet_access_pct
FROM gold_digital_access
ORDER BY internet_access_pct ASC
""")

# COMMAND ----------

display(spark.sql("SELECT * FROM vw_executive_unemployment_summary"))
display(spark.sql("SELECT * FROM vw_training_demand_summary"))
display(spark.sql("SELECT * FROM vw_digital_access_summary"))

print("BI views created.")
