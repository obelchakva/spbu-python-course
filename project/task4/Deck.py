import random
from typing import List
from .Card import Card


class Deck:
    """Deck of playing cards."""

    def __init__(self, num_decks: int = 1):
        """
        Initializes a deck of cards.

        Parameters:
            num_decks : int (Number of standard decks to use, default 1)
        """
        self.suits = ["♥", "♦", "♣", "♠"]
        self.ranks = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 10,
            "Q": 10,
            "K": 10,
            "A": 11,
        }
        self.cards: List[Card] = []
        self.build(num_decks)
        self.shuffle()

    def build(self, num_decks: int) -> None:
        """
        Builds the deck from multiple standard decks.

        Parameters:
            num_decks : int (Number of standard decks to combine)
        """
        self.cards = []
        for _ in range(num_decks):
            for suit in self.suits:
                for rank, value in self.ranks.items():
                    self.cards.append(Card(suit, rank, value))

    def shuffle(self) -> None:
        """Shuffles the deck of cards."""
        random.shuffle(self.cards)

    def deal(self) -> Card:
        """
        Deals one card from the deck.

        Returns:
            Card: Single card from the top of the deck
        """
        if not self.cards:
            self.build(1)
            self.shuffle()
        return self.cards.pop()

    def __len__(self) -> int:
        """Returns number of cards remaining in the deck."""
        return len(self.cards)
