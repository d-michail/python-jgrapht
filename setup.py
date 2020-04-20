import os
import sys
import subprocess

import setuptools
from setuptools import setup
from setuptools.command.install import install

import distutils
from distutils.command.build import build
from distutils.cmd import Command
from distutils.core import Extension

class BuildConfig(object):
    """Global build configuration"""

    def __init__(self):
        self.libraries = []

    @property
    def build_capi(self):    
        """Return a command for building the jgraph-capi"""
        build_cfg = self

        class BuildCapiCommand(Command): 
            """A custom command to build the jgrapht-capi from source."""

            description = 'build jgrapht-capi'

            def initialize_options(self):
                pass

            def finalize_options(self):
                pass

            def run(self):
                build_cfg.is_capi_build = build_cfg.compile_capi('vendor/source/jgrapht-capi')
                #command = ['echo Hello']
                #self.announce('Running command: %s' % str(command), level=distutils.log.INFO)
                #subprocess.check_call(command)

        return BuildCapiCommand

    def compile_capi(self, source_folder):
        source_folder = os.path.abspath(source_folder)
        build_folder = os.path.join(source_folder, 'build')
        BuildConfig.create_dir_unless_exists(build_folder)

        cwd = os.getcwd()
        try: 
            os.chdir(build_folder)

            print("Configuring jgrapht-capi")
            retcode = subprocess.call('cmake ..', shell=True)
            if retcode:
                return False

            print("Build jgrapht-capi")
            retcode = subprocess.call('make', shell=True)
            if retcode:
                return False
        finally:
            os.chdir(cwd)

    @staticmethod
    def create_dir_unless_exists(dirname):
        """Creates a directory unless it exists already."""
        path = os.path.join(dirname)
        if not os.path.isdir(path):
            os.makedirs(path)

class CustomBuild(build):
    def run(self):
        self.run_command('build_capi')
        self.run_command('build_ext')
        build.run(self)

class CustomInstall(install):
    def run(self):
        self.run_command('build_ext')
        self.do_egg_install()

if sys.version_info < (3, 4):
    raise Exception('jgrapht-python requires Python 3.3 or higher.')


_jgrapht_extension = Extension('_jgrapht', ['jgrapht/jgrapht.i', 'jgrapht/jgrapht.c'], 
                               include_dirs=['jgrapht/'],
                               library_dirs=['jgrapht/'], 
                               libraries=['jgrapht_capi'])

build_config = BuildConfig()

setup(
    name='python-jgrapht',
    cmdclass={
        'build_capi': build_config.build_capi,
        'build': CustomBuild,
        'install': CustomInstall
    },
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

