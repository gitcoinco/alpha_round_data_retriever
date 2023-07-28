import requests
import os
import json
from pprint import pprint
import time
from web3 import Web3

# Connect to the Ethereum network or your preferred provider
web3 = Web3(
    Web3.HTTPProvider(
        "https://eth-mainnet.g.alchemy.com/v2/5QPthzD45A2kb7VKlphviV2voxiIEMqL"
    )
)

ETHERSCAN_API_KEY = os.environ.get("ETHERSCAN_API_KEY")


def load_transactions(contract_address):
    startblock = "16350193"
    old_startblock = None
    while True:
        print(f"Loading transactions for {contract_address}, startblock {startblock}")
        response = requests.get(
            "https://api.etherscan.io/api",
            params={
                "module": "account",
                "action": "txlist",
                "address": contract_address,
                "startblock": startblock,
                # "endblock": "16350193",
                # "page": page,
                # "offset": 10000,
                "sort": "asc",
                "apikey": ETHERSCAN_API_KEY,
            },
            timeout=60,
        )

        data = response.json()
        if data["status"] == "1":
            print(f"   -> loaded {len(data['result'])} transactions")
            old_startblock = startblock
            startblock = data["result"][-1]["blockNumber"]
            with open(
                f"transactions_{contract_address}.json", "a+", encoding="utf-8"
            ) as file:
                for record in data["result"]:
                    file.write(json.dumps(record) + "\n")
            if startblock == old_startblock:
                break
            time.sleep(2)
        else:
            print("!!! ERROR !!!")
            pprint(data)
            break


contract_addresses = [
    "0xd95a1969c41112cee9a2c931e849bcef36a16f4c",
    "0xe575282b376e3c9886779a841a2510f1dd8c2ce4",
    "0x1b165fe4da6bc58ab8370ddc763d367d29f50ef0",
]

for contract_address in contract_addresses:
    load_transactions(contract_address)
