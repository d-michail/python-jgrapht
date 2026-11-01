"""Guards against the public API, ``__all__`` and the documentation drifting apart."""

import pathlib
import re

import jgrapht as jg

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs" / "api"


def documented_in(module):
    """The names documented with ``autofunction``, ``autoclass`` or ``autoexception`` under a
    ``currentmodule`` directive naming ``module``."""
    names = set()
    for rst in DOCS.rglob("*.rst"):
        current = None
        for line in rst.read_text().splitlines():
            m = re.match(r"^\.\. currentmodule:: (\S+)", line)
            if m:
                current = m.group(1)
            m = re.match(r"^\.\. auto(?:function|class|exception):: (\w+)", line)
            if m and current == module:
                names.add(m.group(1))
    return names


def documented_names():
    return documented_in("jgrapht")


def test_all_names_exist():
    assert jg.__all__ == sorted(jg.__all__)
    assert len(jg.__all__) == len(set(jg.__all__))
    for name in jg.__all__:
        assert hasattr(jg, name), name


def test_core_names_are_exported():
    for name in ("Graph", "SparseGraph", "GraphPath", "GraphError", "shortest_path", "Matching"):
        assert name in jg.__all__


def test_every_public_name_is_documented():
    missing = sorted(set(jg.__all__) - documented_names())
    assert not missing, f"public but not in docs/api/*.rst: {missing}"


def test_documentation_only_mentions_existing_names():
    unknown = sorted(documented_names() - set(jg.__all__))
    assert not unknown, f"documented but not exported: {unknown}"


def test_every_public_callable_has_a_docstring():
    undocumented = [
        n for n in jg.__all__ if callable(getattr(jg, n)) and not (getattr(jg, n).__doc__ or "").strip()
    ]
    assert not undocumented, undocumented


def test_submodules_are_documented():
    import importlib

    for module in ("jgrapht.drawing", "jgrapht.convert"):
        mod = importlib.import_module(module)
        assert sorted(mod.__all__) == sorted(documented_in(module)), module
        for name in mod.__all__:
            assert (getattr(mod, name).__doc__ or "").strip(), f"{module}.{name}"
