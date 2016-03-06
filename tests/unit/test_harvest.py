import os
import os.path
import pytest
import shutil
import tempfile

import requests

import autumn.harvest
import autumn.hunt
from autumn.harvest import harvest


@pytest.fixture(scope='function')
def tempdir(request):
    # NOTE(fxfitz): In py34, using the tempfile.TemporaryDirectory()
    # context manager would probably be best instead of doing it this
    # way, but it looks like it was never backported to py27 :-(
    dirpath = tempfile.mkdtemp()

    def cleanup():
        shutil.rmtree(dirpath)

    request.addfinalizer(cleanup)
    return dirpath


def test_get_sha1():
    test_file = 'tests/fixtures/sha1_test.txt'
    known_sha1 = '9d9aecd30e523986aa2c6ad05e08f91ae86dfbfb'

    with open(test_file, 'rb') as fd:
        assert autumn.harvest.get_sha1(fd) == known_sha1


def test_harvest_returns_none_if_response_is_not_ok(tempdir, monkeypatch):
    monkeypatch.setattr(requests, 'get',
                        lambda *args, **kwargs: FakeResponse(False))

    url = "http://www.somefakewebsitethatdoesntexist.com/fjoeijfa.pdf"
    result = harvest(url, tempdir)

    assert result is None


def test_harvest__downloads_and_names_file_as_sha1(tempdir, monkeypatch):
    test_file = 'tests/fixtures/sha1_test.txt'
    known_sha1 = '9d9aecd30e523986aa2c6ad05e08f91ae86dfbfb'
    with open(test_file) as test:
        content = test.read().encode('utf-8')
        monkeypatch.setattr(requests, 'get',
                            lambda *a, **kw: FakeResponse(content=content))

        url = "http://www.oursamplepdf.com/"
        result = harvest(url, tempdir)

        assert result == os.path.join(tempdir, known_sha1)


def test_harvest_verifies_certificates(tempdir, monkeypatch):
    def cert_verify_failed():
        raise requests.exceptions.SSLError
    monkeypatch.setattr(requests, 'get', lambda *a, **k: cert_verify_failed())

    with pytest.raises(requests.exceptions.SSLError):
        harvest("https://www.evilwebsite.com", tempdir)


class FakeResponse(object):

    def __init__(self, ok=True, content=None):
        self.ok = ok
        self.content = content
