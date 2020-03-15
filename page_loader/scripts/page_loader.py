#!/usr/bin/env python3
import sys
from page_loader.engine import get_text_resp, file_save, arg_parse, give_a_name, create_file_path


def main():
    args = arg_parse(sys.argv[1:])
    file_name = give_a_name(args.url)
    text = get_text_resp(args.url)
    file_save(create_file_path(args.output, file_name), text)


if __name__ == '__main__':
    main()
