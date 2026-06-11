CREATE TABLE IF NOT EXISTS seip_audit.aud_etl_run_log (
    etl_run_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    pipeline_name VARCHAR(100),
    source_file_name VARCHAR(255),
    status VARCHAR(30),
    records_received INT DEFAULT 0,
    records_loaded INT DEFAULT 0,
    records_rejected INT DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS seip_audit.aud_person_changes (
    change_id BIGSERIAL PRIMARY KEY,
    person_key BIGINT,
    action_type VARCHAR(20),
    changed_by VARCHAR(100) DEFAULT CURRENT_USER,
    old_record JSONB,
    new_record JSONB,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION seip_audit.fn_audit_person_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO seip_audit.aud_person_changes (person_key, action_type, new_record)
        VALUES (NEW.person_key, TG_OP, row_to_json(NEW)::jsonb);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO seip_audit.aud_person_changes (person_key, action_type, old_record, new_record)
        VALUES (NEW.person_key, TG_OP, row_to_json(OLD)::jsonb, row_to_json(NEW)::jsonb);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO seip_audit.aud_person_changes (person_key, action_type, old_record)
        VALUES (OLD.person_key, TG_OP, row_to_json(OLD)::jsonb);
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_audit_person_changes ON seip_core.dim_person;

CREATE TRIGGER trg_audit_person_changes
AFTER INSERT OR UPDATE OR DELETE ON seip_core.dim_person
FOR EACH ROW EXECUTE FUNCTION seip_audit.fn_audit_person_changes();
