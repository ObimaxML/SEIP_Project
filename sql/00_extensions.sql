CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

SELECT 
    uuid_generate_v4() AS test_uuid,
    PostGIS_Version() AS postgis_version;