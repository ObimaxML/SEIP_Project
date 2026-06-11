from pathlib import Path
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

POSTGRES_DB = os.getenv("POSTGRES_DB", "seip_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "seip_admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "change_me")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

POPIA_SECRET_KEY = os.getenv("POPIA_SECRET_KEY")
POPIA_HMAC_SECRET = os.getenv("POPIA_HMAC_SECRET", "dev-hmac-secret-change-me")

RAW_DATA_DIR = PROJECT_ROOT / os.getenv("RAW_DATA_DIR", "data/raw")
PROCESSED_DATA_DIR = PROJECT_ROOT / os.getenv("PROCESSED_DATA_DIR", "data/processed")
REJECTED_DATA_DIR = PROJECT_ROOT / os.getenv("REJECTED_DATA_DIR", "data/rejected")
LOG_DIR = PROJECT_ROOT / os.getenv("LOG_DIR", "logs")

for path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, REJECTED_DATA_DIR, LOG_DIR]:
    path.mkdir(parents=True, exist_ok=True)

SUPPORTED_EXTENSIONS = [".csv", ".xlsx"]

JOB_SEEKER_REQUIRED_COLUMNS = [
    "respondent_id", "consent_given", "first_name", "last_name",
    "id_number", "date_of_birth", "gender", "township", "survey_date"
]

VALID_TOWNSHIPS = {
    "SOWETO", "DIEPSLOOT", "ALEXANDRA", "ORANGE_FARM",
    "TEMBISA", "KATLEHONG", "VOSLOORUS", "KAGISO", "PROTEA_GLEN"
}
