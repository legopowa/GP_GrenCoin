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
arg1 = "GPGrens"
arg2 = "GPG"

# ABI encode the arguments
encoded_args = encode_abi(['string', 'string'], [arg1, arg2])

# Load the bytecode of the contract (replace with actual bytecode)
full_bytecode = "0x6080604052600680546001600160a01b031990811673a4ccb212e4c7249a987eaf68335de28bf9e87625179091556007805490911673be5e3ecc8109e16fa7f8003cb7e8b2935fce22e117905534801561005857600080fd5b50600654600080546001600160a01b03199081166001600160a01b03938416179091556007546001805490921692169190911790556119568061009c6000396000f3fe608060405234801561001057600080fd5b50600436106100ea5760003560e01c80639d4635201161008c578063e15336ef11610066578063e15336ef1461021d578063f59cc9781461024d578063f785eb2a14610256578063facd743b1461027657600080fd5b80639d463520146101d6578063b8f41a3c146101df578063d0b6b6db146101f257600080fd5b80635c9c3ed2116100c85780635c9c3ed21461016357806364c8c5a7146101bd5780636f1aab4a146101c557806384e7e3d3146101cd57600080fd5b8063143acc71146100ef5780631e9ad446146101215780633592696d14610143575b600080fd5b61011f6100fd366004611059565b600080546001600160a01b0319166001600160a01b0392909216919091179055565b005b610130670de0b6b3a764000081565b6040519081526020015b60405180910390f35b61015661015136600461121a565b610299565b60405161013a9190611257565b6101a86101713660046112a4565b8151602081840181018051600382529282019482019490942091909352909152600090815260409020805460019091015460ff1682565b6040805192835290151560208301520161013a565b61011f610318565b610130604081565b61013061012c81565b61013060055481565b61011f6101ed36600461130f565b6103fd565b600154610205906001600160a01b031681565b6040516001600160a01b03909116815260200161013a565b61011f61022b366004611059565b600180546001600160a01b0319166001600160a01b0392909216919091179055565b61013061025881565b61026961026436600461143b565b6106c8565b60405161013a91906114ad565b610289610284366004611059565b610781565b604051901515815260200161013a565b6000546005546040516385d8f13d60e01b81526060926001600160a01b0316916385d8f13d916102cd9186916004016114c0565b600060405180830381865afa1580156102ea573d6000803e3d6000fd5b505050506040513d6000823e601f3d908101601f191682016040526103129190810190611529565b92915050565b60008060009054906101000a90046001600160a01b03166001600160a01b0316633dc0ff7d6040518163ffffffff1660e01b8152600401600060405180830381865afa15801561036c573d6000803e3d6000fd5b505050506040513d6000823e601f3d908101601f1916820160405261039491908101906115c3565b905060005b81518110156103f15760008282815181106103b6576103b66116b0565b6020026020010151905060006103cb826107f0565b905080156103dc576103dc81610aab565b505080806103e9906116dc565b915050610399565b506103fa610c90565b50565b61040682610781565b6104625760405162461bcd60e51b8152602060048201526024808201527f43616c6c6572206973206e6f74206120726567697374657265642076616c696460448201526330ba37b960e11b606482015260840160405180910390fd5b6000805b8451811015610660576000858281518110610483576104836116b0565b602002602001015160200151519050604081846104a091906116f5565b11156104ac5750610660565b6104b681846116f5565b9250606060005b8784815181106104cf576104cf6116b0565b6020026020010151602001515181101561055057818885815181106104f6576104f66116b0565b6020026020010151602001518281518110610513576105136116b0565b602002602001015160405160200161052c929190611708565b60405160208183030381529060405291508080610548906116dc565b9150506104bd565b5080516020820120875188908590811061056c5761056c6116b0565b60200260200101516020015160046000838152602001908152602001600020908051906020019061059e929190610f77565b506105c68885815181106105b4576105b46116b0565b60200260200101516000015188610e4e565b604051806040016040528082815260200187151581525060038986815181106105f1576105f16116b0565b60200260200101516000015160405161060a9190611737565b90815260408051602092819003830190206001600160a01b038b16600090815290835220825181559101516001909101805460ff1916911515919091179055508291506106589050816116dc565b915050610466565b5060055442906000906106739083611753565b9050600061068361012c8461177c565b61068f9061012c611753565b905061012c82101580156106a4575061012c81105b156106bf576106b1610318565b6106bb8184611753565b6005555b50505050505050565b600460205281600052604060002081815481106106e457600080fd5b9060005260206000200160009150915050805461070090611790565b80601f016020809104026020016040519081016040528092919081815260200182805461072c90611790565b80156107795780601f1061074e57610100808354040283529160200191610779565b820191906000526020600020905b81548152906001019060200180831161075c57829003601f168201915b505050505081565b6000805460405163facd743b60e01b81526001600160a01b0384811660048301529091169063facd743b90602401602060405180830381865afa1580156107cc573d6000803e3d6000fd5b505050506040513d601f19601f8201168201806040525081019061031291906117ca565b6000806002836040516108039190611737565b908152604080519182900360209081018320805480830285018301909352828452919083018282801561085f57602002820191906000526020600020905b81546001600160a01b03168152600190910190602001808311610841575b50505050509050600060648251603c61087891906117e7565b61088291906117fe565b82519091506000908190819067ffffffffffffffff8111156108a6576108a661107d565b6040519080825280602002602001820160405280156108eb57816020015b60408051808201909152600080825260208201528152602001906001900390816108c45790505b50905060005b8551811015610a8b57600060038960405161090c9190611737565b9081526020016040518091039020600088848151811061092e5761092e6116b0565b60200260200101516001600160a01b03166001600160a01b031681526020019081526020016000206000015490506000805b84518110156109d6578285828151811061097c5761097c6116b0565b602002602001015160000151036109c45784818151811061099f5761099f6116b0565b602002602001015160200180518091906109b8906116dc565b905250600191506109d6565b806109ce816116dc565b915050610960565b5080610a105760405180604001604052808381526020016001815250848481518110610a0457610a046116b0565b60200260200101819052505b84848481518110610a2357610a236116b0565b6020026020010151602001511115610a7657838381518110610a4757610a476116b0565b6020026020010151602001519450838381518110610a6757610a676116b0565b60200260200101516000015195505b50508080610a83906116dc565b9150506108f1565b50838210610a9e57509095945050505050565b5060009695505050505050565b600081815260046020908152604080832080548251818502810185019093528083529192909190849084015b82821015610b83578382906000526020600020018054610af690611790565b80601f0160208091040260200160405190810160405280929190818152602001828054610b2290611790565b8015610b6f5780601f10610b4457610100808354040283529160200191610b6f565b820191906000526020600020905b815481529060010190602001808311610b5257829003601f168201915b505050505081526020019060010190610ad7565b5050505090506000610b9482610299565b90506000610ba0610f3d565b905060005b8251811015610c895760006001600160a01b0316838281518110610bcb57610bcb6116b0565b60200260200101516001600160a01b031614610c775760015483516001600160a01b039091169063f0dda65c90859084908110610c0a57610c0a6116b0565b6020026020010151846040518363ffffffff1660e01b8152600401610c449291906001600160a01b03929092168252602082015260400190565b600060405180830381600087803b158015610c5e57600080fd5b505af1158015610c72573d6000803e3d6000fd5b505050505b80610c81816116dc565b915050610ba5565b5050505050565b60008060009054906101000a90046001600160a01b03166001600160a01b0316633dc0ff7d6040518163ffffffff1660e01b8152600401600060405180830381865afa158015610ce4573d6000803e3d6000fd5b505050506040513d6000823e601f3d908101601f19168201604052610d0c91908101906115c3565b905060005b8151811015610e4a576000828281518110610d2e57610d2e6116b0565b602002602001015190506000600282604051610d4a9190611737565b9081526040805191829003602090810183208054808302850183019093528284529190830182828015610da657602002820191906000526020600020905b81546001600160a01b03168152600190910190602001808311610d88575b5050505050905060005b8151811015610e34576000600384604051610dcb9190611737565b90815260200160405180910390206000848481518110610ded57610ded6116b0565b6020908102919091018101516001600160a01b03168252810191909152604001600020600101805460ff191691151591909117905580610e2c816116dc565b915050610db0565b5050508080610e42906116dc565b915050610d11565b5050565b6000805b600284604051610e629190611737565b90815260405190819003602001902054811015610ee757826001600160a01b0316600285604051610e939190611737565b90815260200160405180910390208281548110610eb257610eb26116b0565b6000918252602090912001546001600160a01b031603610ed55760019150610ee7565b80610edf816116dc565b915050610e52565b5080610f3857600283604051610efd9190611737565b90815260405160209181900382019020805460018101825560009182529190200180546001600160a01b0319166001600160a01b0384161790555b505050565b60008060055442610f4e9190611753565b9050610258811115610f5f57506102585b610f71670de0b6b3a7640000826117e7565b91505090565b828054828255906000526020600020908101928215610fbd579160200282015b82811115610fbd5782518290610fad9082611860565b5091602001919060010190610f97565b50610fc9929150610fcd565b5090565b80821115610fc9576000610fe18282610fea565b50600101610fcd565b508054610ff690611790565b6000825580601f10611006575050565b601f0160209004906000526020600020908101906103fa91905b80821115610fc95760008155600101611020565b6001600160a01b03811681146103fa57600080fd5b803561105481611034565b919050565b60006020828403121561106b57600080fd5b813561107681611034565b9392505050565b634e487b7160e01b600052604160045260246000fd5b6040805190810167ffffffffffffffff811182821017156110b6576110b661107d565b60405290565b604051601f8201601f1916810167ffffffffffffffff811182821017156110e5576110e561107d565b604052919050565b600067ffffffffffffffff8211156111075761110761107d565b5060051b60200190565b600067ffffffffffffffff82111561112b5761112b61107d565b50601f01601f191660200190565b600082601f83011261114a57600080fd5b813561115d61115882611111565b6110bc565b81815284602083860101111561117257600080fd5b816020850160208301376000918101602001919091529392505050565b600082601f8301126111a057600080fd5b813560206111b0611158836110ed565b82815260059290921b840181019181810190868411156111cf57600080fd5b8286015b8481101561120f57803567ffffffffffffffff8111156111f35760008081fd5b6112018986838b0101611139565b8452509183019183016111d3565b509695505050505050565b60006020828403121561122c57600080fd5b813567ffffffffffffffff81111561124357600080fd5b61124f8482850161118f565b949350505050565b6020808252825182820181905260009190848201906040850190845b818110156112985783516001600160a01b031683529284019291840191600101611273565b50909695505050505050565b600080604083850312156112b757600080fd5b823567ffffffffffffffff8111156112ce57600080fd5b6112da85828601611139565b92505060208301356112eb81611034565b809150509250929050565b80151581146103fa57600080fd5b8035611054816112f6565b60008060006060848603121561132457600080fd5b833567ffffffffffffffff8082111561133c57600080fd5b818601915086601f83011261135057600080fd5b81356020611360611158836110ed565b82815260059290921b8401810191818101908a84111561137f57600080fd5b8286015b848110156114105780358681111561139a57600080fd5b87016040818e03601f190112156113b15760008081fd5b6113b9611093565b85820135888111156113cb5760008081fd5b6113d98f8883860101611139565b8252506040820135888111156113ef5760008081fd5b6113fd8f888386010161118f565b8288015250845250918301918301611383565b5097506114209050888201611049565b95505050505061143260408501611304565b90509250925092565b6000806040838503121561144e57600080fd5b50508035926020909101359150565b60005b83811015611478578181015183820152602001611460565b50506000910152565b6000815180845261149981602086016020860161145d565b601f01601f19169290920160200192915050565b6020815260006110766020830184611481565b6000604082016040835280855180835260608501915060608160051b8601019250602080880160005b8381101561151757605f19888703018552611505868351611481565b955093820193908201906001016114e9565b50509490940194909452949350505050565b6000602080838503121561153c57600080fd5b825167ffffffffffffffff81111561155357600080fd5b8301601f8101851361156457600080fd5b8051611572611158826110ed565b81815260059190911b8201830190838101908783111561159157600080fd5b928401925b828410156115b85783516115a981611034565b82529284019290840190611596565b979650505050505050565b600060208083850312156115d657600080fd5b825167ffffffffffffffff808211156115ee57600080fd5b818501915085601f83011261160257600080fd5b8151611610611158826110ed565b81815260059190911b8301840190848101908883111561162f57600080fd5b8585015b838110156116a35780518581111561164b5760008081fd5b8601603f81018b1361165d5760008081fd5b87810151604061166f61115883611111565b8281528d828486010111156116845760008081fd5b611693838c830184870161145d565b8652505050918601918601611633565b5098975050505050505050565b634e487b7160e01b600052603260045260246000fd5b634e487b7160e01b600052601160045260246000fd5b6000600182016116ee576116ee6116c6565b5060010190565b80820180821115610312576103126116c6565b6000835161171a81846020880161145d565b83519083019061172e81836020880161145d565b01949350505050565b6000825161174981846020870161145d565b9190910192915050565b81810381811115610312576103126116c6565b634e487b7160e01b600052601260045260246000fd5b60008261178b5761178b611766565b500690565b600181811c908216806117a457607f821691505b6020821081036117c457634e487b7160e01b600052602260045260246000fd5b50919050565b6000602082840312156117dc57600080fd5b8151611076816112f6565b8082028115828204841417610312576103126116c6565b60008261180d5761180d611766565b500490565b601f821115610f3857600081815260208120601f850160051c810160208610156118395750805b601f850160051c820191505b8181101561185857828155600101611845565b505050505050565b815167ffffffffffffffff81111561187a5761187a61107d565b61188e816118888454611790565b84611812565b602080601f8311600181146118c357600084156118ab5750858301515b600019600386901b1c1916600185901b178555611858565b600085815260208120601f198616915b828110156118f2578886015182559484019460019091019084016118d3565b50858210156119105787850151600019600388901b60f8161c191681555b5050505050600190811b0190555056fea2646970667358221220d01a41f1a21c52280c049b4b5c2a0a75fe73af40a31ed55b8121e8bddaeeb7ac64736f6c63430008150033"
#print(encoded_args.hex())
# Append the encoded arguments to the bytecode
#print(full_bytecode)
class LamportTest:
    
    def __init__(self):

        self.k1 = KeyTracker("master1") # new keys made here
        self.k2 = KeyTracker("master2")
        self.k3 = KeyTracker("oracle1")
        self.k4 = KeyTracker("master3")
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

        self.load_two_masters(pkhs, "master")
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

    
    def load_two_masters(self, pkhs, filename):
        pkh_index = 0
        master1_loaded = False
        master2_loaded = False
        global master_pkh_1
        global master_pkh_2

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

        if not master2_loaded:
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
        #global master_pkh_3
        print("Running 'can_test_key_functions'...")
        with open('contract_AnonID.txt', 'r') as file:
            contract_address = file.read()
            contract_address = contract_address.strip().replace('\n', '')  # Remove whitespace and newlines

        _contract = AnonIDContract.at(contract_address)
        print("Contract referenced.")
        print('master_pkh_1', master_pkh_1)
        private_key = '163f5f0f9a621d72fedd85ffca3d08d131ab4e812181e0d30ffd1c885d20aac7'
        brownie_account = accounts.add(private_key)
        current_keys = self.k1.load(self, "master1", master_pkh_1)
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
        self.k1.save(trim = False)
        #self.k4.save(trim = False)
        master_pkh_1 = nextpkh

        #current_keys = self.k2.load(self, "master2", master_pkh_2)
        #next_keys = self.k2.get_next_key_pair()
        #nextpkh = self.k2.pkh_from_public_key(next_keys.pub)

        #paddressToBroadcast = '0xfd003CA44BbF4E9fB0b2fF1a33fc2F05A6C2EFF9'

        #packed_message = str.lower(full_bytecode)[2:].encode() + nextpkh[2:].encode()

        #callhash = hash_b(str(packed_message.decode()))
        #sig = sign_hash(callhash, current_keys.pri) 


        
        tx = _contract.createContractStepTwo(

            full_bytecode,
            {'from': brownie_account, 'gas_limit': 3999999}    
        )


        tx.wait(1)

        # Extract the new contract address from the transaction's events
        new_contract_address = tx.events['ContractCreated']['contractAddress']

        print(f"New contract address: {new_contract_address}")
        #self.k2.save(trim = False)

        with open('contract_GameValidator-coin.txt', 'w') as file:
            # Write the contract address to the file
            file.write(new_contract_address)
        exit()