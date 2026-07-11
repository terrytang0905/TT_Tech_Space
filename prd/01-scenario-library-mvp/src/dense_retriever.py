"""Exact dense-vector retrieval for the controlled experiment."""

import math
from typing import Mapping, Sequence, Tuple

from .bm25_retriever import SearchHit


def _validated_vector(vector: Sequence[float]) -> Tuple[float, ...]:
    if not vector:
        raise ValueError("vector must not be empty")
    values = tuple(float(value) for value in vector)
    if any(not math.isfinite(value) for value in values):
        raise ValueError("vector values must be finite")
    return values


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    a = _validated_vector(left)
    b = _validated_vector(right)
    if len(a) != len(b):
        raise ValueError("vector dimension mismatch")
    left_norm = math.sqrt(sum(value * value for value in a))
    right_norm = math.sqrt(sum(value * value for value in b))
    if left_norm == 0 or right_norm == 0:
        raise ValueError("zero vector is not allowed")
    return sum(x * y for x, y in zip(a, b)) / (left_norm * right_norm)


class DenseRetriever:
    def __init__(self, vectors: Mapping[str, Sequence[float]]):
        if not vectors:
            raise ValueError("vectors must not be empty")
        self._vectors = {scene_id: _validated_vector(vector) for scene_id, vector in vectors.items()}
        dimensions = {len(vector) for vector in self._vectors.values()}
        if len(dimensions) != 1:
            raise ValueError("vector dimension mismatch")
        self._dimension = next(iter(dimensions))

    def search(self, query_vector: Sequence[float], top_k: int = 5) -> Tuple[SearchHit, ...]:
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        query = _validated_vector(query_vector)
        if len(query) != self._dimension:
            raise ValueError("query vector dimension mismatch")
        hits = [SearchHit(scene_id, cosine_similarity(query, vector)) for scene_id, vector in self._vectors.items()]
        hits.sort(key=lambda hit: (-hit.score, hit.scene_id))
        return tuple(hits[:top_k])
