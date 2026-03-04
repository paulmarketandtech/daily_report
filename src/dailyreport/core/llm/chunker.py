from pathlib import Path


def read_document(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def chunk_by_chars(text: str, chunk_size: int = 500, overlap: int = 50) -> list[dict]:
    """
    Simple chunking by character count with overlap.

    Args:
        text: The document text
        chunk_size: Characters per chunk
        overlap: Characters to overlap between chunks

    Returns:
        List of chunk dictionaries
    """
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(text):
        # Get chunk
        end = start + chunk_size
        chunk_text = text[start:end]

        # Store chunk with metadata
        chunks.append(
            {
                "id": chunk_id,
                "text": chunk_text,
                "start": start,
                "end": min(end, len(text)),
                "char_count": len(chunk_text),
            }
        )

        # Move start position (subtract overlap)
        start = end - overlap
        chunk_id += 1

    return chunks


def chunk_by_sentences(text: str, max_chunk_size: int = 500) -> list[dict]:
    """
    Chunk by sentences - never cuts mid-sentence.

    Args:
        text: The document text
        max_chunk_size: Target max characters per chunk

    Returns:
        List of chunk dictionaries
    """
    # Simple sentence splitting (handles . ! ?)
    import re

    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    current_chunk = ""
    chunk_id = 0
    start_pos = 0

    for sentence in sentences:
        # If adding this sentence exceeds limit, save current chunk
        if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
            chunks.append(
                {
                    "id": chunk_id,
                    "text": current_chunk.strip(),
                    "char_count": len(current_chunk.strip()),
                }
            )
            chunk_id += 1
            current_chunk = ""

        current_chunk += sentence + " "

    # Don't forget the last chunk!
    if current_chunk.strip():
        chunks.append(
            {
                "id": chunk_id,
                "text": current_chunk.strip(),
                "char_count": len(current_chunk.strip()),
            }
        )

    return chunks


def display_chunks(chunks: list[dict]):
    """Pretty print chunks for inspection"""
    for chunk in chunks:
        print(f"\n{'=' * 50}")
        print(
            f"CHUNK {chunk['id']} | chars: {chunk['char_count']}"  # | pos: {chunk['start']}-{chunk['end']}"
        )
        print("=" * 50)
        print(
            chunk["text"][:200] + "..." if len(chunk["text"]) > 200 else chunk["text"]
        )


def main():
    doc_path = "docs/company_report.txt"

    text = read_document(doc_path)
    print(f"Document length: {len(text)} characters\n")

    # Compare methods
    print("=" * 50)
    print("METHOD 1: Character chunking")
    print("=" * 50)
    char_chunks = chunk_by_chars(text, chunk_size=500, overlap=50)
    print(f"Created {len(char_chunks)} chunks")

    print("\n" + "=" * 50)
    print("METHOD 2: Sentence chunking")
    print("=" * 50)
    sent_chunks = chunk_by_sentences(text, max_chunk_size=500)
    print(f"Created {len(sent_chunks)} chunks")

    # Show sentence chunks
    print("\nSentence-based chunks:")
    display_chunks(sent_chunks)


if __name__ == "__main__":
    main()
