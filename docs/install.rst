.. _install:

Install
=======

We automatically build 64-bit wheels for python versions 3.6, 3.7, and 3.8 on Linux,
Windows and MacOSX. Thus, on a recent machine, installation should be as easy as::

  $ pip install pip --upgrade
  $ pip install jgrapht

Just make sure you have a recent version of pip installed. If you want to use 
`virtualenv` or `venv` module, you can easily write::

  $ python -m venv venv
  $ source venv/bin/activate
  $ pip install pip --upgrade
  $ pip install jgrapht

Installation in the user directory is also possible::

  $ pip install --user jgrapht

