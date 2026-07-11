import unittest

from src.corpus import atomic_facts, build_corpus, render_raw_chunk, render_scene_unit
from src.schemas import Scene
from tests.fixtures import valid_scene


class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.scene = Scene.from_dict(valid_scene())

    def test_raw_chunk_omits_field_labels(self):
        text = render_raw_chunk(self.scene)
        self.assertNotIn("触发事件：", text)
        self.assertNotIn("环境：", text)

    def test_scene_unit_uses_fixed_field_order(self):
        text = render_scene_unit(self.scene)
        labels = ["环境：", "参与者：", "触发事件：", "系统响应：", "期望行为：", "风险：", "证据："]
        positions = [text.index(label) for label in labels]
        self.assertEqual(positions, sorted(positions))

    def test_both_representations_use_identical_atomic_facts(self):
        facts = atomic_facts(self.scene)
        raw = render_raw_chunk(self.scene)
        structured = render_scene_unit(self.scene)
        for fact in facts:
            self.assertIn(fact, raw)
            self.assertIn(fact, structured)

    def test_build_corpus_preserves_scene_order_and_ids(self):
        second = valid_scene()
        second["scene_id"] = "SCN-002"
        items = build_corpus([self.scene, Scene.from_dict(second)], "raw")
        self.assertEqual([item.scene_id for item in items], ["SCN-001", "SCN-002"])

    def test_rejects_unknown_representation(self):
        with self.assertRaisesRegex(ValueError, "representation"):
            build_corpus([self.scene], "unknown")


if __name__ == "__main__":
    unittest.main()
