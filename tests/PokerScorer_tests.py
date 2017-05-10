from nose import tools
from PokerScorer.parse import card
from PokerScorer.parse import get_sorted_hands
from PokerScorer.score import score_hand


def test_get_sorted_hands():
    ah = [card(suit='club', rank='j', ah_idx=9, al_idx=10),
          card(suit='club', rank='10', ah_idx=8, al_idx=9),
          card(suit='club', rank='9', ah_idx=7, al_idx=8),
          card(suit='club', rank='8', ah_idx=6, al_idx=7),
          card(suit='club', rank='7', ah_idx=5, al_idx=6)]
    ahr = [card(suit='club', rank='j', ah_idx=9, al_idx=10),
           card(suit='club', rank='10', ah_idx=8, al_idx=9),
           card(suit='club', rank='9', ah_idx=7, al_idx=8),
           card(suit='club', rank='8', ah_idx=6, al_idx=7),
           card(suit='club', rank='7', ah_idx=5, al_idx=6)]
    al = [card(suit='club', rank='j', ah_idx=9, al_idx=10),
          card(suit='club', rank='10', ah_idx=8, al_idx=9),
          card(suit='club', rank='9', ah_idx=7, al_idx=8),
          card(suit='club', rank='8', ah_idx=6, al_idx=7),
          card(suit='club', rank='7', ah_idx=5, al_idx=6)]
    alr = [card(suit='club', rank='j', ah_idx=9, al_idx=10),
           card(suit='club', rank='10', ah_idx=8, al_idx=9),
           card(suit='club', rank='9', ah_idx=7, al_idx=8),
           card(suit='club', rank='8', ah_idx=6, al_idx=7),
           card(suit='club', rank='7', ah_idx=5, al_idx=6)]
    rc = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 1, '8': 1, '9': 1, '10': 1, 'J': 1, 'Q': 0, 'K': 0, 'A': 0}
    sc = {'club': 5, 'diamond': 0, 'heart': 0, 'spade': 0}
    a, b, c, d, e, f = get_sorted_hands('clubJ-club10-club9-club8-club7')
    assert map(lambda x: x[0] == x[1], zip(a, ah))
    assert map(lambda x: x[0] == x[1], zip(b, ahr))
    assert map(lambda x: x[0] == x[1], zip(c, al))
    assert map(lambda x: x[0] == x[1], zip(d, alr))
    assert map(lambda x: x[0] == x[1], zip(e.values(), rc.values()))
    assert map(lambda x: x[0] == x[1], zip(f.values(), sc.values()))
    with tools.assert_raises(ValueError) as ve:
        get_sorted_hands('club1-club2-club3-club4-club5')
    with tools.assert_raises(AssertionError) as ae:
        get_sorted_hands('club2-club3')
        get_sorted_hands('diamondA-heartK-clubJ-spade10')
        get_sorted_hands('diamondA-diamondA-heartK-clubJ-spade10')


def test_score_hand():
    assert score_hand('diamondA-diamondK-diamondQ-diamondJ-diamond10') == 'Royal Flush'
    assert score_hand('spade10-spadeJ-spadeQ-spadeK-spadeA') == 'Royal Flush'
    assert score_hand('club6-club4-club7-club5-club8') == 'Straight Flush'
    assert score_hand('clubA-club2-club3-club4-club5') == 'Straight Flush'
    assert score_hand('diamond2-club2-spade2-heart2-heart3') == 'Four of a Kind'
    assert score_hand('diamond2-club3-spade3-heart2-heart3') == 'Full House'
    assert score_hand('heartA-heart2-heartQ-heart4-heart10') == 'Flush'
    assert score_hand('heartA-club2-diamond3-spade4-club5') == 'Straight'
    assert score_hand('heartA-club10-diamondQ-spadeK-clubJ') == 'Straight'
    assert score_hand('heartA-club2-diamondA-spade5-spadeA') == 'Three of a Kind'
    assert score_hand('heart9-club9-diamond3-spade3-club5') == 'Two Pair'
    assert score_hand('club7-heart5-diamond3-spadeJ-club5') == 'Pair'
    assert score_hand('club7-heart9-diamond3-spadeA-club5') == 'High Card'
