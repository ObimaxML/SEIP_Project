-- 1. People without consent
SELECT *
FROM seip_core.dim_person
WHERE consent_given = FALSE;

-- 2. People with invalid age
-- Invalid ages derived from DOB
SELECT *
FROM seip_core.dim_person
WHERE date_of_birth IS NULL
   OR EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) < 14
   OR EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) > 80;

-- 3. People without location
SELECT *
FROM seip_core.dim_person
WHERE location_key IS NULL;

-- 4. Employment facts without matching person
SELECT f.*
FROM seip_core.fact_employment_status f
LEFT JOIN seip_core.dim_person p
    ON f.person_key = p.person_key
WHERE p.person_key IS NULL;

-- 5. Location records without geometry
SELECT *
FROM seip_core.dim_location
WHERE geom IS NULL;

-- 6. Duplicate ID hashes
SELECT
    id_number_hash,
    COUNT(*) AS duplicate_count
FROM seip_core.dim_person
WHERE id_number_hash IS NOT NULL
GROUP BY id_number_hash
HAVING COUNT(*) > 1;

-- 7. Township-level unemployment sanity check
SELECT *
FROM seip_core.vw_unemployment_by_township
ORDER BY unemployment_rate DESC;