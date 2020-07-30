[![Build Status](https://travis-ci.org/d-michail/python-jgrapht.svg?branch=master)](https://travis-ci.org/d-michail/python-jgrapht)

# Python-JGraphT

Python bindings for the  [JGraphT graph library](https://jgrapht.org/).

The JGraphT is a free Java class library that provides mathematical graph-theory objects and algorithms. It
contains very efficient and generic graph data-structures along with a sizeable collection of sophisticated
algorithms. The library is written with stability, performance and interoperability in mind. It includes
algorithms encountered in diverse application domains such as  path planning, routing, network analysis,
combinatorial optimization, computational biology, and others.

While the original library is written in Java, this package uses a *native build* provided by
the [jgrapht-capi](https://github.com/jgrapht/jgrapht-capi) project. The native build is in the form of a 
shared library, created by [GraalVM](https://www.graalvm.org/).

The result is a *native self-contained library* with *no dependency* on the JVM!

## Installing

We automatically build 64-bit wheels for python versions 3.6, 3.7, and 3.8 on Linux,
Windows and MacOSX. They can be directly downloaded from [PyPI](https://pypi.org/project/jgrapht/)
or using pip.
For linux we use [PEP 571](https://www.python.org/dev/peps/pep-0571/)
which means that pip version must be `>= 19.0`.

Thus, on a recent machine, installation should be as easy as:

```
pip install jgrapht
```

If your pip version is older than `19.0` you will need to upgrade: 

```
pip install --upgrade pip
pip install jgrapht
```

If you want to use `virtualenv` or `venv` module, you can write:

```
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install jgrapht
```

Installation on the user directory is also possible:

```
pip install --upgrade pip
pip install --user jgrapht
```

## Documentation 

Automatically generated documentation with a tutorial and examples can be found at 
<https://python-jgrapht.readthedocs.io/>. This includes full API docs, tutorials and examples.

## Citing

Are you using the software in your research? We would appreciate if you cite the following publication:

```
@article{jgrapht,
  title = {{J}{G}raph{T}--{A} {J}ava {L}ibrary for {G}raph {D}ata {S}tructures and {A}lgorithms},
  author = {Michail, Dimitrios and Kinable, Joris and Naveh, Barak and Sichi, John V.},
  year = {2020},
  issue_date = {May 2020},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  volume = {46},
  number = {2},
  journal = {ACM Trans. Math. Softw.},
  month = may,
  articleno = {16},
  numpages = {29},
}
```

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

If all the above are installed properly, building can be done using

```
python setup.py build
```

For Windows you will need Microsoft Visual C++ (MSVC) 2017 15.5.5 or later. Build the
system using the proper
[Developer Command Prompt](https://docs.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=vs-2019#developer_command_prompt_shortcuts)
for your version of [Visual Studio](https://visualstudio.microsoft.com/vs/). This means
`x64 Native Tools Command Prompt`. Use Visual Studio 2017 or later.

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
pip install -r requirements/test.txt
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
