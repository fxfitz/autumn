import contextlib
import sys

import six
import vcr

vcrconf = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='tests/fixtures/cassettes',
    record_mode='once',
    match_on=['method']
)


@contextlib.contextmanager
def override_argv(*args):
    if not all(isinstance(arg, six.string_types) for arg in args):
        raise TypeError('All args must be strings')

    old_argv, sys.argv = sys.argv, sys.argv[:1] + list(args)

    try:
        yield
    finally:
        sys.argv = old_argv


def _fake_generator(*args, **kwargs):
    while True:
        yield("https://www.google.com")
