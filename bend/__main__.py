import argparse
import pathlib

from . import jbend
from . import copy_header
from . import version

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='store_true')
    subparsers = parser.add_subparsers()

    parser_jpeg = subparsers.add_parser('jpg')
    parser_jpeg.add_argument('infile', type=pathlib.Path)
    parser_jpeg.add_argument('outfile', type=pathlib.Path)
    parser_jpeg.add_argument('-m', type=int, default=0, dest='magnitude')
    parser_jpeg.set_defaults(func=jbend.main)

    parser_cphdr = subparsers.add_parser('cphdr')
    parser_cphdr.add_argument('source', type=pathlib.Path)
    parser_cphdr.add_argument('target', type=pathlib.Path, nargs='+')
    parser_cphdr.set_defaults(func=copy_header.main)

    args = parser.parse_args()

    if args.version:
        version.print_version()
        exit(1)

    if not hasattr(args, 'func'):
        parser.print_usage()
        exit(1)
    args.func(args)

if __name__ == '__main__':
    main()