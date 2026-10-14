from sentence_transformers import SentenceTransformer
from app.config import settings

model_name = settings.embed_model

model = SentenceTransformer(model_name)

def embed_text(text: str) -> list:
    embedding = model.encode(text, normalize_embeddings = True)
    return embedding.tolist()

