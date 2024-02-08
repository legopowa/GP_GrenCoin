// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.1;

contract AnonIDContract {
    
    uint256 public freeGasCap; // Add this state variable for freeGasFee
    uint256 public _coinCommission;
    uint256 private lastUsedCommission;
    bytes32 public lastUsedBytecodeHash;
    bytes32 constant master1 = 0xb7b18ded9664d1a8e923a5942ec1ca5cd8c13c40eb1a5215d5800600f5a587be;
    bytes32 constant master2 = 0x1ed304ab73e124b0b99406dfa1388a492a818837b4b41ce5693ad84dacfc3f25;
    bytes32 constant oracle = 0xd62569e61a6423c880a429676be48756c931fe0519121684f5fb05cbd17877fa;
    // uint256 public hourlyUserTxLimit;
    // uint256 public hourlyValidatorTxLimit;
    // uint256 public hourlyExchangeTxLimit;
    //mapping(address => uint256[]) public userTxTimestamps;
    mapping(address => uint256) public hourlyTxQuota;
    address private _commissionAddress;
    address private SFCContractAddress;
    address private netinitContractAddress;

    // Mapping of permitted contracts
    mapping(address => bool) public isContractPermitted;
    // user mappings
    //mapping(bytes32 => bool) public whitelist;
    mapping(address => bool) public whitelist;

    mapping(address => uint256) public minutesPlayed;
    mapping(address => uint256) public lastClaim;
    mapping(address => uint256) public lastLastClaim;
    mapping(address => bytes32) public addressToHashedID;
    Key[] public keys; // For iteration
    mapping(bytes32 => Key) public keyData; // For search
    mapping(address => UserQuota) private userQuotaInfo;
    mapping(address => uint256[500]) private userTxTimestamps; // Example with max 500 transactions

    event LogLastCalculatedHash(uint256 hash);
    event VerificationFailed(uint256 hashedData);
    event PkhUpdated(KeyType keyType, bytes32 previousPKH, bytes32 newPKH);
    event KeyAdded(KeyType keyType, bytes32 newPKH);
    event KeyModified(KeyType originalKeyType, bytes32 originalPKH, bytes32 modifiedPKH, KeyType newKeyType);
    event Whitelisted(address indexed _address, bytes32 hashedID);
    event QuotaSet(address indexed _address, uint256 _quota);
    event TxRecorded(address indexed _user, uint256 timestamp);
    event RemovedFromWhitelist(address indexed _address);
    event MinutesPlayedIncremented(address indexed user, uint256 _minutes);
    event CommissionSet(uint256 newCoinCommission);
    event ContractPermissionGranted(address contractAddress);
    event ContractPermissionRevoked(address contractAddress);
    event FreeGasCapSet(uint256 newFreeGasCap);
    event ClaimedGP(address indexed userAddress, uint256 lastClaimValue, uint256 minutesPlayed);
    event CommissionAddressSet(address indexed newCommissionAddress);


    constructor() {
        // Directly set the initial Lamport keys in the constructor
        addKey(KeyType.MASTER, master1);
        addKey(KeyType.MASTER, master2);
        addKey(KeyType.ORACLE, oracle);
        _commissionAddress = 0xfd003CA44BbF4E9fB0b2fF1a33fc2F05A6C2EFF9;
        SFCContractAddress = 0xFC00FACE00000000000000000000000000000000;
        netinitContractAddress = 0xD1005Eed00000000000000000000000000000000;
        // hourlyUserTxLimit = 5;
        // hourlyValidatorTxLimit = 120;
        // hourlyExchangeTxLimit = 1200;
    }

    bool public lastVerificationResult;

    // Define different key types
    enum KeyType { MASTER, ORACLE, DELETED }

    // Store the keys and their corresponding pkh
    struct Key {
        KeyType keyType;
        bytes32 pkh;
    }
    struct LastPlayedInfo {
        uint256 gameId;
        uint256 timestamp;
    }
    struct UserQuota {
        uint256 start; // Index of the oldest timestamp
        uint256 count; // Current count of timestamps
    }
    function setCoinCommissionStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        uint256 newCoinCommission
    )
        public
        onlyLamportMaster(
            currentpub,
            sig,
            nextPKH,
            abi.encodePacked(newCoinCommission)
        )
    {
        lastUsedCommission = newCoinCommission;
    }

    // Step 2: Verify and set the coinCommission
    function setCoinCommissionStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        uint256 newCoinCommission
    )
        public
        onlyLamportMaster(
            currentpub,
            sig,
            nextPKH,
            abi.encodePacked(newCoinCommission)
        )
    {
        require(newCoinCommission >= 0 && newCoinCommission <= 20, "AnonIDContract: Commission should be between 0% and 20%");

        require(newCoinCommission == lastUsedCommission, "AnonIDContract: Mismatched commission values between step one and two");

        _coinCommission = newCoinCommission;

        // Reset the temporary variable
        lastUsedCommission = 0;
        emit CommissionSet(newCoinCommission);

    }
    function commissionAddress() public view returns (address) {
        return _commissionAddress;
    }
    function coinCommission() public view returns (uint256) {
        return _coinCommission;
    }

    // Assuming there's a mapping to track the last mint time for each player in each game
    // Mapping for each player's last played information
    mapping(address => LastPlayedInfo) public lastPlayed;

    // Check if the player is active in the specified game
    function isPlayerActiveInGame(uint256 gameID, address player) public view returns (uint8) {
        LastPlayedInfo memory lastPlayedInfo = lastPlayed[player];
        bool isWithinTimeLimit = block.timestamp - lastPlayedInfo.timestamp < 8 minutes;

        if (isWithinTimeLimit && lastPlayedInfo.gameId == gameID) {
            return 2; // Player is active in this game and recently minted
        } else if (isWithinTimeLimit && lastPlayedInfo.gameId != gameID) {
            return 1; // Player is active but in a different game
        }
        return 0; // Player is not currently active
    }


    function addToWhitelist(address _address, string memory anonID) external {
        require(isContractPermitted[msg.sender], "Not permitted to modify whitelist");
        
        bytes32 hashedID = keccak256(abi.encodePacked(anonID));

        // Ensure the address is not already whitelisted
        require(!whitelist[_address], "Address already whitelisted");

         // Initialize the hourly transaction quota for the address
        hourlyTxQuota[_address] = 5; // Initial quota set to 10, adjust as needed

        // Whitelist the address
        whitelist[_address] = true;

        // Update the address to hashedID mapping
        addressToHashedID[_address] = hashedID;

        emit Whitelisted(_address, hashedID);

    }
    // function getHourlyTxQuota(address _address) external view returns (uint256) {
    //     return hourlyTxQuota[_address];
    // }

    function setHourlyTxQuota(address _address, uint256 _quota) external {
        require(isContractPermitted[msg.sender], "Not permitted to modify hourly transaction quota");

        // Ensure the address is indeed whitelisted before setting the quota
        require(whitelist[_address], "Address not found in whitelist");

        // Set the hourly transaction quota for the address
        hourlyTxQuota[_address] = _quota;
        emit QuotaSet(_address, _quota);

    }

    function toHexString(address _address) internal pure returns (string memory) {
        bytes32 value = bytes32(uint256(uint160(_address)));
        bytes memory alphabet = "0123456789abcdef";
        bytes memory str = new bytes(42);

        str[0] = '0';
        str[1] = 'x';

        for (uint256 i = 0; i < 20; i++) {
            str[2+i*2] = alphabet[uint8(value[i + 12] >> 4)];
            str[3+i*2] = alphabet[uint8(value[i + 12] & 0x0f)];
        }

        return string(str);
    }
    function isThisTxFree(address _user) external returns (bool) {
        // Ensure only TheRock can call this function
        require(msg.sender == 0x2685751d3C7A49EbF485e823079ac65e2A35A3DD,
                string(abi.encodePacked("Only TheRock can call this function. Caller: ", toHexString(msg.sender))));

        // Check if the user is whitelisted
        if (!whitelist[_user]) {
            return false;
        }

        // Return false if quota is zero
        if (hourlyTxQuota[_user] == 0) {
            return false;
        }

        UserQuota storage quotaInfo = userQuotaInfo[_user];
        uint256[500] storage timestamps = userTxTimestamps[_user];

        // Check if quota is exceeded within the last hour
        if (quotaInfo.count >= hourlyTxQuota[_user]) {
            uint256 oldestTimestampIndex = quotaInfo.start;
            if (block.timestamp - timestamps[oldestTimestampIndex] <= 1 hours) {
                // Quota exceeded, as the oldest transaction is within the last hour
                return false;
            }

            // Move the start index forward as we will overwrite the oldest timestamp
            quotaInfo.start = (quotaInfo.start + 1) % hourlyTxQuota[_user];
        } else {
            // Increment the count if the buffer is not full
            quotaInfo.count++;
        }

        // Add the new transaction timestamp
        uint256 newIndex = (quotaInfo.start + quotaInfo.count - 1) % hourlyTxQuota[_user];
        timestamps[newIndex] = block.timestamp;

        emit TxRecorded(_user, block.timestamp);
        return true;
    }
    // function isThisTxFree(address _user) external returns (bool) {
    //     // Ensure only TheRock can call this function
    //     require(msg.sender == 0x2685751d3C7A49EbF485e823079ac65e2A35A3DD,
    //             string(abi.encodePacked("Only TheRock can call this function. Caller: ", toHexString(msg.sender))));

    //     // Check if the user is whitelisted
    //     if (!whitelist[_user]) {
    //         return false;
    //     }

    //     // Return false if quota is zero
    //     if (hourlyTxQuota[_user] == 0) {
    //         return false;
    //     }

    //     // Get the array of timestamps for the user
    //     uint256[] storage timestamps = userTxTimestamps[_user];

    //     // Check if the user has made fewer transactions than the quota allows
    //     if (timestamps.length < hourlyTxQuota[_user]) {
    //         // User has not reached their quota yet, add the new timestamp
    //         timestamps.push(block.timestamp);
    //         emit TxRecorded(_user, block.timestamp);
    //         return true;
    //     }

    //     // User has reached or exceeded their quota, check the timestamp for quota enforcement
    //     if (block.timestamp - timestamps[0] <= 1 hours) {
    //         // Quota exceeded, as the oldest transaction is within the last hour
    //         return false;
    //     }

    //     // Remove the oldest timestamp and add the new one
    //     removeOldestTimestamp(_user);
    //     timestamps.push(block.timestamp);
    //     emit TxRecorded(_user, block.timestamp);
    //     return true;
    // }

    // function removeOldestTimestamp(address _user) internal {
    //     uint256[] storage timestamps = userTxTimestamps[_user];
    //     for (uint i = 0; i < timestamps.length - 1; i++) {
    //         timestamps[i] = timestamps[i + 1];
    //     }
    //     timestamps.pop();
    // }

    // function removeOldestTimestamp(address _user) internal {
    //     uint256[] storage timestamps = userTxTimestamps[_user];
    //     for (uint i = 0; i < timestamps.length - 1; i++) {
    //         timestamps[i] = timestamps[i + 1];
    //     }
    //     timestamps.pop();
    // }

// Add the toHexString function here if it's not already present in your contract


    // function isThisTxFree(address _user) external returns (bool) {
    //     // Ensure only the coinbase can call this function
    //     // THIS IS ROCK
    //     require(
    //         msg.sender == 0x2685751d3C7A49EbF485e823079ac65e2A35A3DD, 
    //         string(abi.encodePacked("Only TheRock can call this function. Caller: ", toHexString(msg.sender)))
    //     );
    //     // Check if the user is whitelisted
    //     if (!whitelist[_user]) {
    //         return false;
    //     }

    //     uint256[] storage timestamps = userTxTimestamps[_user];
    //     emit TxRecorded(_user, block.timestamp);


    //     // If the user has reached their hourly quota, check the oldest timestamp
    //     if (timestamps.length >= hourlyTxQuota[_user]) {
    //         if (block.timestamp - timestamps[0] <= 1 hours) {
    //             // If the oldest transaction is within the last hour, the quota has been exceeded
    //             return false;
    //         } else {
    //             // Otherwise, remove the oldest timestamp to make space for the new one
    //             for (uint i = 0; i < timestamps.length - 1; i++) {
    //                 timestamps[i] = timestamps[i + 1];
    //             }
    //             timestamps.pop();
    //         }
    //     }

    //     // Add the new transaction timestamp
    //     timestamps.push(block.timestamp);
    //     return true;
    // }
    // Remove an address from the whitelist
// Remove an address from the whitelist
    function removeFromWhitelist(address _address) external {
        require(isContractPermitted[msg.sender], "Not permitted to modify whitelist");

        // Ensure the address is indeed whitelisted before removing
        require(whitelist[_address], "Address not found in whitelist");

        // Remove the address from the whitelist
        whitelist[_address] = false;

        // Remove the address and hashedID association from the addressToHashedID mapping
        delete addressToHashedID[_address];
        emit RemovedFromWhitelist(_address);

    }

    function incrementMinutesPlayed(address user, uint256 _minutes) external {
        require(isContractPermitted[msg.sender], "Not permitted to modify minutes played");
        minutesPlayed[user] += _minutes;
        emit MinutesPlayedIncremented(user, _minutes);

    }

    function updateLastPlayed(address _address, uint256 _gameId) external {
        require(isContractPermitted[msg.sender], "Not permitted to update last played");

        lastPlayed[_address] = LastPlayedInfo({
            gameId: _gameId,
            timestamp: block.timestamp
        });

    }
    // Function to get the minutes played by a user
    function getMinutesPlayed(address user) external view returns (uint256) {
        return minutesPlayed[user];
    }
 // New function to check if an address is whitelisted
    function isWhitelisted(address _address) external view returns (bool) {
        return whitelist[_address];
    }
    function claimGP() external {
        // The invoking address is the user's address
        address userAddress = msg.sender;

        // Check if the user's address is whitelisted
        require(whitelist[userAddress], "User is not whitelisted");

        // Use the user's address to fetch lastClaim and lastLastClaim from AnonID contract
        uint256 lastClaimValue = lastClaim[userAddress];
        uint256 lastLastClaimValue = lastLastClaim[userAddress];
        
        require(lastClaimValue >= lastLastClaimValue, "Invalid claim values");

        // uint256 amountToMint = lastClaimValue.sub(lastLastClaimValue); // Using SafeMath

        // uint256 commissionAmount = amountToMint.mul(coinCommission).div(100); // Using SafeMath
        // amountToMint = amountToMint.sub(commissionAmount); // Using SafeMath

        // // Transfer the commission
        // token.transfer(commissionAddress, commissionAmount);

        // // Transfer the tokens to the user
        // token.transfer(userAddress, amountToMint);

        // Update lastClaim and lastLastClaim in the AnonID contract
        lastLastClaim[userAddress] = lastClaimValue;
        lastClaim[userAddress] = minutesPlayed[userAddress];  // Update with the current minutes played
        emit ClaimedGP(userAddress, lastClaimValue, minutesPlayed[userAddress]);

    }
    function grantActivityContractPermission(address contractAddress, bytes32[2][256] calldata currentpub, bytes[256] calldata sig, bytes32 nextPKH) public onlyLamportMaster(currentpub, sig, nextPKH, abi.encodePacked(contractAddress)) {
        isContractPermitted[contractAddress] = true;
        emit ContractPermissionGranted(contractAddress);

    }

    // Function to revoke permission from a contract
    function revokeActivityContractPermission(address contractAddress, bytes32[2][256] calldata currentpub, bytes[256] calldata sig, bytes32 nextPKH) public onlyLamportMaster(currentpub, sig, nextPKH, abi.encodePacked(contractAddress)) {
        isContractPermitted[contractAddress] = false;
    }

 
// Temporary storage for the new commission address during the update process
    bytes32 private lastUsedCommissionAddressHash;

    // Step 1: Temporarily store the hash of the new commission address
    function setCommissionAddressStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address newCommissionAddress
    )
        public
        onlyLamportMaster(
            currentpub,
            sig,
            nextPKH,
            abi.encodePacked(newCommissionAddress)
        )
    {
        lastUsedCommissionAddressHash = keccak256(abi.encodePacked(newCommissionAddress));
    }

    // Step 2: Verify and set the commissionAddress
    function setCommissionAddressStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address newCommissionAddress
    )
        public
        onlyLamportMaster(
            currentpub,
            sig,
            nextPKH,
            abi.encodePacked(newCommissionAddress)
        )
    {
        require(lastUsedCommissionAddressHash == keccak256(abi.encodePacked(newCommissionAddress)), "AnonIDContract: Mismatched address hash between step one and two");

        _commissionAddress = newCommissionAddress;

        // Reset the temporary variable
        lastUsedCommissionAddressHash = 0;
        emit CommissionAddressSet(newCommissionAddress);
    }

    function updateMinStakeStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        bytes memory newMinStake
    )
        public
        onlyLamportMaster(
            currentpub,
            sig,
            nextPKH,
            abi.encodePacked(newMinStake)
        )
    {
        // Save the used master NextPKH in a global variable
        lastUsedNextPKH = nextPKH;
    }

    function updateMinStakeStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        bytes32 newMinStake
    )
        public payable
        onlyLamportMaster(
            currentpub,
            sig,
            nextPKH,
            abi.encodePacked(newMinStake)
        )
    {
        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        bool pkhMatched = (lastUsedNextPKH != currentPKH);
        lastUsedNextPKH = bytes32(0);

        // If checks pass, call the target function
        require(pkhMatched, "PKH does not match last used PKH");

        // This is the signature of the function "updateMinSelfStake(uint256)"
        bytes4 methodId = bytes4(keccak256("updateMinSelfStake(uint256)"));

        // Encoding the method ID and parameters
        bytes memory data = abi.encodeWithSelector(methodId, uint256(newMinStake));

        // Perform the low-level call with the encoded data
        (bool success, ) = SFCContractAddress.call{value: msg.value}(data);

        // It's a good idea to handle the possibility that the call failed
        require(success, "Call to updateMinSelfStake failed");
    }

    function callMinStake() public returns (uint256 minStakeValue) {
        // This is the signature of the function "minStake()"
        bytes4 methodId = bytes4(keccak256("minStake()"));

        // Perform the low-level call with the encoded method ID
        (bool success, bytes memory returnData) = netinitContractAddress.staticcall(abi.encodeWithSelector(methodId));

        require(success, "Call to minStake failed");

        // Decode the returned data
        (minStakeValue) = abi.decode(returnData, (uint256));

        return minStakeValue;
    }

    // Add a new key
    function addKey(KeyType keyType, bytes32 newPKH) private {
        Key memory newKey = Key(keyType, newPKH);
        keys.push(newKey);
        keyData[newPKH] = newKey;
        emit KeyAdded(keyType, newPKH);
    }
    // Search for a key by its PKH, return the key and its position in the keys array
    function getKeyAndPosByPKH(bytes32 pkh) public view returns (KeyType, bytes32, uint) {
        Key memory key = keyData[pkh];
        require(key.pkh != 0, "AnonIDContract: No such key");

        // Iterate over keys array to find the position
        for (uint i = 0; i < keys.length; i++) {
            if (keys[i].pkh == pkh) {
                return (key.keyType, key.pkh, i);
            }
        }
        revert("AnonIDContract: No such key");
    }
    function getPKHsByPrivilege(KeyType privilege) public view returns (bytes32[] memory) {
        bytes32[] memory pkhs = new bytes32[](keys.length);
        uint counter = 0;

        for (uint i = 0; i < keys.length; i++) {
            if (keys[i].keyType == privilege) {
                pkhs[counter] = keys[i].pkh;
                counter++;
            }
        }

        // Prepare the array to return
        bytes32[] memory result = new bytes32[](counter);
        for(uint i = 0; i < counter; i++) {
            result[i] = pkhs[i];
        }

        return result;
    }



    bytes32 private lastUsedDeleteKeyHash;
    bytes32 private storedNextPKH;

    function deleteKeyStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        bytes32 deleteKeyHash
    )
        public
        onlyLamportMaster(
            currentpub,
            sig,
            nextPKH,
            abi.encodePacked(deleteKeyHash)
        )
    {
        // Save the used deleteKeyHash in a global variable
        lastUsedDeleteKeyHash = deleteKeyHash;
        storedNextPKH = nextPKH;
    }

    function deleteKeyStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        bytes32 confirmDeleteKeyHash
    )
        public
        onlyLamportMaster(
            currentpub,
            sig,
            nextPKH,
            abi.encodePacked(confirmDeleteKeyHash)
        )
    {
        // Calculate the current public key hash (currentPKH)
        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        
        // Check if storedNextPKH is not the same as the current PKH
        require(currentPKH != storedNextPKH, "AnonIDContract: Cannot use the same keychain twice for this function");
        
        // Check if the used deleteKeyHash matches the last used deleteKeyHash
        require(lastUsedDeleteKeyHash == confirmDeleteKeyHash, "AnonIDContract: Keys do not match");
        
        // Execute the delete key logic
        // Assuming firstMasterPKH and secondMasterPKH are correctly verified and provided
        bytes32 firstMasterPKH = storedNextPKH; // Placeholder, replace with the actual value
        bytes32 secondMasterPKH = currentPKH; // Placeholder, replace with the actual value
        bytes32 targetPKH = confirmDeleteKeyHash;
        
        // Check that the two provided keys are master keys
        require(keyData[firstMasterPKH].keyType == KeyType.MASTER && keyData[secondMasterPKH].keyType == KeyType.MASTER, "AnonIDContract: Provided keys are not master keys");
        
        // Disallow master keys from deleting themselves
        require(targetPKH != firstMasterPKH && targetPKH != secondMasterPKH, "AnonIDContract: Master keys cannot delete themselves");
        

        require(keyData[targetPKH].pkh != 0, "AnonIDContract: No such key (deletion)");
        for (uint i = 0; i < keys.length; i++) {
            if (keys[i].pkh == targetPKH) {

                KeyType originalKeyType = keyData[targetPKH].keyType; // Store the original KeyType
                // Overwriting the first 7 characters with "de1e7ed" and the rest with random values
                bytes32 modifiedPKH = 0xde1e7ed000000000000000000000000000000000000000000000000000000000;
                uint256 randomValue = uint256(keccak256(abi.encodePacked(block.timestamp, block.prevrandao)));
                modifiedPKH ^= bytes32(randomValue); // XOR to keep "de1e7ed" in the first 7 characters
                
                // Modify the existing entry instead of deleting it
                keyData[targetPKH].pkh = modifiedPKH;
                keyData[targetPKH].keyType = KeyType.DELETED; // Set the keyType to DELETED
                
                emit KeyModified(originalKeyType, targetPKH, modifiedPKH, KeyType.DELETED); // Emitting a new event for modification                    
                break;
            }
        }


        
        // Reset lastUsedDeleteKeyHash
        lastUsedDeleteKeyHash = bytes32(0);
        storedNextPKH = bytes32(0);
    }




    function verify_u256(
        uint256 bits,
        bytes[256] calldata sig,
        bytes32[2][256] calldata pub
    ) public pure returns (bool) {
        unchecked {
            for (uint256 i; i < 256; i++) {
                if (
                    pub[i][((bits & (1 << (255 - i))) > 0) ? 1 : 0] !=
                    keccak256(sig[i])
                ) return false;
            }

            return true;
        }
    }

    modifier onlyLamportMaster(bytes32[2][256] calldata currentpub, bytes[256] calldata sig, bytes32 nextPKH, bytes memory prepacked) {
        //require(initialized, "AnonIDContract: not initialized");

        bytes32 pkh = keccak256(abi.encodePacked(currentpub));
        require(keyData[pkh].keyType == KeyType.MASTER, "AnonIDContract: Not a master key");

        uint256 hashedData = uint256(keccak256(abi.encodePacked(prepacked, nextPKH)));
        emit LogLastCalculatedHash(hashedData);

        bool verificationResult = verify_u256(hashedData, sig, currentpub);

        lastVerificationResult = verificationResult;

        if (!verificationResult) {
            emit VerificationFailed(hashedData);
            revert("AnonIDContract: Verification failed");
        } else {
            emit PkhUpdated(keyData[pkh].keyType, pkh, nextPKH);
            updateKey(pkh, nextPKH);
        }

        _;
    }



    function updateKey(bytes32 oldPKH, bytes32 newPKH) internal {
        require(keyData[oldPKH].pkh != 0, "AnonIDContract: No such key");

        // Update the public key hash in the key data mapping
        Key memory updatedKey = Key(keyData[oldPKH].keyType, newPKH);
        keyData[newPKH] = updatedKey;

        // Remove the old key from key data
        delete keyData[oldPKH];

        // Update the public key hash in the keys array
        for (uint i = 0; i < keys.length; i++) {
            if (keys[i].pkh == oldPKH) {
                keys[i] = updatedKey;
                break;
            }
        }

        emit PkhUpdated(updatedKey.keyType, oldPKH, newPKH);
    }



    modifier onlyLamportOracle(bytes32[2][256] calldata currentpub, bytes[256] calldata sig, bytes32 nextPKH, bytes memory prepacked) {
        //require(initialized, "AnonIDContract: not initialized");

        bytes32 pkh = keccak256(abi.encodePacked(currentpub));
        require(keyData[pkh].keyType == KeyType.ORACLE, "AnonIDContract: Not an oracle key");

        uint256 hashedData = uint256(keccak256(abi.encodePacked(prepacked, nextPKH)));
        emit LogLastCalculatedHash(hashedData);

        bool verificationResult = verify_u256(hashedData, sig, currentpub);

        lastVerificationResult = verificationResult;

        if (!verificationResult) {
           // emit VerificationFailed(hashedData);
            revert("AnonIDContract: Verification failed");
        } else {
            emit PkhUpdated(keyData[pkh].keyType, pkh, nextPKH);
            updateKey(pkh, nextPKH);
        }

        _;
    }

    bytes32 public lastUsedNextPKH;

    function createMasterKeyStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        bytes memory newmasterPKH
    )
        public
        onlyLamportMaster(
            currentpub,
            sig,
            nextPKH,
            abi.encodePacked(newmasterPKH)
        )
    {
        // Save the used master NextPKH in a global variable
        lastUsedNextPKH = nextPKH;
    }

    function createMasterKeyStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        bytes32 newmasterPKH
    )
        public
        onlyLamportMaster(
            currentpub,
            sig,
            nextPKH,
            abi.encodePacked(newmasterPKH)
        )
    {
        // Check if the used master NextPKH matches the last used PKH
        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        bool pkhMatched = (lastUsedNextPKH != currentPKH);
        lastUsedNextPKH = bytes32(0);
        // If checks pass, add the new master key
        require(pkhMatched, "AnonIDContract: PKH matches last used PKH (use separate second key)");

        addKey(KeyType.MASTER, newmasterPKH);

        // Reset lastUsedNextPKH
        lastUsedNextPKH = bytes32(0);
    }


    function createOracleKeyFromMaster(
        bytes32[2][256] calldata currentpub,
        bytes32 nextPKH,
        bytes[256] calldata sig,
        bytes32 neworaclePKH
    )
        public
        onlyLamportMaster(
            currentpub,
            sig,
            nextPKH,
            abi.encodePacked(neworaclePKH)
        )
    {
        
        addKey(KeyType.ORACLE, neworaclePKH);
      
    }


    function createContractStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        bytes memory bytecode
    )
        public
        onlyLamportMaster(
            currentpub,
            sig,
            nextPKH,
            abi.encodePacked(bytecode)
        )
    {
        // Save the hash of the bytecode in a global variable
        lastUsedBytecodeHash = keccak256(bytecode);
    }

    function createContractStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        bytes memory bytecode
    )
        public
        onlyLamportMaster(
            currentpub,
            sig,
            nextPKH,
            abi.encodePacked(bytecode)
        )
        returns (address)
    {
         // Verify bytecode hash matches
        require(keccak256(bytecode) == lastUsedBytecodeHash, "Bytecode does not match previously provided bytecode.");
        address newContract;
        assembly {
            newContract := create(0, add(bytecode, 0x20), mload(bytecode))
        }
        require(newContract != address(0), "Contract creation failed");
        return newContract;
    }
    function setFreeGasCap(uint256 _newCap, bytes32[2][256] calldata currentpub, bytes[256] calldata sig, bytes32 nextPKH) public onlyLamportMaster(currentpub, sig, nextPKH, abi.encodePacked(_newCap)) {
        freeGasCap = _newCap;
        emit FreeGasCapSet(_newCap);

    }

}
