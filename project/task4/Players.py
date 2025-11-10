from typing import List
from .Hand import Hand
from .Strategies import Strategy
from .Card import Card


class Player:
    """Base player class."""

    def __init__(self, name: str, chips: int = 1000) -> None:
        """
        Initializes a player.

        Parameters:
            name : str (Player name)
            chips : int (Starting chip count, default 1000)
        """
        self.name = name
        self.hand = Hand()
        self.chips = chips
        self.bet = 0
        self.standing = False
        self.busted = False

    def place_bet(self, amount: int) -> bool:
        """
        Places a bet.

        Parameters:
            amount : int (Bet amount)

        Returns:
            bool: True if bet successful, False otherwise
        """
        if 0 < amount <= self.chips:
            self.bet = amount
            self.chips -= amount
            return True
        return False

    def reset(self) -> None:
        """Resets player state for new round."""
        self.hand.clear()
        self.standing = False
        self.busted = False
        self.bet = 0

    def __str__(self) -> str:
        """Returns string representation of the player."""
        return f"{self.name} ({self.chips} chips)"


class Bot(Player):
    """Bot player with strategy."""

    def __init__(self, name: str, strategy: Strategy, chips: int = 1000) -> None:
        """
        Initializes a bot player.

        Parameters:
            name : str (Bot name)
            strategy : Strategy (Playing strategy)
            chips : int (Starting chip count, default 1000)
        """
        super().__init__(name, chips)
        self.strategy = strategy

    def make_bet(self) -> bool:
        """
        Makes an automated bet.

        Returns:
            bool: True if bet successful, False otherwise
        """
        if self.chips <= 0:
            return False
        bet_size = max(10, min(self.chips // 10, 100))
        return self.place_bet(bet_size)

    def make_decision(self, dealer_card: Card) -> str:
        """
        Makes gameplay decision.

        Parameters:
            dealer_card : Card (Dealer's visible card)

        Returns:
            str: 'hit' or 'stand'
        """
        if self.standing or self.busted:
            return "stand"

        decision = self.strategy.decide(self.hand, dealer_card)
        if decision == "stand":
            self.standing = True
        return decision


class Dealer(Player):
    """Dealer player."""

    def __init__(self) -> None:
        """Initializes the dealer."""
        super().__init__("Dealer", 0)

    def should_hit(self) -> bool:
        """
        Determines if dealer should hit according to casino rules.

        Returns:
            bool: True if dealer should hit, False otherwise
        """
        return self.hand.value < 17 or (self.hand.value == 17 and self.hand.aces > 0)

    def make_decision(self, dealer_card: Card) -> str:
        """
        Makes dealer's gameplay decision.

        Parameters:
            dealer_card : Card (Dealer's visible card)

        Returns:
            str: 'hit' or 'stand' based on casino rules
        """
        return "hit" if self.should_hit() else "stand"
