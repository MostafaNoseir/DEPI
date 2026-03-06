# app/main.py

from app.llm_client import run_llm


def main():
    print("LLM Function Calling Demo (Local)")
    print("Type a request or Ctrl+C to exit")

    while True:
        user_input = input("\nUser: ")
        result = run_llm(user_input)
        print("Assistant:", result)


if __name__ == "__main__":
    main()