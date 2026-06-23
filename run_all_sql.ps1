$container = "seip_postgres_airflow"
$db = "seip_db"
$user = "postgres"

$sqlFiles = @(
    "sql/00_extensions.sql",
    "sql/01_schemas.sql",
    "sql/02_reference_tables.sql",
    "sql/03_dimensions.sql",
    "sql/04_bridge_tables.sql",
    "sql/05_staging_tables.sql",
    "sql/06_fact_tables.sql",
    "sql/07_audit_tables.sql",
    "sql/08_indexes.sql",
    "sql/09_views.sql",
    "sql/10_rbac.sql",
    "sql/11_sample_data_tests.sql",
    "sql/12_constraints.sql"
)

foreach ($file in $sqlFiles) {
    Write-Host "Running $file ..."
    Get-Content $file | docker exec -i $container psql -U $user -d $db
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed on $file"
        exit 1
    }
}
Write-Host "All SEIP SQL scripts completed successfully."
