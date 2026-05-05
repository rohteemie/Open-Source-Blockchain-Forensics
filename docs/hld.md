# High-Level Design (HLD) / System Architecture

## 1. Purpose
Provide a clear, modular system architecture for the Phase 1 MVP: Bitcoin-only address analysis using the Common Input Ownership Heuristic (CIOH).

## 2. Architectural Goals
- Keep the MVP small, testable, and easy to extend.
- Separate data access, parsing, and analysis.
- Produce deterministic results for the same input.
- Minimize external dependencies for Phase 1.

## 3. System Context
### Actors
- End user (CLI)
- Data provider (public API or node RPC)

### External Systems
- Bitcoin data source (API or full node)

## 4. Logical Components
1. CLI Interface
2. Data Provider Adapter
3. Transaction Normalizer
4. Clustering Engine (CIOH)
5. Confidence Scorer
6. Output Writer

## 5. Component Responsibilities
### 5.1 CLI Interface
- Validates user input.
- Orchestrates end-to-end flow.
- Emits user-friendly errors.

### 5.2 Data Provider Adapter
- Fetches raw transaction data for an address.
- Abstracts the provider (API or node RPC).

### 5.3 Transaction Normalizer
- Converts provider data into a minimal internal schema.
- Ensures required fields for CIOH are present.

### 5.4 Clustering Engine (CIOH)
- Applies CIOH to group addresses that appear as inputs in the same transaction.
- Produces raw clusters.

### 5.5 Confidence Scorer
- Assigns a simple confidence score per cluster based on input evidence count.

### 5.6 Output Writer
- Saves output to JSON.
- Prints a brief summary to the console.

## 6. Data Flow
1. User runs CLI with a Bitcoin address.
2. CLI calls Data Provider Adapter.
3. Raw transactions are normalized.
4. Clustering Engine builds clusters.
5. Confidence Scorer assigns scores.
6. Output Writer writes results.

## 7. Minimal Internal Data Model (Phase 1)
- Transaction
  - txid (string)
  - inputs (list of address + amount)
  - outputs (list of address + amount)
  - timestamp (string or int)

## 8. Diagrams

- High-level architecture: docs/diagrams/hld-architecture.png
- System context and data flow: docs/diagrams/system-design.png

## 9. HLD Diagram (Text)

[User] -> [CLI] -> [Provider Adapter] -> [Normalizer] -> [CIOH Clustering] -> [Scorer] -> [JSON Output]

## 10. Key Design Decisions
- CIOH chosen for MVP because it is simple, well-known, and provides meaningful clustering without complex heuristics.
- Provider adapter is abstracted to support API or node RPC without changing core logic.
- No graph database in Phase 1 to reduce setup complexity.

## 11. Risks and Mitigations
- Risk: API rate limits.
  - Mitigation: Pluggable provider adapter for alternative sources.
- Risk: Over-clustering with CIOH.
  - Mitigation: Clear confidence scores and documentation of limitations.

## 12. Non-Functional Considerations
- Logging should be minimal and informative.
- Errors should be actionable.
- Tests focus on deterministic outputs.

## 13. Future Extensions (Post-MVP)
- Change address detection.
- Graph database integration.
- Ethereum and cross-chain analysis.
- API server and dashboard.
