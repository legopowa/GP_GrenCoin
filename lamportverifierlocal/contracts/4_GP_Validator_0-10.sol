// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IPlayerDatabase {
    function getAllPlayerNames() external view returns (string[] memory);
    function getServerIPList() external view returns (string[] memory);
    function getValidRewardAddressesByNames(string[] memory playerNames, uint256 lastMintTime) external view returns (address[] memory);
    function isValidator(address _address) external view returns (bool);

}
interface IGP_Mint {
    function mintTokens(address to, uint256 amount) external;
    // Add other function signatures as needed
}
contract GameValidator {
    IPlayerDatabase playerDatabase;
    IGP_Mint public mintContract;

    uint256 public lastMintTime;
    uint256 public constant MINT_INTERVAL = 5 minutes;
    uint256 public constant MAX_PLAYERS_PER_SUBMISSION = 64;
    uint256 public constant MAX_MINT_TIME = 10 minutes; // 10 minutes cap
    //uint256 public constant TOKENS_PER_SECOND = 1e18 / 60; // 1 token per minute
    uint256 public constant TOKENS_PER_SECOND = (1e18 * 60) / 60; // 1e18 represents 1 token, and we divide by 60 seconds


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


    // Function to set the GP_Mint contract address
    function setMintContractAddress(address _mintContractAddress) public {
        // Additional checks for access control, like onlyOwner
        mintContract = IGP_Mint(_mintContractAddress);
    }
    function calculateMintAmount() private view returns (uint256) {
        uint256 elapsedSeconds = block.timestamp - lastMintTime;

        if (elapsedSeconds > MAX_MINT_TIME) {
            elapsedSeconds = MAX_MINT_TIME; // Cap the elapsed time to MAX_MINT_TIME
        }

        return elapsedSeconds * TOKENS_PER_SECOND; // Calculate the mint amount based on elapsed time
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

        // Check if it's time to perform mass minting
        uint256 currentTime = block.timestamp;
        uint256 timeSinceLastMint = currentTime - lastMintTime;
        uint256 timeToNextInterval = MINT_INTERVAL - (currentTime % MINT_INTERVAL);

        if (timeSinceLastMint >= MINT_INTERVAL && timeToNextInterval < MINT_INTERVAL) {
            performMassMinting();
            lastMintTime = currentTime - timeToNextInterval; // Align with the 5-minute interval
        }
    }
    // function submitPlayerList(ServerPlayers[] memory serverPlayerLists, address validatorID, bool canMintFlag) public {
    //     require(isValidator(validatorID), "Caller is not a registered validator");

    //     uint256 totalPlayerCount = 0;

    //     for (uint i = 0; i < serverPlayerLists.length; i++) {
    //         uint256 serverPlayerCount = serverPlayerLists[i].playerNames.length;
    //         if (totalPlayerCount + serverPlayerCount > MAX_PLAYERS_PER_SUBMISSION) {
    //             break; // Stop if the max players per submission is exceeded
    //         }

    //         totalPlayerCount += serverPlayerCount;

    //         // Create a hash for the player list
    //         bytes32 playerListHash = keccak256(abi.encodePacked(serverPlayerLists[i].playerNames));
    //         hashToPlayerList[playerListHash] = serverPlayerLists[i].playerNames;

    //         // Overwrite the existing submission for this server IP and validator
    //         serverSubmissions[serverPlayerLists[i].serverIP][validatorID] = ServerSubmission({
    //             playerListHash: playerListHash,
    //             canMint: canMintFlag
    //         });
    //     }
    // }

    function isValidator(address _address) public view returns (bool) {
        //PlayerDatabase playerDatabase = PlayerDatabase(playerDatabaseAddress);
        return playerDatabase.isValidator(_address);
    }
    function resetSubmissions() private {
        string[] memory serverIPs = playerDatabase.getServerIPList();
        for (uint i = 0; i < serverIPs.length; i++) {
            string memory serverIP = serverIPs[i];
            for (uint j = 0; j < serverSubmissions[serverIP].length; j++) {
                address validator = serverSubmissions[serverIP][j].validator;
                serverSubmissions[serverIP][validator].canMint = false;
            }
        }
    }

    // Function to perform mass minting
    function performMassMinting() public {
        string[] memory serverIPs = playerDatabase.getServerIPList();
        for (uint i = 0; i < serverIPs.length; i++) {
            string memory serverIP = serverIPs[i];
            bytes32 commonHash = findMostCommonHash(serverIP);
            if (commonHash != bytes32(0)) {
                mintForServer(serverIP, commonHash);
            }
        }
        resetSubmissions();
    }
    function mintForServer(string memory serverIP, bytes32 playerListHash) private {
        // Retrieve the player list for the given hash
        string[] memory playerList = hashToPlayerList[playerListHash];
        address[] memory rewardAddresses = getValidRewardAddressesByNames(playerList);

        uint256 mintAmount = calculateMintAmount(); // Define logic for mint amount

        // Mint tokens for each player
        for (uint i = 0; i < rewardAddresses.length; i++) {
            if (rewardAddresses[i] != address(0)) { // Check for valid address
                mintContract.mintTokens(rewardAddresses[i], mintAmount);
            }
        }
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
    function getValidRewardAddressesByNames(string[] memory playerNames) public view returns (address[] memory) {
        return playerDatabase.getValidRewardAddressesByNames(playerNames, lastMintTime);
    }



    // Additional functions...
}
