# -*- encoding: utf-8 -*-
"""
Provide conversion between Musa and other scripts, initially IPA
"""

from __future__ import absolute_import, division, print_function, unicode_literals

__author__ = "Ezra Bradford"
__version__ = "0.1.0"
__license__ = "BSD"

import codecs
import collections
import csv
import itertools
import sys


def raw_open(filename):
    if sys.version_info[0] < 3:
        infile = open(filename, 'rb')
    else:
        infile = open(filename, 'r', newline='', encoding='utf8')
    return infile


def load_tables(limit=None):
    with raw_open('musa_table.csv') as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__() # skip header

        # musa char to list of ipa readings
        musa_to_ipas = collections.defaultdict(list)
        # ipa sequence to list of musa chars
        ipa_to_musas = collections.defaultdict(list)

        # for speed, test with just the head
        if limit:
            reader = itertools.islice(reader, limit)

        for row in reader:
            codepoint, trans, ipa_string, uni = row
            musa_char = chr(int(codepoint, 16))
            ipas = ipa_string.split()
            if trans == 'xd': # interpunct <=> space
                ipas.append(' ')
            # build the data structures
            musa_to_ipas[musa_char] = ipas
            for ipa in ipas:
                ipa_to_musas[ipa].append(musa_char)

    return musa_to_ipas, ipa_to_musas


def test_it():
    musa_to_ipas, ipa_to_musas = load_tables(limit=10)

    for d in [musa_to_ipas, ipa_to_musas]:
        for k, vs in d.items():
            if vs:
                print(k)
                for v in vs:
                    print('\t', v)


if __name__ == '__main__':
    test_it()
