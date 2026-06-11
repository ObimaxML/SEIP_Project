# SEIP Phase 5A — Power BI Row-Level Security Rules

## Objective

Restrict dashboard access by township, role or stakeholder group.

## Recommended RLS table

Create/import a table called:

```text
security_user_access
```

Columns:

```text
user_email
role_name
township_code
access_level
```

Example:

```csv
user_email,role_name,township_code,access_level
analyst@seip.co.za,Analyst,SOWETO,TOWNSHIP
ngo_soweto@seip.co.za,NGO,SOWETO,TOWNSHIP
admin@seip.co.za,Admin,ALL,ALL
```

## Relationship

```text
security_user_access[township_code] → dim_location[township_code]
```

Use many-to-one or bridge carefully if multiple townships per user.

## RLS DAX rule

Apply this rule to `security_user_access`:

```DAX
[user_email] = USERPRINCIPALNAME()
    || [access_level] = "ALL"
```

## Alternative township filter rule

Apply this rule directly to `dim_location`:

```DAX
dim_location[township_code]
    IN
    SELECTCOLUMNS (
        FILTER (
            security_user_access,
            security_user_access[user_email] = USERPRINCIPALNAME()
                || security_user_access[access_level] = "ALL"
        ),
        "township_code",
        security_user_access[township_code]
    )
```

## Production note

Do not expose raw PII in Power BI. Use only:

```text
vw_person_safe
Gold aggregates
Masked or hashed identifiers
```
