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
    pattern_string = "".join(pattern_string_list)

    pattern_re = re.compile(pattern_string, re.IGNORECASE)

    result = []

    #TODO: edit in python3 style.
    with codecs.open(filename, mode="r", encoding="utf-8") as fd:
        for line in fd:
            if pattern_re.search(line):
                result.append(line.strip())

    return result

def main():
    script_args = sys.argv[1:]
    pp(script_args)
    pp(graphiteFileParser(FILE_NAME, script_args))

if __name__ == "__main__":
    main()
