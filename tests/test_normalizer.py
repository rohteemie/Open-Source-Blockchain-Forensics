"""Basic tests for the Blockstream normalizer."""

import unittest

from blockchain_forensics.normalizer import normalize_blockstream_txs


class TestNormalizer(unittest.TestCase):
    def test_normalize_blockstream(self) -> None:
        raw = [
            {
                "txid": "abc",
                "vin": [
                    {"prevout": {"scriptpubkey_address": "a", "value": 10}},
                    {"prevout": {"scriptpubkey_address": "b", "value": 5}},
                ],
                "vout": [
                    {"scriptpubkey_address": "c", "value": 7},
                    {"scriptpubkey_address": "d", "value": 8},
                ],
                "status": {"block_time": 123},
            }
        ]
        txs = normalize_blockstream_txs(raw)
        self.assertEqual(len(txs), 1)
        self.assertEqual(txs[0].txid, "abc")
        self.assertEqual(len(txs[0].inputs), 2)
        self.assertEqual(len(txs[0].outputs), 2)
        self.assertEqual(txs[0].timestamp, 123)


if __name__ == "__main__":
    unittest.main()
