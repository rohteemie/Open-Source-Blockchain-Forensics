"""Bitcoin Core RPC provider."""

import base64
import json
from typing import Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


class BitcoinRpcProvider:
    """Bitcoin Core RPC provider for mainnet nodes."""

    def __init__(
        self,
        rpc_url: str,
        rpc_user: Optional[str] = None,
        rpc_password: Optional[str] = None,
        timeout: int = 30,
    ) -> None:
        self.rpc_url = rpc_url
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password
        self.timeout = timeout

    def fetch_address_txs(self, address: str, max_pages: Optional[int] = None) -> List[dict]:
        """Fetch transactions touching the address using RPC.

        Note: This relies on scantxoutset and returns transactions for current
        UTXOs. Full history requires an address indexer.
        """
        descriptor = f"addr({address})"
        result = self._rpc("scantxoutset", ["start", [descriptor]])
        unspents = result.get("unspents", []) if isinstance(result, dict) else []

        txs: List[dict] = []
        prev_cache: Dict[str, dict] = {}

        for utxo in unspents:
            txid = utxo.get("txid")
            if not txid:
                continue
            raw_tx = self._rpc("getrawtransaction", [txid, True])
            if isinstance(raw_tx, dict):
                txs.append(self._to_blockstream_shape(raw_tx, prev_cache))

        return txs

    def _rpc(self, method: str, params: List[object]) -> object:
        payload = json.dumps({"jsonrpc": "1.0", "id": "bf", "method": method, "params": params})
        headers = {"Content-Type": "application/json"}
        auth_header = self._build_auth_header()
        if auth_header:
            headers["Authorization"] = auth_header

        request = Request(self.rpc_url, data=payload.encode("utf-8"), headers=headers)
        try:
            with urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except HTTPError as exc:
            raise RuntimeError(f"RPC error: HTTP {exc.code}") from exc
        except URLError as exc:
            raise RuntimeError("RPC error: network failure") from exc

        data = json.loads(raw)
        if data.get("error"):
            raise RuntimeError(f"RPC error: {data['error']}")
        return data.get("result")

    def _build_auth_header(self) -> Optional[str]:
        if self.rpc_user is not None and self.rpc_password is not None:
            token = f"{self.rpc_user}:{self.rpc_password}".encode("utf-8")
            return "Basic " + base64.b64encode(token).decode("ascii")

        parsed = urlsplit(self.rpc_url)
        if parsed.username and parsed.password:
            token = f"{parsed.username}:{parsed.password}".encode("utf-8")
            return "Basic " + base64.b64encode(token).decode("ascii")

        return None

    def _to_blockstream_shape(self, raw_tx: dict, prev_cache: Dict[str, dict]) -> dict:
        inputs: List[dict] = []
        for vin in raw_tx.get("vin", []):
            prevout = None
            txid = vin.get("txid")
            vout_index = vin.get("vout")
            if txid is not None and vout_index is not None:
                prev_tx = prev_cache.get(txid)
                if prev_tx is None:
                    prev_tx = self._rpc("getrawtransaction", [txid, True])
                    if isinstance(prev_tx, dict):
                        prev_cache[txid] = prev_tx
                if isinstance(prev_tx, dict):
                    prevout = self._extract_prevout(prev_tx, vout_index)
            if prevout:
                inputs.append({"prevout": prevout})

        outputs: List[dict] = []
        for vout in raw_tx.get("vout", []):
            prevout = self._extract_output(vout)
            if prevout:
                outputs.append(prevout)

        status = {}
        if "time" in raw_tx:
            status = {"block_time": raw_tx.get("time")}

        return {
            "txid": raw_tx.get("txid"),
            "vin": inputs,
            "vout": outputs,
            "status": status,
        }

    def _extract_prevout(self, prev_tx: dict, vout_index: int) -> Optional[dict]:
        vouts = prev_tx.get("vout", [])
        if vout_index < 0 or vout_index >= len(vouts):
            return None
        return self._extract_output(vouts[vout_index])

    def _extract_output(self, vout: dict) -> Optional[dict]:
        script = vout.get("scriptPubKey", {})
        address = script.get("address")
        if address is None:
            addresses = script.get("addresses")
            if isinstance(addresses, list) and addresses:
                address = addresses[0]
        value_btc = vout.get("value")
        if address and isinstance(value_btc, (int, float)):
            return {
                "scriptpubkey_address": address,
                "value": int(round(value_btc * 100_000_000)),
            }
        return None
