# MVP Definition

## MVP Goal
Deliver a minimal Bitcoin-only forensics workflow that takes a target address, fetches transactions, clusters addresses using CIOH, and outputs results with confidence scores via a CLI command.

## MVP Scope
### Included
- Bitcoin address input.
- One data provider adapter (public API or node RPC).
- Transaction normalization model.
- CIOH clustering.
- Confidence scoring per cluster.
- CLI command with JSON output.
- Basic tests and documentation.

### Excluded
- Change address detection.
- Additional heuristics or ML models.
- Ethereum or other chains.
- Graph database integration.
- Web dashboard or API.

## MVP User Flow
1. User runs CLI with a Bitcoin address.
2. Tool fetches transactions and normalizes data.
3. Tool clusters addresses using CIOH.
4. Tool prints and saves JSON output.

## MVP Deliverables
- Source code modules for data access, parsing, and clustering.
- CLI entry point and usage documentation.
- Sample output file and example command.
- Unit tests for key logic.

## MVP Acceptance Criteria
- One command runs end-to-end successfully for a valid address.
- Output includes cluster IDs, addresses, and confidence scores.
- Errors are user-friendly for invalid input or fetch failures.
