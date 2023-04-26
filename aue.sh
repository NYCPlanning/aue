#!/bin/bash
set -e
source config.sh

echo "Buffering lots and calculating intersections ..."

mkdir -p data

psql $RECIPE_ENGINE --set ON_ERROR_STOP=1 -c "\COPY (SELECT t1.bbl AS t1, t2.bbl AS t2,
  (CASE WHEN ST_Intersects(ST_buffer(t1.wkb_geometry, 500), t2.wkb_geometry) then 0 else 1 END) as intersection 
  FROM dcp_proximity_establishments.\"20230425\" AS t1
  INNER JOIN dcp_proximity_establishments.\"20230425\" AS t2 on (t1.bbl != t2.bbl))
  TO "data/intersection.csv" DELIMITER ',' CSV HEADER;"

echo "Beginning python calculations ..."

docker run --rm\
    -v `pwd`:/home/aue\
    -w /home/aue\
    --env-file .env\
    nycplanning/cook:latest bash -c "pip3 install -r python/requirements.txt; python3 python/aue.py"

echo "Done!"