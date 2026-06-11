INSERT INTO seip_core.dim_location (township_code, ward_number, suburb, municipality, province, latitude, longitude, geom)
VALUES
('SOWETO', 'WARD_001', 'Orlando East', 'City of Johannesburg', 'Gauteng', -26.2311, 27.9226, ST_SetSRID(ST_MakePoint(27.9226, -26.2311), 4326))
ON CONFLICT DO NOTHING;

INSERT INTO seip_core.dim_skill (skill_name, skill_category_code, skill_type, nqf_level, demand_level)
VALUES
('Microsoft Excel', 'DIGITAL', 'Technical', 4, 'High'),
('SQL', 'DIGITAL', 'Technical', 5, 'High'),
('Python', 'DIGITAL', 'Technical', 6, 'High');
