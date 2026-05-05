"""Provider adapter interface."""

from typing import List, Optional, Protocol


class Provider(Protocol):
    """Fetch raw transaction data for a Bitcoin address."""

    def fetch_address_txs(
        self,
        address: str,
        max_pages: Optional[int] = None,
        progress: bool = False,
    ) -> List[dict]:
        """Return raw transaction payloads for the address."""
