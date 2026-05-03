"""Output helpers for Phase 1."""

import json
from datetime import datetime, timezone
from typing import Dict, List


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
