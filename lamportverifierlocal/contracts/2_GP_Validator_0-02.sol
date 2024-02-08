pragma solidity ^0.8.0;

interface IPlayerDatabase {
    function getAllPlayerNames() external view returns (string[] memory);
}

contract GameValidator {
    IPlayerDatabase playerDatabase;
    uint256 public lastMintTime;
    uint256 public constant MINT_INTERVAL = 5 minutes;

    struct ServerSubmission {
        address validator;
        bytes32 playerListHash; // Hash of the player list for gas efficiency
        bool canMint;
    }

    struct ServerPlayers {
        string serverIP;
        string[] playerNames;
    }
    mapping(string => ServerSubmission[]) public serverSubmissions; // serverIP -> submissions
    mapping(bytes32 => string[]) public hashToPlayerList; // playerListHash -> playerNames

    constructor(address _playerDatabaseAddress) {
        playerDatabase = IPlayerDatabase(_playerDatabaseAddress);
    }

     function submitPlayerList(ServerPlayers[] memory serverPlayerLists, address validatorID, bool canMintFlag) public {
        require(isValidator(validatorID), "Caller is not a registered validator");

        uint256 totalPlayerCount = 0;

        for (uint i = 0; i < serverPlayerLists.length; i++) {
            if (totalPlayerCount + serverPlayerLists[i].playerNames.length > MAX_PLAYERS_PER_SUBMISSION) {
                break;
            }

            totalPlayerCount += serverPlayerLists[i].playerNames.length;

            bytes32 playerListHash = keccak256(abi.encodePacked(serverPlayerLists[i].playerNames));
            hashToPlayerList[playerListHash] = serverPlayerLists[i].playerNames;

            ServerSubmission memory submission = ServerSubmission({
                validator: validatorID,
                playerListHash: playerListHash,
                canMint: canMintFlag
            });

            serverSubmissions[serverPlayerLists[i].serverIP].push(submission);
        }
    }
    function isValidator(address _address) public view returns (bool) {
        PlayerDatabase playerDatabase = PlayerDatabase(playerDatabaseAddress);
        return playerDatabase.isValidator(_address);
    }
    function resetSubmissions() private {
        // Iterate over serverSubmissions and reset canMint flags
        // Optionally clear player lists if needed
    }
    // Function to perform mass minting
    function performMassMinting() public {
        // Ensure mass minting conditions are met (e.g., time interval)

        // Iterate through each server to find the most common hash
        for (string memory serverIP in allServerIPs) {
            bytes32 commonHash = findMostCommonHash(serverIP);
            
            // Proceed with minting for the player list corresponding to commonHash
            mintForServer(serverIP, commonHash);
        }
    }


    function mintForServer(string memory serverIP, bytes32 playerListHash) private {
        // Logic to mint tokens for the players in the list corresponding to the given hash
        // This requires access to the actual player list, not just the hash
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
