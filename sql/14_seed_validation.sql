SELECT 'ref_township' AS table_name, COUNT(*) AS record_count
FROM seip_core.ref_township

UNION ALL

SELECT 'ref_skill_category', COUNT(*)
FROM seip_core.ref_skill_category

UNION ALL

SELECT 'ref_industry_sector', COUNT(*)
FROM seip_core.ref_industry_sector

UNION ALL

SELECT 'dim_location', COUNT(*)
FROM seip_core.dim_location

UNION ALL

SELECT 'dim_person', COUNT(*)
FROM seip_core.dim_person

UNION ALL

SELECT 'dim_skill', COUNT(*)
FROM seip_core.dim_skill

UNION ALL

SELECT 'fact_employment_status', COUNT(*)
FROM seip_core.fact_employment_status

UNION ALL

SELECT 'fact_job_seeker_survey', COUNT(*)
FROM seip_core.fact_job_seeker_survey;