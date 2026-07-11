"""Ranking, abstention, latency, and cost metrics for the W2 experiment."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
import math
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


def _relevant_ids(relevance: Mapping[str, int]) -> set:
    return {scene_id for scene_id, grade in relevance.items() if grade >= 2}


def recall_at_k(ranking: Sequence[str], relevance: Mapping[str, int], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be positive")
    relevant = _relevant_ids(relevance)
    if not relevant:
        return 0.0
    return 1.0 if relevant.intersection(ranking[:k]) else 0.0


def reciprocal_rank(ranking: Sequence[str], relevance: Mapping[str, int]) -> float:
    relevant = _relevant_ids(relevance)
    for rank, scene_id in enumerate(ranking, 1):
        if scene_id in relevant:
            return 1.0 / rank
    return 0.0


def _dcg(grades: Sequence[int]) -> float:
    return sum((2 ** grade - 1) / math.log2(rank + 1) for rank, grade in enumerate(grades, 1))


def ndcg_at_k(ranking: Sequence[str], relevance: Mapping[str, int], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be positive")
    actual = [int(relevance.get(scene_id, 0)) for scene_id in ranking[:k]]
    ideal = sorted((int(grade) for grade in relevance.values()), reverse=True)[:k]
    ideal_score = _dcg(ideal)
    return _dcg(actual) / ideal_score if ideal_score else 0.0


def percentile(values: Sequence[float], probability: float) -> float:
    if not values:
        raise ValueError("values must not be empty")
    if not 0 < probability <= 1:
        raise ValueError("probability must be in (0, 1]")
    ordered = sorted(float(value) for value in values)
    if any(not math.isfinite(value) for value in ordered):
        raise ValueError("values must be finite")
    rank = max(1, math.ceil(probability * len(ordered)))
    return ordered[rank - 1]


def estimate_cost_cny(input_tokens: int, price_per_1k_tokens: Decimal) -> Decimal:
    if not isinstance(input_tokens, int) or input_tokens < 0:
        raise ValueError("input_tokens must be a non-negative integer")
    if price_per_1k_tokens < 0:
        raise ValueError("price must not be negative")
    cost = Decimal(input_tokens) / Decimal(1000) * price_per_1k_tokens
    return cost.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class ThresholdSelection:
    status: str
    threshold: Optional[float]


def choose_threshold(examples: Sequence[Tuple[float, bool]]) -> ThresholdSelection:
    if not examples:
        return ThresholdSelection("unvalidated", None)
    positives = [float(score) for score, answerable in examples if answerable]
    negatives = [float(score) for score, answerable in examples if not answerable]
    if not positives or not negatives or any(not math.isfinite(score) for score, _ in examples):
        return ThresholdSelection("unvalidated", None)
    highest_negative = max(negatives)
    lowest_positive = min(positives)
    if lowest_positive <= highest_negative:
        return ThresholdSelection("unvalidated", None)
    return ThresholdSelection("validated", (highest_negative + lowest_positive) / 2.0)


def false_answer_rate(examples: Sequence[Tuple[float, bool]], threshold: float) -> float:
    negatives = [score for score, answerable in examples if not answerable]
    if not negatives:
        return 0.0
    return sum(float(score) >= threshold for score in negatives) / len(negatives)


def summarize_results(rows: Sequence[Mapping[str, float]]) -> Dict[str, float]:
    if not rows:
        raise ValueError("rows must not be empty")
    keys = ("recall_at_1", "recall_at_5", "mrr", "ndcg_at_5")
    summary = {key: sum(float(row[key]) for row in rows) / len(rows) for key in keys}
    latencies = [float(row["latency_ms"]) for row in rows]
    summary["latency_p50_ms"] = percentile(latencies, 0.50)
    summary["latency_p95_ms"] = percentile(latencies, 0.95)
    return summary
