"""Blockstream public API provider (no API key required)."""

import json
from typing import List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class BlockstreamProvider:
    """Blockstream API provider for Bitcoin mainnet."""

    def __init__(self, base_url: str = "https://blockstream.info/api") -> None:
        self.base_url = base_url.rstrip("/")

    def fetch_address_txs(self, address: str) -> List[dict]:
        url = f"{self.base_url}/address/{address}/txs"
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
