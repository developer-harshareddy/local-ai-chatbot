
import chromadb
from embeddings import LocalEmbedder

class VectorStore:
    
    def __init__(self):
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="payment_documents", metadata={"hnsw:space": "cosine"})
        self.embedder = LocalEmbedder()
    
    def add_chunks(self, chunks, document_id, filename):
        if not chunks: return 0
        texts = [c["text"] for c in chunks]
        vectors = self.embedder.embed_texts(texts)
        self.collection.upsert(
            ids=[c["chunk_id"] for c in chunks], documents=texts,
            embeddings=vectors,
            metadatas=[{"document_id": document_id,
                        "source_filename": filename,
                        "page_number": c["page_number"]} for c in chunks])
        return len(chunks)
    
    def search(self, question, top_k=4):
        vector = self.embedder.embed_query(question)
        return self.collection.query(query_embeddings=[vector], n_results=top_k,
            include=["documents", "metadatas", "distances"])
        
        Integrate PDF upload
After Step 7 extracts pages, add an “Index PDF” button. On click call split_into_chunks(pages), create a document_id with uuid4(), then call VectorStore().add_chunks(chunks, document_id, uploaded_pdf.name). Display the number of indexed chunks. Use stable IDs or delete old chunks before re-indexing the same document to avoid duplicate copies.
