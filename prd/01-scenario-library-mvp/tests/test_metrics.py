from decimal import Decimal
import unittest

from src.metrics import (
    choose_threshold,
    estimate_cost_cny,
    false_answer_rate,
    ndcg_at_k,
    percentile,
    recall_at_k,
    reciprocal_rank,
)


class MetricsTests(unittest.TestCase):
    def test_recall_at_five_uses_grade_two_as_relevant(self):
        self.assertEqual(recall_at_k(["B", "A"], {"A": 2}, 5), 1.0)
        self.assertEqual(recall_at_k(["B", "A"], {"A": 2}, 1), 0.0)

    def test_mrr_is_inverse_first_relevant_rank(self):
        self.assertEqual(reciprocal_rank(["X", "A"], {"A": 3}), 0.5)
        self.assertEqual(reciprocal_rank(["X"], {"A": 3}), 0.0)

    def test_ndcg_is_one_for_ideal_order(self):
        self.assertAlmostEqual(ndcg_at_k(["A", "B"], {"A": 3, "B": 1}, 5), 1.0)

    def test_ndcg_penalizes_reversed_order(self):
        self.assertLess(ndcg_at_k(["B", "A"], {"A": 3, "B": 1}, 5), 1.0)

    def test_nearest_rank_percentile(self):
        self.assertEqual(percentile([1, 2, 3, 4], 0.50), 2.0)
        self.assertEqual(percentile([1, 2, 3, 4], 0.95), 4.0)

    def test_cost_uses_tokens_and_per_thousand_price(self):
        self.assertEqual(estimate_cost_cny(2000, Decimal("0.0005")), Decimal("0.001000"))

    def test_threshold_is_selected_only_when_it_perfectly_separates_dev_examples(self):
        result = choose_threshold([(0.9, True), (0.8, True), (0.3, False), (0.1, False)])
        self.assertEqual(result.status, "validated")
        self.assertGreater(result.threshold, 0.3)
        self.assertLessEqual(result.threshold, 0.8)

    def test_overlapping_scores_leave_threshold_unvalidated(self):
        result = choose_threshold([(0.7, True), (0.8, False)])
        self.assertEqual(result.status, "unvalidated")
        self.assertIsNone(result.threshold)

    def test_false_answer_rate_counts_unanswerable_queries_above_threshold(self):
        rate = false_answer_rate([(0.8, False), (0.2, False), (0.9, True)], threshold=0.5)
        self.assertEqual(rate, 0.5)


if __name__ == "__main__":
    unittest.main()
