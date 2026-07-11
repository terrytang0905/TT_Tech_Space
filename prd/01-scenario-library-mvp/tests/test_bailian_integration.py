import os
from pathlib import Path
import tempfile
import unittest

from src.bailian_client import BailianClient


@unittest.skipUnless(
    os.getenv("RUN_BAILIAN_INTEGRATION") == "1" and os.getenv("DASHSCOPE_API_KEY"),
    "explicit Bailian integration opt-in required",
)
class BailianIntegrationTests(unittest.TestCase):
    def test_real_api_returns_dense_and_sparse_vectors(self):
        with tempfile.TemporaryDirectory() as tmp:
            batch = BailianClient.from_env(cache_dir=Path(tmp)).embed(
                ["雨夜行人突然横穿"], "dense&sparse", refresh=True
            )
        self.assertEqual(len(batch.dense[0]), 1024)
        self.assertTrue(batch.sparse[0])
        self.assertGreaterEqual(batch.input_tokens, 1)
        self.assertGreaterEqual(batch.request_count, 1)


if __name__ == "__main__":
    unittest.main()
