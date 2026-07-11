"""Four-arm retrieval experiment orchestration and artifact verification."""

import argparse
from dataclasses import dataclass
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import tempfile
import time
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

from .bailian_client import BailianClient, DIMENSIONS, MODEL, EmbeddingBatch
from .bm25_retriever import BM25Retriever, SearchHit
from .corpus import build_corpus
from .dense_retriever import DenseRetriever
from .hybrid_retriever import HybridRetriever, select_alpha
from .metrics import (
    choose_threshold,
    estimate_cost_cny,
    false_answer_rate,
    ndcg_at_k,
    recall_at_k,
    reciprocal_rank,
    summarize_results,
)
from .schemas import Query, Scene, load_jsonl, validate_query_references


class ExperimentFailed(RuntimeError):
    pass


@dataclass(frozen=True)
class ExperimentOutputs:
    manifest: Mapping[str, Any]
    query_results: Tuple[Mapping[str, Any], ...]
    metrics: Mapping[str, Any]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=path.name, suffix=".tmp", dir=str(path.parent))
    try:
        with open(handle, "w", encoding="utf-8", closefd=True) as stream:
            json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
        Path(temporary_name).replace(path)
    finally:
        temporary = Path(temporary_name)
        if temporary.exists():
            temporary.unlink()


def _atomic_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=path.name, suffix=".tmp", dir=str(path.parent))
    try:
        with open(handle, "w", encoding="utf-8", closefd=True) as stream:
            for row in rows:
                stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
        Path(temporary_name).replace(path)
    finally:
        temporary = Path(temporary_name)
        if temporary.exists():
            temporary.unlink()


def _timed_search(search: Any) -> Tuple[Tuple[SearchHit, ...], float]:
    search()
    samples: List[float] = []
    result: Tuple[SearchHit, ...] = ()
    for _ in range(3):
        started = time.perf_counter_ns()
        result = tuple(search())
        samples.append((time.perf_counter_ns() - started) / 1_000_000)
    return result, sorted(samples)[1]


def _usage_add(total: MutableMapping[str, float], batch: EmbeddingBatch) -> None:
    total["input_tokens"] += batch.input_tokens
    total["request_count"] += batch.request_count
    total["api_latency_ms"] += batch.api_latency_ms
    total["cache_hits"] += batch.cache_hits


def _ranking_row(arm: str, query: Query, hits: Sequence[SearchHit], retrieval_ms: float, api_ms: float) -> Dict[str, Any]:
    ranking = [hit.scene_id for hit in hits]
    return {
        "arm": arm,
        "query_id": query.query_id,
        "query_type": query.query_type,
        "answerable": query.answerable,
        "ranking": ranking,
        "scores": [round(hit.score, 12) for hit in hits],
        "top_score": round(hits[0].score, 12) if hits else None,
        "recall_at_1": recall_at_k(ranking, query.relevance, 1),
        "recall_at_5": recall_at_k(ranking, query.relevance, 5),
        "mrr": reciprocal_rank(ranking, query.relevance),
        "ndcg_at_5": ndcg_at_k(ranking, query.relevance, 5),
        "retrieval_latency_ms": round(retrieval_ms, 6),
        "api_latency_ms": round(api_ms, 6),
        "latency_ms": round(retrieval_ms + api_ms, 6),
    }


def _embed_query(client: Any, text: str, output_type: str, usage: MutableMapping[str, float]) -> EmbeddingBatch:
    batch = client.embed([text], output_type)
    _usage_add(usage, batch)
    return batch


def _arm_metrics(rows: Sequence[Mapping[str, Any]], threshold: Any) -> Dict[str, Any]:
    answerable = [row for row in rows if row["answerable"]]
    summary = summarize_results(answerable)
    summary["query_count"] = len(rows)
    summary["answerable_query_count"] = len(answerable)
    summary["abstention_status"] = threshold.status
    summary["abstention_threshold"] = threshold.threshold
    if threshold.threshold is None:
        summary["false_answer_rate"] = None
    else:
        summary["false_answer_rate"] = false_answer_rate(
            [(float(row["top_score"]), bool(row["answerable"])) for row in rows], threshold.threshold
        )
    return summary


def _slice_metrics(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    slices: Dict[str, Any] = {}
    for query_type in sorted({str(row["query_type"]) for row in rows}):
        selected = [row for row in rows if row["query_type"] == query_type and row["answerable"]]
        if selected:
            slices[query_type] = summarize_results(selected)
    return slices


def _error_analysis(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# W2 Retrieval Error Analysis", "", "由逐查询结果自动生成；数据均为合成场景。", ""]
    for arm in "ABCD":
        candidates = [row for row in rows if row["arm"] == arm and row["answerable"]]
        candidates.sort(key=lambda row: (row["recall_at_5"], row["ndcg_at_5"], row["mrr"], row["query_id"]))
        lines.extend((f"## Arm {arm}", ""))
        for row in candidates[:3]:
            label = "Recall@5 失败" if row["recall_at_5"] == 0 else "低 nDCG 薄弱案例"
            lines.append(
                f"- {row['query_id']}（{row['query_type']}，{label}，nDCG@5={row['ndcg_at_5']:.4f}）："
                f"Top 5 = {', '.join(row['ranking'])}"
            )
        lines.append("")
    return "\n".join(lines)


def run_experiment(
    data_dir: Path,
    client: Any,
    artifact_dir: Path,
    price_per_1k_tokens: Decimal,
    git_commit: str,
) -> ExperimentOutputs:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    manifest: Dict[str, Any] = {
        "status": "failed",
        "git_commit": git_commit,
        "python_version": platform.python_version(),
        "model": MODEL,
        "dimensions": DIMENSIONS,
    }
    _atomic_json(artifact_dir / "run-manifest.json", manifest)
    try:
        scene_path = data_dir / "scenes.jsonl"
        dev_path = data_dir / "dev_queries.jsonl"
        golden_path = data_dir / "golden_queries.jsonl"
        scenes = load_jsonl(scene_path, Scene.from_dict)
        dev_queries = load_jsonl(dev_path, Query.from_dict)
        golden_queries = load_jsonl(golden_path, Query.from_dict)
        if (len(scenes), len(dev_queries), len(golden_queries)) != (40, 8, 36):
            raise ValueError("dataset must contain 40 scenes, 8 dev queries, and 36 golden queries")
        validate_query_references(dev_queries + golden_queries, {scene.scene_id for scene in scenes})

        raw_corpus = build_corpus(scenes, "raw")
        structured_corpus = build_corpus(scenes, "structured")
        usage: Dict[str, float] = {"input_tokens": 0, "request_count": 0, "api_latency_ms": 0.0, "cache_hits": 0}

        raw_dense = client.embed([item.text for item in raw_corpus], "dense")
        structured_dense = client.embed([item.text for item in structured_corpus], "dense")
        structured_hybrid = client.embed([item.text for item in structured_corpus], "dense&sparse")
        for batch in (raw_dense, structured_dense, structured_hybrid):
            _usage_add(usage, batch)

        arm_a = BM25Retriever(raw_corpus)
        arm_b = DenseRetriever(dict(zip((item.scene_id for item in raw_corpus), raw_dense.dense)))
        arm_c = DenseRetriever(dict(zip((item.scene_id for item in structured_corpus), structured_dense.dense)))
        hybrid_dense = dict(zip((item.scene_id for item in structured_corpus), structured_hybrid.dense))
        hybrid_sparse = dict(zip((item.scene_id for item in structured_corpus), structured_hybrid.sparse))

        dev_vectors: Dict[str, Tuple[EmbeddingBatch, EmbeddingBatch]] = {}
        for query in dev_queries:
            dev_vectors[query.query_id] = (
                _embed_query(client, query.text, "dense", usage),
                _embed_query(client, query.text, "dense&sparse", usage),
            )

        def evaluate_alpha(alpha: float) -> float:
            retriever = HybridRetriever(hybrid_dense, hybrid_sparse, alpha)
            values = []
            for query in dev_queries:
                if query.answerable:
                    hybrid_query = dev_vectors[query.query_id][1]
                    ranking = [hit.scene_id for hit in retriever.search(hybrid_query.dense[0], hybrid_query.sparse[0], 5)]
                    values.append(ndcg_at_k(ranking, query.relevance, 5))
            return sum(values) / len(values)

        alpha = select_alpha(evaluate_alpha)
        arm_d = HybridRetriever(hybrid_dense, hybrid_sparse, alpha)

        dev_scores: Dict[str, List[Tuple[float, bool]]] = {arm: [] for arm in "ABCD"}
        for query in dev_queries:
            dense_query, hybrid_query = dev_vectors[query.query_id]
            dev_hits = {
                "A": arm_a.search(query.text, 5),
                "B": arm_b.search(dense_query.dense[0], 5),
                "C": arm_c.search(dense_query.dense[0], 5),
                "D": arm_d.search(hybrid_query.dense[0], hybrid_query.sparse[0], 5),
            }
            for arm, hits in dev_hits.items():
                dev_scores[arm].append((hits[0].score, query.answerable))
        thresholds = {arm: choose_threshold(scores) for arm, scores in dev_scores.items()}

        rows: List[Mapping[str, Any]] = []
        for query in golden_queries:
            dense_query = _embed_query(client, query.text, "dense", usage)
            hybrid_query = _embed_query(client, query.text, "dense&sparse", usage)
            searches = {
                "A": (lambda q=query: arm_a.search(q.text, 5), 0.0),
                "B": (lambda qv=dense_query.dense[0]: arm_b.search(qv, 5), dense_query.api_latency_ms),
                "C": (lambda qv=dense_query.dense[0]: arm_c.search(qv, 5), dense_query.api_latency_ms),
                "D": (lambda d=hybrid_query.dense[0], s=hybrid_query.sparse[0]: arm_d.search(d, s, 5), hybrid_query.api_latency_ms),
            }
            for arm in "ABCD":
                hits, retrieval_ms = _timed_search(searches[arm][0])
                rows.append(_ranking_row(arm, query, hits, retrieval_ms, searches[arm][1]))

        arm_summaries = {}
        slices = {}
        for arm in "ABCD":
            arm_rows = [row for row in rows if row["arm"] == arm]
            arm_summaries[arm] = _arm_metrics(arm_rows, thresholds[arm])
            slices[arm] = _slice_metrics(arm_rows)
        metrics: Dict[str, Any] = {
            "arms": arm_summaries,
            "query_type_slices": slices,
            "comparisons": {
                "C_minus_B": {key: arm_summaries["C"][key] - arm_summaries["B"][key] for key in ("recall_at_5", "ndcg_at_5")},
                "D_minus_C": {key: arm_summaries["D"][key] - arm_summaries["C"][key] for key in ("recall_at_5", "ndcg_at_5")},
                "D_minus_A": {key: arm_summaries["D"][key] - arm_summaries["A"][key] for key in ("recall_at_5", "ndcg_at_5")},
            },
        }

        usage_serialized = {
            "input_tokens": int(usage["input_tokens"]),
            "request_count": int(usage["request_count"]),
            "api_latency_ms": round(usage["api_latency_ms"], 6),
            "cache_hits": int(usage["cache_hits"]),
            "estimated_cost_cny": str(estimate_cost_cny(int(usage["input_tokens"]), price_per_1k_tokens)),
            "price_cny_per_1k_tokens": str(price_per_1k_tokens),
        }
        manifest.update({
            "status": "success",
            "dataset_sha256": _sha256(scene_path),
            "dev_query_sha256": _sha256(dev_path),
            "golden_query_sha256": _sha256(golden_path),
            "alpha": alpha,
            "thresholds": {arm: {"status": value.status, "threshold": value.threshold} for arm, value in thresholds.items()},
            "cache": {"hits": usage_serialized["cache_hits"]},
            "usage": usage_serialized,
        })
        _atomic_jsonl(artifact_dir / "query-results.jsonl", rows)
        _atomic_json(artifact_dir / "metrics.json", metrics)
        (artifact_dir / "error-analysis.md").write_text(_error_analysis(rows), encoding="utf-8")
        _atomic_json(artifact_dir / "run-manifest.json", manifest)
        verify_artifacts(data_dir, artifact_dir)
        return ExperimentOutputs(manifest, tuple(rows), metrics)
    except Exception as exc:
        manifest["status"] = "failed"
        manifest["error_type"] = exc.__class__.__name__
        _atomic_json(artifact_dir / "run-manifest.json", manifest)
        raise ExperimentFailed(f"experiment failed: {exc.__class__.__name__}") from exc


def verify_artifacts(data_dir: Path, artifact_dir: Path) -> Dict[str, Any]:
    manifest = json.loads((artifact_dir / "run-manifest.json").read_text(encoding="utf-8"))
    metrics = json.loads((artifact_dir / "metrics.json").read_text(encoding="utf-8"))
    rows = [json.loads(line) for line in (artifact_dir / "query-results.jsonl").read_text(encoding="utf-8").splitlines()]
    if manifest.get("status") != "success":
        raise ValueError("manifest status is not success")
    expected_hashes = {
        "dataset_sha256": _sha256(data_dir / "scenes.jsonl"),
        "dev_query_sha256": _sha256(data_dir / "dev_queries.jsonl"),
        "golden_query_sha256": _sha256(data_dir / "golden_queries.jsonl"),
    }
    for key, value in expected_hashes.items():
        if manifest.get(key) != value:
            raise ValueError(f"artifact hash mismatch: {key}")
    if len(rows) != 144:
        raise ValueError("query-results must contain 144 rows")
    for arm in "ABCD":
        arm_rows = [row for row in rows if row.get("arm") == arm]
        if len(arm_rows) != 36 or len({row["query_id"] for row in arm_rows}) != 36:
            raise ValueError(f"arm {arm} does not contain 36 unique golden queries")
        answerable = [row for row in arm_rows if row["answerable"]]
        recomputed = summarize_results(answerable)
        for key in ("recall_at_1", "recall_at_5", "mrr", "ndcg_at_5"):
            if abs(recomputed[key] - metrics["arms"][arm][key]) > 1e-12:
                raise ValueError(f"metric mismatch: {arm}.{key}")
    return {"query_result_count": len(rows), "status": "verified"}


def _git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--artifact-dir", type=Path, default=Path("artifacts"))
    parser.add_argument("--price-per-1k", type=Decimal, default=Decimal("0.0005"))
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--refresh-embeddings", action="store_true")
    args = parser.parse_args()
    if args.verify_only:
        print(json.dumps(verify_artifacts(args.data_dir, args.artifact_dir), ensure_ascii=False))
        return
    client = BailianClient.from_env()
    if args.refresh_embeddings:
        original_embed = client.embed
        client.embed = lambda texts, output_type: original_embed(texts, output_type, refresh=True)  # type: ignore
    outputs = run_experiment(args.data_dir, client, args.artifact_dir, args.price_per_1k, _git_commit())
    print(json.dumps({"status": outputs.manifest["status"], "usage": outputs.manifest["usage"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
