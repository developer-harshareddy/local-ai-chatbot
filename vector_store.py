
import chromadb
from pathlib import Path


class VectorStore:

    def __init__(
        self,
        persist_directory="chroma_db",
        collection_name="pdf_documents"
    ):
        """
        Initialize persistent ChromaDB storage.
        """

        self.persist_directory = str(Path(persist_directory))

        self.client = chromadb.PersistentClient(
            path=self.persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        print("ChromaDB initialized successfully.")
        print("Storage directory:", self.persist_directory)
        print("Collection:", collection_name)
    def upsert_chunks(self, chunks, embeddings):
        """
        Store or update document chunks and their embeddings.
        """

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match"
            )

        if not chunks:
            return

        ids = [item["id"] for item in chunks]

        documents = [
            item["text"] for item in chunks
        ]

        metadatas = [
            item["metadata"] for item in chunks
        ]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(f"Successfully stored {len(chunks)} chunks.")

    def search(self, query_embedding, top_k=3):
        """
        Search for the most relevant document chunks.
        """

        if not query_embedding:
            raise ValueError("Query embedding cannot be empty")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")

        total_chunks = self.collection.count()

        if total_chunks == 0:
             return []

        results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=min(top_k, total_chunks),
                    include=[
                            "documents",
                            "metadatas",
                            "distances"
            ]
        )

        matches = []

        if not results["ids"] or not results["ids"][0]:
            return matches

        for index, chunk_id in enumerate(results["ids"][0]):

            matches.append({
                "id": chunk_id,
                "text": results["documents"][0][index],
                "metadata": results["metadatas"][0][index],
                "distance": results["distances"][0][index]
            })

        return matches

    def get_total_chunks(self):
        """
        Return the total number of stored chunks.
        """

        return self.collection.count()
    