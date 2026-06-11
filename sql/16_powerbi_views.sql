CREATE OR REPLACE VIEW seip_core.vw_powerbi_employment_fact AS
SELECT
    f.employment_status_key,
    f.person_key,
    f.location_key,
    f.survey_date,
    f.currently_employed,
    f.months_unemployed,
    f.seeking_work,
    f.preferred_sector,
    f.income_band
FROM seip_core.fact_employment_status f;

CREATE OR REPLACE VIEW seip_core.vw_powerbi_job_seeker_survey AS
SELECT
    s.survey_key,
    s.person_key,
    s.location_key,
    s.survey_date,
    s.digital_literacy_level,
    s.has_smartphone,
    s.transport_mode,
    s.willing_to_relocate,
    s.training_interest,
    s.completeness_score,
    s.quality_score
FROM seip_core.fact_job_seeker_survey s;

CREATE OR REPLACE VIEW seip_core.vw_powerbi_location AS
SELECT
    location_key,
    township_code,
    ward_number,
    suburb,
    municipality,
    province,
    latitude,
    longitude
FROM seip_core.dim_location;
