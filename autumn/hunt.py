import google


def get_filetype(filetype):
    return _search("filetype:{}".format(filetype))


def _search(term):
    return google.search(term, num=50)
