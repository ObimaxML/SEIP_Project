# Phase 5B — Power BI Visual Build Walkthrough

## Objective

Phase 5B guides you through building the SEIP Power BI report page by page.

You will create five report pages:

1. Executive Overview
2. Township Employment Profile
3. Youth and Skills Gap
4. Digital Access and Readiness
5. Data Quality Monitor

## Before you start

Complete Phase 5A first.

You should already have imported either:

### PostgreSQL model

```text
vw_person_safe
vw_powerbi_location
vw_powerbi_employment_fact
vw_powerbi_job_seeker_survey
```

or:

### Databricks Gold CSV model

```text
gold_unemployment_by_township
gold_skills_training_demand
gold_digital_access
```

For the full detailed dashboard, use the PostgreSQL model.

---

# Report Theme

## Canvas settings

In Power BI:

```text
Format page → Canvas settings
Type: 16:9
```

## Suggested layout

```text
Top row: Title and filters
Second row: KPI cards
Middle: Main visuals
Bottom: Detail matrix / table
```

## Suggested colours

Use a clean public-sector style:

```text
Background: #F7F9FB
Text: dark grey
Accent: blue or green
Warning: orange/red for high unemployment
```

Do not overuse colours. Let the KPIs and maps carry the message.

---

# Page 1 — Executive Overview

## Purpose

Give a fast summary of the employment situation across SEIP target townships.

## Page title

```text
SEIP Executive Employment Overview
```

## Visual 1 — KPI Cards

Create six cards:

| Card | Measure |
|---|---|
| Total Job Seekers | Total Job Seekers |
| Unemployed Count | Unemployed Count |
| Unemployment Rate | Unemployment Rate % |
| Youth Unemployment Rate | Youth Unemployment Rate % |
| Avg Months Unemployed | Average Months Unemployed |
| Training Interest Rate | Training Interest Rate % |

## Visual 2 — Township Unemployment Bar Chart

Visual type:

```text
Clustered bar chart
```

Fields:

```text
Y-axis: vw_powerbi_location[township_code]
X-axis: Unemployment Rate %
Tooltips: Total Job Seekers, Unemployed Count, Average Months Unemployed
```

Sort:

```text
Unemployment Rate % descending
```

## Visual 3 — Employment Split Donut

Visual type:

```text
Donut chart
```

Fields:

```text
Legend: vw_powerbi_employment_fact[currently_employed]
Values: Total Employment Records
```

Rename labels:

```text
TRUE = Employed
FALSE = Unemployed
```

## Visual 4 — Township Matrix

Visual type:

```text
Matrix
```

Rows:

```text
vw_powerbi_location[township_code]
```

Values:

```text
Total Job Seekers
Employed Count
Unemployed Count
Unemployment Rate %
Youth Job Seekers
Youth Unemployment Rate %
```

## Slicers

Add slicers:

```text
Township
Gender
Highest Qualification
Survey Date
```

## Formatting tips

- Use large KPI cards.
- Set unemployment percentage to one decimal place.
- Use conditional formatting on unemployment rate.
- Keep the matrix at the bottom.

---

# Page 2 — Township Employment Profile

## Purpose

Allow users to drill into each township and ward.

## Page title

```text
Township Employment Profile
```

## Visual 1 — KPI Cards

Cards:

```text
Total Job Seekers
Employed Count
Unemployed Count
Seeking Work Count
Long-Term Unemployment Rate %
```

## Visual 2 — Ward/Township Breakdown

Visual type:

```text
Clustered column chart
```

Fields:

```text
X-axis: vw_powerbi_location[ward_number]
Y-axis: Unemployed Count
Legend: vw_powerbi_location[township_code]
```

## Visual 3 — Months Unemployed Distribution

Visual type:

```text
Column chart
```

Fields:

```text
X-axis: vw_powerbi_employment_fact[months_unemployed]
Y-axis: Count of person_key
```

Group months into bins if needed:

```text
0–3 months
4–6 months
7–12 months
13–24 months
24+ months
```

## Visual 4 — Age vs Months Unemployed

Visual type:

```text
Scatter chart
```

Fields:

```text
X-axis: vw_person_safe[age]
Y-axis: vw_powerbi_employment_fact[months_unemployed]
Details: vw_person_safe[person_key]
Legend: vw_person_safe[gender_code]
```

## Visual 5 — Detail Table

Visual type:

```text
Table
```

Columns:

```text
township_code
ward_number
gender_code
age
highest_qualification
nqf_level
employment_status_code
months_unemployed
preferred_sector
```

Important: do not add PII fields.

---

# Page 3 — Youth and Skills Gap

## Purpose

Highlight youth unemployment, qualifications, preferred sectors and training demand.

## Page title

```text
Youth and Skills Gap Analysis
```

## Visual 1 — KPI Cards

Cards:

```text
Youth Job Seekers
Youth Unemployed Count
Youth Unemployment Rate %
Training Interest Count
Matric or Higher Rate %
Average NQF Level
```

## Visual 2 — Preferred Training Area

Visual type:

```text
Bar chart
```

Fields:

```text
Y-axis: vw_powerbi_job_seeker_survey[preferred_training_area]
X-axis: Training Interest Count
```

If using Gold CSV:

```text
Y-axis: gold_skills_training_demand[preferred_training_area]
X-axis: Total Training Interest
```

## Visual 3 — Qualification by Township

Visual type:

```text
Stacked column chart
```

Fields:

```text
X-axis: vw_powerbi_location[township_code]
Y-axis: Total Job Seekers
Legend: vw_person_safe[highest_qualification]
```

## Visual 4 — Preferred Sector by Township

Visual type:

```text
Matrix
```

Rows:

```text
township_code
```

Columns:

```text
preferred_sector
```

Values:

```text
Unemployed Count
```

## Visual 5 — Digital Literacy

Visual type:

```text
100% stacked bar chart
```

Fields:

```text
Y-axis: township_code
X-axis: Total Job Seekers
Legend: digital_literacy_level
```

---

# Page 4 — Digital Access and Readiness

## Purpose

Show whether job seekers can access digital employment and training services.

## Page title

```text
Digital Access and Readiness
```

## Visual 1 — KPI Cards

Cards:

```text
Smartphone Users
Smartphone Access Rate %
Internet Users
Internet Access Rate %
Average NQF Level
Training Interest Rate %
```

## Visual 2 — Smartphone Access by Township

Visual type:

```text
Clustered bar chart
```

Fields:

```text
Y-axis: township_code
X-axis: Smartphone Access Rate %
```

## Visual 3 — Transport Mode

Visual type:

```text
Donut chart
```

Fields:

```text
Legend: transport_mode
Values: Total Survey Responses
```

## Visual 4 — Digital Literacy by Township

Visual type:

```text
Stacked bar chart
```

Fields:

```text
Y-axis: township_code
X-axis: Total Job Seekers
Legend: digital_literacy_level
```

## Visual 5 — Readiness Matrix

Visual type:

```text
Matrix
```

Rows:

```text
township_code
```

Values:

```text
Total Job Seekers
Smartphone Access Rate %
Training Interest Rate %
Willing To Relocate Rate %
Average NQF Level
```

---

# Page 5 — Data Quality Monitor

## Purpose

Track survey quality, completeness and pipeline health.

## Page title

```text
SEIP Data Quality Monitor
```

## Visual 1 — KPI Cards

Cards:

```text
Total Survey Responses
Average Completeness Score
Average Quality Score
Low Quality Survey Count
Low Quality Survey Rate %
```

## Visual 2 — Quality by Township

Visual type:

```text
Clustered bar chart
```

Fields:

```text
Y-axis: township_code
X-axis: Average Quality Score
```

## Visual 3 — Survey Source Channel

Visual type:

```text
Donut chart
```

Fields:

```text
Legend: source_channel
Values: Total Survey Responses
```

## Visual 4 — Quality Trend

Visual type:

```text
Line chart
```

Fields:

```text
X-axis: survey_date
Y-axis: Average Quality Score
```

## Visual 5 — Low Quality Records Table

Visual type:

```text
Table
```

Columns:

```text
survey_date
township_code
ward_number
quality_score
completeness_score
digital_literacy_level
transport_mode
```

Filter:

```text
quality_score < 70
```

---

# Navigation Setup

Create buttons:

```text
Executive Overview
Township Profile
Youth & Skills
Digital Access
Data Quality
```

Place them at the top of every page.

Use:

```text
Insert → Buttons → Navigator → Page navigator
```

---

# Tooltip Pages

Create a tooltip page called:

```text
Township Tooltip
```

Fields:

```text
Township
Total Job Seekers
Unemployed Count
Unemployment Rate %
Youth Unemployment Rate %
Smartphone Access Rate %
Training Interest Rate %
```

Use this tooltip on township bar charts.

---

# Drillthrough Page

Create a drillthrough page:

```text
Township Drillthrough
```

Drillthrough field:

```text
township_code
```

Visuals:

```text
KPI cards
Ward breakdown
Qualification split
Training demand
Digital access
```

---

# Testing Checklist

Before saving the final PBIX, test:

```text
☐ Slicers filter all visuals correctly
☐ Township bar chart sorts descending by unemployment rate
☐ All percentage measures display as %
☐ No PII fields are visible
☐ RLS test works for township users
☐ Matrix totals are correct
☐ Data Quality page shows survey quality scores
☐ Navigation buttons work
☐ Report refreshes successfully
```

---

# Save File

Save as:

```text
SEIP_Employment_Intelligence_Dashboard.pbix
```

Recommended folder:

```text
bi/powerbi/pbix/
```

Do not commit large `.pbix` files to Git unless you intentionally want to version them.

Recommended:

```gitignore
*.pbix
```
