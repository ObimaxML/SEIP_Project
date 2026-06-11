CREATE TABLE IF NOT EXISTS seip_core.ref_township (
    township_code VARCHAR(30) PRIMARY KEY,
    township_name VARCHAR(100) NOT NULL,
    municipality VARCHAR(100),
    province VARCHAR(100) DEFAULT 'Gauteng'
);

INSERT INTO seip_core.ref_township (township_code, township_name, municipality, province)
VALUES
('SOWETO', 'Soweto', 'City of Johannesburg', 'Gauteng'),
('DIEPSLOOT', 'Diepsloot', 'City of Johannesburg', 'Gauteng'),
('ALEXANDRA', 'Alexandra', 'City of Johannesburg', 'Gauteng'),
('ORANGE_FARM', 'Orange Farm', 'City of Johannesburg', 'Gauteng'),
('TEMBISA', 'Tembisa', 'Ekurhuleni', 'Gauteng'),
('KATLEHONG', 'Katlehong', 'Ekurhuleni', 'Gauteng'),
('VOSLOORUS', 'Vosloorus', 'Ekurhuleni', 'Gauteng'),
('KAGISO', 'Kagiso', 'Mogale City', 'Gauteng'),
('PROTEA_GLEN', 'Protea Glen', 'City of Johannesburg', 'Gauteng')
ON CONFLICT (township_code) DO NOTHING;

CREATE TABLE IF NOT EXISTS seip_core.ref_skill_category (
    skill_category_code VARCHAR(30) PRIMARY KEY,
    skill_category_name VARCHAR(100) NOT NULL
);

INSERT INTO seip_core.ref_skill_category VALUES
('DIGITAL', 'Digital Skills'),
('TECHNICAL', 'Technical Skills'),
('SOFT', 'Soft Skills'),
('BUSINESS', 'Business Skills'),
('TRADE', 'Trade Skills')
ON CONFLICT (skill_category_code) DO NOTHING;

CREATE TABLE IF NOT EXISTS seip_core.ref_industry_sector (
    sector_code VARCHAR(30) PRIMARY KEY,
    sector_name VARCHAR(150) NOT NULL
);

INSERT INTO seip_core.ref_industry_sector VALUES
('RETAIL', 'Retail'),
('ICT', 'Information and Communication Technology'),
('CONSTRUCTION', 'Construction'),
('MANUFACTURING', 'Manufacturing'),
('HOSPITALITY', 'Hospitality'),
('TRANSPORT', 'Transport and Logistics'),
('FINANCE', 'Financial Services'),
('EDUCATION', 'Education and Training'),
('HEALTH', 'Healthcare'),
('INFORMAL', 'Informal Economy')
ON CONFLICT (sector_code) DO NOTHING;
