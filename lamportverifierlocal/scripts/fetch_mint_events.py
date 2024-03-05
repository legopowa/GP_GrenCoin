from brownie import GP_Mint, network
from web3 import Web3
web3 = Web3()
def main():
    # Set the contract address here
    contract_address = "0xdc05bAa675DC2DD2FA7a926f73A2d20C6899Db48"
    
    # Ensure you're on the correct network
    print(f"Current network: {network.show_active()}")
    
    # Access the contract
    contract = GP_Mint.at(contract_address)

    # Define block range
    start_block = 1  # Adjust based on your needs
    end_block = "latest"  # Use 'latest' for the most recent block

    # Fetch events
    events = contract.events.AuthorizedMinterSet#(fromBlock=start_block, toBlock=end_block)

    # Process and print events
    for event in events:
        print(f"Event {event.event} found:")
        print(f"  Minter: {event.args['minter']}")
        print(f"  Block Number: {event.blockNumber}")