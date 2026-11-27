

from chunking import chunk_pages
from embeddings import EmbeddingService
from vector_store import VectorStore


print("\n========== STEP 1: PREPARE SAMPLE DOCUMENT ==========")

sample_pages = [
    {
        "page": 1,
        "text": (
            "MiniBank supports customer registration "
            "and account management. Customers can register "
            "using their email address. "
        ) * 15
    },
    {
        "page": 2,
        "text": (
            "MiniBank supports transaction processing "
            "and payment operations. Customers can transfer "
            "money between accounts. "
        ) * 15
    }
]


print("\n========== STEP 2: GENERATE CHUNKS ==========")

chunks = chunk_pages(
    sample_pages,
    chunk_size=200,
    overlap=40,
    source="banking_document.pdf"
)

print("Total chunks:", len(chunks))


print("\n========== STEP 3: GENERATE EMBEDDINGS ==========")

embedding_service = EmbeddingService()

chunk_texts = [
    item["text"] for item in chunks
]

embeddings = embedding_service.generate_embeddings(
    chunk_texts
)

print("Generated vectors:", len(embeddings))


print("\n========== STEP 4: INITIALIZE CHROMADB ==========")

vector_store = VectorStore()

print(
    "Existing stored chunks:",
    vector_store.get_total_chunks()
)


print("\n========== STEP 5: STORE DOCUMENT CHUNKS ==========")

vector_store.upsert_chunks(
    chunks,
    embeddings
)

print(
    "Total stored chunks:",
    vector_store.get_total_chunks()
)


print("\n========== STEP 6: SEMANTIC SEARCH ==========")

user_question = "How can a customer transfer money?"

query_embedding = embedding_service.generate_embedding(
    user_question
)

search_results = vector_store.search(
    query_embedding,
    top_k=3
)


print("\nQuestion:", user_question)
print("\nTop matching results:")

for index, result in enumerate(search_results, start=1):

    print(f"\nResult {index}")
    print("Chunk ID:", result["id"])
    print("Page:", result["metadata"]["page"])
    print("Source:", result["metadata"]["source"])
    print("Distance:", result["distance"])
    print("Text:", result["text"])


print("\n========== ALL VECTOR STORE TESTS COMPLETED ==========")
