// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

// interface IPlayerDatabaseSubcontract {
//     function addOrUpdatePlayer(address _address, string calldata _steamID, bool _isValidator, bool _isRegistered) external;
// }

interface IPlayerDatabase {
    function addOrUpdatePlayer(address _address, string calldata _steamID, bool _isValidator, string memory _playerName) external;
    function deletePlayer(address _address) external;
    // Include other functions from PlayerDatabase that PlayerOnrampContract needs to call

    function setGameAdminStatus(address admin, bool status) external;
    function setValidatorStatus(address validator, bool status) external;

}

contract PlayerOnboardContract {
    IPlayerDatabase public playerDatabase;

    event PlayerOnboarded(address indexed playerAddress, string steamID, bool isValidator, string _playerName);
    event PlayerRemoved(address indexed deletedPlayerAddress);
    address _playerDatabaseAddress = 0xB03A6aFd440a2a9db8834F1A6093680f02f1114C;

    constructor() {
        playerDatabase = IPlayerDatabase(_playerDatabaseAddress);
    }

    function onboardPlayer(address _address, string calldata _steamID, bool _isValidator, string memory _playerName) public {
        // Additional logic and security checks as needed
        playerDatabase.addOrUpdatePlayer(_address, _steamID, _isValidator, _playerName);
        emit PlayerOnboarded(_address, _steamID, _isValidator, _playerName);
    }

    function deletePlayer(address _address) public {
        playerDatabase.deletePlayer(_address);
        emit PlayerRemoved(_address);
    }

    function setPlayerDatabaseAddress(address __playerDatabaseAddress) public {
        playerDatabase = IPlayerDatabase(__playerDatabaseAddress);
    }
    // Additional functions and logic as required for onramping...


    function registerValidator(address validator) public {
        // Add appropriate checks here
        playerDatabase.setValidatorStatus(validator, true);
    }

    function removeValidator(address validator) public {
        // Add appropriate checks here
        playerDatabase.setValidatorStatus(validator, false);
    }

    function registerAdmin(address admin) public {
        // Add appropriate checks here
        playerDatabase.setGameAdminStatus(admin, true);
    }

    function removeAdmin(address admin) public {
        // Add appropriate checks here
        playerDatabase.setGameAdminStatus(admin, false);
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
