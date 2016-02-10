import os
import os.path
import tempfile

import autumn.harvest
from autumn.harvest import harvest
import tests.util


@tests.util.vcrconf.use_cassette()
def test_harvest_returns_list():
    filetype = 'pdf'
    count = 1
    results = harvest(filetype,
                      tempfile.gettempdir(),
                      count)

    assert isinstance(results, list)


@tests.util.vcrconf.use_cassette()
def test_harvest_returns_list_of_proper_size():
    # TODO: Maybe use pytest parameterize to test lots of different counts
    filetype = 'pdf'
    count = 3
    results = harvest(filetype,
                      tempfile.gettempdir(),
                      count)

    assert len(results) == count


@tests.util.vcrconf.use_cassette()
def test_harvest_returns_sha1_filenames():
    filetype = 'pdf'
    count = 1
    results = harvest(filetype, tempfile.gettempdir(), count)

    with open(results[0], 'rb') as fd:
        sha1 = autumn.harvest.get_sha1(fd)

    expected = os.path.join(tempfile.gettempdir(),
                            '{}.{}'.format(sha1, filetype))

    assert results[0] == expected


def test_get_sha1():
    test_file = 'tests/fixtures/sha1_test.txt'
    known_sha1 = '9d9aecd30e523986aa2c6ad05e08f91ae86dfbfb'

    with open(test_file, 'rb') as fd:
        assert autumn.harvest.get_sha1(fd) == known_sha1
