import lorem

import sys
from itertools import chain
import random
import hashlib
import base64
from web3 import Web3
from web3.exceptions import InvalidAddress
from brownie import network, web3, accounts, Wei, GP_Mint, AnonIDContract, LamportBase2, Contract
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy
from eth_utils import encode_hex #, encode
from eth_abi import encode, encode
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

SOF = b'\x01'  # Start Of File marker
EOF = b'\x04'  # End Of File marker
CRC_START = b'<CRC>'
CRC_END = b'</CRC>'



gas_strategy = LinearScalingStrategy("120 gwei", "1200 gwei", 1.1)

# if network.show_active() == "development":
gas_price(gas_strategy)

# ITERATIONS = 3

# def compute_crc(self, data: str) -> int:
#     return crc32(data.encode())

offchain.data_temp.received_data = b''

def encode_packed(*args):
    return b"".join([struct.pack(f"<{len(arg)}s", arg) for arg in args])


def custom_encode_packed(address, integer):
    # Convert the address to bytes and pad with zeroes
    address_bytes = bytes(Web3.toBytes(hexstr=address))

    # Convert the integer to bytes and pad with zeroes
    integer_bytes = encode('uint', integer)

    # Concatenate everything together
    result = address_bytes + b'\0' * 12 + integer_bytes + b'\0' * 12

    return result.decode('unicode_escape')

def main():
    for _ in range(1):  # This will repeat the whole logic 3 times
        lamport_test = LamportTest()
        
        # Convert all account objects to strings before passing them
        lamport_test.can_test_key_functions([str(acc) for acc in accounts])


oracle_pkh = []
master_pkh_1 = []
master_pkh_2 = []
master_pkh_3 = []
master_pkh_4 = []
arg1 = "GPGrens"
arg2 = "GPG"

# ABI encode the arguments
encoded_args = encode(['string', 'string'], [arg1, arg2])

# Load the bytecode of the contract (replace with actual bytecode)
full_bytecode = "0x6080604052600180546001600160a01b03191673b03a6afd440a2a9db8834f1a6093680f02f1114c17905534801561003657600080fd5b50600154600080546001600160a01b0319166001600160a01b03909216919091179055610734806100686000396000f3fe608060405234801561001057600080fd5b50600436106100885760003560e01c806340a141ff1161005b57806340a141ff146100f85780639fca51691461010b578063c38c58131461011e578063cb7449931461013157600080fd5b806312243b671461008d578063143acc71146100a257806315fca479146100d25780631785f53c146100e5575b600080fd5b6100a061009b366004610459565b610160565b005b6100a06100b0366004610459565b600080546001600160a01b0319166001600160a01b0392909216919091179055565b6100a06100e036600461051e565b6101f6565b6100a06100f3366004610459565b610326565b6100a0610106366004610459565b610391565b6100a0610119366004610459565b6103cb565b6100a061012c366004610459565b610404565b600054610144906001600160a01b031681565b6040516001600160a01b03909116815260200160405180910390f35b6000546040516312243b6760e01b81526001600160a01b038381166004830152909116906312243b6790602401600060405180830381600087803b1580156101a757600080fd5b505af11580156101bb573d6000803e3d6000fd5b50506040516001600160a01b03841692507f9ac3117b086b001d2bcd36ff49e64f86a26f25d7c9ff453e9dbd9d496b8bf0849150600090a250565b826000036102645760405162461bcd60e51b815260206004820152603160248201527f4f7261636c65206b657920696e64657820312063616e6e6f74206265207a65726044820152706f20666f72206e657720706c617965727360781b606482015260840160405180910390fd5b600054604051631851edbf60e11b81526001600160a01b03909116906330a3db7e906102a0908a908a908a908a908a908a908a90600401610659565b600060405180830381600087803b1580156102ba57600080fd5b505af11580156102ce573d6000803e3d6000fd5b50505050866001600160a01b03167f8b06958157a003611013dd834a3bdfb55eeb806af66ebdb86b4952ede3191d5f878787878787604051610315969594939291906106b0565b60405180910390a250505050505050565b600080546040516316227ecd60e21b81526001600160a01b0384811660048301526024820193909352911690635889fb34906044015b600060405180830381600087803b15801561037657600080fd5b505af115801561038a573d6000803e3d6000fd5b5050505050565b6000805460405163aca2490b60e01b81526001600160a01b038481166004830152602482019390935291169063aca2490b9060440161035c565b60005460405163aca2490b60e01b81526001600160a01b038381166004830152600160248301529091169063aca2490b9060440161035c565b6000546040516316227ecd60e21b81526001600160a01b0383811660048301526001602483015290911690635889fb349060440161035c565b80356001600160a01b038116811461045457600080fd5b919050565b60006020828403121561046b57600080fd5b6104748261043d565b9392505050565b634e487b7160e01b600052604160045260246000fd5b600082601f8301126104a257600080fd5b813567ffffffffffffffff808211156104bd576104bd61047b565b604051601f8301601f19908116603f011681019082821181831017156104e5576104e561047b565b816040528381528660208588010111156104fe57600080fd5b836020870160208301376000602085830101528094505050505092915050565b600080600080600080600060c0888a03121561053957600080fd5b6105428861043d565b9650602088013567ffffffffffffffff8082111561055f57600080fd5b818a0191508a601f83011261057357600080fd5b81358181111561058257600080fd5b8b602082850101111561059457600080fd5b6020830198508097505060408a01359150808211156105b257600080fd5b506105bf8a828b01610491565b94505060608801359250608088013591506105dc60a0890161043d565b905092959891949750929550565b81835281816020850137506000828201602090810191909152601f909101601f19169091010190565b6000815180845260005b818110156106395760208185018101518683018201520161061d565b506000602082860101526020601f19601f83011685010191505092915050565b600060018060a01b03808a16835260c0602084015261067c60c08401898b6105ea565b838103604085015261068e8189610613565b606085019790975250608083019490945250911660a090910152949350505050565b60a0815260006106c460a08301888a6105ea565b82810360208401526106d68188610613565b6040840196909652505060608101929092526001600160a01b0316608090910152939250505056fea26469706673582212206cd275aa18b2375163660c4d0746913b2b4d30919e7f30560c6951e9f1f3118164736f6c63430008180033"
#print(encoded_args.hex())
# Append the encoded arguments to the bytecode
#print(full_bytecode)
class LamportTest:
    
    def __init__(self):

        self.k1 = KeyTracker("Gmaster1") # new keys made here
        self.k2 = KeyTracker("Gmaster2")
        self.k3 = KeyTracker("oracle1")
        self.k4 = KeyTracker("master3")
        self.k5 = KeyTracker("master4")
        print("Initializing LamportTest...")
        with open('contract_LamportBase2-coin.txt', 'r') as file:
            contract_address = file.read().strip()
        #print(contract_address)
        self.contract = LamportBase2.at(contract_address)
        #lamport_base = LamportBase.at(contract_address) # <<< not working!
        accounts.default = str(accounts[0]) 
        # link it up
        pkhs = self.get_pkh_list(self.contract, 0)
        opkhs = self.get_pkh_list(self.contract, 1)
        # priv level set here with integer ^
        print("contract pkh", pkhs)

        self.load_four_masters(pkhs, "master")
        self.load_keys(opkhs, "oracle")
        print('init done')

    def get_pkh_list(self, contract, privilege_level):
        with open('contract_LamportBase2-coin.txt', 'r') as file:
            contract_address = file.read().strip()
        contract2 = LamportBase2.at(contract_address)

        contract_pkh = str(contract2.getPKHsByPrivilege(privilege_level))
        # gonna need some kind of wait / delay here for primetime
        print(contract_pkh)
        contract_pkh_list = re.findall(r'0x[a-fA-F0-9]+', contract_pkh)
        pkh_list = [pkh for pkh in contract_pkh_list]  # Removing '0x' prefix
        contract_pkh_string = json.dumps(contract_pkh)
        contract_pkh_list = json.dumps(contract_pkh_string)
        return pkh_list

    
    def load_four_masters(self, pkhs, filename):
        pkh_index = 0
        master1_loaded = False
        master2_loaded = False
        master3_loaded = False
        master4_loaded = False
        global master_pkh_1
        global master_pkh_2
        global master_pkh_3
        global master_pkh_4

        while not master1_loaded and pkh_index < len(pkhs):
            try:
                self.k1.load(self, 'G' + filename + '1', pkhs[pkh_index])
                print(f"Load successful for Master 1, PKH: {pkhs[pkh_index]}")
                master1_loaded = True
                key_tracker_1 = self.k1.current_key_pair()
                master_pkh_1 = pkhs[pkh_index]
                pkh_index += 1  # increment the pkh_index after successful load
            except InvalidAddress:
                print(f"No valid keys found for Master 1, PKH: {pkhs[pkh_index]}")
                pkh_index += 1  # increment the pkh_index if load failed

        if not master1_loaded:
            print("Load failed for all provided PKHs for Master 1")
            return

        while not master2_loaded and pkh_index < len(pkhs):
            try:
                self.k2.load(self, 'G' + filename + '2', pkhs[pkh_index])
                print(f"Load successful for Master 2, PKH: {pkhs[pkh_index]}")
                master2_loaded = True
                key_tracker_2 = self.k2.current_key_pair()
                master_pkh_2 = pkhs[pkh_index]
                pkh_index += 1  # increment the pkh_index after successful load
            except InvalidAddress:
                print(f"No valid keys found for Master 2, PKH: {pkhs[pkh_index]}")
                pkh_index += 1  # increment the pkh_index if load failed

        if not master2_loaded:
            print("Load failed for all provided PKHs for Master 2")

        while not master3_loaded and pkh_index < len(pkhs):
            try:
                self.k4.load(self, filename + '3', pkhs[pkh_index])
                print(f"Load successful for Master 3, PKH: {pkhs[pkh_index]}")
                master3_loaded = True
                key_tracker_3 = self.k4.current_key_pair()
                master_pkh_3 = pkhs[pkh_index]
                pkh_index += 1  # increment the pkh_index after successful load
            except InvalidAddress:
                print(f"No valid keys found for Master 3, PKH: {pkhs[pkh_index]}")
                pkh_index += 1  # increment the pkh_index if load failed

        if not master3_loaded:
            print("Load failed for all provided PKHs for Master 3")

        while not master4_loaded and pkh_index < len(pkhs):
            try:
                self.k5.load(self, filename + '4', pkhs[pkh_index])
                print(f"Load successful for Master 3, PKH: {pkhs[pkh_index]}")
                master4_loaded = True
                key_tracker_4 = self.k5.current_key_pair()
                master_pkh_4 = pkhs[pkh_index]
                pkh_index += 1  # increment the pkh_index after successful load
            except InvalidAddress:
                print(f"No valid keys found for Master 3, PKH: {pkhs[pkh_index]}")
                pkh_index += 1  # increment the pkh_index if load failed

        if not master4_loaded:
            print("Load failed for all provided PKHs for Master 4")            

    def load_keys(self, pkhs, filename):
        global oracle_pkh
        for pkh in pkhs:
            try:
                oracle_pkh = pkh
                self.k3.load(self, filename + '1', pkh)
                print(f"Load successful for PKH: {pkh}")
                return  # Exit function after successful load
            except InvalidAddress:
                print(f"No valid keys found for PKH: {pkh}")
                continue  # Try the next pkh if this one fails
        print("Load failed for all provided PKHs")

    def can_test_key_functions(self, accs):
        global master_pkh_1
        global master_pkh_2
        global master_pkh_3
        global master_pkh_4
        print("Running 'can_test_key_functions'...")
        with open('contract_GP_Mint-coin.txt', 'r') as file:
            contract_address = file.read()
            contract_address = contract_address.strip().replace('\n', '')  # Remove whitespace and newlines

        _contract = GP_Mint.at(contract_address)
        print("Contract referenced.")
        print('master_pkh_1', master_pkh_1)
        private_key = '163f5f0f9a621d72fedd85ffca3d08d131ab4e812181e0d30ffd1c885d20aac7'
        brownie_account = accounts.add(private_key)
        current_keys = self.k1.load(self, "Gmaster1", master_pkh_1)
        current_pkh = self.k1.pkh_from_public_key(current_keys.pub)
        print('current pkh', current_pkh)
        next_keys = self.k1.get_next_key_pair()
        nextpkh = self.k1.pkh_from_public_key(next_keys.pub)
        #pairs = generate_address_value_pairs(10)
        #packed_pairs = solidity_pack_pairs(pairs)
        #_newCap = int(300000)
        #numToBroadcast = int(1000000)
        #pnumToBroadcast = numToBroadcast.to_bytes(4, 'big')
        #paddednumToBroadcast = solidity_pack_value_bytes(pnumToBroadcast)
        #paddressToBroadcast = '0x99a840C3BEEe41c3F5B682386f67277CfE3E3e29' # activity contract needing approval
        # with open('whitelist_contract.txt', 'r') as file:
        #     contract_address2 = file.read()
        #     contract_address2 = contract_address2.strip().replace('\n', '') 
        #paddressToBroadcast = '0xF3A99A9a2836a6fcFcEB846161B900B3d1447236'

        paddressToBroadcast = _contract.viewAuthorizedMinter({'from': brownie_account})

        print(paddressToBroadcast)
        packed_message = str.lower(paddressToBroadcast)[2:].encode() + nextpkh[2:].encode()
        print(packed_message)
        callhash = hash_b(str(packed_message.decode()))
        sig = sign_hash(callhash, current_keys.pri) 
        private_key = '163f5f0f9a621d72fedd85ffca3d08d131ab4e812181e0d30ffd1c885d20aac7'
        brownie_account = accounts.add(private_key)
        
        _contract.removeAuthorizedMinterStepOne(
            current_keys.pub,
            sig,
            nextpkh,
            #paddressToBroadcast,
            {'from': brownie_account, 'gas_limit': 3000000}    
        )
        self.k1.save(trim = False)
        #self.k4.save(trim = False)
        master_pkh_1 = nextpkh


        current_keys = self.k2.load(self, "Gmaster2", master_pkh_2)
        current_pkh = self.k2.pkh_from_public_key(current_keys.pub)
        print('current pkh', current_pkh)
        next_keys = self.k2.get_next_key_pair()
        nextpkh = self.k2.pkh_from_public_key(next_keys.pub)
        #pairs = generate_address_value_pairs(10)
        #packed_pairs = solidity_pack_pairs(pairs)
        #_newCap = int(300000)
        #numToBroadcast = int(1000000)
        #pnumToBroadcast = numToBroadcast.to_bytes(4, 'big')
        #paddednumToBroadcast = solidity_pack_value_bytes(pnumToBroadcast)
        #paddressToBroadcast = '0x99a840C3BEEe41c3F5B682386f67277CfE3E3e29' # activity contract needing approval
        # with open('whitelist_contract.txt', 'r') as file:
        #     contract_address2 = file.read()
        #     contract_address2 = contract_address2.strip().replace('\n', '') 
        hashToBroadcast = Web3.keccak(hexstr=full_bytecode)
        print(hashToBroadcast.hex())
        packed_message = str.lower(paddressToBroadcast)[2:].encode() + nextpkh[2:].encode()
        print(packed_message)
        callhash = hash_b(str(packed_message.decode()))
        sig = sign_hash(callhash, current_keys.pri) 
        private_key = '163f5f0f9a621d72fedd85ffca3d08d131ab4e812181e0d30ffd1c885d20aac7'
        brownie_account = accounts.add(private_key)
        
        _contract.removeAuthorizedMinterStepTwo(
            current_keys.pub,
            sig,
            nextpkh,
           #paddressToBroadcast,
            {'from': brownie_account, 'gas_limit': 3000000}    
        )
        self.k2.save(trim = False)
        #self.k4.save(trim = False)
        master_pkh_2 = nextpkh

        #current_keys = self.k2.load(self, "master2", master_pkh_2)
        #next_keys = self.k2.get_next_key_pair()
        #nextpkh = self.k2.pkh_from_public_key(next_keys.pub)

        #paddressToBroadcast = '0xfd003CA44BbF4E9fB0b2fF1a33fc2F05A6C2EFF9'

        #packed_message = str.lower(full_bytecode)[2:].encode() + nextpkh[2:].encode()

        #callhash = hash_b(str(packed_message.decode()))
        #sig = sign_hash(callhash, current_keys.pri) 


        

        exit()