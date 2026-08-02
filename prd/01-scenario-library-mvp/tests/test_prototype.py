import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts import build_prototype


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class PrototypeBuildTests(unittest.TestCase):
    def test_payload_uses_frozen_w2_assets(self):
        payload = build_prototype.load_payload(PROJECT_ROOT)

        self.assertEqual(len(payload["scenes"]), 40)
        self.assertEqual(len(payload["queries"]), 36)
        self.assertEqual(set(payload["metrics"]["arms"]), {"A", "B", "C", "D"})
        self.assertIn("Q-G-001", payload["results"])
        self.assertIn("C", payload["results"]["Q-G-001"])

    def test_build_writes_openable_static_html(self):
        with TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "index.html"

            build_prototype.build(PROJECT_ROOT, output)

            html = output.read_text(encoding="utf-8")
            self.assertIn("场景知识 Agent", html)
            self.assertIn("W4 可交互原型", html)
            self.assertIn("prototype-data", html)
            self.assertNotIn("DASHSCOPE_API_KEY", html)

            match = re.search(
                r'<script id="prototype-data" type="application/json">(.*?)</script>',
                html,
                re.S,
            )
            self.assertIsNotNone(match)
            embedded = json.loads(match.group(1))
            self.assertEqual(len(embedded["queries"]), 36)


if __name__ == "__main__":
    unittest.main()
