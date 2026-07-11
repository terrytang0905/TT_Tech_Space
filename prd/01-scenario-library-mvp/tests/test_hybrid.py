import unittest

from src.hybrid_retriever import HybridRetriever, hybrid_score, minmax, select_alpha, sparse_dot


class HybridTests(unittest.TestCase):
    def test_constant_scores_normalize_to_zero(self):
        self.assertEqual(minmax([2.0, 2.0]), [0.0, 0.0])

    def test_minmax_maps_extremes_to_zero_and_one(self):
        self.assertEqual(minmax([2.0, 4.0, 3.0]), [0.0, 1.0, 0.5])

    def test_sparse_dot_uses_shared_indices(self):
        self.assertEqual(sparse_dot({1: 2.0, 3: 4.0}, {1: 0.5, 2: 8.0}), 1.0)

    def test_hybrid_score_uses_frozen_alpha(self):
        self.assertEqual(hybrid_score(1.0, 0.0, 0.7), 0.7)

    def test_alpha_selection_tie_defaults_to_point_seven(self):
        selected = select_alpha(lambda alpha: 0.8)
        self.assertEqual(selected, 0.7)

    def test_alpha_selection_chooses_highest_development_score(self):
        scores = {0.5: 0.6, 0.7: 0.8, 0.8: 0.7}
        self.assertEqual(select_alpha(scores.__getitem__), 0.7)

    def test_hybrid_retriever_combines_normalized_scores(self):
        retriever = HybridRetriever(
            dense_vectors={"SCN-001": [1, 0], "SCN-002": [0, 1]},
            sparse_vectors={"SCN-001": {1: 0.1}, "SCN-002": {1: 1.0}},
            alpha=0.7,
        )
        hits = retriever.search([1, 0], {1: 1.0}, 2)
        self.assertEqual(hits[0].scene_id, "SCN-001")
        self.assertGreater(hits[0].score, hits[1].score)


if __name__ == "__main__":
    unittest.main()
