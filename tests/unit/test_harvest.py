import magic
import os
import os.path
import pytest
import shutil
import tempfile

import autumn.harvest
from autumn.harvest import harvest
import tests.util


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


@tests.util.vcrconf.use_cassette()
def test_harvest_returns_list(tempdir):
    filetype = 'pdf'
    count = 1
    results = harvest(filetype, tempdir, count)

    assert isinstance(results, list)


@tests.util.vcrconf.use_cassette()
def test_harvest_returns_list_of_proper_size(tempdir):
    # TODO: Maybe use pytest parameterize to test different counts
    filetype = 'pdf'
    count = 3
    results = harvest(filetype, tempdir, count)

    assert len(results) == count


@tests.util.vcrconf.use_cassette()
def test_harvest_returns_sha1_filenames(tempdir):
    filetype = 'pdf'
    count = 1
    results = harvest(filetype, tempdir, count)

    with open(results[0], 'rb') as fd:
        sha1 = autumn.harvest.get_sha1(fd)

    expected = os.path.join(tempdir, '{}.{}'.format(sha1, filetype))

    assert results[0] == expected


def test_harvest_only_returns_correct_filetype(tempdir):
    filetype = 'pdf'
    count = 3
    results = harvest(filetype, tempdir, count)

    for path in results:
        with magic.Magic() as m:
            assert filetype.lower() in m.id_filename(path).lower()


def test_get_sha1():
    test_file = 'tests/fixtures/sha1_test.txt'
    known_sha1 = '9d9aecd30e523986aa2c6ad05e08f91ae86dfbfb'

    with open(test_file, 'rb') as fd:
        assert autumn.harvest.get_sha1(fd) == known_sha1
