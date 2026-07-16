-- fact_employment_status
CREATE TABLE IF NOT EXISTS seip_core.fact_employment_status (
    employment_status_key   SERIAL PRIMARY KEY,
    person_key              INT,
    location_key            INT REFERENCES seip_core.dim_location(location_key),
    survey_date             DATE,
    currently_employed      BOOLEAN,
    months_unemployed       INT,
    seeking_work            BOOLEAN,
    preferred_sector        VARCHAR(100),
    income_band             VARCHAR(50)
);

-- fact_job_seeker_survey
CREATE TABLE IF NOT EXISTS seip_core.fact_job_seeker_survey (
    survey_key              SERIAL PRIMARY KEY,
    person_key              INT,
    location_key            INT REFERENCES seip_core.dim_location(location_key),
    survey_date             DATE,
    digital_literacy_level  VARCHAR(50),
    has_smartphone          BOOLEAN,
    transport_mode          VARCHAR(50),
    willing_to_relocate     BOOLEAN,
    training_interest       VARCHAR(100),
    completeness_score      NUMERIC(5,2),
    quality_score           NUMERIC(5,2)
);