import jgrapht


def test_version_metadata():
    assert jgrapht.__version__
    assert jgrapht.__backend_version__
