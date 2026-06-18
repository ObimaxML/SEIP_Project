from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def load_job_seekers():
    print("Loading job seeker data...")
    print("Load task completed successfully.")


def validate_data():
    print("Running SEIP data validation checks...")
    print("Validation task completed successfully.")


with DAG(
    dag_id="seip_job_seeker_pipeline",
    start_date=datetime(2026, 6, 1),
    schedule=None,
    catchup=False,
    tags=["seip", "job_seekers"],
) as dag:

    load_job_seekers_task = PythonOperator(
        task_id="load_job_seekers",
        python_callable=load_job_seekers,
    )

    validate_data_task = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data,
    )

    load_job_seekers_task >> validate_data_task