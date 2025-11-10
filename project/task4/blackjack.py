import random
from typing import List, Dict, Any, Optional
from .Card import Card
from .Hand import Hand
from .Deck import Deck
from .Players import Player, Bot, Dealer
from .Strategies import (
    Strategy,
    ConservativeStrategy,
    AggressiveStrategy,
    BasicStrategy,
)


class Blackjack:
    """Main Blackjack game class."""

    def __init__(self, num_decks: int = 6, max_rounds: int = 100) -> None:
        """
        Initializes a Blackjack game.

        Parameters:
            num_decks : int (Number of decks to use, default 6)
            max_rounds : int (Maximum number of rounds, default 100)
        """
        self.deck = Deck(num_decks)
        self.dealer = Dealer()
        self.players: List[Player] = []
        self.current_round = 0
        self.max_rounds = max_rounds
        self.game_active = False
        self.history: List[Dict[str, Any]] = []

    def add_bot(self, name: str, strategy: Strategy, chips: int = 1000) -> None:
        """
        Adds a bot to the game.

        Parameters:
            name : str (Bot name)
            strategy : Strategy (Bot playing strategy)
            chips : int (Starting chips, default 1000)
        """
        bot = Bot(name, strategy, chips)
        self.players.append(bot)
        print(f"Added bot: {name} (500 chips)")

    def start(self) -> None:
        """Starts the game."""
        self.deck.shuffle()
        self.game_active = True
        self.current_round = 0

        print(f"Players: {len(self.players)}")
        print(f"Maximum rounds: {self.max_rounds}")

    def play_round(self) -> Optional[Dict[str, Any]]:
        """
        Plays one round of Blackjack.

        Returns:
            Optional[Dict[str, Any]]: Game state after round, None if game ended
        """
        if not self.game_active or self.current_round >= self.max_rounds:
            return None

        self.current_round += 1
        print(f"\nROUND {self.current_round}")

        # Round preparation
        self._prepare_round()

        # Betting phase
        self._take_bets()

        # Card dealing
        self._deal_cards()

        # Check for dealer blackjack
        if self._check_dealer_blackjack():
            self._save_state()
            return self._get_state()

        # Player turns
        self._play_turns()

        # Dealer turn
        self._dealer_turn()

        # Bet settlement
        self._settle_bets()

        # Game over check
        self._check_game_over()

        self._save_state()
        return self._get_state()

    def _prepare_round(self) -> None:
        """Prepares all participants for new round."""
        self.dealer.reset()
        for player in self.players:
            player.reset()

    def _take_bets(self) -> None:
        """Handles player betting phase."""
        print("\nBets:")
        for player in self.players:
            if player.chips > 0:
                if isinstance(player, Bot) and player.make_bet():
                    print(f"{player.name}: {player.bet} chips")
                else:
                    print(f"{player.name}: cannot bet")
            else:
                print(f"{player.name}: BANKRUPT (0 chips)")

    def _deal_cards(self) -> None:
        """Deals initial cards to players and dealer."""
        print("\nDealing:")

        # First cards to players
        for player in self.players:
            if player.bet > 0:
                card = self.deck.deal()
                player.hand.add_card(card)

        # First dealer card (face up)
        card = self.deck.deal()
        self.dealer.hand.add_card(card)
        print(f"Dealer: {card} [hidden]")

        # Second cards to players
        for player in self.players:
            if player.bet > 0:
                card = self.deck.deal()
                player.hand.add_card(card)
                print(f"{player.name}: {player.hand} ({player.hand.value})")

        # Second dealer card (face down)
        card = self.deck.deal()
        self.dealer.hand.add_card(card)

    def _check_dealer_blackjack(self) -> bool:
        """
        Checks if dealer has blackjack.

        Returns:
            bool: True if dealer has blackjack, False otherwise
        """
        if self.dealer.hand.is_blackjack():
            print("\nDEALER HAS BLACKJACK!")

            for player in self.players:
                if player.bet > 0:
                    if player.hand.is_blackjack():
                        # Push
                        player.chips += player.bet
                        print(f"{player.name}: push!")
                    else:
                        # Loss
                        print(f"{player.name}: lost!")
                    player.bet = 0

            self._check_game_over()

            return True
        return False

    def _play_turns(self) -> None:
        """Handles all player turns."""
        print("\nPlayer turns:")
        dealer_card = self.dealer.hand.cards[0]

        for player in self.players:
            if player.bet == 0 or player.busted:
                continue

            print(f"\n{player.name}: {player.hand} ({player.hand.value})")

            while not player.standing and not player.busted:
                if hasattr(player, "make_decision"):
                    decision = player.make_decision(dealer_card)
                else:
                    # For base player use conservative strategy
                    decision = "hit" if player.hand.value < 16 else "stand"

                if decision == "hit":
                    card = self.deck.deal()
                    player.hand.add_card(card)
                    print(f"+ {card} -> {player.hand} ({player.hand.value})")

                    if player.hand.is_busted():
                        player.busted = True
                        print(f"Busted!")
                else:
                    print(f"Stand")
                    break

    def _dealer_turn(self) -> None:
        """Handles dealer's turn."""
        print(f"\nDealer's turn:")
        print(f"Cards: {self.dealer.hand} ({self.dealer.hand.value})")

        while self.dealer.should_hit():
            card = self.deck.deal()
            self.dealer.hand.add_card(card)
            print(f"+ {card} -> {self.dealer.hand} ({self.dealer.hand.value})")

        print(f"Dealer stands at {self.dealer.hand.value}")

    def _settle_bets(self) -> None:
        """Settles all player bets."""
        print("\nResults:")
        dealer_value = self.dealer.hand.value
        dealer_busted = self.dealer.hand.is_busted()

        for player in self.players:
            if player.bet == 0:
                continue

            print(f"\n{player.name}:")
            print(f"Cards: {player.hand} ({player.hand.value})")

            if player.busted:
                print(f"Busted - lose {player.bet} chips")
            elif player.hand.is_blackjack():
                win = player.bet * 2.5
                player.chips += int(win)
                print(f"Blackjack! Win: {int(win)} chips")
            elif dealer_busted:
                win = player.bet * 2
                player.chips += win
                print(f"Dealer busted! Win: {win} chips")
            elif player.hand.value > dealer_value:
                win = player.bet * 2
                player.chips += win
                print(f"Win! Win: {win} chips")
            elif player.hand.value == dealer_value:
                player.chips += player.bet
                print(f"Push! Return {player.bet} chips")
            else:
                print(f"Lose {player.bet} chips")

            player.bet = 0

    def _check_game_over(self) -> None:
        """Checks game over conditions."""
        active_players = [p for p in self.players if p.chips > 0]

        if not active_players:
            print("\nAll players bankrupt!")
            self.game_active = False
        elif self.current_round >= self.max_rounds:
            print(f"\nReached limit of {self.max_rounds} rounds!")
            self.game_active = False

    def _save_state(self) -> None:
        """Saves current game state to history."""
        state = self._get_state()
        self.history.append(state)

    def _get_state(self) -> Dict[str, Any]:
        """
        Gets current game state.

        Returns:
            Dict[str, Any]: Current game state
        """
        return {
            "round": self.current_round,
            "max_rounds": self.max_rounds,
            "active_players": len([p for p in self.players if p.chips > 0]),
            "cards_in_deck": len(self.deck),
            "players": [
                {
                    "name": p.name,
                    "chips": p.chips,
                    "hand": str(p.hand),
                    "hand_value": p.hand.value,
                    "busted": p.busted,
                }
                for p in self.players
            ],
            "dealer": {
                "hand": str(self.dealer.hand),
                "hand_value": self.dealer.hand.value,
                "busted": self.dealer.hand.is_busted(),
            },
        }

    def get_state(self) -> Dict[str, Any]:
        """
        Public method to get game state.

        Returns:
            Dict[str, Any]: Current game state
        """
        return self._get_state()

    def show_status(self) -> None:
        """Shows current game status."""
        state = self.get_state()

        print(f"\nGame status (Round {state['round']}/{state['max_rounds']}):")
        print(f"Active players: {state['active_players']}")
        print(f"Cards in deck: {state['cards_in_deck']}")

        print("\nPlayers:")
        for player in state["players"]:
            status = "BANKRUPT" if player["chips"] == 0 else f"{player['chips']} chips"
            print(f"{player['name']}: {status}")

        if self.dealer.hand.cards:
            print(f"\nDealer: {self.dealer.hand} ({self.dealer.hand.value})")


def run_simple_game() -> None:
    """
    Runs a simple demonstration game.

    Creates a Blackjack game with multiple bots using different strategies
    and runs the game until completion.
    """
    print("\nSIMPLE GAME")
    print("\n")

    game = Blackjack(num_decks=2, max_rounds=5)

    game.add_bot("Conservative", ConservativeStrategy(), 500)
    game.add_bot("Aggressive", AggressiveStrategy(), 500)
    game.add_bot("Tactical", BasicStrategy(), 500)

    game.start()

    while game.game_active:
        input("\nPress Enter for next round...")
        game.play_round()
        game.show_status()

    print("\nFINAL RESULTS:")

    state = game.get_state()
    players_sorted = sorted(state["players"], key=lambda x: x["chips"], reverse=True)

    for i, player in enumerate(players_sorted, 1):
        profit = player["chips"] - 500
        print(f"{player['name']}: {player['chips']} chips ({profit:+})")


def strategy_demo() -> None:
    """
    Demonstrates different Blackjack strategies.

    Shows how each strategy makes decisions in a sample game situation.
    """
    print("\nSTRATEGY DEMONSTRATION")

    strategies = [
        ("Conservative", ConservativeStrategy()),
        ("Aggressive", AggressiveStrategy()),
        ("Basic", BasicStrategy()),
    ]

    for strategy_name, strategy in strategies:
        print(f"\nTesting {strategy_name} strategy:")

        hand = Hand()
        hand.add_card(Card("♥", "10", 10))
        hand.add_card(Card("♠", "6", 6))

        dealer_card = Card("♦", "9", 9)

        decision = strategy.decide(hand, dealer_card)
        print(f"Hand: {hand} ({hand.value})")
        print(f"Dealer card: {dealer_card}")
        print(f"Decision: {decision.upper()}")
