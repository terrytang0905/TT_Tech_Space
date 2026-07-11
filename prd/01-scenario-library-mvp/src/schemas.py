"""Validated immutable records used by the retrieval experiment."""

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any, Callable, Dict, Iterable, List, Mapping, Sequence, Set, Tuple, TypeVar


_SCENE_ID = re.compile(r"^SCN-(00[1-9]|0[1-3][0-9]|040)$")
_QUERY_ID = re.compile(r"^Q-(D|G)-\d{3}$")
_QUERY_TYPES = {"exact", "paraphrase", "two-condition", "three-condition", "hard-negative", "out-of-scope"}
T = TypeVar("T")


def _required_text(raw: Mapping[str, Any], key: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value.strip()


def _text_tuple(raw: Mapping[str, Any], key: str) -> Tuple[str, ...]:
    value = raw.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key} must be a non-empty list")
    result = tuple(item.strip() for item in value if isinstance(item, str) and item.strip())
    if len(result) != len(value):
        raise ValueError(f"{key} must contain non-empty strings")
    return result


@dataclass(frozen=True)
class Environment:
    weather: str
    lighting: str
    road_type: str
    surface: str

    @classmethod
    def from_dict(cls, raw: Any) -> "Environment":
        if not isinstance(raw, dict):
            raise ValueError("environment must be an object")
        return cls(*(_required_text(raw, key) for key in ("weather", "lighting", "road_type", "surface")))


@dataclass(frozen=True)
class Scene:
    scene_id: str
    title: str
    summary: str
    environment: Environment
    actors: Tuple[str, ...]
    trigger: str
    system_behavior: str
    expected_behavior: str
    risk: str
    evidence: Tuple[str, ...]
    tags: Tuple[str, ...]
    synthetic: bool
    source_basis: str

    @classmethod
    def from_dict(cls, raw: Any) -> "Scene":
        if not isinstance(raw, dict):
            raise ValueError("scene must be an object")
        scene_id = _required_text(raw, "scene_id")
        if not _SCENE_ID.fullmatch(scene_id):
            raise ValueError("scene_id must match SCN-001 through SCN-040")
        if raw.get("synthetic") is not True:
            raise ValueError("synthetic must be true")
        if raw.get("source_basis") != "method-only":
            raise ValueError("source_basis must be method-only")
        return cls(
            scene_id=scene_id,
            title=_required_text(raw, "title"),
            summary=_required_text(raw, "summary"),
            environment=Environment.from_dict(raw.get("environment")),
            actors=_text_tuple(raw, "actors"),
            trigger=_required_text(raw, "trigger"),
            system_behavior=_required_text(raw, "system_behavior"),
            expected_behavior=_required_text(raw, "expected_behavior"),
            risk=_required_text(raw, "risk"),
            evidence=_text_tuple(raw, "evidence"),
            tags=_text_tuple(raw, "tags"),
            synthetic=True,
            source_basis="method-only",
        )


@dataclass(frozen=True)
class Query:
    query_id: str
    text: str
    query_type: str
    relevance: Mapping[str, int]
    answerable: bool

    @classmethod
    def from_dict(cls, raw: Any) -> "Query":
        if not isinstance(raw, dict):
            raise ValueError("query must be an object")
        query_id = _required_text(raw, "query_id")
        if not _QUERY_ID.fullmatch(query_id):
            raise ValueError("query_id must match Q-D-000 or Q-G-000")
        query_type = _required_text(raw, "query_type")
        if query_type not in _QUERY_TYPES:
            raise ValueError("query_type is unsupported")
        relevance = raw.get("relevance")
        if not isinstance(relevance, dict):
            raise ValueError("relevance must be an object")
        normalized: Dict[str, int] = {}
        for scene_id, grade in relevance.items():
            if not isinstance(scene_id, str) or not _SCENE_ID.fullmatch(scene_id):
                raise ValueError("relevance contains an invalid scene_id")
            if not isinstance(grade, int) or isinstance(grade, bool) or grade < 0 or grade > 3:
                raise ValueError("relevance grades must be integers from 0 to 3")
            normalized[scene_id] = grade
        answerable = raw.get("answerable")
        if not isinstance(answerable, bool):
            raise ValueError("answerable must be boolean")
        if answerable and not any(grade >= 2 for grade in normalized.values()):
            raise ValueError("answerable query requires relevance grade >= 2")
        if not answerable and any(grade >= 2 for grade in normalized.values()):
            raise ValueError("unanswerable query cannot have relevance grade >= 2")
        return cls(query_id, _required_text(raw, "text"), query_type, normalized, answerable)


def validate_query_references(queries: Iterable[Query], scene_ids: Set[str]) -> None:
    for query in queries:
        unknown = set(query.relevance) - scene_ids
        if unknown:
            raise ValueError(f"query {query.query_id} references unknown scene IDs")


def load_jsonl(path: Path, parser: Callable[[Any], T]) -> List[T]:
    records: List[T] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ValueError(f"cannot read {path}: {exc.__class__.__name__}") from exc
    for line_number, line in enumerate(lines, 1):
        try:
            raw = json.loads(line)
            records.append(parser(raw))
        except (json.JSONDecodeError, ValueError, TypeError) as exc:
            raise ValueError(f"invalid record at {path}:{line_number}: {exc.__class__.__name__}") from exc
    return records
