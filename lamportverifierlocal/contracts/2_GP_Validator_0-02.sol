pragma solidity ^0.8.0;

interface IPlayerDatabase {
    function getAllPlayerNames() external view returns (string[] memory);
}

contract GameValidator {
    IPlayerDatabase playerDatabase;
    uint256 public lastMintTime;
    uint256 public constant MINT_INTERVAL = 5 minutes;
    uint256 public constant MAX_PLAYERS_PER_SUBMISSION = 64;


    struct ServerSubmission {
        address validator;
        bytes32 playerListHash; // Hash of the player list for gas efficiency
        bool canMint;
    }

    struct ServerPlayers {
        string serverIP;
        string[] playerNames;
    }
    //mapping(string => ServerSubmission[]) public serverSubmissions; // serverIP -> submissions

    mapping(string => mapping(address => ServerSubmission)) public serverSubmissions; 
    mapping(bytes32 => string[]) public hashToPlayerList; // playerListHash -> playerNames

    constructor(address _playerDatabaseAddress) {
        playerDatabase = IPlayerDatabase(_playerDatabaseAddress);
    }

    GP_Mint public mintContract;

    // Function to set the GP_Mint contract address
    function setMintContractAddress(address _mintContractAddress) public {
        // Additional checks for access control, like onlyOwner
        mintContract = GP_Mint(_mintContractAddress);
    }

    function mintForServer(string memory serverIP, bytes32 playerListHash) private {
        // Retrieve the player list for the given hash
        string[] memory playerList = hashToPlayerList[playerListHash];
        address[] memory rewardAddresses = getRewardAddresses(playerList);

        // Mint tokens for each player
        for (uint i = 0; i < rewardAddresses.length; i++) {
            if (rewardAddresses[i] != address(0)) { // Check for valid address
                uint256 mintAmount = calculateMintAmount(); // Define logic for mint amount
                mintContract.mintTokens(rewardAddresses[i], mintAmount);
            }
        }
    }

    function submitPlayerList(ServerPlayers[] memory serverPlayerLists, address validatorID, bool canMintFlag) public {
        require(isValidator(validatorID), "Caller is not a registered validator");

        uint256 totalPlayerCount = 0;

        for (uint i = 0; i < serverPlayerLists.length; i++) {
            uint256 serverPlayerCount = serverPlayerLists[i].playerNames.length;
            if (totalPlayerCount + serverPlayerCount > MAX_PLAYERS_PER_SUBMISSION) {
                break; // Stop if the max players per submission is exceeded
            }

            totalPlayerCount += serverPlayerCount;

            // Create a hash for the player list
            bytes32 playerListHash = keccak256(abi.encodePacked(serverPlayerLists[i].playerNames));
            hashToPlayerList[playerListHash] = serverPlayerLists[i].playerNames;

            // Overwrite the existing submission for this server IP and validator
            serverSubmissions[serverPlayerLists[i].serverIP][validatorID] = ServerSubmission({
                playerListHash: playerListHash,
                canMint: canMintFlag
            });
        }
    }

    function isValidator(address _address) public view returns (bool) {
        PlayerDatabase playerDatabase = PlayerDatabase(playerDatabaseAddress);
        return playerDatabase.isValidator(_address);
    }
    function resetSubmissions() private {
        // Iterate over each server IP
        for (uint i = 0; i < allServerIPs.length; i++) {
            string memory serverIP = allServerIPs[i];
            // Iterate over each validator's submission for this server IP
            for (uint j = 0; j < serverSubmissions[serverIP].length; j++) {
                address validator = serverSubmissions[serverIP][j].validator;
                // Clear the canMint flag
                serverSubmissions[serverIP][validator].canMint = false;
            }
        }
    }

    // Function to perform mass minting
    function performMassMinting() public {
        // Ensure mass minting conditions are met (e.g., time interval)
        require(block.timestamp >= lastMintTime + MINT_INTERVAL, "Mass minting interval not yet elapsed");

        // Iterate through each server to find the most common hash
        for (uint i = 0; i < allServerIPs.length; i++) {
            string memory serverIP = allServerIPs[i];
            bytes32 commonHash = findMostCommonHash(serverIP);
            
            // Proceed with minting for the player list corresponding to commonHash
            if (commonHash != bytes32(0)) { // Check if a common hash was found
                mintForServer(serverIP, commonHash);
            }
        }

        // Update the last minting time to the current time
        lastMintTime = block.timestamp;
    }

    function getRewardAddresses(string[] memory playerNames) public view returns (address[] memory) {
        return playerDatabase.getRewardAddressesByNames(playerNames);
    }


    function findMostCommonHash(string memory serverIP) private view returns (bytes32) {
        ServerSubmission[] memory submissions = serverSubmissions[serverIP];
        uint256 submissionCount = submissions.length;
        uint256 majorityThreshold = (submissionCount * 60) / 100; // 60% of total submissions
        mapping(bytes32 => uint256) memory hashCounts;
        bytes32 majorityHash;
        bool majorityFound = false;

        for (uint i = 0; i < submissionCount; i++) {
            bytes32 hash = submissions[i].playerListHash;
            hashCounts[hash]++;

            if (hashCounts[hash] > majorityThreshold) {
                majorityHash = hash;
                majorityFound = true;
                break; // Stop as soon as a majority is found
            }
        }

        return majorityFound ? majorityHash : bytes32(0); // Return majority hash or zero hash if no majority
    }

    // Additional functions...
}
