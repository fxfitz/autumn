import autumn


def test_version_is_available():
    from autumn import __version__ as test_version
    assert autumn.__version__ == test_version
