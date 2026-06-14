ALTER TABLE seip_core.dim_person
ADD CONSTRAINT chk_person_nqf_level
CHECK (nqf_level IS NULL OR nqf_level BETWEEN 1 AND 10);

ALTER TABLE seip_core.dim_person
ADD CONSTRAINT chk_person_consent_date
CHECK (
    consent_given = FALSE
    OR consent_date IS NOT NULL
);

ALTER TABLE seip_core.dim_person
ADD CONSTRAINT chk_person_birth_date
CHECK (
    date_of_birth IS NULL
    OR date_of_birth <= CURRENT_DATE
);

ALTER TABLE seip_core.fact_employment_status
ADD CONSTRAINT chk_months_unemployed
CHECK (
    months_unemployed IS NULL
    OR months_unemployed >= 0
);

ALTER TABLE seip_core.fact_job_seeker_survey
ADD CONSTRAINT chk_completeness_score
CHECK (
    completeness_score IS NULL
    OR completeness_score BETWEEN 0 AND 100
);

ALTER TABLE seip_core.fact_job_seeker_survey
ADD CONSTRAINT chk_quality_score
CHECK (
    quality_score IS NULL
    OR quality_score BETWEEN 0 AND 100
);

ALTER TABLE seip_core.fact_business_vacancy
ADD CONSTRAINT chk_vacancy_count
CHECK (vacancy_count >= 0);

ALTER TABLE seip_core.fact_training_outcome
ADD CONSTRAINT chk_training_counts
CHECK (
    completed_count <= enrolled_count
    AND placed_count <= completed_count
);

ALTER TABLE seip_core.fact_training_outcome
ADD CONSTRAINT chk_training_rates
CHECK (
    completion_rate BETWEEN 0 AND 100
    AND placement_rate BETWEEN 0 AND 100
);