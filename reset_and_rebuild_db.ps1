Get-Content sql/15_rollback_dev.sql | docker exec -i seip_postgres psql -U seip_admin -d seip_db
powershell -ExecutionPolicy Bypass -File run_all_sql.ps1
