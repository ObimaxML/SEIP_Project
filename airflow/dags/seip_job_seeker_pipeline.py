from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

import subprocess


def run_job_seeker_etl():

    subprocess.run(
        [
            "python",
            "run_phase_3b_job_seeker_to_postgres.py"
        ],
        check=True
    )


with DAG(
    dag_id="seip_job_seeker_pipeline",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    schedule="@daily"
) as dag:

    load_job_seekers = PythonOperator(
        task_id="load_job_seekers",
        python_callable=run_job_seeker_etl
    )

    load_job_seekers