from typing import List
from .Card import Card


class Hand:
    """Hand of playing cards."""

    def __init__(self) -> None:
        """Initializes an empty hand."""
        self.cards: List[Card] = []
        self.value = 0
        self.aces = 0

    def add_card(self, card: Card) -> None:
        """
        Adds a card to the hand.

        Parameters:
            card : Card (Card to add to the hand)
        """
        self.cards.append(card)
        self.value += card.value

        if card.rank == "A":
            self.aces += 1

        # Adjust ace value if hand is busted
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

    def clear(self) -> None:
        """Clears all cards from the hand."""
        self.cards.clear()
        self.value = 0
        self.aces = 0

    def is_blackjack(self) -> bool:
        """
        Checks if hand is a blackjack.

        Returns:
            bool: True if hand is blackjack (21 with 2 cards), False otherwise
        """
        return len(self.cards) == 2 and self.value == 21

    def is_busted(self) -> bool:
        """
        Checks if hand is busted (over 21).

        Returns:
            bool: True if hand value exceeds 21, False otherwise
        """
        return self.value > 21

    def __str__(self) -> str:
        """Returns string representation of the hand."""
        return " ".join(str(card) for card in self.cards)
