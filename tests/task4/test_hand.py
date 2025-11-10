import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from project.task4.Hand import Hand
from project.task4.Card import Card


class TestHand:
    def test_hand_initialization(self):
        """Test hand initialization."""
        hand = Hand()
        assert len(hand.cards) == 0
        assert hand.value == 0
        assert hand.aces == 0

    def test_add_card(self):
        """Test adding card to hand."""
        hand = Hand()
        card = Card("♥", "7", 7)
        hand.add_card(card)

        assert len(hand.cards) == 1
        assert hand.value == 7
        assert hand.cards[0] == card

    def test_multiple_cards(self):
        """Test adding multiple cards."""
        hand = Hand()
        cards = [Card("♥", "5", 5), Card("♠", "8", 8), Card("♦", "3", 3)]

        for card in cards:
            hand.add_card(card)

        assert len(hand.cards) == 3
        assert hand.value == 16

    def test_blackjack_detection(self):
        """Test blackjack detection."""
        hand = Hand()
        hand.add_card(Card("♥", "A", 11))
        hand.add_card(Card("♠", "K", 10))

        assert hand.is_blackjack() == True
        assert hand.value == 21

    def test_not_blackjack(self):
        """Test non-blackjack hands."""
        hand = Hand()
        hand.add_card(Card("♥", "K", 10))
        hand.add_card(Card("♠", "Q", 10))

        assert hand.is_blackjack() == False

        hand2 = Hand()
        hand2.add_card(Card("♥", "7", 7))
        hand2.add_card(Card("♠", "7", 7))
        hand2.add_card(Card("♦", "7", 7))

        assert hand2.is_blackjack() == False

    def test_bust_detection(self):
        """Test bust detection."""
        hand = Hand()
        hand.add_card(Card("♥", "K", 10))
        hand.add_card(Card("♠", "Q", 10))
        hand.add_card(Card("♦", "5", 5))

        assert hand.is_busted() == True
        assert hand.value == 25

    def test_ace_value_adjustment(self):
        """Test ace value adjustment."""
        hand = Hand()
        hand.add_card(Card("♥", "A", 11))
        hand.add_card(Card("♠", "8", 8))
        hand.add_card(Card("♦", "7", 7))

        assert hand.value == 16
        assert hand.is_busted() == False

    def test_multiple_aces(self):
        """Test multiple aces handling."""
        hand = Hand()
        hand.add_card(Card("♥", "A", 11))
        hand.add_card(Card("♠", "A", 11))
        hand.add_card(Card("♦", "9", 9))

        assert hand.value == 21
        assert hand.is_busted() == False

    def test_hand_clear(self):
        """Test hand clearing."""
        hand = Hand()
        hand.add_card(Card("♥", "K", 10))
        hand.add_card(Card("♠", "5", 5))

        hand.clear()

        assert len(hand.cards) == 0
        assert hand.value == 0
        assert hand.aces == 0

    def test_hand_string_representation(self):
        """Test hand string representation."""
        hand = Hand()
        hand.add_card(Card("♥", "A", 11))
        hand.add_card(Card("♠", "K", 10))

        hand_str = str(hand)
        assert "A♥" in hand_str
        assert "K♠" in hand_str
