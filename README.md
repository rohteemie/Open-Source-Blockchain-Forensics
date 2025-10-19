# Open-Source Blockchain Forensics

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-in%20development-orange.svg)]()

A scalable, open-source tool for clustering and de-anonymizing transaction patterns on public blockchains (Bitcoin and Ethereum). This project combines advanced graph analytics, machine learning, and blockchain analysis to trace cryptocurrency flows and identify entities behind pseudonymous addresses.

## 🎯 Project Overview

This project represents a comprehensive exploration of blockchain forensics, privacy analysis, and entity resolution in decentralized systems.

### Motivation

While blockchain technology promises transparency, the pseudonymous nature of cryptocurrency addresses creates challenges for:
- Law enforcement investigating illicit activities
- Researchers studying transaction patterns and network effects
- Compliance officers ensuring regulatory adherence
- Users understanding privacy implications of blockchain transactions

This tool addresses these challenges by implementing state-of-the-art clustering algorithms and heuristics to link related addresses and identify real-world entities.

## 🔬 Research Questions

1. **Clustering Effectiveness**: How accurately can we cluster blockchain addresses belonging to the same entity using various heuristics?
2. **Cross-chain Analysis**: Can transaction patterns be traced across different blockchains?
3. **Privacy Implications**: What privacy vulnerabilities exist in current blockchain implementations?
4. **Scalability**: How can forensics tools scale to analyze billions of transactions efficiently?

## 🚀 Key Features

### Current Capabilities (Planned)

- **Multi-Blockchain Support**
  - Bitcoin transaction analysis
  - Ethereum transaction and smart contract analysis
  - Extensible architecture for additional blockchains

- **Advanced Clustering Algorithms**
  - Common Input Ownership Heuristic (CIOH)
  - Change Address Detection
  - Behavior-based clustering
  - Machine learning-enhanced entity resolution

- **Transaction Graph Analysis**
  - Graph database integration for efficient querying
  - Path tracing between addresses
  - Community detection algorithms
  - Temporal pattern analysis

- **De-anonymization Techniques**
  - Exchange deposit/withdrawal pattern matching
  - Address tagging with known entities
  - Network topology analysis
  - Cross-referencing with public data sources

- **Visualization and Reporting**
  - Interactive transaction flow diagrams
  - Entity relationship maps
  - Statistical reports and metrics
  - Export capabilities for further analysis

## 🏗️ Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                  │
│         (CLI, Web Dashboard, API Endpoints)              │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Analysis Engine                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Clustering  │  │  ML Models   │  │  Heuristics  │  │
│  │  Algorithms  │  │  & Features  │  │  Engine      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                Data Processing Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Transaction │  │  Address     │  │  Entity      │  │
│  │  Parser      │  │  Indexer     │  │  Resolver    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Data Storage & Indexing                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Graph DB    │  │  Time-Series │  │  Cache       │  │
│  │  (Neo4j)     │  │  DB          │  │  (Redis)     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Blockchain Data Sources                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Bitcoin     │  │  Ethereum    │  │  Public      │  │
│  │  Node/API    │  │  Node/API    │  │  Datasets    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Language**: Python 3.8+
- **Blockchain Interaction**: 
  - Bitcoin: `bitcoinlib`, `bitcoin-rpc`
  - Ethereum: `web3.py`, `eth-brownie`
- **Graph Database**: Neo4j for relationship storage and querying
- **Data Processing**: Pandas, NumPy, Apache Spark (for large-scale processing)
- **Machine Learning**: scikit-learn, TensorFlow/PyTorch
- **Visualization**: Plotly, NetworkX, D3.js
- **API Framework**: FastAPI
- **Testing**: pytest, unittest

## 🛠️ Installation

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Neo4j (optional, for graph storage)
# Install from: https://neo4j.com/download/

# Bitcoin/Ethereum node or API access
```

### Setup

```bash
# Clone the repository
git clone https://github.com/rohteemie/Open-Source-Blockchain-Forensics.git
cd Open-Source-Blockchain-Forensics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your blockchain node URLs and API keys

# Initialize database
python scripts/init_db.py

# Run tests
pytest tests/
```

## 📖 Usage

### Basic Example

```python
from blockchain_forensics import BitcoinAnalyzer, AddressClusterer

# Initialize analyzer
analyzer = BitcoinAnalyzer(api_key="your_api_key")

# Fetch transactions for an address
transactions = analyzer.get_transactions("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")

# Perform clustering
clusterer = AddressClusterer()
clusters = clusterer.cluster_addresses(transactions)

# Print results
for cluster_id, addresses in clusters.items():
    print(f"Cluster {cluster_id}: {len(addresses)} addresses")
    print(f"Confidence: {clusterer.get_confidence(cluster_id)}")
```

### CLI Usage

```bash
# Analyze a Bitcoin address
python -m blockchain_forensics analyze-btc --address 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa

# Trace transaction flow
python -m blockchain_forensics trace --txid <transaction_id> --depth 3

# Generate report
python -m blockchain_forensics report --cluster-id <cluster_id> --output report.pdf
```

### API Usage

```bash
# Start the API server
python -m blockchain_forensics.api

# API will be available at http://localhost:8000
# Documentation at http://localhost:8000/docs
```

## 🔬 Development Roadmap

### Phase 1: Foundation
- [x] Project setup and architecture design
- [ ] Bitcoin data collection module
- [ ] Basic CIOH clustering implementation
- [ ] Graph database integration
- [ ] Unit tests and documentation

### Phase 2: Core Features
- [ ] Ethereum support
- [ ] Advanced clustering algorithms
- [ ] Change address detection
- [ ] Performance optimization for large datasets
- [ ] CLI interface development

### Phase 3: Advanced Analysis
- [ ] Machine learning models for entity resolution
- [ ] Cross-chain analysis capabilities
- [ ] Behavioral pattern detection
- [ ] Integration with public datasets (WalletExplorer, etc.)

### Phase 4: Evaluation & Refinement
- [ ] Benchmark against existing tools
- [ ] Ground truth evaluation
- [ ] Privacy analysis and ethical considerations
- [ ] Performance optimization
- [ ] Web dashboard development

### Phase 5: Documentation & Presentation
- [ ] Comprehensive documentation
- [ ] Case studies and examples

## 📊 Evaluation Metrics

- **Clustering Accuracy**: Precision, Recall, F1-Score
- **Scalability**: Transactions processed per second
- **Coverage**: Percentage of addresses successfully clustered
- **Confidence Scores**: Distribution and reliability
- **False Positive Rate**: Incorrectly merged clusters
- **False Negative Rate**: Missed clustering opportunities

## 🔒 Privacy & Ethics

This tool is designed for:
- ✅ Legal investigations with proper authorization
- ✅ Compliance and risk management
- ✅ Privacy research and education

**Important**: This tool should NOT be used for:
- ❌ Unauthorized surveillance
- ❌ Harassment or stalking
- ❌ Illegal activities
- ❌ Violations of privacy rights

Users are responsible for complying with applicable laws and regulations in their jurisdiction.

## 📚 Related Work & References

### Academic Papers
- Meiklejohn, S., et al. (2013). "A Fistful of Bitcoins: Characterizing Payments Among Men with No Names"
- Reid, F., & Harrigan, M. (2013). "An Analysis of Anonymity in the Bitcoin System"
- Androulaki, E., et al. (2013). "Evaluating User Privacy in Bitcoin"
- Möser, M., et al. (2013). "An Inquiry into Money Laundering Tools in the Bitcoin Ecosystem"

### Existing Tools
- **BlockSci**: Academic blockchain analysis platform
- **Chainalysis**: Commercial blockchain forensics
- **Elliptic**: Enterprise-grade blockchain analytics
- **Crystal Blockchain**: Compliance and investigation tool

### Datasets
- **WalletExplorer**: Bitcoin address tags and clusters
- **Bitcoin-OTC**: Trust network and verified addresses
- **Blockchain.com API**: Public transaction data
- **Etherscan**: Ethereum transaction and contract data

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and development process.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Rohteemie**
- GitHub: [@rohteemie](https://github.com/rohteemie)
- Project: Computer Science/Blockchain Technology/Digital Forensics

## 🙏 Acknowledgments

- Open-source blockchain community
- Contributors to related research and tools
- Neo4j and graph database community

## 📞 Contact & Support

For questions, suggestions, or collaboration opportunities:
- Open an issue on GitHub
- Email: <rotimijournal@outlook.com>
- LinkedIn: <https://www.linkedin.com/in/rotimijournal>

## 🔖 Citation

If you use this tool in your research, please cite:

```bibtex
@misc{blockchain_forensics_2025,
  title={Open-Source Blockchain Forensics: A Scalable Tool for Transaction Clustering and De-anonymization},
  author={Rohteemie},
  year={2025},
  howpublished={\url{https://github.com/rohteemie/Open-Source-Blockchain-Forensics}}
}
```

---

**Status**: 🚧 This project is under active development. Contributions and feedback are welcome!

**Last Updated**: October 2025
