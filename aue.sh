#!/bin/bash
source config.sh

echo "Buffering lots and calculating intersections"

psql $RECIPE_ENGINE -c "\COPY (SELECT t1.bbl AS t1, t2.bbl AS t2,
  (CASE WHEN ST_Intersects(ST_buffer(t1.wkb_geometry, 500), t2.wkb_geometry) then 0 else 1 END) as intersection 
  FROM aue_lots.latest AS t1
  INNER JOIN aue_lots.latest AS t2 on (t1.bbl != t2.bbl))
  TO STDOUT DELIMITER ',' CSV HEADER;" > data/intersection.csv

echo "Beginning python calculations"

docker run --rm\
    -v `pwd`:/home/aue\
    -w /home/aue\
    --env-file .env\
    sptkl/cook:latest bash -c "pip3 install -r python/requirements.txt; python3 python/aue.py"