class Card:
    """Playing card."""

    def __init__(self, suit: str, rank: str, value: int) -> None:
        """
        Initializes a playing card.

        Parameters:
            suit : str (Card suit: ♥, ♦, ♣, ♠)
            rank : str (Card rank: 2-10, J, Q, K, A)
            value : int (Card value in Blackjack)
        """
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self) -> str:
        """Returns string representation of the card."""
        return f"{self.rank}{self.suit}"

    def __repr__(self) -> str:
        """Returns formal string representation of the card."""
        return f"Card('{self.suit}', '{self.rank}', {self.value})"
