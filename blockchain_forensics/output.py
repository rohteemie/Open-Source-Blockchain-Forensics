"""Output helpers for Phase 1."""

import csv
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional


def build_output(
    address: str,
    provider: str,
    clusters: Dict[str, List[str]],
    evidence: Dict[str, int],
    scores: Dict[str, float],
    tx_count: int,
) -> dict:
    ordered = sorted(
        ((root, members) for root, members in clusters.items()),
        key=lambda item: (item[1][0] if item[1] else ""),
    )
    cluster_list = []
    for idx, (root, members) in enumerate(ordered, start=1):
        cluster_list.append(
            {
                "cluster_id": f"cluster-{idx}",
                "addresses": members,
                "confidence": scores.get(root, 0.0),
                "evidence_txs": evidence.get(root, 0),
            }
        )

    address_count = sum(len(item["addresses"]) for item in cluster_list)
    payload = {
        "address": address,
        "provider": provider,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "cluster_count": len(cluster_list),
            "address_count": address_count,
            "tx_count": tx_count,
        },
        "clusters": cluster_list,
    }
    return payload


def write_json(path: str, payload: dict) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def write_report(path: str, payload: dict, report_type: str) -> None:
    if report_type == "csv":
        _write_csv_report(path, payload)
        return
    if report_type == "text":
        _write_text_report(path, payload)
        return
    raise ValueError(f"Unknown report type: {report_type}")


def _write_csv_report(path: str, payload: dict) -> None:
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["cluster_id", "address_count", "confidence", "evidence_txs"])
        for cluster in payload.get("clusters", []):
            writer.writerow(
                [
                    cluster.get("cluster_id"),
                    len(cluster.get("addresses", [])),
                    cluster.get("confidence"),
                    cluster.get("evidence_txs"),
                ]
            )


def _write_text_report(path: str, payload: dict) -> None:
    summary = payload.get("summary", {})
    lines = [
        "Phase 1 Report",
        "",
        f"Address: {payload.get('address')}",
        f"Provider: {payload.get('provider')}",
        f"Generated: {payload.get('generated_at')}",
        "",
        "Summary",
        f"- Clusters: {summary.get('cluster_count')}",
        f"- Addresses: {summary.get('address_count')}",
        f"- Transactions: {summary.get('tx_count')}",
        "",
        "Clusters",
    ]

    for cluster in payload.get("clusters", []):
        lines.append(
            f"{cluster.get('cluster_id')}: {len(cluster.get('addresses', []))} addresses | "
            f"confidence {cluster.get('confidence')} | evidence {cluster.get('evidence_txs')}"
        )

    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def derive_report_path(json_path: str, report_type: str) -> Optional[str]:
    if not json_path:
        return None
    if report_type == "csv" and json_path.endswith(".json"):
        return json_path[:-5] + ".csv"
    if report_type == "text" and json_path.endswith(".json"):
        return json_path[:-5] + ".txt"
    extension = ".csv" if report_type == "csv" else ".txt"
    return json_path + extension
