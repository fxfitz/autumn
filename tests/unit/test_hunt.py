import types

import google
import pytest  # NOQA

import autumn.hunt

from tests.util import vcrconf, _fake_generator


@vcrconf.use_cassette()
def test_get_filetype_returns_generator(monkeypatch):
    monkeypatch.setattr(google, "search", _fake_generator)
    results = autumn.hunt.get_filetype('pdf')
    assert isinstance(results, types.GeneratorType)
