from datetime import datetime
from src.config.settings import (
    RAW_DATA_DIR, PROCESSED_DATA_DIR, REJECTED_DATA_DIR, LOG_DIR,
    SUPPORTED_EXTENSIONS, JOB_SEEKER_REQUIRED_COLUMNS, VALID_TOWNSHIPS,
    DATABASE_URL, POPIA_SECRET_KEY, POPIA_HMAC_SECRET
)
from src.extractors.excel_extractor import SurveyExtractor
from src.validators.survey_validator import JobSeekerValidator
from src.utils.logger import setup_logger, log_event
from src.utils.popia import POPIAProtector
from src.loaders.postgres_loader import PostgresLoader
from src.utils.data_quality_report import write_quality_report

def main():
    logger = setup_logger(LOG_DIR)
    log_event(logger, "PHASE_3B_START")

    extractor = SurveyExtractor(SUPPORTED_EXTENSIONS)
    df = extractor.read_directory(RAW_DATA_DIR)

    if df.empty:
        print(f"No CSV/XLSX files found in {RAW_DATA_DIR}")
        return

    validator = JobSeekerValidator(JOB_SEEKER_REQUIRED_COLUMNS, VALID_TOWNSHIPS)
    accepted, rejected = validator.validate(df)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    accepted_path = PROCESSED_DATA_DIR / f"job_seekers_accepted_{timestamp}.csv"
    rejected_path = REJECTED_DATA_DIR / f"job_seekers_rejected_{timestamp}.csv"

    accepted.to_csv(accepted_path, index=False)
    rejected.to_csv(rejected_path, index=False)
    quality_report_path = write_quality_report(df, accepted, rejected, PROCESSED_DATA_DIR)

    protector = POPIAProtector(POPIA_SECRET_KEY, POPIA_HMAC_SECRET)
    loader = PostgresLoader(DATABASE_URL, protector)
    result = loader.load_job_seekers(accepted, rejected)

    log_event(logger, "PHASE_3B_COMPLETE", **result)

    print("Phase 3B completed.")
    print(result)
    print(f"Accepted output: {accepted_path}")
    print(f"Rejected output: {rejected_path}")
    print(f"Quality report: {quality_report_path}")

if __name__ == "__main__":
    main()
