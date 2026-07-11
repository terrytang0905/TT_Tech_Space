from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest

from scripts.build_dataset import build_dataset_bytes
from src.schemas import Query, Scene, load_jsonl, validate_query_references


ROOT = Path(__file__).resolve().parents[1]


class DatasetContractTests(unittest.TestCase):
    def setUp(self):
        self.scenes = load_jsonl(ROOT / "data/scenes.jsonl", Scene.from_dict)
        self.dev = load_jsonl(ROOT / "data/dev_queries.jsonl", Query.from_dict)
        self.golden = load_jsonl(ROOT / "data/golden_queries.jsonl", Query.from_dict)

    def test_dataset_has_exact_frozen_counts(self):
        self.assertEqual(len(self.scenes), 40)
        self.assertEqual(len(self.dev), 8)
        self.assertEqual(len(self.golden), 36)

    def test_ids_are_unique_and_references_exist(self):
        scene_ids = [scene.scene_id for scene in self.scenes]
        self.assertEqual(len(scene_ids), len(set(scene_ids)))
        query_ids = [query.query_id for query in self.dev + self.golden]
        self.assertEqual(len(query_ids), len(set(query_ids)))
        validate_query_references(self.dev + self.golden, set(scene_ids))

    def test_golden_query_distribution_is_exact(self):
        counts = Counter(query.query_type for query in self.golden)
        self.assertEqual(counts, {
            "exact": 6,
            "paraphrase": 8,
            "two-condition": 8,
            "three-condition": 6,
            "hard-negative": 4,
            "out-of-scope": 4,
        })

    def test_queries_do_not_leak_ids_or_exact_titles(self):
        titles = {scene.title for scene in self.scenes}
        for query in self.dev + self.golden:
            self.assertNotIn("SCN-", query.text)
            self.assertNotIn(query.text, titles)
            self.assertTrue(all(title not in query.text for title in titles))

    def test_every_scene_is_marked_synthetic_and_method_only(self):
        for scene in self.scenes:
            self.assertTrue(scene.synthetic)
            self.assertEqual(scene.source_basis, "method-only")

    def test_scene_summaries_are_between_80_and_150_characters(self):
        for scene in self.scenes:
            self.assertGreaterEqual(len(scene.summary), 80, scene.scene_id)
            self.assertLessEqual(len(scene.summary), 150, scene.scene_id)

    def test_generated_files_are_byte_stable(self):
        generated = build_dataset_bytes()
        for filename, content in generated.items():
            self.assertEqual((ROOT / "data" / filename).read_bytes(), content)

    def test_dataset_contains_at_least_ten_minimal_pair_labels(self):
        pair_tags = [tag for scene in self.scenes for tag in scene.tags if tag.startswith("pair-")]
        counts = Counter(pair_tags)
        self.assertGreaterEqual(sum(1 for count in counts.values() if count == 2), 10)


if __name__ == "__main__":
    unittest.main()
