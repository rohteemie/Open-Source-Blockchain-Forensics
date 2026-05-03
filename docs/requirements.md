# Requirements Analysis and Definition

## 1. Purpose
Provide a minimal, open-source blockchain forensics tool that can collect Bitcoin transaction data for a target address, apply a basic clustering heuristic, and output clusters with confidence scores.

## 2. Scope
### In Scope (Phase 1)
- Bitcoin-only analysis (no Ethereum in Phase 1).
- Single input: a Bitcoin address.
- Data retrieval via one configurable provider (public API or full node).
- Transaction normalization into a minimal schema used by the analyzer.
- Clustering using Common Input Ownership Heuristic (CIOH).
- Output clusters with confidence scores.
- Command-line interface (CLI) for running analysis.
- Basic logging and error handling.
- Unit tests for core parsing and clustering logic.
- Clear documentation for setup and usage.

### Out of Scope (Phase 1)
- Change address detection.
- Advanced heuristics and machine learning.
- Cross-chain analysis.
- Web dashboard or API.
- Graph database integration (Neo4j).
- Large-scale performance optimization.

## 3. Stakeholders
- Open-source contributors.
- Researchers and educators.
- Analysts needing a simple, transparent clustering tool.

## 4. User Stories (Phase 1)
- As a user, I can provide a Bitcoin address and receive a list of clustered addresses.
- As a user, I can see a confidence score for each cluster.
- As a user, I can run the analysis from the CLI and save the output.
- As a developer, I can extend the data source implementation without changing the clustering logic.

## 5. Functional Requirements
- FR-01: Accept a Bitcoin address as input.
- FR-02: Fetch transactions for the address via a configured provider.
- FR-03: Normalize transactions into a consistent internal model.
- FR-04: Apply CIOH clustering to produce address clusters.
- FR-05: Generate a confidence score per cluster.
- FR-06: Output results in JSON format.
- FR-07: Provide a CLI command for the end-to-end flow.
- FR-08: Provide basic logging and error messages for failed fetches or invalid input.

## 6. Non-Functional Requirements
- NFR-01: Clear documentation for setup and usage.
- NFR-02: Unit tests for parsing and clustering.
- NFR-03: Modular architecture that separates data access, parsing, and clustering.
- NFR-04: Deterministic clustering results for the same input.

## 7. Data Requirements
- DR-01: Transaction data must include inputs, outputs, amounts, and timestamps.
- DR-02: Input and output address lists must be preserved for CIOH.

## 8. Risks and Assumptions
- Assumption: Data provider is available and reliable.
- Risk: Public APIs may enforce rate limits.
- Risk: CIOH may over-cluster in specific patterns.

## 9. Acceptance Criteria (Phase 1)
- Given a valid address, CLI produces a JSON file containing one or more clusters.
- Each cluster includes a unique cluster ID, list of addresses, and confidence score.
- Invalid addresses return a clear error without a crash.
- Unit tests cover parser and clustering logic with at least one fixture.
