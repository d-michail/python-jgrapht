
# python-jgrapht

A python interface to the [JGraphT](https://jgrapht.org/) graph library. 

JGraphT is a free Java class library that provides mathematical graph-theory objects and algorithms. It  contains
very efficient and generic graph data-structures along with a sizeable collection of sophisticated algorithms.
The library is written in Java, with stability, performance and interoperability in mind. It includes algorithms
encountered in diverse application domains such as  path planning, routing, network analysis, combinatorial
optimization, computational biology, and others.

While the original library is written in Java, this package uses a *native build* provided by
the [jgrapht-capi](https://github.com/d-michail/jgrapht-capi) project. The native build is in the form of a 
shared library, created by [GraalVM](https://www.graalvm.org/).

The result is a *native self-contained library* with no dependency on the JVM.

## Building

The jgrapht-capi project is included in the sources as a git submodule in folder `vendor/source/jgrapht-capi`.
You need to either initialize the submodule by hand, or you can pass option `--recurse-submodules` when 
cloning this repository.

The following pieces of software are required for the build to succeed:

 * GraalVM 20.0 with Java 11 support
 * Native Image component from GraalVM
 * Maven Java build tool
 * GNU C compiler or clang
 * CMake 
 * Python 3.6 and above
 * SWIG 3 and above

If all the above are installed properly, building should be as simple as 

```
python setup.py build
```

## Install

Install using 

```
pip install .
```

## Develop

Since the library contains parts which are written in C that need to be compiled before use, make sure you have 
the necessary compilers and development headers installed. Compiled code means that additional steps are required
in order to import from the development sources. Using the following commands you can setup an in-place development 
environment:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

This allows you to import the in-place build from the repository base directory. If you want it to 
also be visible outside the base dir, you have to adjust the `PYTHONPATH` accordingly.
Note also that the above commands call `python setup.py develop`. Instead of adjusting PYTHONPATH, this installs
a .egg-link file into your site-packages as well as adjusts the easy-install.pth there, so its a more permanent
operation.

## Tests

Execute the tests by giving

```
pytest
```

## Building the docs

```
pip install -r requirements/doc.txt
cd docs && make html
```

## License

This library may be used under the terms of either the

 * GNU Lesser General Public License (LGPL) 2.1
   http://www.gnu.org/licenses/lgpl-2.1.html

or the

 * Eclipse Public License (EPL)
   http://www.eclipse.org/org/documents/epl-v20.php

As a recipient, you may choose which license to receive the code under.
A copy of the [EPL license](license-EPL.txt) and the [LPGL license](license-LGPL.txt) is included in this repository.

Please note that this library is distributed WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Please refer to the license for details.

SPDX-License-Identifier: LGPL-2.1-or-later OR EPL-2.0

## Author

(C) Copyright 2020, by Dimitrios Michail


Enjoy!
