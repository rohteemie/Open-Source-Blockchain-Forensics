"""Basic tests for CIOH clustering."""

import unittest

from blockchain_forensics.clustering import cluster_cioh
from blockchain_forensics.models import Transaction, TxIO
from blockchain_forensics.scoring import score_clusters


class TestCiohClustering(unittest.TestCase):
    def test_cluster_creation(self) -> None:
        txs = [
            Transaction(
                txid="tx1",
                inputs=[TxIO("a", 1), TxIO("b", 2)],
                outputs=[TxIO("c", 3)],
                timestamp=None,
            ),
            Transaction(
                txid="tx2",
                inputs=[TxIO("b", 1), TxIO("d", 2)],
                outputs=[TxIO("e", 3)],
                timestamp=None,
            ),
        ]
        clusters, evidence = cluster_cioh(txs)
        self.assertEqual(len(clusters), 1)
        only_cluster = next(iter(clusters.values()))
        self.assertEqual(sorted(only_cluster), ["a", "b", "d"])
        self.assertEqual(sum(evidence.values()), 2)

    def test_score_bounds(self) -> None:
        scores = score_clusters({"root": 10})
        self.assertEqual(scores["root"], 1.0)

    def test_evidence_after_merge(self) -> None:
        txs = [
            Transaction(
                txid="tx1",
                inputs=[TxIO("a", 1), TxIO("b", 2)],
                outputs=[TxIO("c", 3)],
                timestamp=None,
            ),
            Transaction(
                txid="tx2",
                inputs=[TxIO("d", 1), TxIO("e", 2)],
                outputs=[TxIO("f", 3)],
                timestamp=None,
            ),
            Transaction(
                txid="tx3",
                inputs=[TxIO("b", 1), TxIO("d", 2)],
                outputs=[TxIO("g", 3)],
                timestamp=None,
            ),
        ]
        clusters, evidence = cluster_cioh(txs)
        self.assertEqual(len(clusters), 1)
        self.assertEqual(len(evidence), 1)
        self.assertEqual(next(iter(evidence.values())), 3)


if __name__ == "__main__":
    unittest.main()
