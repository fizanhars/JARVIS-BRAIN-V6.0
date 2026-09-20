from brain.orchestrator import process
from brain.memory import init_memory, save_memory


def main():
    init_memory()

    print("=" * 40)
    print("       JARVIS BRAIN V6.0")
    print("=" * 40)
    print("Type 'exit' to stop.\n")

    while True:
        user_input = input("You > ").strip()

        if user_input.lower() == "exit":
            print("JARVIS > Goodbye!")
            break

        if not user_input:
            continue

        response = process(user_input)
        print(f"\nJARVIS > {response}\n")

        save_memory(user_input)


if __name__ == "__main__":
    main()
