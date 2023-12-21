pragma solidity ^0.8.0;

contract TFCPlayAndEarn {
    address public owner;
    mapping(address => bool) public isValidator;
    mapping(address => string[]) public validatorSubmissions;
    mapping(string => bool) private nameExists; // To check if a name has already been added
    string[] private allSubmittedNames; // To store all unique names

    uint256 public lastMintingTime;
    uint256 public interval = 300; // Interval in seconds

    constructor() {
        owner = msg.sender;
    }

    function registerValidator(address validator) public {
        require(msg.sender == owner, "Only the owner can register validators");
        isValidator[validator] = true;
    }

    function removeValidator(address validator) public {
        require(msg.sender == owner, "Only the owner can remove validators");
        isValidator[validator] = false;
    }
    address public parentContract;

    // Address of the AnonID contract
    address public anonIDContractAddress;

    // Set AnonID Contract Address
    function setAnonIDContractAddress(address _address) public {
        require(msg.sender == owner, "Only the owner can set the AnonID contract address");
        anonIDContractAddress = _address;
    }

    function setParentContract(address _parentContract) public {
        require(msg.sender == owner, "Only the owner can set the parent contract");
        parentContract = _parentContract;
    }
    // Other contract members...

    mapping(address => string[]) public validatorSubmissions;
    uint256 public lastMintingTime;
    uint256 public interval = 300; // Example interval in seconds

    function submitNames(string[] memory names) public {
        require(isValidator[msg.sender], "Not a validator");
        validatorSubmissions[msg.sender] = names;

        for(uint i = 0; i < names.length; i++) {
            if (!nameExists[names[i]]) {
                nameExists[names[i]] = true;
                allSubmittedNames.push(names[i]);
            }
        }

        if (block.timestamp >= lastMintingTime + interval) {
            mintTokens();
            lastMintingTime = block.timestamp;
        }
    }

    function mintTokens() private {
        ERC20Token parent = ERC20Token(parentContract);
        AnonIDContract anonID = AnonIDContract(anonIDContractAddress);
        uint256 currentMintTime = block.timestamp;
        uint256 mintAmount;

        for (uint256 i = 0; i < playerAddresses.length; i++) {
            address playerAddress = playerAddresses[i];
            
            // Check if the player is active in the game
            if (anonID.isPlayerActiveInGame(currentGameID, playerAddress)) {
                // Calculate the mint amount based on active time
                mintAmount = calculateMintAmount(anonID.getLastPlayedTimestamp(playerAddress), currentMintTime);
                parent.mint(playerAddress, mintAmount); // Minting from the parent contract
            }
        }
    }

    function registerPlayer(string memory tfcName, address playerAddress) public {
        require(msg.sender == owner, "Only the owner can register players");
        tfcNameToAddress[tfcName] = playerAddress;
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
