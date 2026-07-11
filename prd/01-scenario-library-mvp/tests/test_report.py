import json
from pathlib import Path
import unittest

from scripts.build_report import build_report, decide_prd_branch


ROOT = Path(__file__).resolve().parents[1]


class ReportTests(unittest.TestCase):
    def test_decision_keeps_scene_schema_and_defers_hybrid(self):
        metrics = {
            "arms": {
                "B": {"recall_at_5": 1.0, "ndcg_at_5": 0.97},
                "C": {"recall_at_5": 1.0, "ndcg_at_5": 0.99},
                "D": {"recall_at_5": 1.0, "ndcg_at_5": 0.98},
                "A": {"recall_at_5": 0.95, "ndcg_at_5": 0.91},
            }
        }
        self.assertEqual(decide_prd_branch(metrics), "scene-p0-hybrid-p1")

    def test_report_reads_measured_usage_and_metrics(self):
        metrics = json.loads((ROOT / "artifacts/metrics.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "artifacts/run-manifest.json").read_text(encoding="utf-8"))
        report = build_report(metrics, manifest, "three weak cases")
        self.assertIn("11,043", report)
        self.assertIn("0.005522", report)
        self.assertIn("结构化场景 Schema：P0", report)
        self.assertIn("Dense + Sparse：P1", report)
        self.assertIn("three weak cases", report)


if __name__ == "__main__":
    unittest.main()
