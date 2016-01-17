import requests

import autumn.scour


def test_get_url_for_filetype():
    results = autumn.scour.get_filetype("pdf")
    assert len(results) == 1


def test_get_url_for_filetype_multiple_files():
    count = 5
    results = autumn.scour.get_filetype("pdf", count=count)
    assert len(results) == count


def test_get_url_returns_valid_url():
    results = autumn.scour.get_filetype("pdf")
    assert requests.head(results[0]).status_code == 200
