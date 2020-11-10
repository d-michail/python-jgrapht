.. jgrapht documentation master file, created by
   sphinx-quickstart on Thu Apr 23 10:34:24 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The JGraphT library
===================

Release v\ |version|.

Python bindings for the `JGraphT graph library <https://jgrapht.org/>`_.

The JGraphT library is a highly efficient graph library, written in Java, containing
state-of-the-art graph data-structures as well as a multitude of sophisticated
graph algorithms. It has been in development for many years already and is currently used
in production both in research and industry. 

The |Bindings| is a pure python/native package having no dependency on the JVM. During the
build process the backend JGraphT library is compiled as a shared library and bundled
inside the python package.

Backend version v\ |BackendVersion|.

Audience
--------

The audience of the library is any user who needs to use graphs or networks in their every 
day work, including engineers and researchers either from the industry or academia.

Why another library?
--------------------

Well, this is not really a new library. This is just making a library cross boundaries between 
two different programming worlds.

Development
-----------

Development happens in the following places.

 * https://github.com/d-michail/python-jgrapht 
 * https://github.com/jgrapht/jgrapht-capi
 * https://github.com/jgrapht/jgrapht


Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: JGraphT

   install
   tutorials/index
   api/index
   license
   citing
   credits

.. toctree::
   :maxdepth: 2
   :caption: Example galleries

   auto_examples/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
