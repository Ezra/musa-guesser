#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Use Wikipedia to guess Musa spellings, e.g. for place names.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

__author__ = "Ezra Bradford"
__version__ = "0.1.0"
__license__ = "BSD"

import argparse
import copy
import re
import sys
import wikipedia

from musa_table import ipa_to_musas


# limit ourselves to one request every 50ms
wikipedia.set_rate_limiting(True)

RE_SQUARE_BRACKETS = re.compile(r'\[([^]]*)\]')

# add syllable break
my_dict = copy.deepcopy(ipa_to_musas)
my_dict['.'] = list(chr(int('E100', 16)))



class AmbiguousPronunciationError(Exception): pass

class NoPronunciationError(Exception): pass


def setup_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('title', help='article title to check for pronunciation')
    return parser


def title_to_pron(title):
    """
    Given a Wikipedia article title, return an IPA pronunciation.

    Raises:
        musa_guesser.NoPronunciationError if none is found
        musa_guesser.AmbiguousPronunciationError if several are found
        wikipedia.exceptions.DisambiguationError if the title is ambiguous
        [other wikipedia.exceptions and requests.exceptions, as appropriate]
    """

    summary = wikipedia.summary(title, sentences = 2)
    matches = list(RE_SQUARE_BRACKETS.finditer(summary))

    if len(matches) < 1:
        raise NoPronunciationError(
                "No IPA pronunciation found in \"{}\"".format(summary)
                )
    elif len(matches) > 1:
        raise AmbiguousPronunciationError(
                "{} pronunciations found in \"{}\"".format(
                    len(matches),
                    summary
                    )
                )

    # exactly 1 match, extract the pronunciation
    pron = matches[0].group(1)
    return pron


def ipa_to_musa(pron):
    return ''.join([my_dict.get(char, char)[0] for char in pron])


def main():
    args = setup_parser().parse_args()
    title = args.title

    pron = title_to_pron(title)
    musa = ipa_to_musa(pron)
    print(' '.join([title, pron, musa]))
    return


if __name__ == "__main__":
    sys.exit(main())
