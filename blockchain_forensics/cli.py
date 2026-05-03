"""Command-line interface for Phase 1."""

import argparse
from typing import Optional

from blockchain_forensics.clustering import cluster_cioh
from blockchain_forensics.normalizer import normalize_blockstream_txs
from blockchain_forensics.output import build_output, write_json
from blockchain_forensics.providers.blockstream import BlockstreamProvider
from blockchain_forensics.scoring import score_clusters


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="blockchain-forensics")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze-btc", help="Analyze a Bitcoin address")
    analyze.add_argument("--address", required=True, help="Target Bitcoin address")
    analyze.add_argument(
        "--out",
        default="output.json",
        help="Output JSON path (default: output.json)",
    )
    analyze.add_argument(
        "--base-url",
        default="https://blockstream.info/api",
        help="Blockstream API base URL",
    )

    return parser


def _run_analyze(address: str, out_path: str, base_url: str) -> int:
    provider = BlockstreamProvider(base_url=base_url)
    raw_txs = provider.fetch_address_txs(address)
    transactions = normalize_blockstream_txs(raw_txs)

    clusters, evidence = cluster_cioh(transactions)
    scores = score_clusters(evidence)

    payload = build_output(
        address=address,
        provider="blockstream",
        clusters=clusters,
        evidence=evidence,
        scores=scores,
        tx_count=len(transactions),
    )
    write_json(out_path, payload)

    print(f"Saved results to {out_path}")
    print(
        f"Clusters: {payload['summary']['cluster_count']} | "
        f"Addresses: {payload['summary']['address_count']} | "
        f"Transactions: {payload['summary']['tx_count']}"
    )
    return 0


def main(argv: Optional[list] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "analyze-btc":
        return _run_analyze(args.address, args.out, args.base_url)

    parser.error("Unknown command")
    return 2
