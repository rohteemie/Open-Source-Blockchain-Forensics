# Phase 1 Implementation Notes

## CLI Command (Phase 1)
- analyze-btc --address <addr> --out <path>

## Provider
- Blockstream public API (no API key required).

## MVP Flow
1. Fetch transactions for the address.
2. Normalize to internal schema.
3. Apply CIOH clustering.
4. Score clusters.
5. Write JSON output.

## Limitations
- Only the first page of transactions is fetched from Blockstream.
- CIOH can over-cluster; confidence scores are conservative.
