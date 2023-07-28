This repository contains file for:
- retrieving transaction from the Gitcoin Alpha Rounds (Allo protocol)
- parsing the transactions and loading the voting information

Before running the scripts you need to set this `ETHERSCAN_API_KEY` env var.

The scripts need tp be run in this order:
- 01_get_transactions_from_contracts.py
- 02_get_votes_from_transactions.py

> !!! Important:
> the transactions file will contain duplicates, due to the way how the batches are loaded from etherscan.
