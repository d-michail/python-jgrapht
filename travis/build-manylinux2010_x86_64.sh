#!/bin/bash
set -e -x

# zlib-devel is needed for compiling libjgrapht_capi.so
# pcre-devel is needed for compiling SWIG
yum install -y zlib-devel pcre-devel
# Install CMake from PyPI which provides a pre-compiled binary
/opt/python/cp38-cp38/bin/pip install cmake


# Install GraalVM and native-image
curl -LO https://github.com/graalvm/graalvm-ce-builds/releases/download/vm-20.0.0/graalvm-ce-java11-linux-amd64-20.0.0.tar.gz
tar xzf graalvm-ce-java11-linux-amd64-20.0.0.tar.gz -C /opt/
export PATH="/opt/graalvm-ce-java11-20.0.0/bin:$PATH"
gu install native-image

# Install Maven
curl -LO https://downloads.apache.org/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz
tar xzf apache-maven-3.6.3-bin.tar.gz -C /opt/
export PATH="/opt/apache-maven-3.6.3/bin:$PATH"

# Compile and install SWIG
SWIG_VERSION=4.0.1
curl -LO https://vorboss.dl.sourceforge.net/project/swig/swig/swig-$SWIG_VERSION/swig-$SWIG_VERSION.tar.gz
tar xzf swig-$SWIG_VERSION.tar.gz -C /tmp/
cd /tmp/swig-$SWIG_VERSION
./configure
make
make install

cd /io
# Build wheels for Python 3.6, 3.7, 3.8
for PYBIN in /opt/python/cp3{6..8}*/bin; do
    "${PYBIN}/python" setup.py bdist_wheel
done

# Although we have a manylinux compatible wheel generated directly from
# setup.py, PyPI requires that the platform tag is set to a manylinux one
# (e.g. manylinux_x86_64 instead of linux_x86_64). Therefore we auditwheel repair
# our wheels anyway.
# Note that this leads to some trouble with RPATH overriding, so extra care had to
# be taken in setup.py.
for WHL in dist/*.whl
do
    auditwheel repair "$WHL"
done

# auditwheel repair creates new wheels and puts them at wheelhouse/
# Travis CI pypi deploy provider expects to find the wheels to
# upload at dist/
rm /io/dist/*.whl
mv /io/wheelhouse/*.whl /io/dist/

# Generate source distribution with sdist so Travis can upload it to PyPI
/opt/python/cp38-cp38/bin/python setup.py sdist

# Install generated wheels and run the tests
for PYBIN in /opt/python/cp3{6..8}*/bin; do
    "${PYBIN}/pip" install -r requirements/test.txt
    "${PYBIN}/pip" install jgrapht --no-index -f /io/dist
    (cd /io; "${PYBIN}/pytest")
done
