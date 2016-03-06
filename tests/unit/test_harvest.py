import os
import os.path
import pytest

import requests

import autumn.harvest
import autumn.hunt
from autumn.harvest import harvest


def test_get_sha1():
    test_file = 'tests/fixtures/sha1_test.txt'
    known_sha1 = '9d9aecd30e523986aa2c6ad05e08f91ae86dfbfb'

    with open(test_file, 'rb') as fd:
        assert autumn.harvest.get_sha1(fd) == known_sha1


def test_harvest_raises_error_if_response_is_not_ok(tmpdir, monkeypatch):
    monkeypatch.setattr(requests, 'get',
                        lambda *args, **kwargs: FakeResponse(False))

    url = "http://www.somefakewebsitethatdoesntexist.com/fjoeijfa.pdf"

    with pytest.raises(RuntimeError):
        harvest(url, str(tmpdir))


def test_harvest_downloads_and_names_file_as_sha1(tmpdir, monkeypatch):
    test_file = 'tests/fixtures/sha1_test.txt'
    known_sha1 = '9d9aecd30e523986aa2c6ad05e08f91ae86dfbfb'
    with open(test_file) as test:
        content = test.read().encode('utf-8')
        monkeypatch.setattr(requests, 'get',
                            lambda *a, **kw: FakeResponse(content=content))

        url = "http://www.oursamplepdf.com/"
        result = harvest(url, str(tmpdir))

        assert result == os.path.join(str(tmpdir), known_sha1)


def test_harvest_verifies_certificates(tmpdir, monkeypatch):
    def cert_verify_failed():
        raise requests.exceptions.SSLError
    monkeypatch.setattr(requests, 'get', lambda *a, **k: cert_verify_failed())

    with pytest.raises(requests.exceptions.SSLError):
        harvest("https://www.evilwebsite.com", str(tmpdir))


class FakeResponse(object):

    def __init__(self, ok=True, content=None, status_code=200):
        self.ok = ok
        self.status_code = status_code
        self.content = content
