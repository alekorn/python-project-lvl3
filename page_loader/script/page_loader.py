#!/usr/bin/env python3
import sys
from page_loader.engine import page_load, arg_parse


def main():
    args = arg_parse(sys.argv[1:])
    page_load(args.output, args.url)


if __name__ == '__main__':
    main()
