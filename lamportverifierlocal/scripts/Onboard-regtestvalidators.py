import lorem
from pathlib import Path
import sys
from itertools import chain
import random
import hashlib
import base64
from web3 import Web3
from web3.exceptions import InvalidAddress
from brownie import network, web3, accounts, Wei, PlayerOnboardContract, Contract, exceptions
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




gas_strategy = LinearScalingStrategy("1200 gwei", "120000 gwei", 1.1)

gas_price(gas_strategy)

def main():
    for _ in range(1):  # This will repeat the whole logic 3 times
        lamport_test = LamportTest()
        
        lamport_test.can_test_key_functions([str(acc) for acc in accounts])

class LamportTest:
    
    def __init__(self):

        print("Initializing LamportTest...")
        with open('contract_Onboard-coin.txt', 'r') as file:
            contract_address = file.read().strip()
        #print(contract_address)
        self.contract = PlayerOnboardContract.at(contract_address)
        #lamport_base = LamportBase.at(contract_address) # <<< not working!
        #accounts.default = str(accounts[0]) 
        # link it up
    
        print('init done')

    def can_test_key_functions(self, accs):
        global master_pkh_1
        global master_pkh_2
        #global master_pkh_3
        print("Running 'can_test_key_functions'...")
        with open('contract_Onboard-coin.txt', 'r') as file:
            contract_address = file.read()
            contract_address = contract_address.strip().replace('\n', '')  # Remove whitespace and newlines

        _contract = PlayerOnboardContract.at(contract_address)
        print("Contract referenced.")
        #print('master_pkh_1', master_pkh_1)
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

        address = "0xc576Ff74269bd2259E0927404C73b936989eeAd6"
#        0xDe7632E2c610c13dbA2553465f7A6ba3F90dC13f
#0xc576Ff74269bd2259E0927404C73b936989eeAd6

        #steam_id = "76561197971203827"  # Replace with actual Steam Community ID
        steam_id = "4"
        #is_validator = False
        #is_registered = True
        player_name = "val3"

        try:
            _contract.onboardPlayer(
                
                address,
                steam_id,
                player_name,
                2,
                1,
                address,
                {'from': brownie_account, 'gas_limit': 1000000}
            )
        except exceptions.VirtualMachineError as e:
            print(f"Transaction reverted: {e}")

        
# Assuming _contract is your deployed contract instance
        # Onboarded_filter = _contract.events.PlayerOnboarded.createFilter(fromBlock=0)

        # # Iterate through the events
        # for event in Onboarded_filter.get_all_entries():
        #     # Access event data
        #     userAddress = event['args']['playerAddress']  # Adjust field names based on your actual event signature
        #     steamID = event['args']['steamID']
        #     isValidator = event['args']['isValidator']
        #     isRegistered = event['args']['isRegistered']
        #     playerName = event['args']['_playerName']
        #     # Print the data
        #     print(f"userAddress: {userAddress}, steamID: {steamID}, isValidator: {isValidator}, isRegistered: {isRegistered}, _playerName: {playerName}")

        exit()
