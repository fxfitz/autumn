import hashlib
import io
import os.path
import requests
import shutil


def harvest(url, path, verify_certificate=True):
    base_path = os.path.expanduser(path)

    req = requests.get(url, verify=verify_certificate)

    if not req.ok:
        message = "Request to URL ({}) was not OK (Status Code: {})"
        raise RuntimeError(message.format(url, req.status_code))

    content = io.BytesIO(req.content)
    content_sha1 = get_sha1(content)

    filename = os.path.join(base_path, '{}'.format(content_sha1))

    with open(filename, 'wb') as fd:
        content.seek(0)
        shutil.copyfileobj(content, fd)

    return filename


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
