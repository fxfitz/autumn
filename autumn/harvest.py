import hashlib
import io
import os.path
import requests
import shutil


def harvest(url, path, verify_certificate=True):
    base_path = os.path.expanduser(path)

    try:
        req = requests.get(url, verify=verify_certificate)
    except requests.exceptions.SSLError as e:
        raise e

    if not req.ok:
        return None

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
