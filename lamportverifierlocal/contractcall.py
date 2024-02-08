from web3 import Web3

# Connect to local Ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:4000'))

# Check if the connection is successful
if not w3.isConnected():
    print("Failed to connect to the Ethereum node.")
else:
    print("Connected to the Ethereum node.")

# The ABI for the contract, you need only the part for the commissionAddress function
contract_abi = [
    # Only include the ABI definition for the commissionAddress function
    {
        "constant": True,
        "inputs": [],
        "name": "commissionAddress",
        "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
]

# Read the contract address from the file
try:
    with open('contract_AnonID.txt', 'r') as file:
        contract_address = file.read().strip()
except FileNotFoundError:
    print("Error: 'contract_AnonID.txt' file not found.")
    exit()

# Create a contract object with the ABI and address
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Call the commissionAddress function
commission_address = contract.functions.commissionAddress().call()

print(f"The commission address is: {commission_address}")

print(f"The AnonID contract address is: {contract_address}")
