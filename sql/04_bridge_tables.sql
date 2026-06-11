CREATE TABLE IF NOT EXISTS seip_core.bridge_person_skill (
    person_skill_key BIGSERIAL PRIMARY KEY,
    person_key BIGINT REFERENCES seip_core.dim_person(person_key),
    skill_key BIGINT REFERENCES seip_core.dim_skill(skill_key),
    proficiency_level VARCHAR(50),
    years_experience DECIMAL(4,1),
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
