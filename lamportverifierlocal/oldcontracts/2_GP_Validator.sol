// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./GP_PlayerDatabase.sol"; // Import the MintyDatabase contract
import "./AnonID_noinit.sol";


contract TFCPlayAndEarn {
    address public owner;
    IPlayerDatabase public playerDatabase;
    IAnonIDContract public anonIDContract;
    mapping(address => bool) public isValidator;
    mapping(address => string[]) public validatorSubmissions;
    mapping(string => bool) private nameExists; // To check if a name has already been added
    string[] private allSubmittedNames; // To store all unique names

    uint256 public lastMintingTime;
    uint256 public interval = 300; // Interval in seconds

    constructor(address _playerDatabaseAddress, address _anonIDContractAddress) {
        owner = msg.sender;
        playerDatabase = IPlayerDatabase(_playerDatabaseAddress);
        anonIDContract = IAnonIDContract(_anonIDContractAddress);
    }
    
    function registerValidator(address validator) public {
        require(msg.sender == owner, "Only the owner can register validators");
        isValidator[validator] = true;
    }

    function removeValidator(address validator) public {
        require(msg.sender == owner, "Only the owner can remove validators");
        isValidator[validator] = false;
    }
    address public playerDatabaseContract;

    // Address of the AnonID contract
    address public anonIDContractAddress;

    // Set AnonID Contract Address
    function setAnonIDContractAddress(address _address) public {
        require(msg.sender == owner, "Only the owner can set the AnonID contract address");
        anonIDContractAddress = _address;
    }

    function setPlayerDatabaseContract(address _mintyDatabaseContract) public {
        require(msg.sender == owner, "Only the owner can set the mintyDatabase contract");
        playerDatabaseContract = _playerDatabaseContract;
    }
    // Other contract members...

    mapping(string => uint256) private nameFrequency; // Track frequency of each name
    uint256 public totalSubmissions; // Total number of submissions
    
    function evaluateAndMint() private {
        MintyDatabase GPConcs = MintyDatabase(mintyDatabaseContract);
        AnonIDContract anonID = AnonIDContract(anonIDContractAddress);
        uint256 threshold = (totalSubmissions * 3) / 4;
        string[] memory eligibleNames = new string[](allSubmittedNames.length);
        uint256 eligibleCount = 0;

        for (uint i = 0; i < allSubmittedNames.length; i++) {
            if (nameFrequency[allSubmittedNames[i]] >= threshold) {
                eligibleNames[eligibleCount] = allSubmittedNames[i];
                eligibleCount++;
            }
        }

        // Mint tokens for players associated with eligible names
        for (uint i = 0; i < eligibleCount; i++) {
            // Retrieve player address and mint tokens
            // address playerAddress = ...;
            // uint256 mintAmount = ...;
            GPConcs.mint(playerAddress, mintAmount);
        }

        // Reset data for next cycle
        resetData();
    }

    function resetData() private {
        for (uint i = 0; i < allSubmittedNames.length; i++) {
            nameFrequency[allSubmittedNames[i]] = 0;
        }
        delete allSubmittedNames;
        totalSubmissions = 0;
    }

    // function submitNames(string[] memory names) public {
    //     require(isValidator[msg.sender], "Not a validator");

    //     for (uint i = 0; i < names.length; i++) {
    //         if (!nameExists[names[i]]) {
    //             nameExists[names[i]] = true;
    //             allSubmittedNames.push(names[i]);
    //         }
    //         nameFrequency[names[i]] += 1;
    //     }

    //     // Mark submission
    //     totalSubmissions += 1;

    //     // Check if we are past the interval and trigger frequency evaluation and minting
    //     if (block.timestamp >= lastMintingTime + interval) {
    //         evaluateAndMint();
    //         lastMintingTime = block.timestamp;
    //     }
    // }

    // function evaluateAndMint() private {
    //     // Calculate 3/4th of total validator count
    //     uint256 threshold = (totalSubmissions * 3) / 4;

    //     for (uint i = 0; i < allSubmittedNames.length; i++) {
    //         if (nameFrequency[allSubmittedNames[i]] >= threshold) {
    //             // This name is eligible for minting
    //             // Add logic to handle eligible names
    //         }
    //     }

    //     // Reset for next round
    //     totalSubmissions = 0;
    //     // Reset nameFrequency and allSubmittedNames if necessary

    //     // Proceed to mint tokens for eligible names...
    // }
    // function submitNames(string[] memory names) public {
    //     require(isValidator[msg.sender], "Not a validator");
    //     validatorSubmissions[msg.sender] = names;

    //     for(uint i = 0; i < names.length; i++) {
    //         if (!nameExists[names[i]]) {
    //             nameExists[names[i]] = true;
    //             allSubmittedNames.push(names[i]);
    //         }
    //     }

    //     if (block.timestamp >= lastMintingTime + interval) {
    //         mintTokens();
    //         lastMintingTime = block.timestamp;
    //     }
    // }

    // function mintTokens() private {
    //     ERC20Token parent = ERC20Token(parentContract);
    //     AnonIDContract anonID = AnonIDContract(anonIDContractAddress);
    //     uint256 currentMintTime = block.timestamp;
    //     uint256 mintAmount;

    //     for (uint256 i = 0; i < playerAddresses.length; i++) {
    //         address playerAddress = playerAddresses[i];
            
    //         // Check if the player is active in the game
    //         if (anonID.isPlayerActiveInGame(currentGameID, playerAddress)) {
    //             // Calculate the mint amount based on active time
    //             mintAmount = calculateMintAmount(anonID.getLastPlayedTimestamp(playerAddress), currentMintTime);
    //             parent.mint(playerAddress, mintAmount); // Minting from the parent contract
    //         }
    //     }
    // }

    function registerPlayer(string memory tfcName, address playerAddress) public {
        require(msg.sender == owner, "Only the owner can register players");
        tfcNameToAddress[tfcName] = playerAddress;
    }
    function generateAllSubmittedNames() public view returns (string[] memory) {
        return allSubmittedNames;
    }
    function updatePlayer(string memory tfcName, address newPlayerAddress) public {
        require(msg.sender == owner, "Only the owner can update player data");
        tfcNameToAddress[tfcName] = newPlayerAddress;
    }

    function removePlayer(string memory tfcName) public {
        require(msg.sender == owner, "Only the owner can remove players");
        delete tfcNameToAddress[tfcName];
    }


    // Other functions...

    // Existing functions...
}
