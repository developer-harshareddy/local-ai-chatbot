

from rag_service import RAGService


def main():

    print("\n========== RAG TEST ==========")

    rag_service = RAGService()

    question = "How can a customer transfer money?"

    print("\nQuestion:")
    print(question)

    print("\nRetrieving relevant document chunks...")

    results = rag_service.retrieve_context(
        question=question,
        top_k=3
    )

    if not results:
        print("\nNo relevant document chunks found.")
        return

    print(f"\nRetrieved {len(results)} chunks.")

    for index, result in enumerate(results, start=1):

        metadata = result.get("metadata", {})

        print(f"\n----- RESULT {index} -----")
        print("Source:", metadata.get("source"))
        print("Page:", metadata.get("page"))
        print("Distance:", round(result.get("distance", 0), 4))
        print("Content:", result.get("text"))

    print("\n========== BUILDING RAG PROMPT ==========")

    messages = rag_service.build_rag_messages(
        question=question,
        results=results
    )

    for message in messages:

        print(f"\nROLE: {message['role']}")
        print(message["content"])

    print("\nRAG retrieval and prompt generation completed.")


if __name__ == "__main__":
    main()
