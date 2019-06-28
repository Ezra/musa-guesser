#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Use Wikipedia to guess Musa spellings, e.g. for place names.
"""

__author__ = "Ezra Bradford"
__version__ = "0.1.0"
__license__ = "BSD"

import re
import sys
import wikipedia


# limit ourselves to one request every 50ms
wikipedia.set_rate_limiting(True)

RE_SQUARE_BRACKETS = re.compile(r'\[[^]]*\]')


def main():
    title = "xi'an"
    summary = wikipedia.summary(title, sentences = 2)
    matches = RE_SQUARE_BRACKETS.findall(summary)
    if len(matches) == 1:
        print(title + ": " + matches[0])
    else:
        print(title + ": {} results".format(len(matches)))
        print(summary)
    return

if __name__ == "__main__":
    sys.exit(main())
