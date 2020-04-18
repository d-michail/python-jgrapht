import os
import sys
from setuptools import setup
from distutils.core import Extension

# Make sure SWIG runs before installing the generated files.
# http://stackoverflow.com/questions/12491328/python-distutils-not-include-the-swig-generated-module
from setuptools.command.install import install
from distutils.command.build import build
class CustomBuild(build):
    def run(self):
        self.run_command('build_ext')
        build.run(self)
class CustomInstall(install):
    def run(self):
        self.run_command('build_ext')
        self.do_egg_install()
custom_cmdclass = {'build': CustomBuild, 'install': CustomInstall}

if sys.version_info < (3, 3):
    raise Exception('jgrapht-python requires Python 3.3 or higher.')

# This is quite the hack, but we don't want to import our package from here
# since that's recipe for disaster (it might have some uninstalled
# dependencies, or we might import another already installed version).
distmeta = {}
for line in open(os.path.join('jgrapht', '__init__.py')):
    try:
        field, value = (x.strip() for x in line.split('='))
    except ValueError:
        continue
    value = value.strip('\'"')
    distmeta[field] = value

distmeta['__version__'] = '0.1'
distmeta['__version_info__'] = ('0','1')

setup(
    name='python-jgrapht',
    cmdclass=custom_cmdclass,
    ext_modules=[Extension('_jgrapht', ['jgrapht/jgrapht.i', 'jgrapht/jgrapht.c'])],
    version=distmeta['__version__'],
    description='JGraphT library',
    long_description='JGraphT library',
    author='Dimitrios Michail',
    author_email='dimitrios.michail@gmail.com',
    url='https://github.com/d-michail/python-jgrapht',
    license='MIT License',
    platforms=['any'],
    packages=['jgrapht'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering',
    ],
    keywords='graphs, algorithms'
#    ,
#    install_requires=['biopython',
#                      'crossmapper==0.0.1'],
#    dependency_links=[
#        'https://github.com/mutalyzer/crossmapper/archive/v0.0.1.tar.gz#egg=crossmapper-0.0.1'
#    ]
)

