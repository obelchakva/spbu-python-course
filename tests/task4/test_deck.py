import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from project.task4.Deck import Deck
from project.task4.Card import Card


class TestDeck:
    def test_deck_initialization(self):
        """Test deck initialization."""
        deck = Deck(1)
        assert len(deck) == 52

    def test_multiple_decks(self):
        """Test multiple deck creation."""
        double_deck = Deck(2)
        assert len(double_deck) == 104

        six_deck = Deck(6)
        assert len(six_deck) == 312

    def test_shuffle(self):
        """Test deck shuffling."""
        deck = Deck(1)
        original_order = deck.cards.copy()
        deck.shuffle()

        assert original_order != deck.cards
        assert len(original_order) == len(deck.cards)

    def test_deal_card(self):
        """Test card dealing."""
        deck = Deck(1)
        initial_count = len(deck)
        card = deck.deal()

        assert isinstance(card, Card)
        assert len(deck) == initial_count - 1

    def test_deal_from_empty_deck(self):
        """Test dealing from empty deck."""
        deck = Deck(1)
        for _ in range(len(deck)):
            card = deck.deal()
            assert isinstance(card, Card)

        assert len(deck) == 0

        card = deck.deal()
        assert isinstance(card, Card)
        assert len(deck) == 51

    def test_card_values_in_deck(self):
        """Test card values in deck."""
        deck = Deck(1)
        expected_ranks = {
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "J",
            "Q",
            "K",
            "A",
        }
        expected_suits = {"♥", "♦", "♣", "♠"}

        found_ranks = set()
        found_suits = set()

        for card in deck.cards:
            found_ranks.add(card.rank)
            found_suits.add(card.suit)

        assert found_ranks == expected_ranks
        assert found_suits == expected_suits
