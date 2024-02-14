from eth_utils import encode_hex, to_bytes
from web3 import Web3

# Example constructor arguments
arg1 = "Hello"
arg2 = "World"
arg3 = 123

# ABI encode the arguments
encoded_args = Web3.solidityPack(['string', 'string', 'uint256'], [arg1, arg2, arg3])

# Load the bytecode of the contract (replace with actual bytecode)
bytecode = "0x608060405234801561001057600080fd5b506040518060400160405280..."

# Append the encoded arguments to the bytecode
full_bytecode = bytecode + encode_hex(encoded_args)[2:]

# Pass full_bytecode to the deployer contract's function
# ... (this part depends on how you're interacting with the blockchain, e.g., Brownie, Web3.py)
# have to fetch GP_Mint and LamportBase bytecode (together) and make appended bytecode with mint args ...
# for bonus points, deploy via AnonID contract and just keep doing it like that (also make blockchain 
# deploy only via AnonID)