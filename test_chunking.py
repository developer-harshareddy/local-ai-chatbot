

from chunking import chunk_text, chunk_pages


# Test 1: Basic text chunking
sample_text = """
MiniBank is a banking application.

It supports customer registration,
account management and transaction processing.

Customers can register using their email address.
The application validates customer information
before saving records in PostgreSQL.
""" * 10

chunks = chunk_text(
    sample_text,
    chunk_size=200,
    overlap=40
)

print("\n========== TEST 1 ==========")
print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {index}:")
    print(chunk)


# Test 2: PDF page chunking
sample_pages = [
    {
        "page": 1,
        "text": "Customer registration and account management. " * 30
    },
    {
        "page": 2,
        "text": "Transaction processing and payment operations. " * 30
    }
]

page_chunks = chunk_pages(
    sample_pages,
    chunk_size=200,
    overlap=40,
    source="banking_document.pdf"
)

print("\n========== TEST 2 ==========")
print("Total page chunks:", len(page_chunks))

for item in page_chunks:
    print("\nID:", item["id"])
    print("Metadata:", item["metadata"])
    print("Text:", item["text"])


# Test 3: Empty input
print("\n========== TEST 3 ==========")
print("Empty text:", chunk_text(""))


print("\nAll chunking tests executed.")
