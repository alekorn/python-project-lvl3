#!/usr/bin/env python3
import sys
from page_loader.engine import page_load, arg_parse
from page_loader.logger import LOGGER


def main():
    args = arg_parse(sys.argv[1:])
    LOGGER.setLevel(args.log.upper())
    LOGGER.info('Started')
    page_load(args.output, args.url)
    LOGGER.debug('Finished')


if __name__ == '__main__':
    main()
