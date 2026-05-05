"""Normalize provider responses into internal models."""

from typing import List

from blockchain_forensics.models import Transaction, TxIO


def normalize_blockstream_txs(raw_txs: List[dict]) -> List[Transaction]:
    """Normalize provider responses shaped like Blockstream transactions."""
    normalized: List[Transaction] = []
    for raw in raw_txs:
        txid = raw.get("txid")
        if not txid:
            continue

        inputs: List[TxIO] = []
        for vin in raw.get("vin", []):
            prevout = vin.get("prevout") or {}
            address = prevout.get("scriptpubkey_address")
            value = prevout.get("value")
            if address and isinstance(value, int):
                inputs.append(TxIO(address=address, amount_sats=value))

        outputs: List[TxIO] = []
        for vout in raw.get("vout", []):
            address = vout.get("scriptpubkey_address")
            value = vout.get("value")
            if address and isinstance(value, int):
                outputs.append(TxIO(address=address, amount_sats=value))

        timestamp = None
        status = raw.get("status") or {}
        if isinstance(status, dict):
            timestamp = status.get("block_time")

        normalized.append(
            Transaction(txid=txid, inputs=inputs, outputs=outputs, timestamp=timestamp)
        )

    return normalized
