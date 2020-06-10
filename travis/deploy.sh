#!/bin/bash
twine upload \
    --username "${PYPI_USER:-__token__}" \
    --password "$PYPI_PASSWORD" \
    ./dist/*

