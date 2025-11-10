from abc import ABC, abstractmethod
from .Hand import Hand
from .Card import Card


class Strategy(ABC):
    """Abstract strategy for Blackjack gameplay."""

    @abstractmethod
    def decide(self, player_hand: Hand, dealer_card: Card) -> str:
        """
        Makes decision to hit or stand.

        Parameters:
            player_hand : Hand (Player's current hand)
            dealer_card : Card (Dealer's visible card)

        Returns:
            str: 'hit' or 'stand'
        """
        pass


class ConservativeStrategy(Strategy):
    """Conservative strategy: rarely hits."""

    def decide(self, player_hand: Hand, dealer_card: Card) -> str:
        """
        Decides based on conservative approach.

        Parameters:
            player_hand : Hand (Player's current hand)
            dealer_card : Card (Dealer's visible card)

        Returns:
            str: 'hit' if hand value < 13, 'stand' otherwise
        """
        return "hit" if player_hand.value < 13 else "stand"


class AggressiveStrategy(Strategy):
    """Aggressive strategy: frequently hits."""

    def decide(self, player_hand: Hand, dealer_card: Card) -> str:
        """
        Decides based on aggressive approach.

        Parameters:
            player_hand : Hand (Player's current hand)
            dealer_card : Card (Dealer's visible card)

        Returns:
            str: 'hit' for more hands, 'stand' only on high values
        """
        if player_hand.value < 17:
            return "hit"
        elif player_hand.value == 17 and dealer_card.value >= 7:
            return "hit"
        return "stand"


class BasicStrategy(Strategy):
    """Basic mathematical strategy."""

    def decide(self, player_hand: Hand, dealer_card: Card) -> str:
        """
        Decides based on basic Blackjack strategy.

        Parameters:
            player_hand : Hand (Player's current hand)
            dealer_card : Card (Dealer's visible card)

        Returns:
            str: 'hit' or 'stand' based on optimal play
        """
        value = player_hand.value

        # Simplified basic strategy
        if value <= 11:
            return "hit"
        elif value == 12:
            return "hit" if dealer_card.value in [2, 3, 7, 8, 9, 10, 11] else "stand"
        elif 13 <= value <= 16:
            return "hit" if dealer_card.value >= 7 else "stand"
        else:
            return "stand"
