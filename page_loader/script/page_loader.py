#!/usr/bin/env python3
import sys

from page_loader.engine import arg_parse, page_load
from page_loader.logger import LOGGER, KnownError


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
