#!/bin/bash
source config.sh

docker run --rm\
    -v `pwd`:/home/aue\
    -w /home/aue\
    --env-file .env\
    sptkl/cook:latest bash -c "pip3 install -r python/requirements.txt; python3 python/aue.py"