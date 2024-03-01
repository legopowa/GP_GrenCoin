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
full_bytecode = "0x60806040523480156200001157600080fd5b50600080546001600160a01b03191673c3c2750054f28c22b28d87e4006f7cc302c7d7e517905560408051808201909152600781526647504772656e7360c81b6020820152600490620000659082620002b1565b5060408051808201909152600381526247504760e81b60208201526005906200008f9082620002b1565b506200009a620000a0565b620004d7565b600680546001600160a01b03191673f3a99a9a2836a6fcfceb846161b900b3d14472361790556200010d73239fa7623354ec26520de878b52f13fe84b06971620000e8601290565b620000f89060ff16600a62000492565b620001079062013880620004a7565b6200011f565b600680546001600160a01b0319169055565b6006546001600160a01b031633146200017e5760405162461bcd60e51b815260206004820152601c60248201527f47505f4d696e743a20556e617574686f72697a6564206d696e74657200000000604482015260640160405180910390fd5b8060036000828254620001929190620004c1565b90915550506001600160a01b03821660009081526001602052604081208054839290620001c1908490620004c1565b90915550506040518181526001600160a01b0383169033907f9d228d69b5fdb8d273a2336f8fb8612d039631024ea9bf09c424a9503aa078f09060200160405180910390a35050565b634e487b7160e01b600052604160045260246000fd5b600181811c908216806200023557607f821691505b6020821081036200025657634e487b7160e01b600052602260045260246000fd5b50919050565b601f821115620002ac576000816000526020600020601f850160051c81016020861015620002875750805b601f850160051c820191505b81811015620002a85782815560010162000293565b5050505b505050565b81516001600160401b03811115620002cd57620002cd6200020a565b620002e581620002de845462000220565b846200025c565b602080601f8311600181146200031d5760008415620003045750858301515b600019600386901b1c1916600185901b178555620002a8565b600085815260208120601f198616915b828110156200034e578886015182559484019460019091019084016200032d565b50858210156200036d5787850151600019600388901b60f8161c191681555b5050505050600190811b01905550565b634e487b7160e01b600052601160045260246000fd5b600181815b80851115620003d4578160001904821115620003b857620003b86200037d565b80851615620003c657918102915b93841c939080029062000398565b509250929050565b600082620003ed575060016200048c565b81620003fc575060006200048c565b8160018114620004155760028114620004205762000440565b60019150506200048c565b60ff8411156200043457620004346200037d565b50506001821b6200048c565b5060208310610133831016604e8410600b841016171562000465575081810a6200048c565b62000471838362000393565b80600019048211156200048857620004886200037d565b0290505b92915050565b6000620004a08383620003dc565b9392505050565b80820281158282048414176200048c576200048c6200037d565b808201808211156200048c576200048c6200037d565b61129c80620004e76000396000f3fe608060405234801561001057600080fd5b50600436106100f55760003560e01c806370a0823111610097578063dd62ed3e11610066578063dd62ed3e14610206578063e5f855b71461023f578063e951ae2314610252578063f0dda65c1461026557600080fd5b806370a08231146101af5780638486e2ff146101d857806395d89b41146101eb578063a9059cbb146101f357600080fd5b806323b872dd116100d357806323b872dd1461014d5780632a66312014610160578063313ce5671461017557806356bf7b571461018457600080fd5b806306fdde03146100fa578063095ea7b31461011857806318160ddd1461013b575b600080fd5b610102610278565b60405161010f9190610e07565b60405180910390f35b61012b610126366004610e3d565b61030a565b604051901515815260200161010f565b6003545b60405190815260200161010f565b61012b61015b366004610e67565b6103d8565b61017361016e366004610ec7565b6105a7565b005b6040516012815260200161010f565b600054610197906001600160a01b031681565b6040516001600160a01b03909116815260200161010f565b61013f6101bd366004610f34565b6001600160a01b031660009081526001602052604090205490565b6101736101e6366004610f4f565b610699565b610102610882565b61012b610201366004610e3d565b610891565b61013f610214366004610faa565b6001600160a01b03918216600090815260026020908152604080832093909416825291909152205490565b61017361024d366004610f4f565b610976565b610173610260366004610ec7565b610a66565b610173610273366004610e3d565b610c77565b60606004805461028790610fdd565b80601f01602080910402602001604051908101604052809291908181526020018280546102b390610fdd565b80156103005780601f106102d557610100808354040283529160200191610300565b820191906000526020600020905b8154815290600101906020018083116102e357829003601f168201915b5050505050905090565b60006001600160a01b0383166103725760405162461bcd60e51b815260206004820152602260248201527f45524332303a20617070726f766520746f20746865207a65726f206164647265604482015261737360f01b60648201526084015b60405180910390fd5b3360008181526002602090815260408083206001600160a01b03881680855290835292819020869055518581529192917f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b92591015b60405180910390a35060015b92915050565b60006001600160a01b0383166104005760405162461bcd60e51b815260040161036990611017565b6001600160a01b0384166000908152600160205260409020548211156104385760405162461bcd60e51b81526004016103699061105a565b6001600160a01b03841660009081526002602090815260408083203384529091529020548211156104bc5760405162461bcd60e51b815260206004820152602860248201527f45524332303a207472616e7366657220616d6f756e74206578636565647320616044820152676c6c6f77616e636560c01b6064820152608401610369565b6001600160a01b038416600090815260016020526040812080548492906104e49084906110b6565b90915550506001600160a01b038316600090815260016020526040812080548492906105119084906110c9565b90915550506001600160a01b0384166000908152600260209081526040808320338452909152812080548492906105499084906110b6565b92505081905550826001600160a01b0316846001600160a01b03167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef8460405161059591815260200190565b60405180910390a35060019392505050565b6000816040516020016105ba91906110dc565b60408051601f19818403018152908290526000805463333f611160e01b8452919350916001600160a01b039091169063333f611190610603908990899089908890600401611122565b6020604051808303816000875af1158015610622573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906106469190611203565b9050806106655760405162461bcd60e51b815260040161036990611225565b505033600090815260076020526040902080546001600160a01b0319166001600160a01b0392909216919091179055505050565b6000806040516020016106ac91906110dc565b60408051601f19818403018152908290526000805463333f611160e01b8452919350916001600160a01b039091169063333f6111906106f5908890889088908890600401611122565b6020604051808303816000875af1158015610714573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906107389190611203565b9050806107575760405162461bcd60e51b815260040161036990611225565b336000908152600760205260409020546001600160a01b0316156107c95760405162461bcd60e51b815260206004820152602360248201527f47505f4d696e743a204e6f206d696e7465722072656d6f76616c2070726f706f6044820152621cd95960ea1b6064820152608401610369565b6006546001600160a01b031661081a5760405162461bcd60e51b815260206004820152601660248201527511d417d35a5b9d0e88139bc81b5a5b9d195c881cd95d60521b6044820152606401610369565b6006546040516001600160a01b03909116907fc6711413797b8a562634e98c95d50e7619d39702ed5b82ce335dc93546c3a88c90600090a25050600680546001600160a01b031990811690915533600090815260076020526040902080549091169055505050565b60606005805461028790610fdd565b60006001600160a01b0383166108b95760405162461bcd60e51b815260040161036990611017565b336000908152600160205260409020548211156108e85760405162461bcd60e51b81526004016103699061105a565b33600090815260016020526040812080548492906109079084906110b6565b90915550506001600160a01b038316600090815260016020526040812080548492906109349084906110c9565b90915550506040518281526001600160a01b0384169033907fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef906020016103c6565b600654604051600091610997916001600160a01b03909116906020016110dc565b60408051601f19818403018152908290526000805463333f611160e01b8452919350916001600160a01b039091169063333f6111906109e0908890889088908890600401611122565b6020604051808303816000875af11580156109ff573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610a239190611203565b905080610a425760405162461bcd60e51b815260040161036990611225565b505033600090815260076020526040902080546001600160a01b0319169055505050565b600081604051602001610a7991906110dc565b60408051601f19818403018152908290526000805463333f611160e01b8452919350916001600160a01b039091169063333f611190610ac2908990899089908890600401611122565b6020604051808303816000875af1158015610ae1573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610b059190611203565b905080610b245760405162461bcd60e51b815260040161036990611225565b336000908152600760205260409020546001600160a01b03848116911614610b8e5760405162461bcd60e51b815260206004820181905260248201527f4d7945524332303a204d696e7465722061646472657373206d69736d617463686044820152606401610369565b6006546001600160a01b03161580610bb357506006546001600160a01b038481169116145b610c0b5760405162461bcd60e51b815260206004820152602360248201527f4d7945524332303a20416e6f74686572206d696e74657220616c7265616479206044820152621cd95d60ea1b6064820152608401610369565b600680546001600160a01b0319166001600160a01b0385169081179091556040517ffe7c7fcb0ae0ce6bfd0a653fa3ab6c97a51a0819e6c27cdab8a08d456338c5fa90600090a2505033600090815260076020526040902080546001600160a01b031916905550505050565b6006546001600160a01b03163314610cd15760405162461bcd60e51b815260206004820152601c60248201527f47505f4d696e743a20556e617574686f72697a6564206d696e746572000000006044820152606401610369565b610cdb8282610cdf565b5050565b6006546001600160a01b03163314610d395760405162461bcd60e51b815260206004820152601c60248201527f47505f4d696e743a20556e617574686f72697a6564206d696e746572000000006044820152606401610369565b8060036000828254610d4b91906110c9565b90915550506001600160a01b03821660009081526001602052604081208054839290610d789084906110c9565b90915550506040518181526001600160a01b0383169033907f9d228d69b5fdb8d273a2336f8fb8612d039631024ea9bf09c424a9503aa078f09060200160405180910390a35050565b6000815180845260005b81811015610de757602081850181015186830182015201610dcb565b506000602082860101526020601f19601f83011685010191505092915050565b602081526000610e1a6020830184610dc1565b9392505050565b80356001600160a01b0381168114610e3857600080fd5b919050565b60008060408385031215610e5057600080fd5b610e5983610e21565b946020939093013593505050565b600080600060608486031215610e7c57600080fd5b610e8584610e21565b9250610e9360208501610e21565b9150604084013590509250925092565b8061400081018310156103d257600080fd5b8061200081018310156103d257600080fd5b6000806000806140608587031215610ede57600080fd5b610ee88686610ea3565b935061400085013567ffffffffffffffff811115610f0557600080fd5b610f1187828801610eb5565b9350506140208501359150610f296140408601610e21565b905092959194509250565b600060208284031215610f4657600080fd5b610e1a82610e21565b60008060006140408486031215610f6557600080fd5b610f6f8585610ea3565b925061400084013567ffffffffffffffff811115610f8c57600080fd5b610f9886828701610eb5565b92505061402084013590509250925092565b60008060408385031215610fbd57600080fd5b610fc683610e21565b9150610fd460208401610e21565b90509250929050565b600181811c90821680610ff157607f821691505b60208210810361101157634e487b7160e01b600052602260045260246000fd5b50919050565b60208082526023908201527f45524332303a207472616e7366657220746f20746865207a65726f206164647260408201526265737360e81b606082015260800190565b60208082526026908201527f45524332303a207472616e7366657220616d6f756e7420657863656564732062604082015265616c616e636560d01b606082015260800190565b634e487b7160e01b600052601160045260246000fd5b818103818111156103d2576103d26110a0565b808201808211156103d2576103d26110a0565b60609190911b6bffffffffffffffffffffffff1916815260140190565b81835281816020850137506000828201602090810191909152601f909101601f19169091010190565b60006140608281018388845b61010081101561114f5760408083853792830192919091019060010161112e565b50505061400084019190915261606083018660005b6101008110156111db5785830361405f190184528135368a9003601e1901811261118d57600080fd5b8901602081810191359067ffffffffffffffff8211156111ac57600080fd5b8136038313156111bb57600080fd5b6111c68683856110f9565b96810196955093909301925050600101611164565b5050856140208501528381036140408501526111f78186610dc1565b98975050505050505050565b60006020828403121561121557600080fd5b81518015158114610e1a57600080fd5b60208082526021908201527f4c616d706f7274426173653a20417574686f72697a6174696f6e206661696c656040820152601960fa1b60608201526080019056fea26469706673582212209303d947afaad355842fa0b7aed189e0fca237816fb4d96ff971c901100bc41d64736f6c63430008180033"
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

        with open('contract_GP_Mint-coin.txt', 'w') as file:
            # Write the contract address to the file
            file.write(new_contract_address)
        exit()