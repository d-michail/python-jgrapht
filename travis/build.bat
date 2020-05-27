call "C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
:: Set the generator to VS 2017 and target architecture to x64
SET CMAKE_GENERATOR=Visual Studio 15 2017 Win64
:: Set the host architecture to x64, by default CMake selects x86
SET CMAKE_GENERATOR_TOOLSET=host=x64

:: Build, install and test 64-bit wheels for all supported Python versions
FOR %%P IN (3.6.8 3.7.5 3.8.0) DO (
    pyenv global %%P-amd64
    pyenv exec python --version
    pyenv exec python -m pip install -U pip
    pyenv exec python -m pip install pytest wheel
    pyenv exec python setup.py bdist_wheel
    pyenv exec python -m pip install jgrapht --no-index -f dist
    pyenv exec Scripts\pytest
)
