import os
import sys
import setuptools
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

if sys.version_info < (3, 4):
    raise Exception('jgrapht-python requires Python 3.3 or higher.')


_jgrapht_extension = Extension('_jgrapht', ['jgrapht/jgrapht.i', 'jgrapht/jgrapht.c'], 
                               include_dirs=['jgrapht/'],
                               library_dirs=['jgrapht/'], 
                               libraries=['jgrapht_capi'])

setup(
    name='python-jgrapht',
    cmdclass=custom_cmdclass,
    ext_modules=[_jgrapht_extension],
    version='0.1',
    description='JGraphT library',
    long_description='JGraphT library',
    author='Dimitrios Michail',
    author_email='dimitrios.michail@gmail.com',
    url='https://github.com/d-michail/python-jgrapht',
    license='MIT License',
    platforms=['any'],
    packages=setuptools.find_packages(),
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
    keywords='graphs, algorithms',
    python_requires='>=3.4'
)

