# pip requirements files

## Index

- [`default.txt`](default.txt)
  Default requirements
- [`test.txt`](test.txt)
  Requirements for running test suite
- [`optional.txt`](optional.txt)
  Optional requirements for integration with other libraries
- [`doc.txt`](doc.txt)
  Requirements for building the documentation (see `../doc/`)
- [`release.txt`](release.txt)
  Requirements for making releases

## Examples

### Installing requirements

```bash
$ pip install -U -r requirements/default.txt
```

### Running the tests

```bash
$ pip install -U -r requirements/default.txt
$ pip install -U -r requirements/test.txt
```

### Running the tests including optional integration

```bash
$ pip install -U -r requirements/default.txt
$ pip install -U -r requirements/test.txt
$ pip install -U -r requirements/optional.txt
```


