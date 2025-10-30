"""
Специальный пример, демонстрирующий обработку ситуации с блэкджеком у дилера.
Показывает, как игра реагирует на эту особую ситуацию.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.game import Game
from core.deck import Deck
from core.card import Card
from strategies.conservative import ConservativeStrategy
from strategies.aggressive import AggressiveStrategy


class GuaranteedBlackjackDeck(Deck):
    """Колода, которая гарантирует блэкджек дилеру во втором раунде"""

    def __init__(self, num_decks=1):
        super().__init__(num_decks)
        self.current_round = 0
        self.card_count = 0
        self.blackjack_round_cards = None
        self._prepare_blackjack_cards()

    def _prepare_blackjack_cards(self):
        """Подготовка карт для гарантированного блэкджека дилера"""
        # Для второго раунда: дилер получает A и 10 (блэкджек)
        # Игроки получают карты, которые не дают блэкджек
        self.blackjack_round_cards = [
            # Первые карты игроков
            Card("Hearts", "7", 7),  # Игрок1 первая карта
            Card("Diamonds", "8", 8),  # Игрок2 первая карта
            # Первая карта дилера (открытая) - ТУЗ
            Card("Spades", "A", 11),
            # Вторые карты игроков
            Card("Hearts", "9", 9),  # Игрок1 вторая карта
            Card("Diamonds", "6", 6),  # Игрок2 вторая карта
            # Вторая карта дилера (скрытая) - 10
            Card("Spades", "K", 10),
        ]

    def start_new_round(self):
        """Вызывается в начале каждого раунда"""
        self.current_round += 1
        self.card_count = 0
        print(f"🔢 Начало раунда {self.current_round}, сброс счетчика карт")

    def deal_card(self):
        """Выдача карты с гарантированным блэкджеком во втором раунде"""
        self.card_count += 1

        # Для второго раунда используем фиксированные карты для начальной раздачи
        if self.current_round == 2 and self.card_count <= len(
            self.blackjack_round_cards
        ):
            card = self.blackjack_round_cards[self.card_count - 1]
            print(
                f"🎯 Контролируемая выдача: {card} (карта #{self.card_count} в раунде {self.current_round})"
            )
            return card

        # Для всех остальных случаев используем обычную логику
        card = super().deal_card()
        print(
            f"🎲 Случайная карта: {card} (карта #{self.card_count} в раунде {self.current_round})"
        )
        return card


class BlackjackDemoGame(Game):
    """Специальная версия игры для демонстрации блэкджека дилера"""

    def __init__(self, num_decks=1, max_rounds=2):
        super().__init__(num_decks, max_rounds)
        # Заменяем колоду на нашу контролируемую версию
        self.deck = GuaranteedBlackjackDeck(num_decks)

    def play_round(self):
        """Переопределяем метод раунда для использования контролируемой колоды"""
        if not self.is_game_active or self.current_round >= self.max_rounds:
            return {"game_over": True}

        # Сообщаем колоде о начале нового раунда
        self.deck.start_new_round()

        self.current_round += 1
        round_info = {
            "round": self.current_round,
            "bets": [],
            "card_dealing": [],
            "player_turns": [],
            "dealer_turn": {},
            "results": [],
            "final_state": {},
        }

        print(f"\n{'='*60}")
        print(f"🎰 РАУНД {self.current_round}")
        print(f"{'='*60}")

        # Сброс состояний
        self._reset_round()

        # Ставки
        self._place_bets(round_info)

        # Раздача карт
        self._deal_initial_cards(round_info)

        # Проверка блэкджека у дилера
        if self._check_dealer_blackjack(round_info):
            # Сохраняем финальное состояние
            round_info["final_state"] = self.get_game_state()
            # Сохраняем раунд в историю
            self._save_round_to_history(round_info)
            return round_info

        # Ходы игроков
        self._play_players_turns(round_info)

        # Ход дилера
        self._play_dealer_turn(round_info)

        # Определение победителей
        self._determine_winners(round_info)

        # Сохраняем финальное состояние
        round_info["final_state"] = self.get_game_state()

        # Сохраняем раунд в историю
        self._save_round_to_history(round_info)

        # Обновление состояния игры
        self._check_game_status()

        return round_info


def run_dealer_blackjack_example():
    """Пример обработки блэкджека у дилера с гарантированным сценарием"""
    print("=" * 80)
    print("ПРИМЕР: BLACKJACK У ДИЛЕРА (ГАРАНТИРОВАННЫЙ)")
    print("=" * 80)
    print("Этот пример специально настроен для демонстрации ситуации,")
    print("когда у дилера выпадает блэкджек, и как это влияет на игру.")
    print("Во втором раунде дилер ГАРАНТИРОВАННО получает блэкджек.")
    print("=" * 80)

    # Создаем специальную игру для демонстрации
    game = BlackjackDemoGame(num_decks=1, max_rounds=2)

    # Добавляем игроков
    game.add_bot("Игрок1", ConservativeStrategy(), 500)
    game.add_bot("Игрок2", AggressiveStrategy(), 500)

    game.start_game()

    print("\n🎰 РАУНД 1 - ОБЫЧНАЯ СИТУАЦИЯ")
    print("-" * 40)
    print("В этом раунде карты раздаются случайно, как в обычной игре.")
    game.play_round()

    # Показываем отчет по первому раунду
    game.show_round_report(1)

    # Второй раунд - гарантированный блэкджек дилера
    print(f"\n{'='*80}")
    print("🎰 РАУНД 2 - ГАРАНТИРОВАННЫЙ BLACKJACK У ДИЛЕРА")
    print(f"{'='*80}")

    print("\n💥 ГАРАНТИРОВАННАЯ СИТУАЦИЯ: У ДИЛЕРА BLACKJACK!")
    print("В этом раунде дилер гарантированно получает:")
    print("   • Первая карта: A of Spades ♠")
    print("   • Вторая карта: K of Spades ♠")
    print("Это автоматически завершает раунд и влияет на всех игроков.")
    print("\nПРАВИЛА ПРИ BLACKJACKE ДИЛЕРА:")
    print("• Игроки с блэкджеком получают возврат ставки (ничья)")
    print("• Игроки без блэкджера проигрывают свои ставки")
    print("• Дальнейшие ходы игроков не происходят")

    # Играем второй раунд с гарантированным блэкджеком дилера
    game.play_round()

    # Показываем отчет
    game.show_round_report(2)

    print(f"\n{'='*80}")
    print("АНАЛИЗ ВЛИЯНИЯ BLACKJACKA ДИЛЕРА")
    print(f"{'='*80}")

    final_state = game.get_game_state()

    print(f"\n📊 СРАВНЕНИЕ РЕЗУЛЬТАТОВ:")
    for player in final_state["players"]:
        # Находим изменение после второго раунда
        if len(game.round_history) >= 2:
            after_round1 = game.round_history[0]["final_state"]
            player_after_1 = next(
                (p for p in after_round1["players"] if p["name"] == player["name"]),
                None,
            )

            if player_after_1:
                change_round2 = player["chips"] - player_after_1["chips"]
                trend = "📈" if change_round2 > 0 else "📉" if change_round2 < 0 else "➡️"
                print(
                    f"   {trend} {player['name']}: {player['chips']} фишек (изменение во 2 раунде: {change_round2:+})"
                )

    print(f"\n📝 ДЕТАЛИ ВТОРОГО РАУНДА:")
    print("   • Дилер получил: A of Spades ♠ и K of Spades ♠ = BLACKJACK!")
    print("   • Игрок1 получил: 7 of Hearts ♥ и 9 of Hearts ♥ (сумма: 16)")
    print("   • Игрок2 получил: 8 of Diamonds ♦ и 6 of Diamonds ♦ (сумма: 14)")
    print("   • Оба игрока проиграли, так как у дилера блэкджек")

    print(f"\n💡 ВЫВОДЫ:")
    print("   • Blackjack дилера - мощное событие, влияющее на всех игроков")
    print("   • Игроки не могут ничего сделать против blackjack'а дилера")
    print("   • Единственная защита - тоже иметь blackjack для ничьей")
    print("   • Это демонстрирует элемент случайности в игре")
    print("   • В долгосрочной перспективе такие ситуации уравновешиваются")


if __name__ == "__main__":
    run_dealer_blackjack_example()
