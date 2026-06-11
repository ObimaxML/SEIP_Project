CREATE INDEX IF NOT EXISTS idx_dim_location_township ON seip_core.dim_location(township_code);
CREATE INDEX IF NOT EXISTS idx_dim_location_geom ON seip_core.dim_location USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_dim_person_location ON seip_core.dim_person(location_key);
CREATE INDEX IF NOT EXISTS idx_dim_person_id_hash ON seip_core.dim_person(id_number_hash);
CREATE INDEX IF NOT EXISTS idx_fact_employment_person ON seip_core.fact_employment_status(person_key);
CREATE INDEX IF NOT EXISTS idx_fact_employment_location ON seip_core.fact_employment_status(location_key);
