#!/bin/bash
set -e
source $(dirname "$0")/utils.sh

set_env .env

echo "Buffering lots and calculating intersections for version ${INPUT_VERSION} ..."

mkdir -p data
psql $RECIPE_ENGINE --set ON_ERROR_STOP=1 --set INPUT_VERSION="${INPUT_VERSION}" --file sql/calculate_intersections.sql
mv data/intersection_temp.csv data/intersection_$INPUT_VERSION.csv

echo "Beginning python calculations ..."

python3 python/aue.py

echo "Done!"