pyenv global 3.8.0-amd64
pyenv exec python -m pip install -U pip
pyenv exec python -m pip install twine
pyenv exec python -m twine --version
pyenv exec python -m twine upload --username "${PYPI_USER:-__token__}" --password "$PYPI_PASSWORD" dist/*

