from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import subprocess
import os

def run_job_seeker_etl():
    # Using python3 specifically and providing full path
    script_path = "/opt/seip/run_phase_3b_job_seeker_to_postgres.py"
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"ETL Script not found at {script_path}")
        
    subprocess.run(
        ["python3", script_path],
        check=True
    )

with DAG(
    dag_id="seip_job_seeker_pipeline",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    schedule="@daily",
    is_paused_upon_creation=False
) as dag:

    load_job_seekers_task = PythonOperator(
        task_id="load_job_seekers",
        python_callable=run_job_seeker_etl
    )