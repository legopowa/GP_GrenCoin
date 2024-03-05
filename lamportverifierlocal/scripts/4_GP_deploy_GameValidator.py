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
full_bytecode = "0x6080604052600b80546001600160a01b031990811673b03a6afd440a2a9db8834f1a6093680f02f1114c17909155600c805490911673dd17d01307f2ff3a18390f3cdc564cec0f4a0a1d17905534801561005857600080fd5b50600080546001600160a01b031990811673b3830ae69ee5962355e84f6bbac274ff337960e517909155600b546001805483166001600160a01b03928316179055600c546002805490931691161790556126e0806100b76000396000f3fe608060405234801561001057600080fd5b50600436106101005760003560e01c806384e7e3d311610097578063d0b6b6db11610066578063d0b6b6db1461023a578063f59cc9781461024d578063f785eb2a14610256578063facd743b1461027657600080fd5b806384e7e3d31461020257806395a743e01461020b5780639d4635201461021e578063bc0e4ade1461022757600080fd5b80635c9c3ed2116100d35780635c9c3ed21461017a57806361803e75146101d45780636b4674eb146101e75780636f1aab4a146101fa57600080fd5b80631e9ad44614610105578063420230601461012757806356bf7b571461013c5780635920b40714610167575b600080fd5b610114670de0b6b3a764000081565b6040519081526020015b60405180910390f35b61013a610135366004611b79565b610299565b005b60005461014f906001600160a01b031681565b6040516001600160a01b03909116815260200161011e565b61013a610175366004611be7565b6103f2565b6101bf610188366004611d34565b8151602081840181018051600482529282019482019490942091909352909152600090815260409020805460019091015460ff1682565b6040805192835290151560208301520161011e565b61013a6101e2366004611b79565b610669565b61013a6101f5366004611b79565b6108da565b610114604081565b61011461012c81565b61013a610219366004611dc1565b610a38565b610114600a5481565b61013a610235366004611b79565b610e61565b60025461014f906001600160a01b031681565b61011461025881565b610269610264366004611f7c565b6110bf565b60405161011e9190611fee565b610289610284366004612008565b611178565b604051901515815260200161011e565b6000816040516020016102ac9190612025565b60408051601f19818403018152908290526000805463333f611160e01b8452919350916001600160a01b039091169063333f6111906102f590899089908990889060040161206b565b6020604051808303816000875af1158015610314573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610338919061214b565b9050806103bc5760405162461bcd60e51b815260206004820152604160248201527f417574686f72697a6174696f6e206661696c656420666f722070726f706f736560448201527f6420757064617465206f66204d696e7420636f6e7472616374206164647265736064820152607360f81b608482015260a4015b60405180910390fd5b505033600090815260066020526040902080546001600160a01b0319166001600160a01b03929092169190911790556009555050565b6000836040516020016104059190612168565b60408051808303601f190181529082905280516020909101206000805463b9d57c5f60e01b845260048401839052919350916001600160a01b039091169063b9d57c5f90602401606060405180830381865afa158015610469573d6000803e3d6000fd5b505050506040513d601f19601f8201168201806040525081019061048d919061219f565b6001546040516334a88c5b60e01b8152336004820152919450600093508392506001600160a01b0316906334a88c5b906024016040805180830381865afa1580156104dc573d6000803e3d6000fd5b505050506040513d601f19601f8201168201806040525081019061050091906121da565b915091508183148061051157508083145b61056e5760405162461bcd60e51b815260206004820152602860248201527f43616c6c65722773206f7261636c65206b657920696e64657820646f6573206e6044820152670dee840dac2e8c6d60c31b60648201526084016103b3565b6000546040805160208082018c90528251808303909101815281830192839052634a89d52b60e01b9092526001600160a01b0390921691634a89d52b916105be918b918b918b919060440161206b565b6020604051808303816000875af11580156105dd573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610601919061214b565b61064d5760405162461bcd60e51b815260206004820152601b60248201527f4c616d706f7274206f7261636c6520636865636b206661696c6564000000000060448201526064016103b3565b5050336000908152600860205260409020959095555050505050565b60008160405160200161067c9190612025565b60408051808303601f19018152918152336000908152600760205220549091506001600160a01b0383811691161461070e5760405162461bcd60e51b815260206004820152602f60248201527f506c61796572446174616261736520636f6e747261637420616464726573732060448201526e0eae0c8c2e8ca40dad2e6dac2e8c6d608b1b60648201526084016103b3565b6000856040516020016107219190612168565b604051602081830303815290604052805190602001209050806009540361075a5760405162461bcd60e51b81526004016103b3906121fe565b6000805460405163333f611160e01b81526001600160a01b039091169063333f611190610791908a908a908a90899060040161206b565b6020604051808303816000875af11580156107b0573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906107d4919061214b565b9050806108605760405162461bcd60e51b815260206004820152604e60248201527f417574686f72697a6174696f6e206661696c6564206f6e20636f6e6669726d6160448201527f74696f6e206f6620506c61796572446174616261736520636f6e74726163742060648201526d616464726573732075706461746560901b608482015260a4016103b3565b600180546001600160a01b0319166001600160a01b0386169081179091556040519081527f6c200b5398af2592ba382dbf2a45376bbb22a24cab265709486fa967a5b4203d9060200160405180910390a1505033600090815260076020526040812080546001600160a01b03191690556009555050505050565b6000816040516020016108ed9190612025565b60408051601f19818403018152908290526000805463333f611160e01b8452919350916001600160a01b039091169063333f61119061093690899089908990889060040161206b565b6020604051808303816000875af1158015610955573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610979919061214b565b905080610a025760405162461bcd60e51b815260206004820152604b60248201527f417574686f72697a6174696f6e206661696c656420666f722070726f706f736560448201527f6420757064617465206f6620506c61796572446174616261736520636f6e747260648201526a616374206164647265737360a81b608482015260a4016103b3565b505033600090815260076020526040902080546001600160a01b0319166001600160a01b03929092169190911790556009555050565b610a4182611178565b610a995760405162461bcd60e51b8152602060048201526024808201527f43616c6c6572206973206e6f74206120726567697374657265642076616c696460448201526330ba37b960e11b60648201526084016103b3565b606060005b8451811015610b7d5781858281518110610aba57610aba612265565b602002602001015160000151604051602001610ad792919061227b565b604051602081830303815290604052915060005b858281518110610afd57610afd612265565b60200260200101516020015151811015610b745782868381518110610b2457610b24612265565b6020026020010151602001518281518110610b4157610b41612265565b6020026020010151604051602001610b5a92919061227b565b60408051601f198184030181529190529250600101610aeb565b50600101610a9e565b5080516020808301919091206001600160a01b038516600090815260089092526040909120548114610c0c5760405162461bcd60e51b815260206004820152603260248201527f4c697374206861736820646f6573206e6f74206d617463682070726576696f7560448201527139b63c90383937bb34b232b2103430b9b41760711b60648201526084016103b3565b6000805b8651811015610df7576000878281518110610c2d57610c2d612265565b60200260200101516020015151905060408184610c4a91906122c0565b1115610c565750610df7565b610c6081846122c0565b9250606060005b898481518110610c7957610c79612265565b60200260200101516020015151811015610cf057818a8581518110610ca057610ca0612265565b6020026020010151602001518281518110610cbd57610cbd612265565b6020026020010151604051602001610cd692919061227b565b60408051601f198184030181529190529150600101610c67565b508051602082012089518a9085908110610d0c57610d0c612265565b602002602001015160200151600560008381526020019081526020016000209080519060200190610d3e929190611a73565b50610d668a8581518110610d5457610d54612265565b6020026020010151600001518a6111ed565b604051806040016040528082815260200189151581525060048b8681518110610d9157610d91612265565b602002602001015160000151604051610daa91906122d3565b90815260408051602092819003830190206001600160a01b038d16600090815290835220825181559101516001918201805460ff1916911515919091179055939093019250610c10915050565b50600a544290600090610e0a90836122ef565b90506000610e1a61012c84612318565b610e269061012c6122ef565b905061012c8210158015610e3b575061012c81105b15610e5657610e486112d2565b610e5281846122ef565b600a555b505050505050505050565b600081604051602001610e749190612025565b60408051808303601f19018152918152336000908152600660205220549091506001600160a01b03838116911614610efc5760405162461bcd60e51b815260206004820152602560248201527f4d696e7420636f6e7472616374206164647265737320757064617465206d69736044820152640dac2e8c6d60db1b60648201526084016103b3565b600085604051602001610f0f9190612168565b6040516020818303038152906040528051906020012090508060095403610f485760405162461bcd60e51b81526004016103b3906121fe565b6000805460405163333f611160e01b81526001600160a01b039091169063333f611190610f7f908a908a908a90899060040161206b565b6020604051808303816000875af1158015610f9e573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610fc2919061214b565b9050806110455760405162461bcd60e51b8152602060048201526044602482018190527f417574686f72697a6174696f6e206661696c6564206f6e20636f6e6669726d61908201527f74696f6e206f66204d696e7420636f6e747261637420616464726573732075706064820152636461746560e01b608482015260a4016103b3565b600280546001600160a01b0319166001600160a01b0386169081179091556040519081527f7814765089fa4d113b377eb0859fd345095a106617367857878087a128595ec49060200160405180910390a1505033600090815260066020526040812080546001600160a01b03191690556009555050505050565b600560205281600052604060002081815481106110db57600080fd5b906000526020600020016000915091505080546110f79061232c565b80601f01602080910402602001604051908101604052809291908181526020018280546111239061232c565b80156111705780601f1061114557610100808354040283529160200191611170565b820191906000526020600020905b81548152906001019060200180831161115357829003601f168201915b505050505081565b60015460405163facd743b60e01b81526001600160a01b038381166004830152600092169063facd743b90602401602060405180830381865afa1580156111c3573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906111e7919061214b565b92915050565b6000805b60038460405161120191906122d3565b9081526040519081900360200190205481101561127c57826001600160a01b031660038560405161123291906122d3565b9081526020016040518091039020828154811061125157611251612265565b6000918252602090912001546001600160a01b031603611274576001915061127c565b6001016111f1565b50806112cd5760038360405161129291906122d3565b90815260405160209181900382019020805460018101825560009182529190200180546001600160a01b0319166001600160a01b0384161790555b505050565b60015460408051633dc0ff7d60e01b815290516000926001600160a01b031691633dc0ff7d91600480830192869291908290030181865afa15801561131b573d6000803e3d6000fd5b505050506040513d6000823e601f3d908101601f191682016040526113439190810190612366565b905060005b815181101561139557600082828151811061136557611365612265565b60200260200101519050600061137a826113a1565b9050801561138b5761138b81611646565b5050600101611348565b5061139e611821565b50565b6000806003836040516113b491906122d3565b908152604080519182900360209081018320805480830285018301909352828452919083018282801561141057602002820191906000526020600020905b81546001600160a01b031681526001909101906020018083116113f2575b50505050509050600060648251603c6114299190612452565b6114339190612469565b8251909150600090819081906001600160401b0381111561145657611456611c49565b60405190808252806020026020018201604052801561149b57816020015b60408051808201909152600080825260208201528152602001906001900390816114745790505b50905060005b85518110156116265760006004896040516114bc91906122d3565b908152602001604051809103902060008884815181106114de576114de612265565b60200260200101516001600160a01b03166001600160a01b031681526020019081526020016000206000015490506000805b845181101561157c578285828151811061152c5761152c612265565b602002602001015160000151036115745784818151811061154f5761154f612265565b602002602001015160200180518091906115689061247d565b9052506001915061157c565b600101611510565b50806115b657604051806040016040528083815260200160018152508484815181106115aa576115aa612265565b60200260200101819052505b848484815181106115c9576115c9612265565b602002602001015160200151111561161c578383815181106115ed576115ed612265565b602002602001015160200151945083838151811061160d5761160d612265565b60200260200101516000015195505b50506001016114a1565b5083821061163957509095945050505050565b5060009695505050505050565b600081815260056020908152604080832080548251818502810185019093528083529192909190849084015b8282101561171e5783829060005260206000200180546116919061232c565b80601f01602080910402602001604051908101604052809291908181526020018280546116bd9061232c565b801561170a5780601f106116df5761010080835404028352916020019161170a565b820191906000526020600020905b8154815290600101906020018083116116ed57829003601f168201915b505050505081526020019060010190611672565b505050509050600061172f826119c0565b9050600061173b611a39565b905060005b825181101561181a5760006001600160a01b031683828151811061176657611766612265565b60200260200101516001600160a01b0316146118125760025483516001600160a01b039091169063f0dda65c908590849081106117a5576117a5612265565b6020026020010151846040518363ffffffff1660e01b81526004016117df9291906001600160a01b03929092168252602082015260400190565b600060405180830381600087803b1580156117f957600080fd5b505af115801561180d573d6000803e3d6000fd5b505050505b600101611740565b5050505050565b60015460408051633dc0ff7d60e01b815290516000926001600160a01b031691633dc0ff7d91600480830192869291908290030181865afa15801561186a573d6000803e3d6000fd5b505050506040513d6000823e601f3d908101601f191682016040526118929190810190612366565b905060005b81518110156119bc5760008282815181106118b4576118b4612265565b6020026020010151905060006003826040516118d091906122d3565b908152604080519182900360209081018320805480830285018301909352828452919083018282801561192c57602002820191906000526020600020905b81546001600160a01b0316815260019091019060200180831161190e575b5050505050905060005b81518110156119b157600060048460405161195191906122d3565b9081526020016040518091039020600084848151811061197357611973612265565b6020908102919091018101516001600160a01b031682528101919091526040016000206001908101805460ff19169215159290921790915501611936565b505050600101611897565b5050565b600154600a546040516385d8f13d60e01b81526060926001600160a01b0316916385d8f13d916119f4918691600401612496565b600060405180830381865afa158015611a11573d6000803e3d6000fd5b505050506040513d6000823e601f3d908101601f191682016040526111e79190810190612502565b600080600a5442611a4a91906122ef565b9050610258811115611a5b57506102585b611a6d670de0b6b3a764000082612452565b91505090565b828054828255906000526020600020908101928215611ab9579160200282015b82811115611ab95782518290611aa990826125eb565b5091602001919060010190611a93565b50611ac5929150611ac9565b5090565b80821115611ac5576000611add8282611ae6565b50600101611ac9565b508054611af29061232c565b6000825580601f10611b02575050565b601f01602090049060005260206000209081019061139e91905b80821115611ac55760008155600101611b1c565b8061400081018310156111e757600080fd5b8061200081018310156111e757600080fd5b6001600160a01b038116811461139e57600080fd5b8035611b7481611b54565b919050565b6000806000806140608587031215611b9057600080fd5b611b9a8686611b30565b93506140008501356001600160401b03811115611bb657600080fd5b611bc287828801611b42565b9350506140208501359150614040850135611bdc81611b54565b939692955090935050565b6000806000806140608587031215611bfe57600080fd5b84359350611c0f8660208701611b30565b92506140208501356001600160401b03811115611c2b57600080fd5b611c3787828801611b42565b94979396509394614040013593505050565b634e487b7160e01b600052604160045260246000fd5b604080519081016001600160401b0381118282101715611c8157611c81611c49565b60405290565b604051601f8201601f191681016001600160401b0381118282101715611caf57611caf611c49565b604052919050565b60006001600160401b03821115611cd057611cd0611c49565b50601f01601f191660200190565b600082601f830112611cef57600080fd5b8135611d02611cfd82611cb7565b611c87565b818152846020838601011115611d1757600080fd5b816020850160208301376000918101602001919091529392505050565b60008060408385031215611d4757600080fd5b82356001600160401b03811115611d5d57600080fd5b611d6985828601611cde565b9250506020830135611d7a81611b54565b809150509250929050565b60006001600160401b03821115611d9e57611d9e611c49565b5060051b60200190565b801515811461139e57600080fd5b8035611b7481611da8565b600080600060608486031215611dd657600080fd5b6001600160401b038085351115611dec57600080fd5b8435850186601f820112611dff57600080fd5b611e0c611cfd8235611d85565b81358082526020808301929160051b840101891015611e2a57600080fd5b602083015b6020843560051b850101811015611f52578481351115611e4e57600080fd5b803584016040818c03601f19011215611e6657600080fd5b611e6e611c5f565b8660208301351115611e7f57600080fd5b611e918c602080850135850101611cde565b81528660408301351115611ea457600080fd5b6040820135820191508b603f830112611ebc57600080fd5b611ecc611cfd6020840135611d85565b602083810135808352908201919060051b84016040018e1015611eee57600080fd5b604084015b6040602086013560051b860101811015611f33578981351115611f1557600080fd5b611f258f60408335880101611cde565b835260209283019201611ef3565b5080602084015250508085525050602083019250602081019050611e2f565b509550611f659250505060208501611b69565b9150611f7360408501611db6565b90509250925092565b60008060408385031215611f8f57600080fd5b50508035926020909101359150565b60005b83811015611fb9578181015183820152602001611fa1565b50506000910152565b60008151808452611fda816020860160208601611f9e565b601f01601f19169290920160200192915050565b6020815260006120016020830184611fc2565b9392505050565b60006020828403121561201a57600080fd5b813561200181611b54565b60609190911b6bffffffffffffffffffffffff1916815260140190565b81835281816020850137506000828201602090810191909152601f909101601f19169091010190565b60006140608281018388845b61010081101561209857604080838537928301929190910190600101612077565b50505061400084019190915261606083018660005b6101008110156121235785830361405f190184528135368a9003601e190181126120d657600080fd5b890160208181019135906001600160401b038211156120f457600080fd5b81360383131561210357600080fd5b61210e868385612042565b968101969550939093019250506001016120ad565b50508561402085015283810361404085015261213f8186611fc2565b98975050505050505050565b60006020828403121561215d57600080fd5b815161200181611da8565b60008183825b61010081101561218f5760408083853792830192919091019060010161216e565b5050506140008201905092915050565b6000806000606084860312156121b457600080fd5b8351600381106121c357600080fd5b602085015160409095015190969495509392505050565b600080604083850312156121ed57600080fd5b505080516020909101519092909150565b60208082526041908201527f53616d6520504b48207573656420666f7220626f74682073746570733b20757360408201527f652061207365706172617465206b657920666f7220636f6e6669726d6174696f6060820152603760f91b608082015260a00190565b634e487b7160e01b600052603260045260246000fd5b6000835161228d818460208801611f9e565b8351908301906122a1818360208801611f9e565b01949350505050565b634e487b7160e01b600052601160045260246000fd5b808201808211156111e7576111e76122aa565b600082516122e5818460208701611f9e565b9190910192915050565b818103818111156111e7576111e76122aa565b634e487b7160e01b600052601260045260246000fd5b60008261232757612327612302565b500690565b600181811c9082168061234057607f821691505b60208210810361236057634e487b7160e01b600052602260045260246000fd5b50919050565b6000602080838503121561237957600080fd5b82516001600160401b038082111561239057600080fd5b818501915085601f8301126123a457600080fd5b81516123b2611cfd82611d85565b81815260059190911b830184019084810190888311156123d157600080fd5b8585015b83811015612445578051858111156123ed5760008081fd5b8601603f81018b136123ff5760008081fd5b878101516040612411611cfd83611cb7565b8281528d828486010111156124265760008081fd5b612435838c8301848701611f9e565b86525050509186019186016123d5565b5098975050505050505050565b80820281158282048414176111e7576111e76122aa565b60008261247857612478612302565b500490565b60006001820161248f5761248f6122aa565b5060010190565b6000604082016040835280855180835260608501915060608160051b8601019250602080880160005b838110156124ed57605f198887030185526124db868351611fc2565b955093820193908201906001016124bf565b50505050506020929092019290925292915050565b6000602080838503121561251557600080fd5b82516001600160401b0381111561252b57600080fd5b8301601f8101851361253c57600080fd5b805161254a611cfd82611d85565b81815260059190911b8201830190838101908783111561256957600080fd5b928401925b8284101561259057835161258181611b54565b8252928401929084019061256e565b979650505050505050565b601f8211156112cd576000816000526020600020601f850160051c810160208610156125c45750805b601f850160051c820191505b818110156125e3578281556001016125d0565b505050505050565b81516001600160401b0381111561260457612604611c49565b61261881612612845461232c565b8461259b565b602080601f83116001811461264d57600084156126355750858301515b600019600386901b1c1916600185901b1785556125e3565b600085815260208120601f198616915b8281101561267c5788860151825594840194600190910190840161265d565b508582101561269a5787850151600019600388901b60f8161c191681555b5050505050600190811b0190555056fea2646970667358221220e6baf1f3556c354a4b5b90bd3c3258c86830f770e3231f1dc324a523d040a2a264736f6c63430008180033"
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
        with open('contract_GameValidator-coin.txt', 'w') as file:
            # Write the contract address to the file
            file.write(new_contract_address)
        exit()