
import re
from uuid import uuid4

def split_into_chunks(pages, chunk_words=650, overlap_words=100):

    if chunk_words <= 0 or not 0 <= overlap_words < chunk_words:
        raise ValueError("Require chunk_words > overlap_words >= 0")

    chunks = []

    for page in pages:  # each item: {"page": 1, "text": "..."}
        words = re.sub(r"\\s+", " ", page["text"]).strip().split()
        start = 0
        while start < len(words):
            end = min(start + chunk_words, len(words))
            text = " ".join(words[start:end]).strip()
            if text:
                chunks.append({"chunk_id": str(uuid4()),
                               "page_number": int(page["page"]), "text": text})
            if end == len(words):
                break
            start = end - overlap_words
    return chunks