#!/usr/bin/env python3
import sys

from page_loader.engine import page_load
from page_loader.logger import LOGGER, KnownError


def arg_parse():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('url', type=str, help='')
    parser.add_argument(
        '-l',
        '--log',
        help='',
        type=str,
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        default='info'
    )
    parser.add_argument(
        '-o',
        '--output',
        help='',
        type=str,
        default='./'
    )
    args = parser.parse_args()
    return args


def main():
    args = arg_parse()
    LOGGER.setLevel(args.log.upper())
    LOGGER.info('downloading started')
    try:
        page_load(args.output, args.url)
    except KnownError:
        sys.exit(1)
    else:
        LOGGER.info('downloading finished')
        sys.exit(0)


if __name__ == '__main__':
    main()
