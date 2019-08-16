#!/usr/bin/env bash

curl -O https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/linux_geo19b_19_2.zip\
    && unzip *.zip\
    && rm *.zip

export GEOFILES=${TRAVIS_BUILD_DIR}/version-19b_19.2/fls/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${TRAVIS_BUILD_DIR}/version-19b_19.2/lib/

python -m unittest