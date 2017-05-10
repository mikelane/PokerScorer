#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Poker Hand Scoring Utility

Provide a poker hand in a format like spade10-spadeJ-spadeQ-spadeK-spadeA
and this utility will tell you what the score of the hand is.
"""

# Imports
import argparse
from PokerScorer.score import score_hand

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"


parser = argparse.ArgumentParser(description='''This utility scores a poker hand given as a string.
Please ensure that you are using a python3 interpreter.''')
parser.add_argument('hand', help='The poker hand you want to evaluate, e.g. spade10-spadeJ-spadeQ-spadeK-spadeA')
args = parser.parse_args()


if __name__ == '__main__':
    print(score_hand(args.hand))
