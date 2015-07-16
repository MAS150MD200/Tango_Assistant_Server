__author__ = 'Antonio'

import codecs
import re
import sys
from pprint import pprint as pp


FILE_NAME = "../all_data_column.txt"

def graphiteFileParser(filename, args):

    #DEBUG:
    # print(filename)
    # pp(args)

    #TODO: check args for multiple spaces.
    pattern_string_list = ["^"]

    for script_arg in args:
        pattern_string_list.append("(?=.*" + script_arg + ")")

    pattern_string_list.append(".*$")
    pattern_string = "".join(pattern_string_list)   # result pattern string: ^(?=.*bnq)(?=.*tc2)(?=.*messages)(?=.*6004)(?=.*inbound).*$
    # DEBUG.
    # print(pattern_string)

    pattern_re = re.compile(pattern_string, re.IGNORECASE)

    result = []

    # Python3 style.
    with open(filename, mode='r') as fd:
        file_content = fd.read().split('\n')

    # pp(file_content)
    for line in file_content:
        if pattern_re.search(line):
            result.append(line.strip())

    # TODO: edit in python3 style.
    # with codecs.open(filename, mode="r", encoding="utf-8") as fd:
    #     for line in fd:
    #         if pattern_re.search(line):
    #             result.append(line.strip())

    return result

def main():
    script_args = sys.argv[1:]

    # DEBUG.
    script_args = "bnq tc2 messages 6004 inbound".split(" ")
    pp(script_args)
    pp(graphiteFileParser(FILE_NAME, script_args))

if __name__ == "__main__":
    main()
