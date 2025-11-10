import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from project.task4.blackjack import Blackjack
from project.task4.Strategies import (
    ConservativeStrategy,
    AggressiveStrategy,
    BasicStrategy,
)


class TestBlackjackIntegration:
    def test_game_initialization(self):
        """Test game initialization."""
        game = Blackjack(num_decks=1, max_rounds=10)
        game.add_bot("TestBot1", ConservativeStrategy(), 500)
        game.add_bot("TestBot2", AggressiveStrategy(), 500)

        assert len(game.players) == 2
        assert game.current_round == 0
        assert game.max_rounds == 10
        assert game.game_active == False
        assert len(game.history) == 0

    def test_game_start(self):
        """Test game start."""
        game = Blackjack(num_decks=1, max_rounds=10)
        game.add_bot("TestBot", ConservativeStrategy(), 500)
        game.start()

        assert game.game_active == True
        assert game.current_round == 0

    def test_add_bot(self):
        """Test adding bots."""
        game = Blackjack()
        initial_count = len(game.players)
        game.add_bot("NewBot", BasicStrategy(), 300)

        assert len(game.players) == initial_count + 1
        assert game.players[-1].name == "NewBot"
        assert game.players[-1].chips == 300

    def test_game_state(self):
        """Test getting game state."""
        game = Blackjack()
        game.add_bot("TestBot", ConservativeStrategy(), 500)
        state = game.get_state()

        assert "round" in state
        assert "max_rounds" in state
        assert "active_players" in state
        assert "cards_in_deck" in state
        assert "players" in state
        assert "dealer" in state

        assert state["round"] == 0
        assert state["active_players"] == 1

    def test_round_flow(self):
        """Test full round flow."""
        game = Blackjack(max_rounds=5)
        game.add_bot("TestBot", ConservativeStrategy(), 500)
        game.start()

        round_state = game.play_round()

        assert round_state is not None
        assert game.current_round == 1
        assert len(game.history) == 1

        assert "round" in round_state
        assert "players" in round_state
        assert "dealer" in round_state

    def test_game_over_conditions(self):
        """Test game over conditions."""
        game = Blackjack(max_rounds=2)
        game.add_bot("TestBot", ConservativeStrategy(), 500)
        game.start()

        game.play_round()
        game.play_round()

        assert not game.game_active
        assert game.current_round == 2

    def test_bankruptcy_detection(self):
        """Test bankruptcy detection."""
        game = Blackjack(max_rounds=3)
        game.add_bot("BankruptBot", AggressiveStrategy(), 0)
        game.start()
        game.play_round()

        state = game.get_state()
        assert not game.game_active
        assert state["active_players"] == 0
