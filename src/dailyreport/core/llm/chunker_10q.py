import re
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Chunk:
    """Represents a chunk of the document"""

    id: int
    part: str  # "PART I" or "PART II"
    item: str  # "Item 1", "Item 2", etc.
    item_title: str  # "Financial Statements", "MD&A", etc.
    subsection: str  # Optional subsection header
    text: str
    char_count: int
    word_count: int

    def __repr__(self):
        return (
            f"Chunk({self.id}: {self.part} > {self.item} > {self.subsection or 'main'})"
        )


def read_document(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_10q_structure(text: str) -> list[Chunk]:
    """
    Parse 10-Q markdown into structured chunks.
    Respects document hierarchy: Part > Item > Subsection
    """
    chunks = []
    chunk_id = 0

    # Current position trackers
    current_part = ""
    current_item = ""
    current_item_title = ""
    current_subsection = ""

    # Split into lines for processing
    lines = text.split("\n")
    current_content = []

    for line in lines:
        # Check for Part header (# PART I or # PART II)
        part_match = re.match(r"^#\s+(PART\s+[IV]+)", line)
        if part_match:
            # Save previous chunk if exists
            if current_content and current_item:
                chunks.append(
                    create_chunk(
                        chunk_id,
                        current_part,
                        current_item,
                        current_item_title,
                        current_subsection,
                        current_content,
                    )
                )
                chunk_id += 1
                current_content = []

            current_part = part_match.group(1)
            current_item = ""
            current_item_title = ""
            current_subsection = ""
            continue

        # Check for Item header (## Item 1. Title)
        item_match = re.match(r"^##\s+(Item\s+\d+[A-Za-z]?)\.?\s*(.*)", line)
        if item_match:
            # Save previous chunk
            if current_content and current_item:
                chunks.append(
                    create_chunk(
                        chunk_id,
                        current_part,
                        current_item,
                        current_item_title,
                        current_subsection,
                        current_content,
                    )
                )
                chunk_id += 1
                current_content = []

            current_item = item_match.group(1)
            current_item_title = item_match.group(2).strip()
            current_subsection = ""
            continue

        # Check for subsection (### Subsection Title)
        subsection_match = re.match(r"^###\s+(.+)", line)
        if subsection_match:
            # Save previous chunk
            if current_content and current_item:
                chunks.append(
                    create_chunk(
                        chunk_id,
                        current_part,
                        current_item,
                        current_item_title,
                        current_subsection,
                        current_content,
                    )
                )
                chunk_id += 1
                current_content = []

            current_subsection = subsection_match.group(1).strip()
            continue

        # Regular content line
        if line.strip():
            current_content.append(line)

    # Don't forget last chunk!
    if current_content and current_item:
        chunks.append(
            create_chunk(
                chunk_id,
                current_part,
                current_item,
                current_item_title,
                current_subsection,
                current_content,
            )
        )

    return chunks


def create_chunk(
    chunk_id: int,
    part: str,
    item: str,
    item_title: str,
    subsection: str,
    content_lines: list,
) -> Chunk:
    """Helper to create a Chunk object"""
    text = "\n".join(content_lines)
    return Chunk(
        id=chunk_id,
        part=part,
        item=item,
        item_title=item_title,
        subsection=subsection,
        text=text,
        char_count=len(text),
        word_count=len(text.split()),
    )


def display_chunks(chunks: list[Chunk], show_content: bool = False):
    """Display chunk summary"""
    print(f"\n{'=' * 70}")
    print(f"{'ID':<4} {'PART':<8} {'ITEM':<10} {'SUBSECTION':<30} {'WORDS':<8}")
    print("=" * 70)

    for chunk in chunks:
        subsec_display = (
            chunk.subsection[:28] + ".."
            if len(chunk.subsection) > 30
            else chunk.subsection
        )
        print(
            f"{chunk.id:<4} {chunk.part:<8} {chunk.item:<10} {subsec_display:<30} {chunk.word_count:<8}"
        )

        if show_content:
            print(f"    Content preview: {chunk.text[:100]}...")
            print()


def get_chunks_by_item(chunks: list[Chunk], item: str) -> list[Chunk]:
    """Filter chunks by item number"""
    return [c for c in chunks if c.item.lower() == item.lower()]


def get_chunks_by_part(chunks: list[Chunk], part: str) -> list[Chunk]:
    """Filter chunks by part"""
    return [c for c in chunks if part.upper() in c.part.upper()]


def main():
    doc_path = "docs/sample_10q.md"

    print("Parsing 10-Q document...")
    text = read_document(doc_path)
    print(f"Document: {len(text)} chars, {len(text.split())} words\n")

    # Parse into chunks
    chunks = parse_10q_structure(text)
    print(f"Created {len(chunks)} chunks")

    # Display summary
    display_chunks(chunks)

    # Example: Get only Item 2 (MD&A)
    print("\n" + "=" * 70)
    print("Filtering: Only Item 2 (MD&A)")
    print("=" * 70)
    item2_chunks = get_chunks_by_item(chunks, "Item 2")
    display_chunks(item2_chunks, show_content=True)

    # Example: Get Part II only
    print("\n" + "=" * 70)
    print("Filtering: Only Part II")
    print("=" * 70)
    part2_chunks = get_chunks_by_part(chunks, "PART II")
    display_chunks(part2_chunks)


if __name__ == "__main__":
    main()
