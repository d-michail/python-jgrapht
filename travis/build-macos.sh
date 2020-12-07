#!/bin/bash
set -e -x

pyenv global 3.6.9 3.7.5 3.8.0
eval "$(pyenv init -)"

# Build wheels for Python 3.6, 3.7, 3.8, 3.9
for PYBIN in /Users/travis/.pyenv/versions/3*/bin; do
    "${PYBIN}/pip" install wheel
    "${PYBIN}/python" setup.py bdist_wheel
done

# Install generated wheels and run the tests
for PYBIN in /Users/travis/.pyenv/versions/3*/bin; do
    "${PYBIN}/pip" install -r requirements/test.txt
    "${PYBIN}/pip" install jgrapht --no-index -f dist/
    "${PYBIN}/pytest"
done
