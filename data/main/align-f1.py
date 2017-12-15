#!/usr/bin/env python
from __future__ import print_function, division
import sys
from six.moves import zip
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('test', metavar='predict', help='predicted alignments')
argparser.add_argument('gold', metavar='true', help='true alignments')
args = argparser.parse_args()

match = 0
gold = 0
test = 0

for testline, goldline in zip(open(args.test), open(args.gold)):
    testalign = set(testline.split())
    goldalign = set(goldline.split())
    test += len(testalign)
    gold += len(goldalign)
    match += len(testalign & goldalign)

prec = match/test
rec = match/gold
f1 = 2/(1/prec+1/rec)

print("predicted alignments:", test)
print("true alignments:     ", gold)
print("matched alignments:  ", match)
print("precision:           ", prec)
print("recall:              ", rec)
print("F1 score:            ", f1)


