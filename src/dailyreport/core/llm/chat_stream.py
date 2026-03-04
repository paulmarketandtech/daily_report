import ollama
import sys


def chat_stream():
    model = "phi3:3.8b"

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Be concise and direct.",
        }
    ]

    print("=" * 50)
    print("Streaming Chat (type 'quit' to exit)")
    print("=" * 50 + "\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye! 👋")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        # HERE'S THE MAGIC - stream=True
        print("Phi3: ", end="", flush=True)

        full_response = ""

        stream = ollama.chat(
            model=model,
            messages=messages,
            stream=True,  # <-- This enables streaming!
        )

        # stream is a generator - we iterate over chunks
        for chunk in stream:
            # Each chunk has a piece of the response
            token = chunk["message"]["content"]

            # Print without newline, flush immediately
            print(token, end="", flush=True)

            # Build up the full response
            full_response += token
            if chunk.get("total_duration"):
                print(f"\nnumber of output tokes: {chunk.eval_count}")

        print("\n")

        # Add complete response to history
        messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    chat_stream()
