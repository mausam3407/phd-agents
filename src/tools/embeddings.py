from sentence_transformers import SentenceTransformer
import numpy as np

_MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts):
    return _MODEL.encode(texts, normalize_embeddings=True)


def cosine_similarity(vec1, vec2):
    return float(np.dot(vec1, vec2))
