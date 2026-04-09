from core.agent import MemoryAgent

def run_lab():
    bot = MemoryAgent()

    print("\n--- Test 1: Saving FACT ---")
    print(bot.handle_input("I love Italian food."))

    print("\n--- Test 2: Saving EVENT ---")
    print(bot.handle_input("Yesterday I went to a restaurant with my friends."))

    print("\n--- Test 3: Memory usage ---")
    print(bot.handle_input("What should I do tonight?"))

if __name__ == "__main__":
    run_lab()