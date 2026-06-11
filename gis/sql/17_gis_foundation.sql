CREATE SCHEMA IF NOT EXISTS seip_gis;

CREATE TABLE IF NOT EXISTS seip_gis.fact_job_seeker_location (
    location_event_key BIGSERIAL PRIMARY KEY,
    person_key BIGINT,
    survey_date DATE,
    township_code VARCHAR(30),
    ward_number VARCHAR(30),
    latitude NUMERIC(10,8),
    longitude NUMERIC(11,8),
    currently_employed BOOLEAN,
    age INT,
    training_interest BOOLEAN,
    preferred_training_area VARCHAR(150),
    has_smartphone BOOLEAN,
    transport_mode VARCHAR(50),
    geom GEOMETRY(Point, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_gis_jobseeker_geom
ON seip_gis.fact_job_seeker_location
USING GIST (geom);

CREATE OR REPLACE VIEW seip_gis.vw_youth_unemployment_points AS
SELECT *
FROM seip_gis.fact_job_seeker_location
WHERE age BETWEEN 15 AND 34
  AND currently_employed = FALSE;

CREATE OR REPLACE VIEW seip_gis.vw_training_demand_points AS
SELECT *
FROM seip_gis.fact_job_seeker_location
WHERE training_interest = TRUE;

CREATE OR REPLACE VIEW seip_gis.vw_digital_exclusion_points AS
SELECT *
FROM seip_gis.fact_job_seeker_location
WHERE has_smartphone = FALSE;
