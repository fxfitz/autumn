import hashlib
import io
import magic
import os.path
import requests
import shutil

import autumn.hunt


def harvest(filetype, path, count):
    files_downloaded = []
    base_path = os.path.expanduser(path)

    urls = autumn.hunt.get_filetype(filetype)

    while len(files_downloaded) < count:
        req = requests.get(next(urls))
        if not req.ok:
            continue

        content = io.BytesIO(req.content)
        content_sha1 = get_sha1(content)

        if not _correct_filetype(content, filetype):
            continue

        filename = os.path.join(base_path,
                                '{}.{}'.format(content_sha1, filetype))

        with open(filename, 'wb') as fd:
            content.seek(0)
            shutil.copyfileobj(content, fd)

        files_downloaded.append(filename)

    return files_downloaded


def get_sha1(stream):
    buf_size = 65536
    hasher = hashlib.sha1()

    start = stream.tell()
    stream.seek(0)

    buf = stream.read(buf_size)
    while len(buf) > 0:
        hasher.update(buf)
        buf = stream.read(buf_size)

    stream.seek(start)

    return hasher.hexdigest()


def _correct_filetype(stream, desired_filetype):
    start = stream.tell()

    stream.seek(0)
    with magic.Magic() as m:
        magic_filetype = m.id_buffer(stream.read())
    stream.seek(start)

    # NOTE: Is there a better way to do this? Will this work with all
    # filetypes? :-(
    return desired_filetype.lower() in magic_filetype.lower()
