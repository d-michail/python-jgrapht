import sys
if sys.version_info < (3, 6):
    raise Exception('Building jgrapht requires Python 3.6 or higher.')
import os
import codecs

import setuptools
from setuptools import setup
from setuptools import Command
from setuptools import Extension
from setuptools.command.build_ext import build_ext

from distutils.command.build import build

extra_link_args = []
runtime_library_dirs = []

if sys.platform.startswith('win32'):
    so_ext = '.dll'
    capi_filename = 'jgrapht_capi' + so_ext
if sys.platform.startswith('linux'):
    so_ext = '.so'
    capi_filename = 'libjgrapht_capi' + so_ext
    # Make sure that _backend.so will be able to load jgrapht_capi.so
    runtime_library_dirs=['$ORIGIN']
elif sys.platform.startswith('darwin'):
    so_ext = '.dylib'
    capi_filename = 'libjgrapht_capi' + so_ext
    extra_link_args = ['-Wl,-rpath,@loader_path']


class BuildCapiCommand(Command):
    """A custom command to build the jgrapht-capi from source."""

    description = 'build jgrapht-capi'

    def initialize_options(self):
        self.build_lib = None
        self.inplace = 0

        self.src_dir = None
        self.build_dir = None
        self.package_name = None
        self.filename = None

    def finalize_options(self):
        self.set_undefined_options('build',
                                   ('build_lib', 'build_lib'),
                                   )
        self.set_undefined_options('build_ext',
                                   ('inplace', 'inplace'),
                                   )
        self.src_dir = os.path.join('vendor', 'source', 'jgrapht-capi')
        self.build_dir = os.path.join('vendor', 'build', 'jgrapht-capi')
        self.package_name = 'jgrapht'
        self.filename = capi_filename

    def run(self):
        """Compile the jgrapht-capi from the git submodule inside `vendor/source/jgrapht-capi`."""

        # Because setuptools develop command reinitializes the build_ext command with
        # inplace=1 without also reinitializing its subcommands, we need to update
        # the inplace option every time we run
        self.inplace = self.get_finalized_command('build_ext').inplace
        if not os.path.isfile(os.path.join(self.src_dir, "CMakeLists.txt")):
            # No git submodule present with vendored source
            print("Cannot find source in " + self.src_dir)
            print("Make sure that you recursively checkout the submodule")
            print("")
            return False
        print("Found source at {}".format(self.src_dir))
        # Additional CMake parameters should be set as environment variables
        # before calling setup.py depending on the platform and toolchain.
        self.spawn(['cmake', '-B{}'.format(self.build_dir), '-H{}'.format(self.src_dir)])
        self.spawn(['cmake', '--build', self.build_dir])
        lib_source_path = os.path.join(self.build_dir, self.filename)
        # inplace will is set to 1 when the develop command runs.
        # Copy the JgraphT C API directly to the development area
        if self.inplace:
            lib_target_path = self.package_name
        else:
            lib_target_path = os.path.join(self.build_lib, self.package_name)
            self.mkpath(lib_target_path)
        self.copy_file(lib_source_path, os.path.join(lib_target_path, self.filename))


class CustomBuild(build):
    # Because by default distutils build_py runs before build_ext and misses the SWIG
    # generated .py file(s) we need to reorder the sub_commands to something sensible
    sub_commands = [('build_clib', build.has_c_libraries),
                    ('build_ext', build.has_ext_modules),
                    ('build_py', build.has_pure_modules),
                    ('build_scripts', build.has_scripts),
                    ]


class CustomBuildExt(build_ext):
    # I wish this was used more by distutils, but setting it anyway
    sub_commands = [('build_capi', None),
                    ]

    def run(self):
        self.run_command('build_capi')
        super().run()

_backend_extension = Extension('jgrapht._backend', ['jgrapht/backend.i','jgrapht/backend.c'],
                               include_dirs=['jgrapht/', 'vendor/build/jgrapht-capi/', 'vendor/build/jgrapht-capi/src/main/native'],
                               library_dirs=['vendor/build/jgrapht-capi/'],
                               libraries=['jgrapht_capi'],
                               runtime_library_dirs=runtime_library_dirs,
                               extra_link_args=extra_link_args,
                               )

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='jgrapht',
    cmdclass={
        'build_capi': BuildCapiCommand,
        'build_ext': CustomBuildExt,
        'build': CustomBuild,
    },
    ext_modules=[_backend_extension],
    version=get_version('jgrapht/__version__.py'),
    description='JGraphT graph library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Dimitrios Michail',
    author_email='dimitrios.michail@gmail.com',
    url='https://github.com/d-michail/python-jgrapht',
    license='LGPL-2.1-or-later OR EPL-2.0',
    platforms=['any'],
    packages=setuptools.find_packages(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries'
    ],
    keywords='graphs,networks,data-structures,algorithms',
    python_requires='>=3.6'
)
