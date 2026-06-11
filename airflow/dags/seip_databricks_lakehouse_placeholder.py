"""
SEIP Phase 4B placeholder DAG.

In a full Azure Databricks setup, this DAG would use DatabricksSubmitRunOperator.
For Community Edition, run notebooks manually in Databricks.

Production direction:

from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
"""

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

with DAG(
    dag_id="seip_databricks_lakehouse_placeholder",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["seip", "databricks", "lakehouse"],
) as dag:

    start = EmptyOperator(task_id="start")
    bronze = EmptyOperator(task_id="bronze_ingest")
    silver = EmptyOperator(task_id="silver_clean")
    gold = EmptyOperator(task_id="gold_kpis")
    end = EmptyOperator(task_id="end")

    start >> bronze >> silver >> gold >> end
