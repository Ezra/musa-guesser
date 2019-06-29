# -*- encoding: utf-8 -*-
"""
Provide conversion between Musa and other scripts, initially IPA
"""

from __future__ import absolute_import, division, print_function, unicode_literals

__author__ = "Ezra Bradford"
__version__ = "0.1.0"
__license__ = "BSD"

import codecs
import csv
import sys


def raw_open(filename):
    if sys.version_info[0] < 3:
        infile = open(filename, 'rb')
    else:
        infile = open(filename, 'r', newline='', encoding='utf8')
    return infile


def do_stuff():
    with raw_open('musa_table.csv') as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__() # skip header
        import itertools
        reader = itertools.islice(reader, 10)
        for row in reader:
            codepoint, trans, ipa_string, uni = row
            musa_char = chr(int(codepoint, 16))
            ipas = ipa_string.split()
            print("u+{}".format(codepoint), musa_char, ' '.join(ipas))


do_stuff()
