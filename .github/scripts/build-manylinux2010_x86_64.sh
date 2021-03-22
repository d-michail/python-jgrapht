#!/bin/bash
set -e -x

echo "Current dir: `pwd`"
echo "GITHUB_WORKSPACE: $GITHUB_WORKSPACE"

# Build wheels for Python 3.6, 3.7, 3.8, 3.9
# Although we have a manylinux compatible wheel generated directly from
# setup.py, PyPI requires that the platform tag is set to a manylinux one
# (e.g. manylinux_x86_64 instead of linux_x86_64).
# Because auditwheel repair unecessarily bundles in zlib and breaks our
# RPATH we don't use it, instead we directly specify the tag with --plat-name
for PYBIN in /opt/python/cp3{6..9}*/bin; do
    "${PYBIN}/python" setup.py bdist_wheel --plat-name=manylinux2010_x86_64
done

# Show if our wheels are consistent with auditwheel (they should be)
for WHL in dist/*.whl
do
    auditwheel show "$WHL"
done

# Generate source distribution with sdist so we can upload it to PyPI
/opt/python/cp38-cp38/bin/python setup.py sdist

# Install generated wheels and run the tests
for PYBIN in /opt/python/cp3{6..9}*/bin; do
    "${PYBIN}/pip" install -r requirements/test.txt
    "${PYBIN}/pip" install jgrapht --no-index -f $GITHUB_WORKSPACE/dist
    "${PYBIN}/pytest"
done
