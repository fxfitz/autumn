import types

import pytest  # NOQA

import autumn.hunt

from tests.util import vcrconf


@vcrconf.use_cassette()
def test_get_filetype_returns_generator():
    results = autumn.hunt.get_filetype('pdf')
    assert isinstance(results, types.GeneratorType)
