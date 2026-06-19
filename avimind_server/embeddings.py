import json
from functools import lru_cache
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def generate_embedding(text: str) -> List[float]:
    model = get_embedding_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def embedding_to_json(embedding: List[float]) -> str:
    return json.dumps(embedding)


def embedding_from_json(value: str | None) -> List[float] | None:
    if not value:
        return None

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def cosine_similarity(vector_a: List[float], vector_b: List[float]) -> float:
    a = np.array(vector_a)
    b = np.array(vector_b)

    if a.size == 0 or b.size == 0:
        return 0.0

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)