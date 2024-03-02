from brownie import PlayerListHasher, network
import time

def handle_event(event):
    print(f"Event: {event.event_name}")
    for arg in event.args:
        print(f"  {arg}: {event.args[arg]}")

def listen_for_events(contract):
    event_filters = [
        contract.Debug,
        contract.DebugUint,
        contract.DebugBytes32,
        contract.ServerIP,
        contract.PlayerName
    ]
    while True:
        for event_filter in event_filters:
            entries = event_filter.get_all_entries()
            for entry in entries:
                handle_event(entry)
        time.sleep(10)  # Poll every 10 seconds

def main():
    network.gas_limit(8000000)
    contract = PlayerListHasher  # Assumes the contract is already deployed and PlayerListHasher is available in the deployed contracts

    print("Listening for events. Press Ctrl+C to stop.")
    listen_for_events(contract)
