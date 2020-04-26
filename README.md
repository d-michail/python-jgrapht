
# python-jgrapht

A python interface to the JGraphT graph library. The JGraphT graph library is originally written 
in Java, but this package includes it as a natively compiled shared library.

## Build

```
python3 setup.py build
```

## Install

```
python3 setup.py install
```

or

```
pip install .
```

## Develop

Since the library contains parts which are written in C that need to be compiled before use, make sure you have 
the necessary compilers and development headers install. Compiled code means that additional steps are required
in order to import from the development sources. 

### Building in-place

For development you need to run: 

```
python3 -m env venv
source venv/bin/activate
pip install -r requirements.txt
```

or
```
python3 -m env venv
source venv/bin/activate
python3 setup.py develop
```

This allows you to import the in-place build from the repository base directory. If you want it to 
also be visible outside the base dir, you have to adjust the `PYTHONPATH` accordingly.

Note that another way to do an inplace build visible outside the repo base dir is with python setup.py develop. Instead of adjusting PYTHONPATH, this installs a .egg-link file into your site-packages as well as adjusts the easy-install.pth there, so its a more permanent operation.

### Tests

Execute the tests by giving

```
pytest tests/
```

## Requirements 

The build will succeed only if you have the following piece of software installed:

 * GraalVM 20.0 with Java 11 support
 * Native Image component from GraalVM
 * Maven build tool
 * GNU C compiler or clang
 * Python 3.5 and above

For now only Linux has been tested.

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
