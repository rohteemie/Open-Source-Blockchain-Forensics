"""CIOH clustering implementation."""

from typing import Dict, Iterable, List, Tuple

from blockchain_forensics.models import Transaction


class UnionFind:
    """Union-find structure for address clustering."""

    def __init__(self) -> None:
        self.parent: Dict[str, str] = {}
        self.rank: Dict[str, int] = {}

    def find(self, item: str) -> str:
        if item not in self.parent:
            self.parent[item] = item
            self.rank[item] = 0
            return item
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, a: str, b: str) -> None:
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return
        rank_a = self.rank[root_a]
        rank_b = self.rank[root_b]
        if rank_a < rank_b:
            self.parent[root_a] = root_b
        elif rank_a > rank_b:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1


def _pairwise(items: List[str]) -> Iterable[Tuple[str, str]]:
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            yield items[i], items[j]


def cluster_cioh(transactions: List[Transaction]) -> Tuple[Dict[str, List[str]], Dict[str, int]]:
    """Cluster addresses using CIOH and return clusters and evidence counts."""
    uf = UnionFind()
    evidence: Dict[str, int] = {}

    for tx in transactions:
        addresses = sorted({tx_input.address for tx_input in tx.inputs})
        if len(addresses) < 2:
            continue

        for a, b in _pairwise(addresses):
            uf.union(a, b)

        # Increment evidence once per transaction for the cluster root.
        root = uf.find(addresses[0])
        evidence[root] = evidence.get(root, 0) + 1

    clusters: Dict[str, List[str]] = {}
    for address in uf.parent:
        root = uf.find(address)
        clusters.setdefault(root, []).append(address)

    for members in clusters.values():
        members.sort()

    return clusters, evidence
