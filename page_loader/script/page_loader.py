#!/usr/bin/env python3
import sys
import logging
import argparse

from page_loader.engine import load_page
from page_loader.logging import KnownError


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
    logger = logging.getLogger()
    args = arg_parse()
    logger.setLevel(args.log.upper())
    logger.info('downloading started')
    try:
        load_page(args.output, args.url)
    except KnownError:
        sys.exit(1)
    else:
        logger.info('downloading finished')
        sys.exit(0)


if __name__ == '__main__':
    main()
