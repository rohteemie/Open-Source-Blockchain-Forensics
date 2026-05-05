"""Command-line interface for Phase 1."""

import argparse
from typing import Optional

from blockchain_forensics.clustering import cluster_cioh
from blockchain_forensics.normalizer import normalize_blockstream_txs
from blockchain_forensics.output import build_output, derive_report_path, write_json, write_report
from blockchain_forensics.providers.bitcoin_rpc import BitcoinRpcProvider
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
    analyze.add_argument(
        "--provider",
        choices=["blockstream", "bitcoin-rpc"],
        default="blockstream",
        help="Data provider adapter",
    )
    analyze.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Limit Blockstream pagination pages (default: full history)",
    )
    analyze.add_argument(
        "--rpc-url",
        default="http://127.0.0.1:8332",
        help="Bitcoin Core RPC URL",
    )
    analyze.add_argument("--rpc-user", default=None, help="Bitcoin Core RPC user")
    analyze.add_argument("--rpc-password", default=None, help="Bitcoin Core RPC password")
    analyze.add_argument(
        "--report",
        choices=["csv", "text"],
        default=None,
        help="Write an additional report (csv or text)",
    )
    analyze.add_argument(
        "--report-out",
        default=None,
        help="Report output path (default derived from JSON output)",
    )

    return parser


def _run_analyze(
    address: str,
    out_path: str,
    base_url: str,
    provider_name: str,
    max_pages: Optional[int],
    rpc_url: str,
    rpc_user: Optional[str],
    rpc_password: Optional[str],
    report: Optional[str],
    report_out: Optional[str],
) -> int:
    if provider_name == "bitcoin-rpc":
        provider = BitcoinRpcProvider(rpc_url=rpc_url, rpc_user=rpc_user, rpc_password=rpc_password)
    else:
        provider = BlockstreamProvider(base_url=base_url)

    raw_txs = provider.fetch_address_txs(address, max_pages=max_pages)
    transactions = normalize_blockstream_txs(raw_txs)

    clusters, evidence = cluster_cioh(transactions)
    scores = score_clusters(evidence)

    payload = build_output(
        address=address,
        provider=provider_name,
        clusters=clusters,
        evidence=evidence,
        scores=scores,
        tx_count=len(transactions),
    )
    write_json(out_path, payload)

    if report:
        report_path = report_out or derive_report_path(out_path, report)
        if report_path:
            write_report(report_path, payload, report)
            print(f"Saved report to {report_path}")

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
        return _run_analyze(
            args.address,
            args.out,
            args.base_url,
            args.provider,
            args.max_pages,
            args.rpc_url,
            args.rpc_user,
            args.rpc_password,
            args.report,
            args.report_out,
        )

    parser.error("Unknown command")
    return 2
