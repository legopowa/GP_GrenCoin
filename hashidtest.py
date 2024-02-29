from web3 import Web3

# Sample string to hash using keccak256
sample_string = "JohnDoeLosAngeles01011980"

# Calculate keccak256 hash of the string
keccak256_hash = Web3.keccak(text=sample_string).hex()

print(keccak256_hash)
