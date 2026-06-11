DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'seip_engineer') THEN CREATE ROLE seip_engineer; END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'seip_analyst') THEN CREATE ROLE seip_analyst; END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'seip_viewer') THEN CREATE ROLE seip_viewer; END IF;
END $$;
