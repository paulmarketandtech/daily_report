import ollama
from pathlib import Path

models = {"llama": "llama3.2:3b", "qwen": "qwen3:4b", "phi": "phi3:3.8b"}


def read_document(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return content


def ask_about_document(file_path: str, question: str) -> str:
    doc_content = read_document(file_path)

    # Create a prompt with the document
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that answers questions based on the provided document. Only use information from the document. If the answer is not in the document, say so.",
        },
        {
            "role": "user",
            "content": f"""Here is a document:

            ---
            {doc_content}
            ---

            My question: {question}""",
        },
    ]
    response = ollama.chat(
        model=models["llama"],
        messages=messages,
        options={"temperature": 0.3},  # low temp for factual answers
        stream=True,
    )
    return response


def main():
    doc_path = "docs/sample.txt"

    print("=" * 50)
    print("Document Q&A")
    print("=" * 50 + "\n")

    # Show document stats
    content = read_document(doc_path)
    word_count = len(content.split())
    char_count = len(content)

    print(f"Loaded: {doc_path}")
    print(f"Words: {word_count}")
    print(f"Characters: {char_count}")
    print("-" * 50 + "\n")

    while True:
        question = input("\nYour question (or 'quit'): ").strip()

        if question.lower() in ["quit", "q", "exit"]:
            break

        if not question:
            continue

        print("\nThinking...\n")
        answer = ask_about_document(doc_path, question)
        # print(f"Answer: {answer}\n")
        for chunk in answer:
            token = chunk["message"]["content"]
            print(token, end="", flush=True)

            if chunk.get("done"):
                print("\n")
                print(chunk)


if __name__ == "__main__":
    main()
