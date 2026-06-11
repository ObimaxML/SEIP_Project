ALTER TABLE seip_core.dim_person
DROP CONSTRAINT IF EXISTS chk_person_nqf_level;

ALTER TABLE seip_core.dim_person
ADD CONSTRAINT chk_person_nqf_level CHECK (nqf_level IS NULL OR nqf_level BETWEEN 1 AND 10);

ALTER TABLE seip_core.dim_person
DROP CONSTRAINT IF EXISTS chk_person_consent_date;

ALTER TABLE seip_core.dim_person
ADD CONSTRAINT chk_person_consent_date CHECK (consent_given = FALSE OR consent_date IS NOT NULL);

ALTER TABLE seip_core.fact_employment_status
DROP CONSTRAINT IF EXISTS chk_months_unemployed;

ALTER TABLE seip_core.fact_employment_status
ADD CONSTRAINT chk_months_unemployed CHECK (months_unemployed IS NULL OR months_unemployed >= 0);
