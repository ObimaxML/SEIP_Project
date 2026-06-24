FROM seip_audit.aud_etl_run_log
ORDER BY started_at DESC;

SELECT *
FROM seip_staging.stg_job_seeker
ORDER BY loaded_at DESC;
```