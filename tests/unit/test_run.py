import pytest

import autumn.cmd.run
import tests.util


def test_prints_counts_for_filetype(monkeypatch):
    monkeypatch.setattr(autumn.hunt, "_search", tests.util._fake_generator)
    with tests.util.override_argv(
        '--count', '10',
        '--filetype', 'pdf',
    ):
        assert autumn.cmd.run.main() == 0


@tests.util.vcrconf.use_cassette()
def test_downloads_files(monkeypatch, tmpdir):  # NOQA
    monkeypatch.setattr(autumn.hunt, "_search", tests.util._fake_generator)
    with tests.util.override_argv(
        '--count', '10',
        '--filetype', 'pdf',
        '--path', str(tmpdir),
    ):
        assert autumn.cmd.run.main() == 0


@tests.util.vcrconf.use_cassette()
def test_ignores_exceptions_and_moves_on(monkeypatch, tmpdir):
    monkeypatch.setattr(autumn.hunt, "_search", _fake_generator_url_errors)
    with tests.util.override_argv(
        '--count', '5',
        '--filetype', 'pdf',
        '--path', str(tmpdir),
    ):
        assert autumn.cmd.run.main() == 0


@tests.util.vcrconf.use_cassette()
def test_for_stopiteration(monkeypatch, tmpdir):
    monkeypatch.setattr(autumn.hunt, "_search", _fake_generator_url_errors)
    with tests.util.override_argv(
        '--count', '20',
        '--filetype', 'pdf',
        '--path', str(tmpdir),
    ):
        assert autumn.cmd.run.main() == -1


def test_for_valid_directories(capsys):
    fakedir = 'this_is_the_most_fake_directory_ever'
    with tests.util.override_argv(
        '--count', '10',
        '--filetype', 'pdf',
        '--path', fakedir
    ), pytest.raises(SystemExit):
            autumn.cmd.run.main()

    out, err = capsys.readouterr()
    assert "{} is not a directory".format(fakedir) in err


def _fake_generator_url_errors(*args, **kwargs):
    yield('https://www.google.com')
    yield('https://fejapjk')
    yield('https://fejapjk.net')
    yield('https://www.omfieapjthidoesntexistatallomghaha.com')
    yield('https://www.google.com')
    yield('https://www.google.com')
    yield('https://www.google.com')
    yield('https://www.google.com')
