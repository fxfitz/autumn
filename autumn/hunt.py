import google


def get_urls(filetype, count=1):
    res = google.search("filetype:{}".format(filetype),
                        num=count,
                        stop=count)
    return res
