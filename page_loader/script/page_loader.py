#!/usr/bin/env python3
import sys
import os
from page_loader.engine import page_load, arg_parse


def main():
    args = arg_parse(sys.argv[1:])
    page_load(args.output, args.url)
    #file_name = normalize_url(args.url)
    #text = get_text_resp(args.url)
    #file_save(os.path.join(args.output, file_name), text)


if __name__ == '__main__':
    main()
