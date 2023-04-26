#!/bin/bash
set -e

echo "Setting up build environment ..."

# install postgresql client to use psql (postgresql alias)
sudo apt-get update
sudo apt-get --assume-yes install --no-install-recommends postgresql-client

# install python packages
python3 -m pip install --upgrade pip
python3 -m pip install --requirement requirements.txt

echo "Done!"