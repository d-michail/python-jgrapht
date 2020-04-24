import os
import sys
import subprocess

import setuptools
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist

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
                build_cfg.is_capi_build = build_cfg._compile_capi()

        return BuildCapiCommand

    @property
    def build_ext(self):    
        """Return a custom build_ext"""
        build_cfg = self

        class CustomBuildExt(build_ext): 
            """A custom build_ext."""

            def run(self):
                # first run the build_cpi
                self.run_command('build_capi')

                # Run the original build_ext command
                build_ext.run(self) 

                # Install the build_capi in the build/ dir

                if not self.dry_run:
                    print('Original install directory: {}'.format(self.build_lib))

                    # mkpath is a distutils helper to create directories
                    self.mkpath(self.build_lib)

                    capi_lib = 'libjgrapht_capi.so'
                    capi_build_folder = os.path.join('vendor', 'build', 'jgrapht-capi')
                    capi_source = os.path.join(capi_build_folder, capi_lib)
                    capi_target = os.path.join(self.build_lib, capi_lib)
                    outf, copied = self.copy_file(capi_source, capi_target)
                    outf, copied = self.copy_file(capi_source, '.')


        return CustomBuildExt

    @property
    def build_py(self):    
        """Return a custom build_py"""
        build_cfg = self

        class CustomBuildPy(build_py): 
            """A custom build_py."""

            def run(self):
                # first run the build_ext
                self.run_command('build_ext')

                # run the original
                build_py.run(self) 

        return CustomBuildPy

    @property
    def install(self):
        build_cfg = self

        class CustomInstall(install):
            def run(self):
                self.run_command('build_py')
                self.do_egg_install()

        return CustomInstall

    @property
    def build(self):
        build_cfg = self

        class CustomBuild(build):
            def run(self):
                self.run_command('build_py')    
                build.run(self)

        return CustomBuild

    @property
    def sdist(self):
        """`sdist` which first cleans up submodule."""
        buildcfg = self

        class CustomSDist(sdist):
            def run(self):
                # Clean up vendor/source/jgrapht-capi with git
                print("Cleaning up vendor source")
                cwd = os.getcwd()
                try:
                    os.chdir(os.path.join("vendor", "source", "jgrapht-capi"))
                    if os.path.exists(".git"):
                        retcode = subprocess.call("git clean -dfx", shell=True)
                        if retcode:
                            print("Failed to clean vendor/source/jgrapht-capi with git")
                            print("")
                            return False
                finally:
                    os.chdir(cwd)

                # Run the original sdist command
                sdist.run(self)

        return CustomSDist

    def _compile_capi(self):
        """Compile the jgrapht-capi from the git submodule inside `vendor/source/jgrapht-capi`."""

        source_folder = os.path.join("vendor", "source", "jgrapht-capi")
        source_folder = os.path.abspath(source_folder)
        if not os.path.isfile(os.path.join(source_folder, "CMakeLists.txt")):
            # No git submodule present with vendored source
            print("Cannot find source in " + source_folder)
            print("Make sure that you recursively checkout the submodule")
            print("")
            return False
        print("Found source at {}".format(source_folder))

        build_folder = os.path.join("vendor", "build", "jgrapht-capi")
        build_folder = os.path.abspath(build_folder)
        BuildConfig.create_dir_unless_exists(build_folder)

        cwd = os.getcwd()
        try: 
            os.chdir(build_folder)

            print("Configuring jgrapht-capi")
            retcode = subprocess.call('cmake {}'.format(source_folder), shell=True)
            if retcode:
                return False

            print("Build jgrapht-capi")
            print("Using build folder at {}".format(build_folder))
            retcode = subprocess.call('make', shell=True)
            if retcode:
                return False

            return True

        finally:
            os.chdir(cwd)

    @staticmethod
    def create_dir_unless_exists(dirname):
        """Creates a directory unless it exists already."""
        path = os.path.join(dirname)
        if not os.path.isdir(path):
            os.makedirs(path)

    @staticmethod
    def create_env(**kwargs):
        env = os.environ.copy()
        for k, v in kwargs.items():
            prev = os.environ.get(k)
            env[k] = "{0} {1}".format(prev, v) if prev else v
        return env        


if sys.version_info < (3, 5):
    raise Exception('jgrapht-python requires Python 3.5 or higher.')


_jgrapht_extension = Extension('_jgrapht', ['jgrapht/jgrapht.i','jgrapht/jgrapht.c'], 
                               include_dirs=['jgrapht/', 'vendor/build/jgrapht-capi/'],
                               library_dirs=['jgrapht/', 'vendor/build/jgrapht-capi/'], 
                               libraries=['jgrapht_capi']
                               )


build_config = BuildConfig()

setup(
    name='python-jgrapht',
    cmdclass={
        'build_capi': build_config.build_capi,
        'build_ext': build_config.build_ext,
        'build_py': build_config.build_py,
        'build': build_config.build,
        'install': build_config.install,
        'sdist': build_config.sdist
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

