"""Minimal integration test for analyze-btc."""

import json
import os
import tempfile
import unittest
from unittest import mock

from blockchain_forensics import cli


class TestCliIntegration(unittest.TestCase):
    def test_analyze_btc_writes_output(self) -> None:
        sample_txs = [
            {
                "txid": "abc",
                "vin": [
                    {"prevout": {"scriptpubkey_address": "a", "value": 10}},
                    {"prevout": {"scriptpubkey_address": "b", "value": 5}},
                ],
                "vout": [
                    {"scriptpubkey_address": "c", "value": 7},
                ],
                "status": {"block_time": 123},
            }
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "output.json")
            with mock.patch(
                "blockchain_forensics.providers.blockstream.BlockstreamProvider.fetch_address_txs",
                return_value=sample_txs,
            ):
                exit_code = cli.main(
                    [
                        "analyze-btc",
                        "--address",
                        "addr",
                        "--out",
                        out_path,
                        "--no-progress",
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertTrue(os.path.exists(out_path))
            with open(out_path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)

        self.assertEqual(payload["summary"]["tx_count"], 1)
        self.assertEqual(payload["summary"]["cluster_count"], 1)


if __name__ == "__main__":
    unittest.main()
