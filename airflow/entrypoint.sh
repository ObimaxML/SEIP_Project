#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -eq 0 ]; then
  echo "No command supplied. Use 'webserver' or 'scheduler'."
  exit 1
fi

if [ -z "${POSTGRES_HOST:-}" ] || [ -z "${POSTGRES_DB:-}" ] || [ -z "${POSTGRES_USER:-}" ]; then
  echo "POSTGRES_HOST, POSTGRES_DB, and POSTGRES_USER must be defined."
  exit 1
fi

export PGPASSWORD="${POSTGRES_PASSWORD:-}"

until pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "${POSTGRES_DB}"; do
  echo "Waiting for PostgreSQL at $POSTGRES_HOST..."
  sleep 5
done

echo "Waiting for SEIP initialization to complete..."
until psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT 1 FROM information_schema.tables WHERE table_schema='seip_audit' AND table_name='aud_etl_run_log'" | grep -q 1; do
  echo "Waiting for seip_audit.aud_etl_run_log to exist..."
  sleep 5
done

echo "SEIP init complete."

if [ "$1" = "api-server" ]; then
  echo "Initializing Airflow metadata database..."
  airflow db migrate
fi

if [ "$1" = "api-server" ]; then
  if [ -n "${AIRFLOW_ADMIN_USERNAME:-}" ] && [ -n "${AIRFLOW_ADMIN_PASSWORD:-}" ]; then
    echo "Writing simple auth manager password file for ${AIRFLOW_ADMIN_USERNAME}..."
    mkdir -p /opt/airflow
    cat > /opt/airflow/simple_auth_manager_passwords.json <<EOF
{"${AIRFLOW_ADMIN_USERNAME}": "${AIRFLOW_ADMIN_PASSWORD}"}
EOF
    chmod 640 /opt/airflow/simple_auth_manager_passwords.json
    chown airflow:root /opt/airflow/simple_auth_manager_passwords.json || true
  else
    echo "AIRFLOW_ADMIN_USERNAME and AIRFLOW_ADMIN_PASSWORD must be set to create the simple auth password file."
  fi
fi

exec airflow "$@"

