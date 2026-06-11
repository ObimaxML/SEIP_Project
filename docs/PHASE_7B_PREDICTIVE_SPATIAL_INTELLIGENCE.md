# Phase 7B — Predictive Spatial Intelligence

## Objective

Phase 7B moves SEIP from descriptive GIS mapping into predictive and prescriptive spatial intelligence.

It answers questions like:

```text
Where are unemployment clusters?
Where should training centres be placed?
Which job seekers have poor access to opportunities?
Which township zones need the strongest intervention?
Where are youth unemployment hotspots?
```

## Added files

```text
gis/sql/17_gis_foundation.sql
gis/sql/18_spatial_risk_views.sql
gis/scripts/load_gis_sample_to_postgres.py
gis/scripts/spatial_clustering.py
gis/scripts/opportunity_access_score.py
gis/scripts/training_centre_optimisation.py
gis/scripts/create_interactive_gis_map.py
gis/scripts/run_phase_7b_spatial_pipeline.py
gis/sample_data/job_seeker_points_sample.csv
```

## Step 1 — Install dependencies

```powershell
pip install -r requirements.txt
```

Phase 7B adds:

```text
geopandas
folium
shapely
scipy
```

## Step 2 — Run GIS SQL foundation

```powershell
Get-Content gis/sql/17_gis_foundation.sql | docker exec -i seip_postgres psql -U seip_admin -d seip_db
Get-Content gis/sql/18_spatial_risk_views.sql | docker exec -i seip_postgres psql -U seip_admin -d seip_db
```

## Step 3 — Load sample GIS data into PostgreSQL

```powershell
python gis/scripts/load_gis_sample_to_postgres.py
```

## Step 4 — Verify spatial views

In pgAdmin:

```sql
SELECT *
FROM seip_gis.vw_township_intervention_priority
ORDER BY intervention_priority_score DESC;
```

```sql
SELECT *
FROM seip_gis.vw_youth_unemployment_points;
```

## Step 5 — Run full spatial pipeline

```powershell
python gis/scripts/run_phase_7b_spatial_pipeline.py
```

Outputs:

```text
gis/outputs/data/spatial_clusters.csv
gis/outputs/data/opportunity_access_scores.csv
gis/outputs/data/recommended_training_centres.csv
gis/outputs/maps/seip_interactive_spatial_intelligence_map.html
```

## Step 6 — Open interactive map

Open this file in your browser:

```text
gis/outputs/maps/seip_interactive_spatial_intelligence_map.html
```

The map includes:

```text
Unemployment heatmap
Job seeker points
Recommended training centre locations
Popup details
Layer controls
```

## Spatial analytics included

### 1. DBSCAN clustering

Detects dense unemployment clusters without needing a predefined number of clusters.

### 2. KMeans intervention zones

Creates planned intervention zones.

### 3. Opportunity access score

Calculates distance to nearest training or job centre.

### 4. Training centre optimisation

Recommends centre coordinates based on demand clusters.

### 5. Interactive map

Creates a portable HTML map for portfolio demos.

## Important interpretation note

Recommended centre locations are analytical suggestions, not final site decisions.

Before real-world implementation, validate with:

```text
Land availability
Public transport routes
Community safety
Existing training providers
Cost
Stakeholder consultations
```

## Power BI use

Import these CSV outputs into Power BI:

```text
spatial_clusters.csv
opportunity_access_scores.csv
recommended_training_centres.csv
```

Suggested visuals:

```text
Map: recommended centres
Scatter map: unemployment clusters
Bar chart: opportunity access score by township
Matrix: training centre demand count by township
```

## Git commit

```powershell
git add .
git commit -m "Implement Phase 7B predictive spatial intelligence"
```

## Next phase

```text
Phase 8A — Tableau dashboards and public portfolio storytelling
```
