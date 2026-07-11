"""Deterministic BM25 keyword baseline with dependency-free CJK tokens."""

from collections import Counter
from dataclasses import dataclass
import math
import re
from typing import Dict, Iterable, List, Sequence, Tuple

from .corpus import CorpusItem


_SEGMENTS = re.compile(r"[\u3400-\u9fff]+|[a-zA-Z0-9]+(?:[-_.][a-zA-Z0-9]+)*")


@dataclass(frozen=True)
class SearchHit:
    scene_id: str
    score: float


def tokenize(text: str) -> Tuple[str, ...]:
    tokens: List[str] = []
    for segment in _SEGMENTS.findall(text.lower()):
        if "\u3400" <= segment[0] <= "\u9fff":
            tokens.extend(segment)
            tokens.extend(segment[index:index + 2] for index in range(len(segment) - 1))
        else:
            tokens.append(segment)
    return tuple(tokens)


class BM25Retriever:
    def __init__(self, corpus: Sequence[CorpusItem], k1: float = 1.5, b: float = 0.75):
        if not corpus:
            raise ValueError("corpus must not be empty")
        if k1 <= 0 or not 0 <= b <= 1:
            raise ValueError("invalid BM25 parameters")
        self._corpus = tuple(corpus)
        self._k1 = k1
        self._b = b
        self._term_counts = tuple(Counter(tokenize(item.text)) for item in corpus)
        self._lengths = tuple(sum(counts.values()) for counts in self._term_counts)
        self._average_length = sum(self._lengths) / len(self._lengths)
        document_frequency: Counter = Counter()
        for counts in self._term_counts:
            document_frequency.update(counts.keys())
        size = len(corpus)
        self._idf = {
            term: math.log(1.0 + (size - frequency + 0.5) / (frequency + 0.5))
            for term, frequency in document_frequency.items()
        }

    def _score(self, query_tokens: Iterable[str], index: int) -> float:
        counts = self._term_counts[index]
        length = self._lengths[index]
        normalization = self._k1 * (1.0 - self._b + self._b * length / max(self._average_length, 1.0))
        score = 0.0
        for term in set(query_tokens):
            frequency = counts.get(term, 0)
            if frequency:
                score += self._idf.get(term, 0.0) * (frequency * (self._k1 + 1.0)) / (frequency + normalization)
        return score

    def search(self, query: str, top_k: int = 5) -> Tuple[SearchHit, ...]:
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        query_tokens = tokenize(query)
        hits = [SearchHit(item.scene_id, self._score(query_tokens, index)) for index, item in enumerate(self._corpus)]
        hits.sort(key=lambda hit: (-hit.score, hit.scene_id))
        return tuple(hits[:top_k])
