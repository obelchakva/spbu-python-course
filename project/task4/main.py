import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from task4.blackjack import run_simple_game, strategy_demo

if __name__ == "__main__":
    print("Добро пожаловать в Blackjack!")
    print("Выберите режим:")
    print("1 - Простая игра")
    print("2 - Демонстрация стратегий")

    choice = input("Ваш выбор (1 или 2): ").strip()

    if choice == "1":
        run_simple_game()
    elif choice == "2":
        strategy_demo()
    else:
        print("Запускаю простую игру...")
        run_simple_game()
