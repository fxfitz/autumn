import random

import google


def get_filetype(filetype):
    return _search("filetype:{}".format(filetype))


def _search(term):
    start = random.randint(1, 10000)
    return google.search(term, num=50, start=start)
