import pytest
import vcr

import autumn.hunt

vcrconf = vcr.VCR(
    serializer='json',
    cassette_library_dir='tests/fixtures',
    record_mode='once',
    match_on=['uri', 'method']
)


@vcrconf.use_cassette()
@pytest.mark.parametrize("count", [1, 5, 10, 100, 1000, 50000])
def test_get_url_for_filetype_multiple_files(count):
    count = 5
    results = autumn.hunt.get_urls("pdf", count=count)
    assert sum(1 for x in results) == count
