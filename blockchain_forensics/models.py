"""Internal data models for Phase 1."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class TxIO:
    address: str
    amount_sats: int


@dataclass(frozen=True)
class Transaction:
    txid: str
    inputs: List[TxIO]
    outputs: List[TxIO]
    timestamp: Optional[int]
