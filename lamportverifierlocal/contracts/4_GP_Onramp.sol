// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

// interface IPlayerDatabaseSubcontract {
//     function addOrUpdatePlayer(address _address, string calldata _steamID, bool _isValidator, bool _isRegistered) external;
// }

interface IPlayerDatabase {
    function addOrUpdatePlayer(address _address, string calldata _steamID, bool _isValidator, bool _isRegistered, string memory _playerName) external;
    // Include other functions from PlayerDatabase that PlayerOnrampContract needs to call
}

contract PlayerOnrampContract {
    IPlayerDatabase public mintyDatabase;

    event PlayerOnboarded(address indexed playerAddress, string steamID, bool isValidator, bool isRegistered);

    constructor(address _mintyDatabaseAddress) {
        playerDatabase = IPlayerDatabase(_playerDatabaseAddress);
    }

    function onboardPlayer(address _address, string calldata _steamID, bool _isValidator, bool _isRegistered) public {
        // Additional logic and security checks as needed
        playerDatabase.addOrUpdatePlayer(_address, _steamID, _isValidator, _isRegistered);
        emit PlayerOnboarded(_address, _steamID, _isValidator, _isRegistered);
    }

    // Additional functions and logic as required for onramping...

    function registerValidator(address validator) public {
        require(msg.sender == owner, "Only the owner can register validators");
        isValidator[validator] = true;
    }

    function removeValidator(address validator) public {
        require(msg.sender == owner, "Only the owner can remove validators");
        isValidator[validator] = false;
    }
}
// contract PlayerOnrampContract {
//     IMintyDatabaseSubcontract public mintyDatabase;

//     event PlayerOnboarded(address indexed playerAddress, string steamID, bool isValidator, bool isRegistered);

//     constructor(address _mintyDatabaseAddress) {
//         mintyDatabase = IMintyDatabaseSubcontract(_mintyDatabaseAddress);
//     }

//     function onboardPlayer(address _address, string calldata _steamID, bool _isValidator, bool _isRegistered) public {
//         // Additional logic and security checks as needed
//         mintyDatabase.addOrUpdatePlayer(_address, _steamID, _isValidator, _isRegistered);
//         emit PlayerOnboarded(_address, _steamID, _isValidator, _isRegistered);
//     }

//     // Additional functions and logic as required for onramping...
// }
