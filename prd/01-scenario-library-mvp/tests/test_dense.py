import math
import unittest

from src.dense_retriever import DenseRetriever, cosine_similarity


class DenseTests(unittest.TestCase):
    def test_cosine_similarity_has_known_value(self):
        self.assertAlmostEqual(cosine_similarity([1, 0], [1, 1]), 2 ** -0.5)

    def test_zero_vector_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "zero vector"):
            cosine_similarity([0, 0], [1, 0])

    def test_dimension_mismatch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "dimension"):
            cosine_similarity([1, 0], [1])

    def test_non_finite_value_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            cosine_similarity([1, math.nan], [1, 0])

    def test_dense_tie_breaks_by_scene_id(self):
        retriever = DenseRetriever({"SCN-002": [1, 0], "SCN-001": [1, 0]})
        hits = retriever.search([1, 0], 2)
        self.assertEqual([hit.scene_id for hit in hits], ["SCN-001", "SCN-002"])


if __name__ == "__main__":
    unittest.main()
