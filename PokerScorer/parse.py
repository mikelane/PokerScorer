#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Parse a poker hand

Hands are expected to be entered in a format similar to the following:

clubJ-club10-club9-club8-club7

Something other than 5 cards will raise an exception. Any suit other than 
club, spade, heart, or diamond will raise an exception. Any card rank other than
2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A will raise an exception.
"""

# Imports
import re
from collections import namedtuple

from typing import Tuple, List, Dict

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"

card = namedtuple('card', ['suit', 'rank', 'ah_idx', 'al_idx'])


def get_sorted_hands(input_string:str) -> \
        Tuple[List[card], List[card], List[card], List[card], Dict[str, int], Dict[str, int]]:
    """
    Given an input string of cards in the format specified below, parse the string and
    extract some useful information into a few different data structures.
    
    Parameters
    ----------
    input_string: The format should be suitX-suitX-suitX-suitX-suitX where suit is one
    of 'club', 'heart', 'diamond', or 'spade' and X is 2, 3, 4, 5, 6, 7, 8, 9, 10, j, Q,
    K, or A. An exception will be raised (either AssertionError or ValueError) if the 
    input string is not properly formatted.

    Returns
    -------
    A 6-tuple. The first element is the hand sorted with aces high. The second element is
    the hand sorted by the card rank where aces are high. The third and fourth elements are
    the same except aces are low. The fifth element is a suit counter for the given hand.
    The sixth and final element is a counter of the various card ranks in the hand.
    
    """
    # Set up the regex
    card_regex = re.compile(r'(club|spade|diamond|heart){1}(2|3|4|5|6|7|8|9|10|J|Q|K|A){1}')

    # Define the ace high and ace low card values as well as the suits.
    ace_high_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    ace_low_ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['club', 'diamond', 'heart', 'spade']

    # Set up the dictionaries for quick access operations
    suits_to_index = {s: i * 13 for i, s in enumerate(suits)}
    ah_ranks_to_index = {r: i for i, r in enumerate(ace_high_ranks)}
    al_ranks_to_index = {r: i for i, r in enumerate(ace_low_ranks)}

    # Set up the counters for keeping track of the number of suits and ranks in a hand
    suit_counter = {suit: 0 for suit in suits}
    rank_counter = {rank: 0 for rank in ace_high_ranks}

    # Set up the bucket sort
    ah_card_bucket = [None] * 52
    al_card_bucket = [None] * 52

    # Split the string and run a regex search to parse and capture the data
    try:
        hand = [re.findall(card_regex, h)[0] for h in input_string.split('-')]
    except IndexError as e:
        raise ValueError('Invalid card string detected')
    assert len(hand) == 5, 'Invalid number of cards: {}'.format(len(hand))

    # Create the cards, update the metadata, and sort the cards
    for suit, rank in hand:
        assert suit in suits, 'Invalid suit: {}'.format(suit)
        assert rank in ace_high_ranks, 'Invalid rank: {}'.format(rank)
        c = card(
            suit,
            rank,
            suits_to_index[suit] + ah_ranks_to_index[rank],
            suits_to_index[suit] + al_ranks_to_index[rank]
        )

        suit_counter[suit] += 1
        rank_counter[rank] += 1
        ah_card_bucket[c.ah_idx] = c
        al_card_bucket[c.al_idx] = c

    # Finalize the sort and sort by rank, ace high
    ah_sorted_hand = [c for c in ah_card_bucket[::-1] if c]
    ah_rank_sort = sorted(ah_sorted_hand, key=lambda c: ah_ranks_to_index[c.rank], reverse=True)
    # Same for ace low
    al_sorted_hand = [c for c in al_card_bucket[::-1] if c]
    al_rank_sort = sorted(al_sorted_hand, key=lambda c: al_ranks_to_index[c.rank], reverse=True)

    # Verify there are were no duplicates.
    assert len(ah_sorted_hand) == 5, 'Invalid number of cards: {}'.format(len(ah_sorted_hand))
    assert len(al_sorted_hand) == 5, 'Invalid number of cards: {}'.format(len(al_sorted_hand))

    return ah_sorted_hand, ah_rank_sort, al_sorted_hand, al_rank_sort, suit_counter, rank_counter
