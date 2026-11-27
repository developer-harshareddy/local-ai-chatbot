
from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self, model_name="all-MiniLM-L6-v2"):

        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("Embedding model loaded successfully.")

    def generate_embedding(self, text):
        """Convert a single text into a numerical vector."""

        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )
        return embedding.tolist()

    def generate_embeddings(self, texts):
        """
        Convert multiple text chunks into numerical vectors.
        """

        if not texts:
            return []

        if any(not text or not text.strip() for text in texts):
            raise ValueError("All texts must be non-empty")

        embeddings = self.model.encode(
            texts,
            batch_size=8,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        return embeddings.tolist()
