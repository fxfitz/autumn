from __future__ import print_function

import argparse
import os
from six.moves import range

import autumn.hunt
import autumn.harvest


def main():
    args = _parse_args()
    path = getattr(args, "path", None)
    urls = autumn.hunt.get_filetype(args.filetype)

    if path is None:
        for x in range(args.count):
            print(next(urls))
    else:
        files_downloaded = 0
        while files_downloaded != args.count:
            try:
                result = autumn.harvest.harvest(next(urls), path, args.verify)
            except StopIteration:
                return -1
            except Exception:
                continue
            files_downloaded = files_downloaded + 1
            print(result)

    return 0


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--count', required=True, type=int,
                        help="The amount of files to harvest")
    parser.add_argument('-t', '--filetype', required=True,
                        help="The filetype to search for")
    parser.add_argument('-p', '--path', action=_FullPaths, type=_is_dir,
                        help="Download path")
    parser.add_argument('--disable-verification',
                        help="Disables SSL/TLS certification verification",
                        action='store_false',
                        default=True,
                        dest='verify')

    return parser.parse_args()


class _FullPaths(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(
            os.path.expanduser(values)))


def _is_dir(dirname):
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname
