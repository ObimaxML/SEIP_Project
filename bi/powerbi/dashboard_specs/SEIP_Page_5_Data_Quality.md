# Page 5 — Data Quality Monitor Build Sheet

## Objective

Track survey quality, completeness and low-quality records.

## KPI cards

- Total Survey Responses
- Average Completeness Score
- Average Quality Score
- Low Quality Survey Count
- Low Quality Survey Rate %

## Visuals

### Quality by township

```text
Visual: Clustered bar chart
Y-axis: township_code
X-axis: Average Quality Score
```

### Source channel

```text
Visual: Donut chart
Legend: source_channel
Values: Total Survey Responses
```

### Quality trend

```text
Visual: Line chart
X-axis: survey_date
Y-axis: Average Quality Score
```

### Low quality records

```text
Visual: Table
Filter: quality_score < 70
```
