
from uuid import uuid4


def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Divide text into smaller overlapping chunks.

    Args:
        text: Input text.
        chunk_size: Maximum approximate characters per chunk.
        overlap: Number of characters shared between chunks.

    Returns:
        List of text chunks.
    """

    if not text or not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be >= 0 and smaller than chunk_size"
        )

    text = text.strip()
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(start + chunk_size, text_length)

        # Prefer splitting at a word boundary.
        if end < text_length:
            split_position = text.rfind(
                " ",
                start + int(chunk_size * 0.7),
                end
            )

            if split_position > start:
                end = split_position

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        # Move forward while retaining overlapping context.
        start = end - overlap

    return chunks


def chunk_pages(pages, chunk_size=1000, overlap=200, source=None):
    """
    Convert extracted PDF pages into chunks with metadata.

    Args:
        pages: List returned by extract_pdf_text().
        chunk_size: Maximum approximate characters per chunk.
        overlap: Overlapping characters between chunks.
        source: Optional PDF filename.

    Returns:
        List of dictionaries containing chunk text and metadata.
    """

    all_chunks = []

    for page_data in pages:

        page_number = page_data["page"]
        page_text = page_data["text"]

        page_chunks = chunk_text(
            page_text,
            chunk_size=chunk_size,
            overlap=overlap
        )

        for index, chunk in enumerate(page_chunks, start=1):

            all_chunks.append({
                "id": f"page-{page_number}-chunk-{index}",
                "text": chunk,
                "metadata": {
                    "page": page_number,
                    "chunk_index": index,
                    "source": source or "uploaded_document"
                }
            })

    return all_chunks