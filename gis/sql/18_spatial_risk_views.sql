CREATE OR REPLACE VIEW seip_gis.vw_township_spatial_risk AS
SELECT
    township_code,
    COUNT(*) AS total_people,
    COUNT(*) FILTER (WHERE currently_employed = FALSE) AS unemployed_count,
    COUNT(*) FILTER (WHERE age BETWEEN 15 AND 34 AND currently_employed = FALSE) AS youth_unemployed_count,
    COUNT(*) FILTER (WHERE training_interest = TRUE) AS training_interest_count,
    COUNT(*) FILTER (WHERE has_smartphone = FALSE) AS no_smartphone_count,
    ROUND(COUNT(*) FILTER (WHERE currently_employed = FALSE)::NUMERIC / NULLIF(COUNT(*), 0) * 100, 2) AS unemployment_rate_pct,
    ROUND(COUNT(*) FILTER (WHERE age BETWEEN 15 AND 34 AND currently_employed = FALSE)::NUMERIC / NULLIF(COUNT(*), 0) * 100, 2) AS youth_unemployment_rate_pct,
    ROUND(COUNT(*) FILTER (WHERE has_smartphone = FALSE)::NUMERIC / NULLIF(COUNT(*), 0) * 100, 2) AS digital_exclusion_rate_pct,
    ST_Centroid(ST_Collect(geom)) AS township_centroid
FROM seip_gis.fact_job_seeker_location
GROUP BY township_code;

CREATE OR REPLACE VIEW seip_gis.vw_township_intervention_priority AS
SELECT
    township_code,
    total_people,
    unemployed_count,
    youth_unemployed_count,
    training_interest_count,
    no_smartphone_count,
    unemployment_rate_pct,
    youth_unemployment_rate_pct,
    digital_exclusion_rate_pct,
    ROUND(
        unemployment_rate_pct * 0.40
        + youth_unemployment_rate_pct * 0.35
        + digital_exclusion_rate_pct * 0.15
        + LEAST(training_interest_count::NUMERIC / NULLIF(total_people, 0) * 100, 100) * 0.10,
        2
    ) AS intervention_priority_score,
    CASE
        WHEN (
            unemployment_rate_pct * 0.40
            + youth_unemployment_rate_pct * 0.35
            + digital_exclusion_rate_pct * 0.15
            + LEAST(training_interest_count::NUMERIC / NULLIF(total_people, 0) * 100, 100) * 0.10
        ) >= 75 THEN 'CRITICAL'
        WHEN (
            unemployment_rate_pct * 0.40
            + youth_unemployment_rate_pct * 0.35
            + digital_exclusion_rate_pct * 0.15
            + LEAST(training_interest_count::NUMERIC / NULLIF(total_people, 0) * 100, 100) * 0.10
        ) >= 60 THEN 'HIGH'
        WHEN (
            unemployment_rate_pct * 0.40
            + youth_unemployment_rate_pct * 0.35
            + digital_exclusion_rate_pct * 0.15
            + LEAST(training_interest_count::NUMERIC / NULLIF(total_people, 0) * 100, 100) * 0.10
        ) >= 40 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS intervention_priority_band,
    township_centroid
FROM seip_gis.vw_township_spatial_risk;
