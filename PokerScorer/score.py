#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Score a poker hand"""
from typing import List

from PokerScorer.parse import get_sorted_hands, card

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"

rank_order = {
    'Royal Flush': 10,
    'Straight Flush': 9,
    'Four of a Kind': 8,
    'Full House': 7,
    'Flush': 6,
    'Straight': 5,
    'Three of a Kind': 4,
    'Two Pair': 3,
    'Pair': 2,
    'High Card': 1
}


def find_sequence(sorted_hand: List[card], flush: bool, ace_high: bool) -> str:
    """
    Utility function to find sequences of card ranks in a hand.
    
    Parameters
    ----------
    sorted_hand: A list of cards that is either sorted ace high or ace low
    flush: Whether or not this search should expect to find a flush of some kind
    ace_high: Whether or not aces are high in this search.

    Returns
    -------
    The string value of the sequence or High Card if no sequence is found.
    """
    ace_high_ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    ace_low_ranks = ['K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2', 'A']

    hand_ranks = [c.rank for c in sorted_hand]
    if flush and hand_ranks == ['A', 'K', 'Q', 'J', '10']:
        return 'Royal Flush'

    ranks = ace_high_ranks if ace_high else ace_low_ranks
    i = ranks.index(hand_ranks[0])
    found_sequence = False not in map(lambda x: x[0] == x[1], zip(hand_ranks, ranks[i:i + 5]))
    # found_sequence = set(hand_ranks) == set(ranks[i:i+5])
    if flush and found_sequence:
        return 'Straight Flush'
    elif flush and not found_sequence:
        return 'Flush'
    elif not flush and found_sequence:
        return 'Straight'
    else:
        return 'High Card'.format(sorted_hand[0].suit, sorted_hand[0].rank)


def score_hand(input_str: str) -> str:
    """
    Take an input string of the format listed below and return one of the following strings that
    represents the rank:
    
    'Royal Flush'
    'Straight Flush'
    'Four of a Kind'
    'Full House'
    'Flush'
    'Straight'
    'Three of a Kind'
    'Two Pair'
    'Pair'
    'High Card'
    
    Parameters
    ----------
    input_str: The format should be suitX-suitX-suitX-suitX-suitX where suit is one
    of 'club', 'heart', 'diamond', or 'spade' and X is 2, 3, 4, 5, 6, 7, 8, 9, 10, j, Q,
    K, or A. An exception will be raised (either AssertionError or ValueError) if the 
    input string is not properly formatted.

    Returns
    -------
    Poker hand score
    """

    # Get the parsed hand information
    ah_sorted_hand, ah_rank_sort, al_sorted_hand, al_rank_sort, suit_counter, rank_counter = get_sorted_hands(input_str)

    # If all cards are from one suit, it's either a flush of some kind or a high card.
    if 5 in suit_counter.values():
        ah_rank = find_sequence(ah_sorted_hand, flush=True, ace_high=True)
        al_rank = find_sequence(al_sorted_hand, flush=True, ace_high=False)
        return ah_rank if rank_order[ah_rank] >= rank_order[al_rank] else al_rank

    # If there are 4 of the same rank cards, the only possibility is a 4 of a kind.
    if 4 in rank_counter.values():
        return 'Four of a Kind'

    # If there are 3 of the same rank cards, then it could be a full house or a three of a kind
    if 3 in rank_counter.values():
        if 2 in rank_counter.values():
            return 'Full House'
        else:
            return 'Three of a Kind'

    # If there are 2 cards of the same rank, it could be 2 pair or just a pair
    if 2 in rank_counter.values():
        if len([x for x in rank_counter.values() if x == 2]) == 2:
            return 'Two Pair'
        else:
            return 'Pair'

    # Must determine if there is an ace high or ace low straight or not
    ah_rank = find_sequence(ah_rank_sort, flush=False, ace_high=True)
    al_rank = find_sequence(al_rank_sort, flush=False, ace_high=False)

    return ah_rank if rank_order[ah_rank] >= rank_order[al_rank] else al_rank
