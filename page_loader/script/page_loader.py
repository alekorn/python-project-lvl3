#!/usr/bin/env python3
import sys
from page_loader.engine import page_load, arg_parse, KnownError
from page_loader.logger import LOGGER


def main():
    args = arg_parse(sys.argv[1:])
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
