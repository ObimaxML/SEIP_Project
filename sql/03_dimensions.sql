CREATE TABLE IF NOT EXISTS seip_core.dim_location (
    location_key BIGSERIAL PRIMARY KEY,
    location_id UUID DEFAULT uuid_generate_v4() UNIQUE,
    township_code VARCHAR(30) REFERENCES seip_core.ref_township(township_code),
    ward_number VARCHAR(30),
    suburb VARCHAR(100),
    municipality VARCHAR(100),
    province VARCHAR(100) DEFAULT 'Gauteng',
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    geom GEOMETRY(Point, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS seip_core.dim_person (
    person_key BIGSERIAL PRIMARY KEY,
    person_id UUID DEFAULT uuid_generate_v4() UNIQUE,
    first_name_encrypted BYTEA,
    last_name_encrypted BYTEA,
    id_number_hash VARCHAR(256) UNIQUE,
    gender_code VARCHAR(30),
    date_of_birth DATE,
    age INT,
    nationality VARCHAR(100),
    south_african_citizen BOOLEAN,
    highest_qualification VARCHAR(150),
    education_level_code VARCHAR(50),
    field_of_study VARCHAR(150),
    nqf_level INT,
    employment_status_code VARCHAR(50),
    location_key BIGINT REFERENCES seip_core.dim_location(location_key),
    mobile_number_hash VARCHAR(256),
    email_hash VARCHAR(256),
    whatsapp_number_hash VARCHAR(256),
    consent_given BOOLEAN NOT NULL DEFAULT FALSE,
    consent_date TIMESTAMP,
    consent_version VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS seip_core.dim_skill (
    skill_key BIGSERIAL PRIMARY KEY,
    skill_id UUID DEFAULT uuid_generate_v4() UNIQUE,
    skill_name VARCHAR(150) NOT NULL,
    skill_category_code VARCHAR(30) REFERENCES seip_core.ref_skill_category(skill_category_code),
    skill_type VARCHAR(50),
    nqf_level INT,
    demand_level VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
