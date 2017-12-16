"""Simple implementation of single-reference, case-sensitive BLEU
without tokenization."""

from __future__ import division
from six.moves import range, zip
from six import itervalues
import collections
import math

def ngrams(seg, n):
    c = collections.Counter()
    for i in range(len(seg)-n+1):
        c[tuple(seg[i:i+n])] += 1
    return c

def card(c):
    """Cardinality of a multiset."""
    return sum(itervalues(c))

def zero():
    return collections.Counter()

def count(t, r, n=4):
    """Collect statistics for a single test and reference segment."""

    stats = collections.Counter()
    for i in range(1, n+1):
        tngrams = ngrams(t, i)
        stats['guess',i] += card(tngrams)
        stats['match',i] += card(tngrams & ngrams(r, i))
    stats['reflen'] += len(r)
    return stats

def score(stats, n=4):
    """Compute BLEU score.

    :param stats: Statistics collected using bleu.count
    :type stats: dict"""

    b = 1.
    for i in range(1, n+1):
        b *= stats['match',i]/stats['guess',i] if stats['guess',i] > 0 else 0
    b **= 0.25
    if stats['guess',1] < stats['reflen']: 
        b *= math.exp(1-stats['reflen']/stats['guess',1])
    return b

if __name__ == "__main__":
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument('test', metavar='predict', help='predicted translations')
    argparser.add_argument('gold', metavar='true', help='true translations')
    argparser.add_argument('-n', help='maximum n-gram size to score', default=4, type=int)
    args = argparser.parse_args()

    test = [line.split() for line in open(args.test)]
    gold = [line.split() for line in open(args.gold)]

    c = zero()
    for t, g in zip(test, gold):
        c += count(t, g, n=args.n)
    print("BLEU:", score(c, n=args.n))
    
