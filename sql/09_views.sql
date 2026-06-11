CREATE OR REPLACE VIEW seip_core.vw_person_safe AS
SELECT
    p.person_key,
    p.person_id,
    p.gender_code,
    p.age,
    p.nationality,
    p.south_african_citizen,
    p.highest_qualification,
    p.education_level_code,
    p.field_of_study,
    p.nqf_level,
    p.employment_status_code,
    l.township_code,
    t.township_name,
    l.ward_number,
    p.created_at
FROM seip_core.dim_person p
LEFT JOIN seip_core.dim_location l ON p.location_key = l.location_key
LEFT JOIN seip_core.ref_township t ON l.township_code = t.township_code;

CREATE OR REPLACE VIEW seip_core.vw_unemployment_by_township AS
SELECT
    t.township_name,
    COUNT(*) AS total_people,
    COUNT(*) FILTER (WHERE f.currently_employed = FALSE) AS unemployed_count,
    ROUND(COUNT(*) FILTER (WHERE f.currently_employed = FALSE)::NUMERIC / NULLIF(COUNT(*), 0) * 100, 2) AS unemployment_rate
FROM seip_core.fact_employment_status f
JOIN seip_core.dim_location l ON f.location_key = l.location_key
JOIN seip_core.ref_township t ON l.township_code = t.township_code
GROUP BY t.township_name;
