import ollama
from pprint import pprint


def chat_loop():
    model = "phi3:3.8b"

    # This will store our conversation history
    messages = [
        {
            "role": "system",
            "content": "You are a helpful coding assistant. Be concise and direct.",
        }
    ]

    print("=" * 50)
    print("Chat with Phi3 (type 'quit' to exit)")
    print("=" * 50 + "\n")

    while True:
        # Get user input
        user_input = input("You: ").strip()

        # Exit condition
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye! 👋")
            break

        # Skip empty messages
        if not user_input:
            continue

        if user_input.lower() == "history":
            pprint(messages)
            continue

        # Add user message to history
        messages.append({"role": "user", "content": user_input})

        # Get AI response
        response = ollama.chat(model=model, messages=messages)

        # Extract assistant's message
        assistant_message = response["message"]["content"]

        # Add assistant response to history
        messages.append({"role": "assistant", "content": assistant_message})

        # Display response
        print(f"\nPhi3: {assistant_message}\n")

        print("\n" + "=" * 50 + "\n")
        print(response.eval_count)


if __name__ == "__main__":
    chat_loop()
