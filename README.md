
# python-jgrapht

Python interface for JGraphT

## Build

```
python3 setup.py build_ext
python3 setup.py install
```

## Install

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
python setup.py build -i
```


