import lorem

import sys
from itertools import chain
import random
import hashlib
import base64
from web3 import Web3
from web3.exceptions import InvalidAddress
from brownie import network, web3, accounts, Wei, AnonIDContract, LamportBase2, Contract
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
full_bytecode = "0x608060405234801561001057600080fd5b5061055a806100206000396000f3fe608060405234801561001057600080fd5b506004361061004b5760003560e01c806236a479146100505780635cf2737314610067578063a3fc369514610078578063cf09f9531461008d575b600080fd5b6000545b6040519081526020015b60405180910390f35b6100546100753660046101dd565b90565b61008b6100863660046102fa565b6100b2565b005b6100a261009b3660046101dd565b6000541490565b604051901515815260200161005e565b606060005b825181101561019657818382815181106100d3576100d3610488565b6020026020010151600001516040516020016100f09291906104c2565b604051602081830303815290604052915060005b83828151811061011657610116610488565b6020026020010151602001515181101561018d578284838151811061013d5761013d610488565b602002602001015160200151828151811061015a5761015a610488565b60200260200101516040516020016101739291906104c2565b60408051601f198184030181529190529250600101610104565b506001016100b7565b50805160208201206000556040517fc7141718c98b98915637a29753ebd036f810bd5b325c3d1a9ce947794844ed6d906101d19083906104f1565b60405180910390a15050565b6000602082840312156101ef57600080fd5b5035919050565b634e487b7160e01b600052604160045260246000fd5b6040805190810167ffffffffffffffff8111828210171561022f5761022f6101f6565b60405290565b604051601f8201601f1916810167ffffffffffffffff8111828210171561025e5761025e6101f6565b604052919050565b600067ffffffffffffffff821115610280576102806101f6565b5060051b60200190565b600082601f83011261029b57600080fd5b813567ffffffffffffffff8111156102b5576102b56101f6565b6102c8601f8201601f1916602001610235565b8181528460208386010111156102dd57600080fd5b816020850160208301376000918101602001919091529392505050565b60006020828403121561030c57600080fd5b67ffffffffffffffff808335111561032357600080fd5b8235830184601f82011261033657600080fd5b6103486103438235610266565b610235565b81358082526020808301929160051b8401018781111561036757600080fd5b602084015b8181101561047b57858135111561038257600080fd5b803585016040818b03601f1901121561039a57600080fd5b6103a261020c565b87602083013511156103b357600080fd5b6103c58b60208085013585010161028a565b815287604083013511156103d857600080fd5b6040820135820191508a603f8301126103f057600080fd5b602082013561040161034382610266565b81815260059190911b83016040019060208101908d83111561042257600080fd5b604085015b8381101561045b578b8135111561043d57600080fd5b61044d8f6040833589010161028a565b835260209283019201610427565b50806020850152505050808652505060208401935060208101905061036c565b5090979650505050505050565b634e487b7160e01b600052603260045260246000fd5b60005b838110156104b95781810151838201526020016104a1565b50506000910152565b600083516104d481846020880161049e565b8351908301906104e881836020880161049e565b01949350505050565b602081526000825180602084015261051081604085016020870161049e565b601f01601f1916919091016040019291505056fea264697066735822122030670e76cb89575ed3af32fc40f9f4c3a62c331e1ab918f93a7482a28eebec5364736f6c63430008180033"
#print(encoded_args.hex())
# Append the encoded arguments to the bytecode
#print(full_bytecode)
class LamportTest:
    
    def __init__(self):

        self.k1 = KeyTracker("master1") # new keys made here
        self.k2 = KeyTracker("master2")
        self.k3 = KeyTracker("oracle1")
        self.k4 = KeyTracker("master3")
        self.k5 = KeyTracker("master4")
        print("Initializing LamportTest...")
        with open('contract_AnonID.txt', 'r') as file:
            contract_address = file.read().strip()
        #print(contract_address)
        self.contract = AnonIDContract.at(contract_address)
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
        with open('contract_LamportBase2.txt', 'r') as file:
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
                self.k1.load(self, filename + '1', pkhs[pkh_index])
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
                self.k2.load(self, filename + '2', pkhs[pkh_index])
                print(f"Load successful for Master 2, PKH: {pkhs[pkh_index]}")
                master2_loaded = True
                key_tracker_2 = self.k2.current_key_pair()
                master_pkh_2 = pkhs[pkh_index]
                pkh_index += 1  # increment the pkh_index after successful load
            except InvalidAddress:
                print(f"No valid keys found for Master 2, PKH: {pkhs[pkh_index]}")
                pkh_index += 1  # increment the pkh_index if load failed

        if not master3_loaded:
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

        if not master4_loaded:
            print("Load failed for all provided PKHs for Master 2")

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
            print("Load failed for all provided PKHs for Master 2")            

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
        with open('contract_AnonID.txt', 'r') as file:
            contract_address = file.read()
            contract_address = contract_address.strip().replace('\n', '')  # Remove whitespace and newlines

        _contract = AnonIDContract.at(contract_address)
        print("Contract referenced.")
        print('master_pkh_3', master_pkh_3)
        private_key = '163f5f0f9a621d72fedd85ffca3d08d131ab4e812181e0d30ffd1c885d20aac7'
        brownie_account = accounts.add(private_key)
        current_keys = self.k4.load(self, "master3", master_pkh_3)
        current_pkh = self.k4.pkh_from_public_key(current_keys.pub)
        print('current pkh', current_pkh)
        next_keys = self.k4.get_next_key_pair()
        nextpkh = self.k4.pkh_from_public_key(next_keys.pub)
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
        packed_message = str.lower(hashToBroadcast.hex())[2:].encode() + nextpkh[2:].encode()
        print(packed_message)
        callhash = hash_b(str(packed_message.decode()))
        sig = sign_hash(callhash, current_keys.pri) 
        private_key = '163f5f0f9a621d72fedd85ffca3d08d131ab4e812181e0d30ffd1c885d20aac7'
        brownie_account = accounts.add(private_key)
        
        _contract.createContractStepOne(
            current_keys.pub,
            sig,
            nextpkh,
            hashToBroadcast,
            {'from': brownie_account, 'gas_limit': 3999999}    
        )
        self.k4.save(trim = False)
        #self.k4.save(trim = False)
        master_pkh_3 = nextpkh


        current_keys = self.k5.load(self, "master4", master_pkh_4)
        current_pkh = self.k5.pkh_from_public_key(current_keys.pub)
        print('current pkh', current_pkh)
        next_keys = self.k5.get_next_key_pair()
        nextpkh = self.k5.pkh_from_public_key(next_keys.pub)
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
        packed_message = str.lower(hashToBroadcast.hex())[2:].encode() + nextpkh[2:].encode()
        print(packed_message)
        callhash = hash_b(str(packed_message.decode()))
        sig = sign_hash(callhash, current_keys.pri) 
        private_key = '163f5f0f9a621d72fedd85ffca3d08d131ab4e812181e0d30ffd1c885d20aac7'
        brownie_account = accounts.add(private_key)
        
        _contract.createContractStepOne(
            current_keys.pub,
            sig,
            nextpkh,
            hashToBroadcast,
            {'from': brownie_account, 'gas_limit': 3999999}    
        )
        self.k5.save(trim = False)
        #self.k4.save(trim = False)
        master_pkh_4 = nextpkh

        #current_keys = self.k2.load(self, "master2", master_pkh_2)
        #next_keys = self.k2.get_next_key_pair()
        #nextpkh = self.k2.pkh_from_public_key(next_keys.pub)

        #paddressToBroadcast = '0xfd003CA44BbF4E9fB0b2fF1a33fc2F05A6C2EFF9'

        #packed_message = str.lower(full_bytecode)[2:].encode() + nextpkh[2:].encode()

        #callhash = hash_b(str(packed_message.decode()))
        #sig = sign_hash(callhash, current_keys.pri) 


        
        tx = _contract.createContractStepThree(

            full_bytecode,
            {'from': brownie_account, 'gas_limit': 3999999}    
        )
        tx.wait(1)

        # Extract the new contract address from the transaction's events
        new_contract_address = tx.events['ContractCreated']['contractAddress']

        print(f"New contract address: {new_contract_address}")
        #self.k2.save(trim = False)

        with open('contract_test-coin.txt', 'w') as file:
            # Write the contract address to the file
            file.write(new_contract_address)
        exit()