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
from eth_utils import encode_hex #, encode_single
from eth_abi import encode_single, encode_abi
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
from eth_abi import encode_abi, encode_single
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
    integer_bytes = encode_single('uint', integer)

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
encoded_args = encode_abi(['string', 'string'], [arg1, arg2])

# Load the bytecode of the contract (replace with actual bytecode)
full_bytecode = "0x60806040526000805460ff191690553480156200001b57600080fd5b506200004960007fb7b18ded9664d1a8e923a5942ec1ca5cd8c13c40eb1a5215d5800600f5a587be620000b6565b6200007660007f1ed304ab73e124b0b99406dfa1388a492a818837b4b41ce5693ad84dacfc3f25620000b6565b620000a360017fd62569e61a6423c880a429676be48756c931fe0519121684f5fb05cbd17877fa620000b6565b6000805460ff191660011790556200021d565b60006040518060400160405280846002811115620000d857620000d8620001da565b81526020018390526001805480820182556000829052825160029182027fb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6018054949550859490939192849260ff1990921691908490811115620001405762000140620001da565b021790555060209182015160019182015560008481526002928390526040902083518154859492939192849260ff1990921691908490811115620001885762000188620001da565b0217905550602082015181600101559050507f2172c7b01a6de957d29fd6166a23025d181bf56538ad606a526ab2d62603f3fc8383604051620001cd929190620001f0565b60405180910390a1505050565b634e487b7160e01b600052602160045260246000fd5b60408101600384106200021357634e487b7160e01b600052602160045260246000fd5b9281526020015290565b611c66806200022d6000396000f3fe608060405234801561001057600080fd5b50600436106100ea5760003560e01c80635796841a1161008c578063af82f3e711610066578063af82f3e714610202578063b97b4f7714610215578063d83c413c14610235578063e673d71f1461024857600080fd5b80635796841a146101af5780638eb8f1a6146101c2578063a9711ee3146101d557600080fd5b8063333f6111116100c8578063333f61111461015d5780634a89d52b146101705780634bdd4499146101835780634e657d2a1461019a57600080fd5b806305aacc7d146100ef5780630cb6aaf11461011a5780632fd5c2471461013b575b600080fd5b6101026100fd3660046116b2565b61025b565b60405161011193929190611703565b60405180910390f35b61012d6101283660046116b2565b610362565b604051610111929190611722565b60005461014d90610100900460ff1681565b6040519015158152602001610111565b61014d61016b36600461177d565b610394565b61014d61017e36600461177d565b610485565b61018c60055481565b604051908152602001610111565b6101ad6101a836600461177d565b6104dc565b005b6101ad6101bd366004611872565b6106ad565b6101ad6101d03660046118d5565b61090c565b61012d6101e33660046116b2565b6002602052600090815260409020805460019091015460ff9091169082565b61014d610210366004611939565b610ab5565b610228610223366004611992565b610b6a565b60405161011191906119b3565b6101ad610243366004611872565b610d1a565b6101ad610256366004611872565b610ec2565b60008181526002602081905260408083208151808301909252805484938493849390929091839160ff1690811115610295576102956116cb565b60028111156102a6576102a66116cb565b8152600191909101546020918201528101519091506000036102e35760405162461bcd60e51b81526004016102da906119f7565b60405180910390fd5b60005b60015481101561034257856001828154811061030457610304611a2e565b90600052602060002090600202016001015403610330578151602090920151919450909250905061035b565b8061033a81611a44565b9150506102e6565b5060405162461bcd60e51b81526004016102da906119f7565b9193909250565b6001818154811061037257600080fd5b60009182526020909120600290910201805460019091015460ff909116915082565b6000805460ff166103b75760405162461bcd60e51b81526004016102da90611a6b565b6000856040516020016103ca9190611aa2565b60408051601f198184030181529190528051602090910120905060005b60008281526002602081905260409091205460ff169081111561040c5761040c6116cb565b1461041b57600091505061047d565b60008385604051602001610430929190611ad9565b6040516020818303038152906040528051906020012060001c9050600061045882888a610ab5565b90508061046b576000935050505061047d565b61047583876113f7565b600193505050505b949350505050565b6000805460ff166104a85760405162461bcd60e51b81526004016102da90611a6b565b6000856040516020016104bb9190611aa2565b60408051601f198184030181529190528051602090910120905060016103e7565b600054849084908490849060ff166105065760405162461bcd60e51b81526004016102da90611a6b565b6000846040516020016105199190611aa2565b60408051601f19818403018152919052805160209091012090506000808281526002602081905260409091205460ff1690811115610559576105596116cb565b146105765760405162461bcd60e51b81526004016102da90611b0b565b6000828460405160200161058b929190611ad9565b60408051601f198184030181529082905280516020918201208083529250600080516020611bf1833981519152910160405180910390a160006105cf828789610ab5565b6000805461ff0019166101008315150217905590508061065357604051828152600080516020611bd1833981519152906020015b60405180910390a160405162461bcd60e51b815260206004820181905260248201527f4c616d706f7274426173653a20566572696669636174696f6e206661696c656460448201526064016102da565b60008381526002602052604090819020549051600080516020611c11833981519152916106899160ff9091169086908990611703565b60405180910390a161069b83866113f7565b50505060059590955550505050505050565b838383836040516020016106c391815260200190565b60408051601f1981840301815291905260005460ff166106f55760405162461bcd60e51b81526004016102da90611a6b565b6000846040516020016107089190611aa2565b60408051601f19818403018152919052805160209091012090506000808281526002602081905260409091205460ff1690811115610748576107486116cb565b146107655760405162461bcd60e51b81526004016102da90611b0b565b6000828460405160200161077a929190611ad9565b60408051601f198184030181529082905280516020918201208083529250600080516020611bf1833981519152910160405180910390a160006107be828789610ab5565b6000805461ff001916610100831515021790559050806107f657604051828152600080516020611bd183398151915290602001610603565b60008381526002602052604090819020549051600080516020611c118339815191529161082c9160ff9091169086908990611703565b60405180910390a161083e83866113f7565b60008b6040516020016108519190611aa2565b60408051601f198184030181529190528051602090910120600580546000909155909150811415806108ed576040805162461bcd60e51b81526020600482015260248101919091527f4c616d706f7274426173653a20504b48206d617463686573206c61737420757360448201527f656420504b482028757365207365706172617465207365636f6e64206b65792960648201526084016102da565b6108f860008b6115a6565b505060006005555050505050505050505050565b8382848360405160200161092291815260200190565b60408051601f1981840301815291905260005460ff166109545760405162461bcd60e51b81526004016102da90611a6b565b6000846040516020016109679190611aa2565b60408051601f19818403018152919052805160209091012090506000808281526002602081905260409091205460ff16908111156109a7576109a76116cb565b146109c45760405162461bcd60e51b81526004016102da90611b0b565b600082846040516020016109d9929190611ad9565b60408051601f198184030181529082905280516020918201208083529250600080516020611bf1833981519152910160405180910390a16000610a1d828789610ab5565b6000805461ff00191661010083151502179055905080610a5557604051828152600080516020611bd183398151915290602001610603565b60008381526002602052604090819020549051600080516020611c1183398151915291610a8b9160ff9091169086908990611703565b60405180910390a1610a9d83866113f7565b610aa86001896115a6565b5050505050505050505050565b6000805b610100811015610b5d5783816101008110610ad657610ad6611a2e565b602002810190610ae69190611b42565b604051610af4929190611b90565b604051809103902083826101008110610b0f57610b0f611a2e565b6040020160008360ff036001901b881611610b2b576000610b2e565b60015b60ff1660028110610b4157610b41611a2e565b602002013514610b55576000915050610b63565b600101610ab9565b50600190505b9392505050565b60015460609060009067ffffffffffffffff811115610b8b57610b8b611767565b604051908082528060200260200182016040528015610bb4578160200160208202803683370190505b5090506000805b600154811015610c7557846002811115610bd757610bd76116cb565b60018281548110610bea57610bea611a2e565b600091825260209091206002918202015460ff1690811115610c0e57610c0e6116cb565b03610c635760018181548110610c2657610c26611a2e565b906000526020600020906002020160010154838381518110610c4a57610c4a611a2e565b602090810291909101015281610c5f81611a44565b9250505b80610c6d81611a44565b915050610bbb565b5060008167ffffffffffffffff811115610c9157610c91611767565b604051908082528060200260200182016040528015610cba578160200160208202803683370190505b50905060005b82811015610d1157838181518110610cda57610cda611a2e565b6020026020010151828281518110610cf457610cf4611a2e565b602090810291909101015280610d0981611a44565b915050610cc0565b50949350505050565b83838383604051602001610d3091815260200190565b60408051601f1981840301815291905260005460ff16610d625760405162461bcd60e51b81526004016102da90611a6b565b600084604051602001610d759190611aa2565b60408051601f19818403018152919052805160209091012090506000808281526002602081905260409091205460ff1690811115610db557610db56116cb565b14610dd25760405162461bcd60e51b81526004016102da90611b0b565b60008284604051602001610de7929190611ad9565b60408051601f198184030181529082905280516020918201208083529250600080516020611bf1833981519152910160405180910390a16000610e2b828789610ab5565b6000805461ff00191661010083151502179055905080610e6357604051828152600080516020611bd183398151915290602001610603565b60008381526002602052604090819020549051600080516020611c1183398151915291610e999160ff9091169086908990611703565b60405180910390a1610eab83866113f7565b505050600394909455505050600491909155505050565b83838383604051602001610ed891815260200190565b60408051601f1981840301815291905260005460ff16610f0a5760405162461bcd60e51b81526004016102da90611a6b565b600084604051602001610f1d9190611aa2565b60408051601f19818403018152919052805160209091012090506000808281526002602081905260409091205460ff1690811115610f5d57610f5d6116cb565b14610f7a5760405162461bcd60e51b81526004016102da90611b0b565b60008284604051602001610f8f929190611ad9565b60408051601f198184030181529082905280516020918201208083529250600080516020611bf1833981519152910160405180910390a16000610fd3828789610ab5565b6000805461ff0019166101008315150217905590508061100b57604051828152600080516020611bd183398151915290602001610603565b60008381526002602052604090819020549051600080516020611c11833981519152916110419160ff9091169086908990611703565b60405180910390a161105383866113f7565b60008b6040516020016110669190611aa2565b60405160208183030381529060405280519060200120905060045481036110ff5760405162461bcd60e51b815260206004820152604160248201527f4c616d706f7274426173653a2043616e6e6f7420757365207468652073616d6560448201527f206b6579636861696e20747769636520666f7220746869732066756e6374696f6064820152603760f91b608482015260a4016102da565b88600354146111505760405162461bcd60e51b815260206004820152601e60248201527f4c616d706f7274426173653a204b65797320646f206e6f74206d61746368000060448201526064016102da565b600454818a6000808481526002602081905260409091205460ff169081111561117b5761117b6116cb565b1480156111a95750600082815260026020819052604082205460ff16908111156111a7576111a76116cb565b145b61120c5760405162461bcd60e51b815260206004820152602e60248201527f4c616d706f7274426173653a2050726f7669646564206b65797320617265206e60448201526d6f74206d6173746572206b65797360901b60648201526084016102da565b82811415801561121c5750818114155b6112825760405162461bcd60e51b815260206004820152603160248201527f4c616d706f7274426173653a204d6173746572206b6579732063616e6e6f742060448201527064656c657465207468656d73656c76657360781b60648201526084016102da565b60008181526002602052604081206001015490036112ee5760405162461bcd60e51b815260206004820152602360248201527f4c616d706f7274426173653a204e6f2073756368206b6579202864656c6574696044820152626f6e2960e81b60648201526084016102da565b60005b6001548110156113db57816001828154811061130f5761130f611a2e565b906000526020600020906002020160010154036113c957600082815260026020818152604080842080548251428186015244818501528351808203850181526060909101938490528051908501209588905292849052630de1e7ed60e41b85186001820181905560ff198416851790915560ff9092169391927f0643be3612916977c69d5ed1abb75a50cca49df49ba2444d836e2a0cf65fe074916113b991869189918791611ba0565b60405180910390a15050506113db565b806113d381611a44565b9150506112f1565b5050600060038190556004555050505050505050505050505050565b60008281526002602052604081206001015490036114275760405162461bcd60e51b81526004016102da906119f7565b604080518082018252600084815260026020819052928120549092829160ff1690811115611457576114576116cb565b8152602001838152509050806002600084815260200190815260200160002060008201518160000160006101000a81548160ff021916908360028111156114a0576114a06116cb565b02179055506020918201516001918201556000858152600290925260408220805460ff19168155018190555b6001548110156115765783600182815481106114ea576114ea611a2e565b9060005260206000209060020201600101540361156457816001828154811061151557611515611a2e565b906000526020600020906002020160008201518160000160006101000a81548160ff0219169083600281111561154d5761154d6116cb565b021790555060208201518160010155905050611576565b8061156e81611a44565b9150506114cc565b508051604051600080516020611c11833981519152916115999186908690611703565b60405180910390a1505050565b600060405180604001604052808460028111156115c5576115c56116cb565b81526020018390526001805480820182556000829052825160029182027fb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6018054949550859490939192849260ff199092169190849081111561162a5761162a6116cb565b021790555060209182015160019182015560008481526002928390526040902083518154859492939192849260ff199092169190849081111561166f5761166f6116cb565b0217905550602082015181600101559050507f2172c7b01a6de957d29fd6166a23025d181bf56538ad606a526ab2d62603f3fc8383604051611599929190611722565b6000602082840312156116c457600080fd5b5035919050565b634e487b7160e01b600052602160045260246000fd5b600381106116ff57634e487b7160e01b600052602160045260246000fd5b9052565b6060810161171182866116e1565b602082019390935260400152919050565b6040810161173082856116e1565b8260208301529392505050565b80614000810183101561174f57600080fd5b92915050565b80612000810183101561174f57600080fd5b634e487b7160e01b600052604160045260246000fd5b600080600080614060858703121561179457600080fd5b61179e868661173d565b935061400085013567ffffffffffffffff808211156117bc57600080fd5b6117c888838901611755565b945061402087013593506140408701359150808211156117e757600080fd5b818701915087601f8301126117fb57600080fd5b81358181111561180d5761180d611767565b604051601f8201601f19908116603f0116810190838211818310171561183557611835611767565b816040528281528a602084870101111561184e57600080fd5b82602086016020830137600060208483010152809550505050505092959194509250565b600080600080614060858703121561188957600080fd5b611893868661173d565b935061400085013567ffffffffffffffff8111156118b057600080fd5b6118bc87828801611755565b9497949650505050614020830135926140400135919050565b60008060008061406085870312156118ec57600080fd5b6118f6868661173d565b9350614000850135925061402085013567ffffffffffffffff81111561191b57600080fd5b61192787828801611755565b94979396509394614040013593505050565b6000806000614040848603121561194f57600080fd5b83359250602084013567ffffffffffffffff81111561196d57600080fd5b61197986828701611755565b925050611989856040860161173d565b90509250925092565b6000602082840312156119a457600080fd5b813560038110610b6357600080fd5b6020808252825182820181905260009190848201906040850190845b818110156119eb578351835292840192918401916001016119cf565b50909695505050505050565b60208082526018908201527f4c616d706f7274426173653a204e6f2073756368206b65790000000000000000604082015260600190565b634e487b7160e01b600052603260045260246000fd5b600060018201611a6457634e487b7160e01b600052601160045260246000fd5b5060010190565b6020808252601c908201527f4c616d706f7274426173653a206e6f7420696e697469616c697a656400000000604082015260600190565b60008183825b610100811015611ac957604080838537928301929190910190600101611aa8565b5050506140008201905092915050565b6000835160005b81811015611afa5760208187018101518583015201611ae0565b509190910191825250602001919050565b6020808252601d908201527f4c616d706f7274426173653a204e6f742061206d6173746572206b6579000000604082015260600190565b6000808335601e19843603018112611b5957600080fd5b83018035915067ffffffffffffffff821115611b7457600080fd5b602001915036819003821315611b8957600080fd5b9250929050565b8183823760009101908152919050565b60808101611bae82876116e1565b846020830152836040830152611bc760608301846116e1565b9594505050505056fe32629d580208e19f97e5752eef849e102f803999c88aa7f75e12b1744eecd5a7d87e68f36f73a7eb22739d6639e36cafebfcde0b5543340b39f42cac68fdd1f06825a39bd161f4ef5aab6cfd2c26db3ee0005c11b43cffd544fc876312116edda26469706673582212205bc8ba45555b82bd23fe424287277bd652ffb5f4b01d721e3a4f98894033ff0564736f6c63430008150033"
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

        with open('contract_LamportBase2-coin.txt', 'w') as file:
            # Write the contract address to the file
            file.write(new_contract_address)
        exit()