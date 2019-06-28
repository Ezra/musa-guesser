#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Use Wikipedia to guess Musa spellings, e.g. for place names.
"""

__author__ = "Ezra Bradford"
__version__ = "0.1.0"
__license__ = "BSD"

import argparse
import re
import sys
import wikipedia


# limit ourselves to one request every 50ms
wikipedia.set_rate_limiting(True)

RE_SQUARE_BRACKETS = re.compile(r'\[([^]]*)\]')


def setup_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('title', help='article title to check for pronunciation')
    return parser


def main():
    args = setup_parser().parse_args()
    title = args.title

    summary = wikipedia.summary(title, sentences = 2)
    matches = list(RE_SQUARE_BRACKETS.finditer(summary))
    if len(matches) == 1:
        pron = matches[0].group(1)
        print(title + ": " + pron)
        return 0 # success
    else:
        print(title + ": {} results".format(len(matches)))
        print(summary)
        return 1 # failure


if __name__ == "__main__":
    sys.exit(main())
