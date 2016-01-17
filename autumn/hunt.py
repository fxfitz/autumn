import google


def get_filetype(filetype, count=1):
    res = google.search("filetype:{}".format(filetype),
                        num=count,
                        stop=count)
    return res
