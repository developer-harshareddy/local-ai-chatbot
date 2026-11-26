
from sentence_transformers import SentenceTransformer

MODEL_PATH = "sentence-transformers/all-MiniLM-L6-v2"

class LocalEmbedder:
    
    def __init__(self, model_path=MODEL_PATH):
        self.model = SentenceTransformer(model_path)
    
    def embed_texts(self, texts):
        vectors = self.model.encode(texts, normalize_embeddings=True,
                                    show_progress_bar=False)
        return vectors.tolist()
    
    def embed_query(self, question):
        return self.embed_texts([question])[0]