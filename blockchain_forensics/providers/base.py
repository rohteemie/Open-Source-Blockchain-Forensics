"""Provider adapter interface."""

from typing import List, Protocol


class Provider(Protocol):
    """Fetch raw transaction data for a Bitcoin address."""

    def fetch_address_txs(self, address: str) -> List[dict]:
        """Return raw transaction payloads for the address."""
