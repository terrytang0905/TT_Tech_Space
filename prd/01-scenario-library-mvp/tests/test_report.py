import unittest

from scripts.build_report import build_report, decide_prd_branch


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
        metrics = {
            "arms": {
                "A": {"recall_at_1": .8571, "recall_at_5": .9643, "mrr": .9018, "ndcg_at_5": .9187, "false_answer_rate": 0, "latency_p50_ms": .2, "latency_p95_ms": .25},
                "B": {"recall_at_1": .9286, "recall_at_5": 1, "mrr": .9643, "ndcg_at_5": .9752, "false_answer_rate": .125, "latency_p50_ms": 407.6, "latency_p95_ms": 632.37},
                "C": {"recall_at_1": 1, "recall_at_5": 1, "mrr": 1, "ndcg_at_5": .9978, "false_answer_rate": .125, "latency_p50_ms": 405.27, "latency_p95_ms": 632.55},
                "D": {"recall_at_1": .9643, "recall_at_5": 1, "mrr": .9821, "ndcg_at_5": .9856, "false_answer_rate": .5, "latency_p50_ms": 403.73, "latency_p95_ms": 696.11},
            },
            "comparisons": {
                "C_minus_B": {"recall_at_5": 0, "ndcg_at_5": .0226},
                "D_minus_C": {"recall_at_5": 0, "ndcg_at_5": -.0122},
                "D_minus_A": {"recall_at_5": .0357, "ndcg_at_5": .0669},
            },
        }
        manifest = {
            "git_commit": "fixture-commit",
            "model": "text-embedding-v4",
            "dimensions": 1024,
            "alpha": .8,
            "dataset_sha256": "scene-hash",
            "dev_query_sha256": "dev-hash",
            "golden_query_sha256": "golden-hash",
            "usage": {"input_tokens": 11043, "request_count": 100, "api_latency_ms": 46667.5, "estimated_cost_cny": "0.005522", "cache_hits": 0},
        }
        report = build_report(metrics, manifest, "three weak cases")
        self.assertIn("11,043", report)
        self.assertIn("0.005522", report)
        self.assertIn("结构化场景 Schema：P0", report)
        self.assertIn("Dense + Sparse：P1", report)
        self.assertIn("three weak cases", report)


if __name__ == "__main__":
    unittest.main()
