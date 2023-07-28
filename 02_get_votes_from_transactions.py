import os
import json
from tqdm import tqdm
import requests
from web3 import Web3
from pprint import pprint
import traceback
import csv
import eth_abi

# Connect to the Ethereum network or your preferred provider
web3 = Web3(
    Web3.HTTPProvider(
        "https://eth-mainnet.g.alchemy.com/v2/5QPthzD45A2kb7VKlphviV2voxiIEMqL"
    )
)

# class web3.contract.Contract(address)
ETHERSCAN_API_KEY = os.environ.get("ETHERSCAN_API_KEY")


contract_addresses = [
    "0xd95a1969c41112cee9a2c931e849bcef36a16f4c",
    "0xe575282b376e3c9886779a841a2510f1dd8c2ce4",
    "0x1b165fe4da6bc58ab8370ddc763d367d29f50ef0",
]

contract_addresses_checksumed = [
    Web3.to_checksum_address(contract_address)
    for contract_address in contract_addresses
]


class NotAVoteException(Exception):
    pass


class BadTransaction(Exception):
    pass


def get_file_size(file_path):
    return os.path.getsize(file_path)


def get_votes_info(contract, transaction):
    try:
        if transaction["functionName"] != "vote(bytes[] _encodedVotes)":
            raise NotAVoteException()
        if transaction["txreceipt_status"] != "1":
            raise BadTransaction()
        votes_to_return = []
        # Decode function input data
        decoded_input = contract.decode_function_input(transaction["input"])

        # pprint(decoded_input)

        for votes in decoded_input[1]["encodedVotes"]:
            # pprint(votes)
            # pprint(type(votes))
            # pprint(len(votes))
            # pprint(Web3.to_hex(votes))
            decoded_votes = eth_abi.decode(
                ["address", "uint256", "address", "bytes32"], votes
            )
            # pprint(decoded_votes)
            votes_to_return.append(decoded_votes)

        return votes_to_return
    except BadTransaction:
        raise
    except NotAVoteException:
        raise
    except Exception as e:
        print("Exception in get_votes_info:", e)
        traceback.print_exc()
        print("Transaction:", transaction)
        raise


def get_votes_for_contract(contract_address):
    print(f"\nGetting contract ABI for {contract_address}")
    abi_endpoint = "https://api.etherscan.io/api"
    response = requests.get(
        abi_endpoint,
        params={
            "module": "contract",
            "action": "getabi",
            "address": contract_address,
            "apikey": ETHERSCAN_API_KEY,
        },
    )
    print("Response:", response)
    abi = response.json()
    contract = web3.eth.contract(address=contract_address, abi=abi["result"])
    file_path = f"transactions_{contract_address}.json".lower()
    out_file_path = f"votes_{contract_address}.csv".lower()
    file_size = get_file_size(file_path)
    print("\n\nProcessing file: ", file_path)
    with open(out_file_path, "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["token", "amount", "grant_address", "project_id"])
        with open(file_path, "r") as file:
            with tqdm(
                total=file_size, desc="Loading transactions", unit="B", unit_scale=True
            ) as pbar:
                num_errors = 0
                for line in file:
                    json_object = json.loads(line.strip())
                    pbar.update(
                        len(line)
                    )  # Update the progress bar based on the number of bytes read
                    try:
                        votes = get_votes_info(contract, json_object)
                        writer.writerows(votes)
                        # print(votes)
                    except NotAVoteException:
                        pass
                    except BadTransaction:
                        pass
                    except Exception:
                        pass
                print("Number of errors:", num_errors)


for contract_address in contract_addresses_checksumed:
    get_votes_for_contract(contract_address)
