# Phase 1 Usage

## Analyze a Bitcoin address

```bash
python3 -m blockchain_forensics analyze-btc --address <addr> --out output.json
```

## Use Blockstream pagination

```bash
python3 -m blockchain_forensics analyze-btc --address <addr> --max-pages 3
```

## Use Bitcoin Core RPC

```bash
python3 -m blockchain_forensics analyze-btc \
	--address <addr> \
	--provider bitcoin-rpc \
	--rpc-url http://127.0.0.1:8332 \
	--rpc-user <user> \
	--rpc-password <password>
```

## Generate a report

```bash
python3 -m blockchain_forensics analyze-btc \
	--address <addr> \
	--report csv
```

## Output
- JSON file containing clusters, confidence scores, and summary metadata.
- Optional CSV or text report with a summarized cluster view.
