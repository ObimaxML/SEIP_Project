CREATE TABLE IF NOT EXISTS seip_core.fact_employment_status (
    employment_status_key BIGSERIAL PRIMARY KEY,
    person_key BIGINT REFERENCES seip_core.dim_person(person_key),
    location_key BIGINT REFERENCES seip_core.dim_location(location_key),
    survey_date DATE NOT NULL,
    currently_employed BOOLEAN,
    months_unemployed INT,
    seeking_work BOOLEAN,
    preferred_sector VARCHAR(100),
    income_band VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS seip_core.fact_job_seeker_survey (
    survey_key BIGSERIAL PRIMARY KEY,
    person_key BIGINT REFERENCES seip_core.dim_person(person_key),
    location_key BIGINT REFERENCES seip_core.dim_location(location_key),
    survey_date DATE NOT NULL,
    digital_literacy_level VARCHAR(50),
    has_smartphone BOOLEAN,
    transport_mode VARCHAR(50),
    willing_to_relocate BOOLEAN,
    training_interest BOOLEAN,
    completeness_score DECIMAL(5,2),
    quality_score DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
