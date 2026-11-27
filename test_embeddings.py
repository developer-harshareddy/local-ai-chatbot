

from embeddings import EmbeddingService
from chunking import chunk_pages


print("\n========== INITIALIZING EMBEDDING SERVICE ==========")

embedding_service = EmbeddingService()


# Sample extracted PDF pages
sample_pages = [
    {
        "page": 1,
        "text": (
            "MiniBank supports customer registration "
            "and account management. "
        ) * 15
    },
    {
        "page": 2,
        "text": (
            "MiniBank supports transaction processing "
            "and payment operations. "
        ) * 15
    }
]


# Generate text chunks
print("\n========== GENERATING CHUNKS ==========")

chunks = chunk_pages(
    sample_pages,
    chunk_size=200,
    overlap=40,
    source="banking_document.pdf"
)

print("Total chunks:", len(chunks))


# Extract text from chunks
chunk_texts = [item["text"] for item in chunks]


# Generate embeddings
print("\n========== GENERATING EMBEDDINGS ==========")

vectors = embedding_service.generate_embeddings(chunk_texts)


# Verify output
print("\n========== EMBEDDING RESULTS ==========")

print("Total chunks:", len(chunks))
print("Total vectors:", len(vectors))

for index, vector in enumerate(vectors):

    print(f"\nChunk ID: {chunks[index]['id']}")
    print(f"Page: {chunks[index]['metadata']['page']}")
    print(f"Vector dimensions: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")


# Generate a single embedding
print("\n========== SINGLE EMBEDDING TEST ==========")

single_vector = embedding_service.generate_embedding(
    "How can I register a new customer?"
)

print("Single vector dimensions:", len(single_vector))

print("\nAll embedding tests executed successfully.")
