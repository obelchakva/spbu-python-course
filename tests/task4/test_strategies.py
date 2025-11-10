import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from project.task4.Strategies import (
    ConservativeStrategy,
    AggressiveStrategy,
    BasicStrategy,
)
from project.task4.Hand import Hand
from project.task4.Card import Card


class TestStrategies:
    @pytest.fixture
    def strategies(self):
        return {
            "conservative": ConservativeStrategy(),
            "aggressive": AggressiveStrategy(),
            "basic": BasicStrategy(),
        }

    def test_conservative_strategy(self, strategies):
        """Test conservative strategy."""
        hand = Hand()
        dealer_card = Card("♦", "7", 7)

        hand.add_card(Card("♥", "8", 8))
        hand.add_card(Card("♠", "4", 4))
        assert strategies["conservative"].decide(hand, dealer_card) == "hit"

        hand.clear()
        hand.add_card(Card("♥", "8", 8))
        hand.add_card(Card("♠", "5", 5))
        assert strategies["conservative"].decide(hand, dealer_card) == "stand"

    def test_aggressive_strategy(self, strategies):
        """Test aggressive strategy."""
        hand = Hand()

        hand.add_card(Card("♥", "10", 10))
        hand.add_card(Card("♠", "6", 6))
        dealer_card = Card("♦", "2", 2)
        assert strategies["aggressive"].decide(hand, dealer_card) == "hit"

        hand.clear()
        hand.add_card(Card("♥", "10", 10))
        hand.add_card(Card("♠", "7", 7))
        dealer_card = Card("♦", "A", 11)
        assert strategies["aggressive"].decide(hand, dealer_card) == "hit"

        hand.clear()
        hand.add_card(Card("♥", "10", 10))
        hand.add_card(Card("♠", "9", 9))
        assert strategies["aggressive"].decide(hand, dealer_card) == "stand"

    def test_basic_strategy(self, strategies):
        """Test basic strategy."""
        hand = Hand()
        dealer_card = Card("♦", "9", 9)

        hand.add_card(Card("♥", "5", 5))
        hand.add_card(Card("♠", "6", 6))
        assert strategies["basic"].decide(hand, dealer_card) == "hit"

        hand.clear()
        hand.add_card(Card("♥", "6", 6))
        hand.add_card(Card("♠", "6", 6))
        assert strategies["basic"].decide(hand, dealer_card) == "hit"

        hand.clear()
        hand.add_card(Card("♥", "6", 6))
        hand.add_card(Card("♠", "6", 6))
        dealer_card = Card("♦", "4", 4)
        assert strategies["basic"].decide(hand, dealer_card) == "stand"

        hand.clear()
        hand.add_card(Card("♥", "10", 10))
        hand.add_card(Card("♠", "6", 6))
        dealer_card = Card("♦", "10", 10)
        assert strategies["basic"].decide(hand, dealer_card) == "hit"

        hand.clear()
        hand.add_card(Card("♥", "10", 10))
        hand.add_card(Card("♠", "6", 6))
        dealer_card = Card("♦", "6", 6)
        assert strategies["basic"].decide(hand, dealer_card) == "stand"

        hand.clear()
        hand.add_card(Card("♥", "10", 10))
        hand.add_card(Card("♠", "7", 7))
        assert strategies["basic"].decide(hand, dealer_card) == "stand"
