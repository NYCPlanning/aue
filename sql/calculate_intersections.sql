CREATE TEMP TABLE tmp AS (
  SELECT
    t1.bbl AS t1,
    t2.bbl AS t2,
(
    CASE WHEN ST_Intersects(ST_buffer(t1.wkb_geometry, 500), t2.wkb_geometry) THEN
      0
    ELSE
      1
    END
) AS intersection
  FROM
    dcp_proximity_establishments.:INPUT_VERSION AS t1
    INNER JOIN dcp_proximity_establishments.:INPUT_VERSION AS t2 ON (t1.bbl != t2.bbl)
);

\COPY tmp TO 'data/intersection_temp.csv' DELIMITER ',' CSV HEADER;
