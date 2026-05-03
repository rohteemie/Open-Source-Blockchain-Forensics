# Architecture Overview

## 1. Scope
This document provides the system architecture needed for the Phase 1 MVP and includes diagrams for component structure, data flow, and deployment.

## 2. Diagrams (PNG)
- High-level architecture: docs/diagrams/hld-architecture.png
- System context and data flow: docs/diagrams/system-design.png

## 3. Component Architecture (Mermaid Source)
```mermaid
flowchart LR
	user([User]) --> cli[CLI Interface]
	cli --> provider[Data Provider Adapter]
	provider --> normalizer[Transaction Normalizer]
	normalizer --> clusterer[CIOH Clustering Engine]
	clusterer --> scorer[Confidence Scorer]
	scorer --> output[JSON Output Writer]
```

## 4. Data Flow (Sequence, Mermaid Source)
```mermaid
sequenceDiagram
	participant U as User
	participant CLI as CLI Interface
	participant P as Provider Adapter
	participant N as Normalizer
	participant C as CIOH Clusterer
	participant S as Confidence Scorer
	participant O as Output Writer

	U->>CLI: Run analyze-btc --address <addr>
	CLI->>P: fetch_transactions(addr)
	P-->>CLI: raw_transactions
	CLI->>N: normalize(raw_transactions)
	N-->>CLI: normalized_transactions
	CLI->>C: cluster(normalized_transactions)
	C-->>CLI: clusters
	CLI->>S: score(clusters)
	S-->>CLI: scored_clusters
	CLI->>O: write_json(scored_clusters)
	O-->>CLI: output_path
	CLI-->>U: summary and output location
```

## 5. Deployment Diagram (MVP, Mermaid Source)
```mermaid
flowchart TB
	subgraph LocalMachine
		cli[CLI Tool]
		files[Local Output Files]
	end

	subgraph DataSource
		api[Bitcoin API or Node RPC]
	end

	cli --> api
	cli --> files
```

## 6. Core Modules (MVP)
- cli: argument parsing and orchestration.
- provider: adapter interface for data sources.
- normalizer: provider-specific parsing to internal schema.
- clustering: CIOH implementation.
- scoring: basic confidence rules.
- output: JSON writer and summary.

## 7. Design Rationale
- CIOH chosen for simplicity and established research usage.
- Provider adapter keeps data access separate for easy swapping.
- Normalized schema avoids coupling logic to provider formats.
- JSON output keeps MVP lightweight and easy to inspect.

## 8. Risks
- API rate limits or missing fields.
- Over-clustering due to CIOH limitations.

## 9. Future Extensions
- Change address detection and additional heuristics.
- Graph database integration.
- Ethereum support and cross-chain analytics.
- Web API and dashboard.
