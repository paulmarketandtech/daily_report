import ollama

models = {"llama": "llama3.2:3b", "qwen": "qwen3:4b", "phi": "phi3:3.8b"}


def hello_ollama():
    # Make sure ollama is running! (ollama serve in another terminal)

    response = ollama.chat(
        model=models["phi"],  # or whatever model you have pulled
        messages=[
            {"role": "system", "content": "You are a pirate. Always respond like one."},
            {
                "role": "user",
                "content": "Say hello and introduce yourself in one sentence!",
            },
        ],
    )
    # Let's see what we get back
    print("Full response object:")
    print(response)
    print("\n" + "=" * 50 + "\n")

    # The actual message content
    print("AI Response:")
    print(response["message"]["content"])


if __name__ == "__main__":
    hello_ollama()
