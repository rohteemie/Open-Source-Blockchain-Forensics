"""Blockstream public API provider (no API key required)."""

import json
from typing import List, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class BlockstreamProvider:
    """Blockstream API provider for Bitcoin mainnet."""

    def __init__(self, base_url: str = "https://blockstream.info/api") -> None:
        self.base_url = base_url.rstrip("/")

    def fetch_address_txs(
        self,
        address: str,
        max_pages: Optional[int] = None,
        progress: bool = False,
    ) -> List[dict]:
        """Fetch full address history using Blockstream pagination."""
        all_txs: List[dict] = []
        page = 0
        last_txid: Optional[str] = None

        while True:
            if max_pages is not None and page >= max_pages:
                break

            if last_txid:
                url = f"{self.base_url}/address/{address}/txs/chain/{last_txid}"
            else:
                url = f"{self.base_url}/address/{address}/txs"

            data = self._fetch_page(url)
            if not data:
                break

            all_txs.extend(data)
            if progress:
                print(
                    f"Fetched page {page + 1} ({len(data)} txs), total {len(all_txs)}"
                )
            new_last_txid = data[-1].get("txid")
            if not new_last_txid or new_last_txid == last_txid:
                break

            last_txid = new_last_txid
            page += 1

        return all_txs

    def _fetch_page(self, url: str) -> List[dict]:
        request = Request(url, headers={"User-Agent": "blockchain-forensics-mvp"})
        try:
            with urlopen(request, timeout=30) as response:
                payload = response.read().decode("utf-8")
        except HTTPError as exc:
            raise RuntimeError(f"Provider error: HTTP {exc.code}") from exc
        except URLError as exc:
            raise RuntimeError("Provider error: network failure") from exc

        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Provider error: invalid JSON") from exc

        if not isinstance(data, list):
            raise RuntimeError("Provider error: unexpected response")

        return data
