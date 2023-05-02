#!/bin/bash
set -e

# only do this when running locally (rather than in a github action)
if [[ ${CI} != "true" ]]; then
    # load/reload environment variables from .env file
    source $(dirname "$0")/utils.sh
    set_env .devcontainer/.env
fi

echo "Buffering lots and calculating intersections for version ${INPUT_VERSION} ..."

mkdir -p data
psql $RECIPE_ENGINE --set ON_ERROR_STOP=1 --set INPUT_VERSION="${INPUT_VERSION}" --file sql/calculate_intersections.sql
mv data/intersection_temp.csv data/intersection_$INPUT_VERSION.csv

echo "Beginning python calculations ..."

python3 python/aue.py

echo "Done!"