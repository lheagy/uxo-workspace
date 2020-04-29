#!/usr/bin/env bash

# Run the notebook that can use field data both including and excluding
# said data in training, so we can quickly compare its impact.

UXO_USE_FIELD_DATA=0 time jupyter nbconvert --execute --ExecutePreprocessor.timeout=None --to notebook train-with-noise-from-field-data.ipynb --output out-field-data-0.ipynb

UXO_USE_FIELD_DATA=1 time jupyter nbconvert --execute --ExecutePreprocessor.timeout=None --to notebook train-with-noise-from-field-data.ipynb --output out-field-data-1.ipynb
