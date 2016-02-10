import vcr

vcrconf = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='tests/fixtures/cassettes',
    record_mode='once',
    match_on=['method']
)

HARVEST_PATH = 'tests/fixtures/harvester'
