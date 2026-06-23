from datetime import datetime
from sqlalchemy import create_engine, text
from src.config.settings import DATABASE_URL


def log_airflow_success(**context):
    """
    Writes a successful Airflow DAG run record into seip_audit.airflow_run_log.
    """

    dag_name = context["dag"].dag_id

    engine = create_engine(DATABASE_URL)

    insert_sql = text("""
        INSERT INTO seip_audit.airflow_run_log
        (
            dag_name,
            run_status,
            started_at,
            completed_at,
            records_loaded,
            records_rejected
        )
        VALUES
        (
            :dag_name,
            :run_status,
            :started_at,
            :completed_at,
            :records_loaded,
            :records_rejected
        );
    """)

    with engine.begin() as conn:
        conn.execute(
            insert_sql,
            {
                "dag_name": dag_name,
                "run_status": "SUCCESS",
                "started_at": datetime.now(),
                "completed_at": datetime.now(),
                "records_loaded": 0,
                "records_rejected": 0,
            },
        )

    print(f"Airflow run logged successfully for DAG: {dag_name}")