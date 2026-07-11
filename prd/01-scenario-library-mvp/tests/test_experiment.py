from decimal import Decimal
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from src.bailian_client import EmbeddingBatch
from src.experiment import ExperimentFailed, run_experiment, verify_artifacts


ROOT = Path(__file__).resolve().parents[1]


class FakeEmbeddingClient:
    def embed(self, texts, output_type, refresh=False):
        dense = []
        sparse = []
        for text in texts:
            digest = hashlib.sha256(text.encode("utf-8")).digest()
            vector = [0.0] * 1024
            for index, value in enumerate(digest):
                vector[index] = (value + 1) / 256.0
            dense.append(tuple(vector))
            sparse.append({int(value): 1.0 for value in digest[:8]} if output_type == "dense&sparse" else {})
        return EmbeddingBatch(tuple(dense), tuple(sparse), len(texts) * 5, 1, 2.0, 0)


class FailingEmbeddingClient(FakeEmbeddingClient):
    def __init__(self):
        self.calls = 0

    def embed(self, texts, output_type, refresh=False):
        self.calls += 1
        if self.calls == 2:
            raise RuntimeError("synthetic API failure")
        return super().embed(texts, output_type, refresh)


class ExperimentTests(unittest.TestCase):
    def test_experiment_runs_all_arms_on_identical_golden_queries(self):
        with tempfile.TemporaryDirectory() as tmp:
            outputs = run_experiment(
                ROOT / "data", FakeEmbeddingClient(), Path(tmp), Decimal("0.0005"), "test-commit"
            )
            self.assertEqual(set(outputs.metrics["arms"]), {"A", "B", "C", "D"})
            by_arm = {arm: [] for arm in "ABCD"}
            for row in outputs.query_results:
                by_arm[row["arm"]].append(row["query_id"])
            self.assertTrue(all(by_arm[arm] == by_arm["A"] for arm in "BCD"))
            self.assertEqual(len(outputs.query_results), 144)

    def test_manifest_contains_reproducibility_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = run_experiment(
                ROOT / "data", FakeEmbeddingClient(), Path(tmp), Decimal("0.0005"), "test-commit"
            ).manifest
            for key in (
                "git_commit", "dataset_sha256", "dev_query_sha256", "golden_query_sha256",
                "python_version", "model", "dimensions", "alpha", "cache", "usage", "status",
            ):
                self.assertIn(key, manifest)
            self.assertEqual(manifest["status"], "success")

    def test_artifacts_can_be_independently_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp)
            run_experiment(ROOT / "data", FakeEmbeddingClient(), artifact_dir, Decimal("0.0005"), "test-commit")
            verified = verify_artifacts(ROOT / "data", artifact_dir)
            self.assertEqual(verified["query_result_count"], 144)

    def test_partial_api_failure_never_writes_success_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp)
            with self.assertRaises(ExperimentFailed):
                run_experiment(ROOT / "data", FailingEmbeddingClient(), artifact_dir, Decimal("0.0005"), "test-commit")
            manifest = json.loads((artifact_dir / "run-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "failed")

    def test_error_analysis_contains_three_weak_cases_per_arm(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp)
            run_experiment(ROOT / "data", FakeEmbeddingClient(), artifact_dir, Decimal("0.0005"), "test-commit")
            text = (artifact_dir / "error-analysis.md").read_text(encoding="utf-8")
            for arm in "ABCD":
                section = text.split(f"## Arm {arm}", 1)[1].split("## Arm", 1)[0]
                self.assertGreaterEqual(section.count("- "), 3, arm)


if __name__ == "__main__":
    unittest.main()
