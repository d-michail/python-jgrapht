.. _install:

Install
=======

We automatically build 64-bit wheels for python versions 3.6, 3.7, and 3.8 on Linux,
Windows and MacOSX. For linux we use `PEP 571 <https://www.python.org/dev/peps/pep-0571/>`_
which means that pip version must be ``>= 19.0``. 

Thus, on a recent machine, installation should be as easy as::

  $ pip install jgrapht

If your pip version is older than 19.0 use:: 

  $ pip install --upgrade pip
  $ pip install jgrapht

If you want to use `virtualenv` or `venv` module::

  $ python -m venv venv
  $ source venv/bin/activate
  $ pip install --upgrade pip
  $ pip install jgrapht

Installation in the user directory is also possible::

  $ pip install --user jgrapht

