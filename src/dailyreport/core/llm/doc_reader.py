import ollama
from pathlib import Path


def read_document(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return content


def create_base_messages(doc_content: str) -> list:
    return [
        {
            "role": "system",
            "content": f"""You are a helpful assistant that answers questions based on the provided document. 
Only use information from the document. If the answer is not in the document, say so.

Here is the document:

---
{doc_content}
---

Answer questions about this document.""",
        }
    ]


def chat_with_document(file_path: str):
    # Read document once
    doc_content = read_document(file_path)

    messages = create_base_messages(doc_content)

    total_prompt_tokens = 0
    total_response_tokens = 0

    print("=" * 50)
    print("Document Q&A")
    print("=" * 50)
    print(f"Loaded: {file_path}")
    print("-" * 50)
    print("Commands:")
    print("  /clear  - Reset conversation (keep document)")
    print("  /stats  - Show token usage")
    print("  /history - Show conversation length")
    print("  quit    - Exit")
    print("-" * 50 + "\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "q", "exit"]:
            print("Goodbye! 👋")
            break

        if not user_input:
            continue

        if user_input.lower() == "/clear":
            messages = create_base_messages(doc_content)
            total_prompt_tokens = 0
            total_response_tokens = 0
            print("✓ Conversation cleared. Document still loaded.\n")
            continue

        if user_input.lower() == "/stats":
            print(f"Total prompt tokens used: {total_prompt_tokens}")
            print(f"Total response tokens used: {total_response_tokens}")
            print(f"Combined: {total_prompt_tokens + total_response_tokens}\n")
            continue

        if user_input.lower() == "/history":
            qa_pairs = (len(messages) - 1) // 2
            print(f"Messages in history: {len(messages)}")
            print(f"Q&A pairs: {qa_pairs}\n")
            continue

        messages.append({"role": "user", "content": user_input})

        print("AI: ", end="", flush=True)

        full_response = ""
        stream = ollama.chat(
            model="llama3.2:3b",
            messages=messages,
            stream=True,
            options={"temperature": 0.3},
        )

        prompt_tokens = 0
        response_tokens = 0

        for chunk in stream:
            token = chunk["message"]["content"]
            print(token, end="", flush=True)
            full_response += token

            if chunk.get("done"):
                prompt_tokens = chunk.get("prompt_eval_count", 0)
                response_tokens = chunk.get("eval_count", 0)

        # Update totals
        total_prompt_tokens += prompt_tokens
        total_response_tokens += response_tokens

        print(f"\n[prompt: {prompt_tokens}, response: {response_tokens}]\n")

        messages.append({"role": "assistant", "content": full_response})


def main():
    doc_path = "docs/sample.txt"
    chat_with_document(doc_path)


if __name__ == "__main__":
    main()
