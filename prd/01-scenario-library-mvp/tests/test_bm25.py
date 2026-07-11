import unittest

from src.bm25_retriever import BM25Retriever, tokenize
from src.corpus import CorpusItem


class BM25Tests(unittest.TestCase):
    def test_chinese_tokenizer_emits_terms_and_bigrams(self):
        tokens = tokenize("夜间逆光 warning-01")
        self.assertIn("逆光", tokens)
        self.assertIn("warning-01", tokens)

    def test_exact_rare_term_ranks_matching_scene_first(self):
        corpus = (
            CorpusItem("SCN-001", "城市道路正常通行"),
            CorpusItem("SCN-002", "施工锥桶引导临时改道"),
        )
        retriever = BM25Retriever(corpus)
        self.assertEqual(retriever.search("施工锥桶", 1)[0].scene_id, "SCN-002")

    def test_ties_are_broken_by_scene_id(self):
        corpus = (
            CorpusItem("SCN-002", "共同词"),
            CorpusItem("SCN-001", "共同词"),
        )
        hits = BM25Retriever(corpus).search("共同词", 2)
        self.assertEqual([hit.scene_id for hit in hits], ["SCN-001", "SCN-002"])

    def test_empty_query_returns_stable_zero_score_hits(self):
        corpus = (CorpusItem("SCN-002", "甲"), CorpusItem("SCN-001", "乙"))
        hits = BM25Retriever(corpus).search("", 2)
        self.assertEqual([(hit.scene_id, hit.score) for hit in hits], [("SCN-001", 0.0), ("SCN-002", 0.0)])

    def test_invalid_top_k_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "top_k"):
            BM25Retriever((CorpusItem("SCN-001", "文本"),)).search("文本", 0)


if __name__ == "__main__":
    unittest.main()
