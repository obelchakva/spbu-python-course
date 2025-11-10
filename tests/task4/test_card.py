import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from project.task4.Card import Card


class TestCard:
    def test_card_creation(self):
        """Test card creation."""
        card = Card("♥", "A", 11)
        assert card.suit == "♥"
        assert card.rank == "A"
        assert card.value == 11

    def test_card_string_representation(self):
        """Test card string representation."""
        card = Card("♠", "K", 10)
        assert str(card) == "K♠"

    def test_card_repr(self):
        """Test card repr."""
        card = Card("♦", "10", 10)
        assert repr(card) == "Card('♦', '10', 10)"

    def test_card_equality(self):
        """Test card equality."""
        card1 = Card("♣", "Q", 10)
        card2 = Card("♣", "Q", 10)
        card3 = Card("♥", "Q", 10)

        assert card1 == card1
        assert card1 != card3

    def test_different_card_values(self):
        """Test different card values."""
        ace = Card("♥", "A", 11)
        king = Card("♠", "K", 10)
        seven = Card("♦", "7", 7)

        assert ace.value == 11
        assert king.value == 10
        assert seven.value == 7
