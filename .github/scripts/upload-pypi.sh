#!/bin/bash
set -e -x

echo "Current dir: `pwd`"
echo "GITHUB_WORKSPACE: $GITHUB_WORKSPACE"

ls $GITHUB_WORKSPACE/dist/*

/opt/python/cp38-cp38/bin/python -m pip install -U pip
/opt/python/cp38-cp38/bin/python -m pip install twine
/opt/python/cp38-cp38/bin/python -m twine --version
/opt/python/cp38-cp38/bin/python -m twine upload --repository testpypi --username "${PYPI_USER:-__token__}" --password "$PYPI_PASSWORD" dist/*

