#!/usr/bin/env python3
from page_loader.engine import run, arg_parse


def main():
    output_dir, url = arg_parse()
    print(output_dir, url, run())

if __name__ == '__main__':
    main()
