import json
import tempfile
import unittest
from pathlib import Path

from tests.fixtures import valid_query, valid_scene
from src.schemas import Query, Scene, load_jsonl, validate_query_references


class SchemaTests(unittest.TestCase):
    def test_accepts_a_valid_synthetic_scene(self):
        scene = Scene.from_dict(valid_scene())
        self.assertEqual(scene.scene_id, "SCN-001")
        self.assertTrue(scene.synthetic)

    def test_rejects_non_synthetic_scene(self):
        raw = valid_scene()
        raw["synthetic"] = False
        with self.assertRaisesRegex(ValueError, "synthetic"):
            Scene.from_dict(raw)

    def test_rejects_wrong_source_basis(self):
        raw = valid_scene()
        raw["source_basis"] = "real-enterprise"
        with self.assertRaisesRegex(ValueError, "source_basis"):
            Scene.from_dict(raw)

    def test_rejects_invalid_scene_id(self):
        raw = valid_scene()
        raw["scene_id"] = "scene-1"
        with self.assertRaisesRegex(ValueError, "scene_id"):
            Scene.from_dict(raw)

    def test_rejects_invalid_relevance_grade(self):
        raw = valid_query()
        raw["relevance"] = {"SCN-001": 4}
        with self.assertRaisesRegex(ValueError, "relevance"):
            Query.from_dict(raw)

    def test_rejects_answer_to_unknown_scene(self):
        query = Query.from_dict(valid_query())
        with self.assertRaisesRegex(ValueError, "unknown scene"):
            validate_query_references([query], {"SCN-002"})

    def test_jsonl_error_includes_path_and_line_without_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.jsonl"
            path.write_text('{"secret":"do-not-echo"}\nnot-json\n', encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                load_jsonl(path, Scene.from_dict)
            message = str(caught.exception)
            self.assertIn("bad.jsonl:1", message)
            self.assertNotIn("do-not-echo", message)


if __name__ == "__main__":
    unittest.main()
