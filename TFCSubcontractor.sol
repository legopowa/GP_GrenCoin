pragma solidity ^0.8.0;

contract PlayerDatabaseSubcontract {
    struct Player {
        bool isRegistered;
        bool isValidator;
        string steamID;
        address rewardAddress;  // Replaced playerAddress with rewardAddress
    }

    mapping(address => Player) public playerData;
    address[] public playerAddresses; // Tracks all player addresses

    // Function to retrieve the entire player database
    function getAllPlayerData() public view returns (Player[] memory) {
        Player[] memory players = new Player[](playerAddresses.length);
        for (uint i = 0; i < playerAddresses.length; i++) {
            players[i] = playerData[playerAddresses[i]];
        }
        return players;
    }

    // Function to add or update a player's information
    function addOrUpdatePlayer(address _address, string memory _steamID, bool _isValidator, bool _isRegistered) public {
        playerData[_address] = Player({
            steamID: _steamID,
            isValidator: _isValidator,
            isRegistered: _isRegistered,
            rewardAddress: _address
        });
        playerAddresses.push(_address); // Add address to the tracking array
    }
    function toggleValidatorStatus(address _address) public {
        // You might want to add security checks to ensure only authorized users can toggle the status
        playerData[_address].isValidator = !playerData[_address].isValidator;
    }

    // Other functions and security checks as necessary...
}
