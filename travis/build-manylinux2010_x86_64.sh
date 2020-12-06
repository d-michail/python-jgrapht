#!/bin/bash
set -e -x

# zlib-devel is needed for compiling libjgrapht_capi.so
# pcre-devel is needed for compiling SWIG
yum install -y zlib-devel pcre-devel

# Install CMake
curl -LO https://github.com/Kitware/CMake/releases/download/v3.19.1/cmake-3.19.1-Linux-x86_64.sh
sh cmake-3.19.1-Linux-x86_64.sh --skip-license --prefix=/opt --include-subdir
export PATH="/opt/cmake-3.19.1-Linux-x86_64/bin:$PATH"

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
# Although we have a manylinux compatible wheel generated directly from
# setup.py, PyPI requires that the platform tag is set to a manylinux one
# (e.g. manylinux_x86_64 instead of linux_x86_64).
# Because auditwheel repair unecessarily bundles in zlib and breaks our
# RPATH we don't use it, instead we directly specify the tag with --plat-name
for PYBIN in /opt/python/cp3{6..8}*/bin; do
    "${PYBIN}/python" setup.py bdist_wheel --plat-name=manylinux2010_x86_64
done

# Show if our wheels are consistent with auditwheel (they should be)
for WHL in dist/*.whl
do
    auditwheel show "$WHL"
done

# Generate source distribution with sdist so Travis can upload it to PyPI
/opt/python/cp38-cp38/bin/python setup.py sdist

# Install generated wheels and run the tests
for PYBIN in /opt/python/cp3{6..8}*/bin; do
    "${PYBIN}/pip" install -r requirements/test.txt
    "${PYBIN}/pip" install jgrapht --no-index -f /io/dist
    (cd /io; "${PYBIN}/pytest")
done
