"""Secure Alibaba Cloud Model Studio embedding client."""

from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
import time
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple
from urllib import error, request


MODEL = "text-embedding-v4"
DIMENSIONS = 1024
ENDPOINT = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"
RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class ConfigurationError(ValueError):
    pass


class HttpError(RuntimeError):
    def __init__(self, status: int, service_code: str = "request_failed"):
        self.status = status
        self.service_code = service_code if service_code.replace("_", "").replace("-", "").isalnum() else "request_failed"
        super().__init__(f"Bailian request failed: HTTP {status} ({self.service_code})")


class UrllibTransport:
    def post(self, url: str, headers: Mapping[str, str], payload: Mapping[str, Any]) -> Mapping[str, Any]:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = request.Request(url, data=body, headers=dict(headers), method="POST")
        try:
            with request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            service_code = "request_failed"
            try:
                parsed = json.loads(exc.read().decode("utf-8"))
                candidate = parsed.get("code")
                if isinstance(candidate, str):
                    service_code = candidate
            except (json.JSONDecodeError, UnicodeDecodeError, OSError):
                pass
            raise HttpError(exc.code, service_code) from None
        except error.URLError:
            raise HttpError(503, "network_error") from None


@dataclass(frozen=True)
class EmbeddingBatch:
    dense: Tuple[Tuple[float, ...], ...]
    sparse: Tuple[Mapping[int, float], ...]
    input_tokens: int
    request_count: int
    api_latency_ms: float
    cache_hits: int


def cache_key(text: str, output_type: str) -> str:
    identity = json.dumps({
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "output_type": output_type,
        "text": text,
    }, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def _finite_float(value: Any, label: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)):
        raise ValueError(f"{label} must contain finite numbers")
    return float(value)


class BailianClient:
    def __init__(
        self,
        api_key: Optional[str],
        transport: Optional[Any] = None,
        cache_dir: Optional[Path] = None,
        sleeper: Callable[[float], None] = time.sleep,
    ):
        if not api_key:
            raise ConfigurationError("DASHSCOPE_API_KEY is not set")
        self._api_key = api_key
        self._transport = transport or UrllibTransport()
        self._cache_dir = cache_dir or Path(".cache/embeddings")
        self._sleeper = sleeper

    @classmethod
    def from_env(cls, **kwargs: Any) -> "BailianClient":
        return cls(os.getenv("DASHSCOPE_API_KEY"), **kwargs)

    def _cache_path(self, text: str, output_type: str) -> Path:
        return self._cache_dir / f"{cache_key(text, output_type)}.json"

    def _load_cache(self, text: str, output_type: str) -> Optional[Mapping[str, Any]]:
        path = self._cache_path(text, output_type)
        if not path.exists():
            return None
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            return raw if isinstance(raw, dict) else None
        except (OSError, json.JSONDecodeError):
            return None

    def _write_cache(self, text: str, output_type: str, record: Mapping[str, Any]) -> None:
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        target = self._cache_path(text, output_type)
        handle, temporary_name = tempfile.mkstemp(prefix="embedding-", suffix=".tmp", dir=str(self._cache_dir))
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as stream:
                json.dump(record, stream, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary_name, target)
        finally:
            if os.path.exists(temporary_name):
                os.unlink(temporary_name)

    def _request(self, texts: Sequence[str], output_type: str) -> Tuple[Mapping[str, Any], int, float]:
        payload = {
            "model": MODEL,
            "input": {"texts": list(texts)},
            "parameters": {"dimension": DIMENSIONS, "output_type": output_type},
        }
        headers = {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}
        attempts = 0
        started = time.perf_counter_ns()
        while True:
            attempts += 1
            try:
                response = self._transport.post(ENDPOINT, headers, payload)
                latency_ms = (time.perf_counter_ns() - started) / 1_000_000
                return response, attempts, latency_ms
            except HttpError as exc:
                if exc.status not in RETRYABLE_STATUS or attempts >= 3:
                    raise HttpError(exc.status, exc.service_code) from None
                self._sleeper((0.5, 1.0)[attempts - 1])

    def _parse_record(self, raw: Mapping[str, Any], output_type: str) -> Mapping[str, Any]:
        dense_raw = raw.get("embedding")
        if not isinstance(dense_raw, list) or len(dense_raw) != DIMENSIONS:
            raise ValueError(f"dense embedding must contain {DIMENSIONS} values")
        dense = [_finite_float(value, "dense embedding") for value in dense_raw]
        sparse: Dict[int, float] = {}
        if output_type == "dense&sparse":
            sparse_raw = raw.get("sparse_embedding")
            if not isinstance(sparse_raw, list):
                raise ValueError("sparse_embedding must be present for dense&sparse")
            for item in sparse_raw:
                if not isinstance(item, dict) or not isinstance(item.get("index"), int) or item["index"] < 0:
                    raise ValueError("sparse_embedding contains invalid index")
                sparse[item["index"]] = _finite_float(item.get("value"), "sparse embedding")
        return {"dense": dense, "sparse": sparse}

    def embed(self, texts: Sequence[str], output_type: str, refresh: bool = False) -> EmbeddingBatch:
        if output_type not in {"dense", "dense&sparse"}:
            raise ValueError("output_type must be dense or dense&sparse")
        if not texts or any(not isinstance(text, str) or not text.strip() for text in texts):
            raise ValueError("texts must contain non-empty strings")
        records: List[Optional[Mapping[str, Any]]] = [None] * len(texts)
        missing: List[Tuple[int, str]] = []
        cache_hits = 0
        if not refresh:
            for index, text in enumerate(texts):
                cached = self._load_cache(text, output_type)
                if cached is None:
                    missing.append((index, text))
                else:
                    records[index] = self._parse_record(cached, output_type)
                    cache_hits += 1
        else:
            missing = list(enumerate(texts))

        input_tokens = 0
        request_count = 0
        latency_ms = 0.0
        for start in range(0, len(missing), 10):
            batch = missing[start:start + 10]
            response, attempts, request_latency = self._request([text for _, text in batch], output_type)
            request_count += attempts
            latency_ms += request_latency
            output = response.get("output") if isinstance(response, dict) else None
            embeddings = output.get("embeddings") if isinstance(output, dict) else None
            if not isinstance(embeddings, list) or len(embeddings) != len(batch):
                raise ValueError("embedding response count does not match input")
            parsed_by_index: Dict[int, Mapping[str, Any]] = {}
            for fallback_index, raw in enumerate(embeddings):
                if not isinstance(raw, dict):
                    raise ValueError("embedding response item must be an object")
                response_index = raw.get("text_index", fallback_index)
                if not isinstance(response_index, int) or response_index < 0 or response_index >= len(batch):
                    raise ValueError("embedding response has invalid text_index")
                parsed_by_index[response_index] = self._parse_record(raw, output_type)
            if len(parsed_by_index) != len(batch):
                raise ValueError("embedding response contains duplicate text_index")
            for response_index, (original_index, text) in enumerate(batch):
                record = parsed_by_index[response_index]
                records[original_index] = record
                cached_record = {
                    "embedding": record["dense"],
                    "sparse_embedding": [
                        {"index": index, "value": value}
                        for index, value in sorted(record["sparse"].items())
                    ],
                }
                self._write_cache(text, output_type, cached_record)
            usage = response.get("usage", {})
            tokens = usage.get("total_tokens", 0) if isinstance(usage, dict) else 0
            if not isinstance(tokens, int) or tokens < 0:
                raise ValueError("usage.total_tokens must be a non-negative integer")
            input_tokens += tokens

        if any(record is None for record in records):
            raise ValueError("embedding batch is incomplete")
        complete = [record for record in records if record is not None]
        return EmbeddingBatch(
            dense=tuple(tuple(record["dense"]) for record in complete),
            sparse=tuple(dict(record["sparse"]) for record in complete),
            input_tokens=input_tokens,
            request_count=request_count,
            api_latency_ms=latency_ms,
            cache_hits=cache_hits,
        )
