import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from project.task4.Players import Player, Bot, Dealer
from project.task4.Strategies import ConservativeStrategy
from project.task4.Card import Card


class TestPlayer:
    def test_player_initialization(self):
        """Test player initialization."""
        player = Player("TestPlayer", 1000)
        assert player.name == "TestPlayer"
        assert player.chips == 1000
        assert player.bet == 0
        assert player.standing == False
        assert player.busted == False

    def test_place_bet(self):
        """Test placing bets."""
        player = Player("TestPlayer", 1000)

        success = player.place_bet(100)
        assert success == True
        assert player.bet == 100
        assert player.chips == 900

        success = player.place_bet(1000)
        assert success == False
        assert player.bet == 100
        assert player.chips == 900

        success = player.place_bet(-50)
        assert success == False

    def test_player_reset(self):
        """Test player reset."""
        player = Player("TestPlayer", 1000)
        player.place_bet(100)
        player.hand.add_card(Card("♥", "10", 10))
        player.standing = True
        player.busted = True

        player.reset()

        assert player.bet == 0
        assert len(player.hand.cards) == 0
        assert player.hand.value == 0
        assert player.standing == False
        assert player.busted == False

    def test_player_string_representation(self):
        """Test player string representation."""
        player = Player("TestPlayer", 1000)
        player_str = str(player)
        assert "TestPlayer" in player_str
        assert "1000" in player_str


class TestBot:
    def test_bot_initialization(self):
        """Test bot initialization."""
        strategy = ConservativeStrategy()
        bot = Bot("TestBot", strategy, 500)
        assert bot.name == "TestBot"
        assert bot.chips == 500
        assert bot.strategy == strategy

    def test_bot_make_bet(self):
        """Test bot betting."""
        strategy = ConservativeStrategy()
        bot = Bot("TestBot", strategy, 500)
        success = bot.make_bet()
        assert success == True
        assert bot.bet > 0
        assert bot.bet <= bot.chips + bot.bet

    def test_bot_decision(self):
        """Test bot decision making."""
        strategy = ConservativeStrategy()
        bot = Bot("TestBot", strategy, 500)
        dealer_card = Card("♦", "7", 7)

        decision = bot.make_decision(dealer_card)
        assert decision in ["hit", "stand"]

        bot.hand.add_card(Card("♥", "10", 10))
        bot.hand.add_card(Card("♠", "5", 5))
        decision = bot.make_decision(dealer_card)
        assert decision == "stand"

        bot.standing = True
        decision = bot.make_decision(dealer_card)
        assert decision == "stand"

        bot.standing = False
        bot.busted = True
        decision = bot.make_decision(dealer_card)
        assert decision == "stand"


class TestDealer:
    def test_dealer_initialization(self):
        """Test dealer initialization."""
        dealer = Dealer()
        assert dealer.name == "Dealer"
        assert dealer.chips == 0

    def test_dealer_should_hit(self):
        """Test dealer hit decision."""
        dealer = Dealer()
        dealer.hand.add_card(Card("♥", "10", 10))
        dealer.hand.add_card(Card("♠", "6", 6))
        assert dealer.should_hit() == True

        dealer.hand.clear()
        dealer.hand.add_card(Card("♥", "10", 10))
        dealer.hand.add_card(Card("♠", "7", 7))
        assert dealer.should_hit() == False

    def test_dealer_soft_17(self):
        """Test dealer soft 17 handling."""
        dealer = Dealer()
        dealer.hand.add_card(Card("♥", "A", 11))
        dealer.hand.add_card(Card("♠", "6", 6))
        assert dealer.should_hit() == True

    def test_dealer_decision(self):
        """Test dealer decision making."""
        dealer = Dealer()
        dealer_card = Card("♦", "7", 7)

        dealer.hand.add_card(Card("♥", "10", 10))
        dealer.hand.add_card(Card("♠", "6", 6))
        assert dealer.make_decision(dealer_card) == "hit"

        dealer.hand.clear()
        dealer.hand.add_card(Card("♥", "10", 10))
        dealer.hand.add_card(Card("♠", "7", 7))
        assert dealer.make_decision(dealer_card) == "stand"
