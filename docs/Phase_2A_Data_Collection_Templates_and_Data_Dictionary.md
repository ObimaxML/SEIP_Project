# Phase 2A — Data Collection Templates & Data Dictionary

Goal: create standardised collection templates for the four SEIP survey instruments: **Job Seeker, Business, Training Provider, and Informal Economy**. Your blueprint defines these four instruments and notes that the job seeker survey is the primary SEIP instrument.

## Phase 2A Deliverables

```text
data/templates/
├── job_seeker_template.csv
├── business_template.csv
├── training_provider_template.csv
├── informal_business_template.csv
└── seip_data_dictionary.xlsx
```

---

# 1. Job Seeker Template

Create:

```text
data/templates/job_seeker_template.csv
```

Use these columns:

```csv
respondent_id,consent_given,consent_date,first_name,last_name,id_number,date_of_birth,gender,nationality,south_african_citizen,mobile_number,email,whatsapp_number,township,ward_number,suburb,gps_latitude,gps_longitude,highest_qualification,education_level_code,field_of_study,nqf_level,digital_literacy_level,currently_employed,employment_status,months_unemployed,seeking_work,previous_job_title,previous_sector,preferred_sector,preferred_job_type,has_smartphone,has_internet_access,transport_mode,willing_to_relocate,training_interest,preferred_training_area,household_size,household_income_band,grant_recipient,disability_status,disability_type,available_start_date,survey_date,surveyor_name,source_channel
```

Sample row:

```csv
JS001,true,2026-06-10,Thabo,Mokoena,9001015009087,1990-01-01,Male,South African,true,0712345678,thabo@email.com,0712345678,SOWETO,WARD_001,Orlando East,-26.2311,27.9226,Matric,GRADE_12,General,4,Intermediate,false,UNEMPLOYED,18,true,General Worker,Retail,ICT,Full-time,true,true,Taxi,true,true,Data Analytics,5,R0-R1500,true,false,,2026-06-10,Fieldworker 1,KoBoToolbox
```

---

# 2. Business Template

Create:

```text
data/templates/business_template.csv
```

```csv
business_id,consent_given,business_name,registration_status,sector_code,business_type,company_size,township,ward_number,suburb,gps_latitude,gps_longitude,contact_person,contact_number,email,current_employee_count,open_vacancies,job_title,job_level,minimum_qualification,required_skills,salary_band,experience_required_years,vacancy_status,training_offered,willing_to_hire_youth,survey_date,surveyor_name,source_channel
```

Sample row:

```csv
BIZ001,true,Soweto Retail Market,Registered,RETAIL,Spaza/Retail,Small,SOWETO,WARD_001,Orlando East,-26.2311,27.9226,Owner,0711111111,owner@sowetoretail.co.za,8,3,Junior Data Capturer,Entry Level,Matric,"Microsoft Excel; SQL",R4000-R7000,1,OPEN,false,true,2026-06-10,Fieldworker 1,Google Forms
```

---

# 3. Training Provider Template

Create:

```text
data/templates/training_provider_template.csv
```

```csv
provider_id,consent_given,provider_name,provider_type,accredited,accreditation_body,township,ward_number,suburb,contact_person,contact_number,email,programme_name,nqf_level,duration_weeks,enrolled_count,completed_count,placed_count,placement_support,employer_partnerships,programme_cost_band,survey_date,source_channel
```

Sample row:

```csv
TP001,true,Soweto Skills Academy,Private Training Provider,true,SETAs,SOWETO,WARD_001,Orlando East,Admin,0722222222,info@sowetoskills.co.za,Data Analytics Foundation,5,12,40,32,18,true,"RetailCo; ICT Hub",R1000-R5000,2026-06-10,Email
```

---

# 4. Informal Business Template

Create:

```text
data/templates/informal_business_template.csv
```

```csv
informal_business_id,consent_given,owner_first_name,owner_last_name,owner_id_number,business_type,township,ward_number,suburb,gps_latitude,gps_longitude,employee_count,monthly_revenue_band,access_to_finance,growth_intent,main_challenges,uses_digital_payments,needs_training,training_area,survey_date,surveyor_name,source_channel
```

Sample row:

```csv
IB001,true,Nomsa,Dlamini,8502026009088,Food Stall,SOWETO,WARD_001,Orlando East,-26.2311,27.9226,2,R3000-R7000,false,true,"Stock funding; equipment",true,true,Business Management,2026-06-10,Fieldworker 1,ODK
```

---

# 5. Data Dictionary Structure

Create:

```text
data/templates/seip_data_dictionary.xlsx
```

Use these sheets:

```text
1. job_seeker_fields
2. business_fields
3. training_provider_fields
4. informal_business_fields
5. reference_values
6. validation_rules
```

Each field sheet should use this structure:

```csv
field_name,data_type,required,example,description,pii_flag,validation_rule,target_table,target_column
```

Example:

```csv
id_number,VARCHAR(13),Yes,9001015009087,South African ID number,Yes,Must be valid SA ID format,dim_person,id_number_hash
township,VARCHAR(30),Yes,SOWETO,Respondent township,No,Must exist in ref_township,dim_location,township_code
nqf_level,INTEGER,No,4,Qualification level,No,Must be between 1 and 10,dim_person,nqf_level
currently_employed,BOOLEAN,Yes,false,Current employment status,No,true or false,fact_employment_status,currently_employed
```

---

# 6. Validation Rules

Add this to the `validation_rules` sheet:

```csv
rule_code,field_name,rule_description,severity,action
CONSENT_REQUIRED,consent_given,Consent must be true before record is loaded,Critical,Reject
AGE_RANGE_VALID,date_of_birth,Age must be between 14 and 80,High,Quarantine
TOWNSHIP_VALID,township,Township must exist in reference list,High,Quarantine
SA_ID_VALID,id_number,SA ID must pass format and checksum validation,Medium,Flag
NQF_LEVEL_VALID,nqf_level,NQF level must be between 1 and 10,Medium,Correct or flag
GPS_IN_GAUTENG,gps_latitude/gps_longitude,GPS must fall within Gauteng boundary,Medium,Backfill or flag
```

These match the blueprint's required quality rules: consent, age range, township, SA ID, NQF level and Gauteng GPS validation.

---

# 7. Git Commit

```bash
git add data/templates
git commit -m "Add Phase 2A survey templates and data dictionary structure"
```

Phase 2A is complete when:

```text
✅ Job seeker template created
✅ Business template created
✅ Training provider template created
✅ Informal business template created
✅ Data dictionary structure defined
✅ Validation rules documented
```

Next: **Phase 2B — Generate the actual Excel templates and data dictionary file using Python.**
