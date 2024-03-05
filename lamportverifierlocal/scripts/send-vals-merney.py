import lorem
from pathlib import Path
import sys
from itertools import chain
import random
import hashlib
import base64
from web3 import Web3
from web3.exceptions import InvalidAddress
from brownie import network, web3, accounts, Wei, PlayerListHasher, Contract
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy
from eth_utils import encode_hex #, encode
from eth_abi import encode
from Crypto.Hash import keccak
from typing import List
import json
import os
import ast
import time
from time import sleep
import re
from typing import List
import struct
from offchain.local_functions import get_pkh_list
from offchain.KeyTracker_ import KeyTracker
from offchain.soliditypack import solidity_pack_value_bytes, solidity_pack_value, pack_keys, encode_packed_2d_list, solidity_pack_bytes, encode_packed, solidity_pack_pairs, solidity_pack, solidity_pack_bytes, solidity_pack_array
from offchain.Types import LamportKeyPair, Sig, PubPair
from offchain.functions import hash_b, sign_hash, verify_signed_hash
from eth_abi import encode, encode
from binascii import crc32, hexlify
import binascii
from offchain.crc import compute_crc
#from offchain.oracle_functions import extract_data_from_file, get_pkh_list, send_pkh_with_crc, save_received_data, read_till_eof, send_packed_file
import offchain.data_temp


w3 = Web3()

# Function to encode and hash serverPlayerLists
def compute_keccak_hash(serverPlayerLists):
    # Initialize Web3
    #w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Update with your provider

    # Convert the list of tuples into a format for hashing
    types_and_values = []
    for serverIP, playerNames in serverPlayerLists:
        types_and_values.append(('string', serverIP))
        # For dynamic arrays, prepend the length of the array followed by its items
        types_and_values.append(('uint256', len(playerNames)))  # Array length
        for playerName in playerNames:
            types_and_values.append(('string', playerName))  # Array items

    # Separate the types and values
    types = [pair[0] for pair in types_and_values]
    values = [pair[1] for pair in types_and_values]

    # Compute the keccak hash
    hash = w3.solidity_keccak(types, values)

    return hash.hex()



gas_strategy = LinearScalingStrategy("1200 gwei", "120000 gwei", 1.1)

gas_price(gas_strategy)

def main():
    for _ in range(1):  # This will repeat the whole logic 3 times
        lamport_test = LamportTest()
        
        lamport_test.can_test_key_functions([str(acc) for acc in accounts])

class LamportTest:
    
    def __init__(self):

        print("Initializing LamportTest...")
        with open('contract_AnonID.txt', 'r') as file:
            contract_address = file.read().strip()
        #print(contract_address)
        #self.contract = AnonIDContract.at(contract_address)
        #lamport_base = LamportBase.at(contract_address) # <<< not working!
        #accounts.default = str(accounts[0]) 
        # link it up
    
        print('init done')

    def can_test_key_functions(self, accs):
        global master_pkh_1
        global master_pkh_2
        #global master_pkh_3
        print("Running 'can_test_key_functions'...")
        with open('contract_test-coin.txt', 'r') as file:
            contract_address = file.read()
            contract_address = contract_address.strip().replace('\n', '')  # Remove whitespace and newlines

        _contract = PlayerListHasher.at(contract_address)
        print("Contract referenced.")
        ##print('master_pkh_1', master_pkh_1)
        private_key = '163f5f0f9a621d72fedd85ffca3d08d131ab4e812181e0d30ffd1c885d20aac7'
        brownie_account = accounts.add(private_key)
        ##mnemonic using user acct
                # Read mnemonic from file
        mnemonic_path = Path('mnemonic.txt')
        if not mnemonic_path.is_file():
            raise Exception(f"Can't find {mnemonic_path}")

        with open(mnemonic_path, "r") as file:
            mnemonic = file.read().strip()

        # Generate the account using the mnemonic
        user_account = accounts.from_mnemonic(mnemonic) # for account from mnemonic
        
        
        serverPlayersLists = [
            {
                "serverIP": "192.168.1.1",
                "playerNames": ["PlayerA"]
            },
            {
                "serverIP": "192.168.1.2",
                "playerNames": ["PlayerB", "PlayerC", "PlayerD"]
            },
            {
                "serverIP": "192.168.1.3",
                "playerNames": ["PlayerE", "PlayerF"]
            }
        ]
        #hash_value = compute_keccak_hash(serverPlayersLists)
        #print(hash_value)
        # Initialize Web3

        #encodedplayerlist = encode(serverPlayersLists)
        #print(encodedplayerlist)

        # tx =_contract.submitServerPlayersList(
        #     serverPlayersLists,
        #     {'from': user_account, 'gas_limit': 500000}

        # )

        formatted_lists = [
            (item["serverIP"], item["playerNames"]) for item in serverPlayersLists
        ]
        data_to_hash = "192.168.1.1PlayerA192.168.1.2PlayerBPlayerCPlayerD192.168.1.3PlayerEPlayerF".encode()

# Use web3.solidityKeccak to hash the data
        hashed_data = w3.solidity_keccak(['bytes'], [data_to_hash])

        print("clientside solidity_keccak:", hashed_data.hex())
        print(hashed_data)
        clientsidehash = compute_keccak_hash(formatted_lists)
        print(clientsidehash)
        # tx = _contract.submitServerPlayersList(
        #     formatted_lists,
        #     {'from': brownie_account, 'gas_limit': 500000}

        # )        
        # tx2 = _contract.getComputedHash(
        #     {'from': brownie_account, 'gas_limit': 500000}

        # )

        
        # print("solidity keccak function:", tx2)
        # encoded_data_event = tx.events['EncodedData']
        # print(f"Encoded Data: {encoded_data_event[0]['encodedData']}")
        # # ClaimedGP_filter = _contract.events.ClaimedGP.createFilter(fromBlock='latest')
        validators = [
            "0x72Bb7788cdA33503F247A818556c918f57cCa6c3",
            "0xDe7632E2c610c13dbA2553465f7A6ba3F90dC13f",
            "0xc576Ff74269bd2259E0927404C73b936989eeAd6",
        ]
        
        # Amount to send to each validator, e.g., 0.1 Ether
        amount_to_send = Wei("0.1 ether")

        # Your account to send transactions from
        # Ensure this account is loaded in Brownie and has sufficient balance
        sender_account = accounts[0]
        
        # Send Ether to each validator
        for validator in validators:
            print(f"Sending {amount_to_send} to {validator}")
            brownie_account.transfer(validator, amount_to_send)
            print(f"Sent {amount_to_send} to {validator}")

        # # Iterate through the events
        # for event in ClaimedGP_filter.get_all_entries():
        #     # Access event data
        #     userAddress = event['args']['userAddress']
        #     lastClaimValue = event['args']['lastClaimValue']
        #     minutesPlayed = event['args']['minutesPlayed']

        #     # Print the data
        #     print(f"userAddress: {userAddress}, lastClaimValue: {lastClaimValue}, minutesPlayed: {minutesPlayed}")
        exit()