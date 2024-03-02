// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PlayerListHasher {

    struct ServerPlayers {
        string serverIP;
        string[] playerNames;
    }

    bytes32 private lastComputedHash;

    // Function to submit server player lists and compute their keccak256 hash
    // Define an event to emit the encoded data
    event EncodedData(bytes encodedData);

    // Function to submit server player lists and emit their encoded form
    function submitServerPlayersList(ServerPlayers[] memory serverPlayerLists) public {
        bytes memory encodedData;

        for (uint i = 0; i < serverPlayerLists.length; i++) {
            encodedData = abi.encodePacked(encodedData, serverPlayerLists[i].serverIP);
            for (uint j = 0; j < serverPlayerLists[i].playerNames.length; j++) {
                encodedData = abi.encodePacked(encodedData, serverPlayerLists[i].playerNames[j]);
            }
        }
        lastComputedHash = keccak256(encodedData);
        // Emit the encoded data
        emit EncodedData(encodedData);
    }

    // Function to get the last computed hash
    function getComputedHash() public view returns (bytes32) {
        return lastComputedHash;
    }

    // Function to submit a hash and verify it against the last computed hash
    function submitHashAndVerify(bytes32 submittedHash) public view returns (bool) {
        return (submittedHash == lastComputedHash);
    }

    function echoHash(bytes32 hash) public pure returns (bytes32) {
        return hash;
    }
}
