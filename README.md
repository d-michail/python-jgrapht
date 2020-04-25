
# python-jgrapht

Python interface for JGraphT

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
pip install -e .
```

This allows you to import the in-place build from the repository base directory. If you want it to 
also be visible outside the base dir, you have to adjust the `PYTHONPATH` accordingly.

Note that another way to do an inplace build visible outside the repo base dir is with python setup.py develop. Instead of adjusting PYTHONPATH, this installs a .egg-link file into your site-packages as well as adjusts the easy-install.pth there, so its a more permanent operation.

### Tests

Execute the tests by giving

```
pytest tests/
```

Enjoy!
