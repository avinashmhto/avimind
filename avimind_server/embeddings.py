import json
from functools import lru_cache
from typing import List, Optional

import numpy as np
from fastembed import TextEmbedding


MODEL_NAME = "BAAI/bge-small-en-v1.5"


@lru_cache(maxsize=1)
def get_embedding_model() -> TextEmbedding:
    return TextEmbedding(model_name=MODEL_NAME)


def generate_embedding(text: str) -> List[float]:
    model = get_embedding_model()
    embeddings = list(model.embed([text]))

    if not embeddings:
        return []

    return embeddings[0].tolist()


def embedding_to_json(embedding: List[float]) -> str:
    return json.dumps(embedding)


def embedding_from_json(value: Optional[str]) -> Optional[List[float]]:
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