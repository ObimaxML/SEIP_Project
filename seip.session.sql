SELECT
    township_code,
    suburb,
    ST_AsText(geom) AS point_geometry
FROM seip_core.dim_location;