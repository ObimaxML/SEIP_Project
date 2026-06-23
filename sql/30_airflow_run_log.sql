CREATE TABLE IF NOT EXISTS seip_audit.airflow_run_log
(
    run_key BIGSERIAL PRIMARY KEY,
    dag_name VARCHAR(200),
    run_status VARCHAR(50),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    records_loaded INT,
    records_rejected INT
);