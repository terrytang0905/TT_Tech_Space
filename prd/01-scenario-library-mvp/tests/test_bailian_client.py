import json
import tempfile
import unittest
from pathlib import Path

from src.bailian_client import (
    BailianClient,
    ConfigurationError,
    HttpError,
    cache_key,
)


def embedding(index, sparse=False):
    item = {"text_index": index, "embedding": [1.0] + [0.0] * 1023}
    if sparse:
        item["sparse_embedding"] = [{"index": 7, "value": 0.5}]
    return item


def valid_response(count, sparse=False, tokens=None):
    return {
        "output": {"embeddings": [embedding(index, sparse) for index in range(count)]},
        "usage": {"total_tokens": tokens if tokens is not None else count * 3},
    }


class FakeTransport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.payloads = []

    def post(self, url, headers, payload):
        self.payloads.append(payload)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


class BailianClientTests(unittest.TestCase):
    def client(self, transport, cache_dir, sleeper=lambda _: None):
        return BailianClient("secret-value", transport=transport, cache_dir=cache_dir, sleeper=sleeper)

    def test_missing_key_fails_without_leaking_value(self):
        with self.assertRaisesRegex(ConfigurationError, "DASHSCOPE_API_KEY is not set"):
            BailianClient(api_key=None, transport=FakeTransport([]))

    def test_batches_eleven_inputs_as_ten_plus_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            transport = FakeTransport([valid_response(10), valid_response(1)])
            result = self.client(transport, Path(tmp)).embed([str(i) for i in range(11)], "dense")
            self.assertEqual(result.request_count, 2)
            self.assertEqual([len(payload["input"]["texts"]) for payload in transport.payloads], [10, 1])
            self.assertEqual(len(result.dense), 11)

    def test_cache_key_changes_with_output_type(self):
        self.assertNotEqual(cache_key("x", "dense"), cache_key("x", "dense&sparse"))

    def test_cache_avoids_second_request_and_second_usage_charge(self):
        with tempfile.TemporaryDirectory() as tmp:
            transport = FakeTransport([valid_response(1, tokens=9)])
            client = self.client(transport, Path(tmp))
            first = client.embed(["文本"], "dense")
            second = client.embed(["文本"], "dense")
            self.assertEqual(first.input_tokens, 9)
            self.assertEqual(second.input_tokens, 0)
            self.assertEqual(second.request_count, 0)
            self.assertEqual(len(transport.payloads), 1)

    def test_retries_429_but_not_invalid_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            retrying = FakeTransport([HttpError(429, "rate limit"), valid_response(1)])
            result = self.client(retrying, Path(tmp)).embed(["x"], "dense")
            self.assertEqual(result.request_count, 2)
        with tempfile.TemporaryDirectory() as tmp:
            invalid = FakeTransport([HttpError(400, "secret-value in body")])
            with self.assertRaises(HttpError) as caught:
                self.client(invalid, Path(tmp)).embed(["x"], "dense")
            self.assertNotIn("secret-value", str(caught.exception))
            self.assertEqual(len(invalid.payloads), 1)

    def test_dense_and_sparse_response_is_parsed(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.client(FakeTransport([valid_response(1, sparse=True)]), Path(tmp)).embed(["x"], "dense&sparse")
            self.assertEqual(len(result.dense[0]), 1024)
            self.assertEqual(result.sparse[0], {7: 0.5})

    def test_wrong_dense_dimension_is_rejected(self):
        response = valid_response(1)
        response["output"]["embeddings"][0]["embedding"] = [1.0]
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "1024"):
                self.client(FakeTransport([response]), Path(tmp)).embed(["x"], "dense")

    def test_refresh_bypasses_existing_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            transport = FakeTransport([valid_response(1), valid_response(1)])
            client = self.client(transport, Path(tmp))
            client.embed(["x"], "dense")
            refreshed = client.embed(["x"], "dense", refresh=True)
            self.assertEqual(refreshed.request_count, 1)
            self.assertEqual(len(transport.payloads), 2)


if __name__ == "__main__":
    unittest.main()
