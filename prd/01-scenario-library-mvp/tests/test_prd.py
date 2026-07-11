from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PRD = ROOT / "prd.md"


class PrdEvidenceTests(unittest.TestCase):
    def test_prd_exists_and_has_twelve_numbered_sections(self):
        text = PRD.read_text(encoding="utf-8")
        headings = re.findall(r"^## (\d+)\.", text, flags=re.MULTILINE)
        self.assertEqual(headings, [str(number) for number in range(1, 13)])

    def test_prd_uses_measured_w2_decision_branch(self):
        text = PRD.read_text(encoding="utf-8")
        self.assertIn("结构化场景单元 + Dense", text)
        self.assertIn("Dense + Sparse | P1", text)
        self.assertIn("Recall@1 | 100.00%", text)
        self.assertIn("nDCG@5 | 0.9978", text)
        self.assertIn("无答案误召回率 | 12.50%", text)

    def test_prd_keeps_abstention_unvalidated(self):
        text = PRD.read_text(encoding="utf-8")
        self.assertIn("自动阈值拒答 | P1（待验证）", text)
        self.assertNotIn("拒答能力已验证", text)

    def test_prd_has_no_placeholders(self):
        text = PRD.read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"\bTBD\b", text))
        for placeholder in ("TODO", "待补充", "[产品名称]", "XX%", "XXX"):
            self.assertNotIn(placeholder, text)


if __name__ == "__main__":
    unittest.main()
