import requests

import vcr

import autumn.hunt

vcrconf = vcr.VCR(
    serializer='json',
    cassette_library_dir='tests/fixtures',
    record_mode='once',
    match_on=['uri', 'method']
)


@vcrconf.use_cassette()
def test_get_url_for_filetype():
    results = autumn.hunt.get_filetype("pdf")
    assert sum(1 for x in results) == 1


@vcrconf.use_cassette()
def test_get_url_for_filetype_multiple_files():
    count = 5
    results = autumn.hunt.get_filetype("pdf", count=count)
    assert sum(1 for x in results) == count


@vcrconf.use_cassette()
def test_get_url_returns_valid_url():
    results = autumn.hunt.get_filetype("pdf")
    result = next(results)
    assert requests.head(result,
                         allow_redirects=True,
                         verify=False).status_code == 200
