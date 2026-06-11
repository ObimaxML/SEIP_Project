CREATE TABLE IF NOT EXISTS seip_staging.stg_job_seeker (
    staging_id BIGSERIAL PRIMARY KEY,
    source_file_name VARCHAR(255),
    raw_payload JSONB NOT NULL,
    validation_status VARCHAR(30) DEFAULT 'PENDING',
    validation_errors JSONB,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
