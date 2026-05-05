# Phase 1 Implementation Notes

## CLI Command (Phase 1)
- analyze-btc --address <addr> --out <path> [--provider blockstream|bitcoin-rpc]

## Providers
- Blockstream public API (no API key required, paginated for full history).
- Bitcoin Core RPC (requires access to a node; limited by available address indexing).

## MVP Flow
1. Fetch transactions for the address.
2. Normalize to internal schema.
3. Apply CIOH clustering.
4. Score clusters.
5. Write JSON output.
6. Optional CSV or text report.

## Limitations
- Bitcoin Core RPC provider returns transactions for current UTXOs unless an address indexer is available.
- CIOH can over-cluster; confidence scores are conservative.
