import ollama


def test_temperatures():
    """
    Compare responses at different temperatures
    """
    prompt = "Hello, how are you?"

    for temp in [0.2, 0.5, 0.8, 1.0]:
        print(f"\n=== Temperature: {temp} ===")

        response = ollama.chat(
            model="phi3:3.8b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Be concise.",
                },
                {"role": "user", "content": prompt},
            ],
            options={"temperature": temp},
        )

        print(response["message"]["content"])


if __name__ == "__main__":
    test_temperatures()
