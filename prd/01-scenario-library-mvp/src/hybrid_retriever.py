"""Exact dense+sparse hybrid retrieval with frozen global weighting."""

import math
from typing import Callable, Dict, List, Mapping, Sequence, Tuple

from .bm25_retriever import SearchHit
from .dense_retriever import cosine_similarity


DEFAULT_ALPHAS = (0.5, 0.7, 0.8)


def sparse_dot(left: Mapping[int, float], right: Mapping[int, float]) -> float:
    shared = set(left).intersection(right)
    score = sum(float(left[index]) * float(right[index]) for index in shared)
    if not math.isfinite(score):
        raise ValueError("sparse score must be finite")
    return score


def minmax(scores: Sequence[float]) -> List[float]:
    if not scores:
        return []
    values = [float(score) for score in scores]
    if any(not math.isfinite(value) for value in values):
        raise ValueError("scores must be finite")
    low, high = min(values), max(values)
    if high == low:
        return [0.0] * len(values)
    return [(value - low) / (high - low) for value in values]


def hybrid_score(dense_score: float, sparse_score: float, alpha: float) -> float:
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must be between zero and one")
    return alpha * dense_score + (1.0 - alpha) * sparse_score


def select_alpha(evaluate: Callable[[float], float], candidates: Sequence[float] = DEFAULT_ALPHAS) -> float:
    if not candidates or 0.7 not in candidates:
        raise ValueError("candidate alphas must include 0.7")
    scored = {float(alpha): float(evaluate(float(alpha))) for alpha in candidates}
    if any(not math.isfinite(score) for score in scored.values()):
        raise ValueError("development scores must be finite")
    best = max(scored.values())
    tied = [alpha for alpha, score in scored.items() if score == best]
    return 0.7 if 0.7 in tied else min(tied)


class HybridRetriever:
    def __init__(
        self,
        dense_vectors: Mapping[str, Sequence[float]],
        sparse_vectors: Mapping[str, Mapping[int, float]],
        alpha: float,
    ):
        if set(dense_vectors) != set(sparse_vectors) or not dense_vectors:
            raise ValueError("dense and sparse scene IDs must match")
        if not 0 <= alpha <= 1:
            raise ValueError("alpha must be between zero and one")
        self._dense = {scene_id: tuple(map(float, vector)) for scene_id, vector in dense_vectors.items()}
        self._sparse = {scene_id: dict(vector) for scene_id, vector in sparse_vectors.items()}
        self._alpha = alpha

    def search(
        self,
        query_dense: Sequence[float],
        query_sparse: Mapping[int, float],
        top_k: int = 5,
    ) -> Tuple[SearchHit, ...]:
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        scene_ids = sorted(self._dense)
        dense_raw = [cosine_similarity(query_dense, self._dense[scene_id]) for scene_id in scene_ids]
        sparse_raw = [sparse_dot(query_sparse, self._sparse[scene_id]) for scene_id in scene_ids]
        dense_normalized = minmax(dense_raw)
        sparse_normalized = minmax(sparse_raw)
        hits = [
            SearchHit(scene_id, hybrid_score(dense, sparse, self._alpha))
            for scene_id, dense, sparse in zip(scene_ids, dense_normalized, sparse_normalized)
        ]
        hits.sort(key=lambda hit: (-hit.score, hit.scene_id))
        return tuple(hits[:top_k])
