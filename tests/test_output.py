"""Basic tests for output building."""

import unittest

from blockchain_forensics.output import build_output


class TestOutput(unittest.TestCase):
    def test_build_output(self) -> None:
        clusters = {"root": ["a", "b"]}
        evidence = {"root": 2}
        scores = {"root": 0.4}
        payload = build_output(
            address="addr",
            provider="blockstream",
            clusters=clusters,
            evidence=evidence,
            scores=scores,
            tx_count=3,
        )
        self.assertEqual(payload["summary"]["cluster_count"], 1)
        self.assertEqual(payload["summary"]["address_count"], 2)
        self.assertEqual(payload["summary"]["tx_count"], 3)


if __name__ == "__main__":
    unittest.main()
