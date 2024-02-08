// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./GP_MintyDatabase.sol"; // Import the MintyDatabase contract

contract Forum {
    MintyDatabase public mintyDatabase;

    struct Thread {
        address author;
        string content;
        uint256 timestamp;
        bool isDeleted;
    }

    struct Comment {
        address commenter;
        string content;
        uint256 timestamp;
        bool isDeleted;
    }

    mapping(uint256 => Thread) public threads;
    mapping(uint256 => Comment[]) public comments;
    mapping(address => uint256) public lastThreadCreationTime;
    mapping(address => uint256) public lastCommentTime;

    uint256 public threadCount;

    event ThreadCreated(uint256 threadId, address author);
    event CommentAdded(uint256 threadId, address commenter);
    event ThreadDeleted(uint256 threadId);
    event CommentDeleted(uint256 threadId, uint256 commentIndex);

    constructor(address _mintyDatabaseAddress) {
        mintyDatabase = MintyDatabase(_mintyDatabaseAddress);
    }

    modifier onlyRegistered() {
        require(mintyDatabase.isRegistered(msg.sender), "User is not registered");
        _;
    }

    modifier threadExists(uint256 threadId) {
        require(threads[threadId].timestamp != 0, "Thread does not exist");
        _;
    }

    function createThread(string memory content) public onlyRegistered {
        require(block.timestamp >= lastThreadCreationTime[msg.sender] + 1 hours, "Can only create a thread every hour");
        threads[threadCount] = Thread({
            author: msg.sender,
            content: content,
            timestamp: block.timestamp,
            isDeleted: false
        });
        lastThreadCreationTime[msg.sender] = block.timestamp;
        emit ThreadCreated(threadCount, msg.sender);
        threadCount++;
    }

    function commentOnThread(uint256 threadId, string memory content) public onlyRegistered threadExists(threadId) {
        require(block.timestamp >= lastCommentTime[msg.sender] + 5 minutes, "Can only comment every 5 minutes");
        comments[threadId].push(Comment({
            commenter: msg.sender,
            content: content,
            timestamp: block.timestamp,
            isDeleted: false
        }));
        lastCommentTime[msg.sender] = block.timestamp;
        emit CommentAdded(threadId, msg.sender);
    }

    function deleteThread(uint256 threadId) public {
        require(threads[threadId].author == msg.sender || mintyDatabase.isModerator(msg.sender), "Not authorized to delete thread");
        threads[threadId].isDeleted = true;
        emit ThreadDeleted(threadId);
    }

    function deleteComment(uint256 threadId, uint256 commentIndex) public threadExists(threadId) {
        require(comments[threadId][commentIndex].commenter == msg.sender || mintyDatabase.isModerator(msg.sender), "Not authorized to delete comment");
        comments[threadId][commentIndex].isDeleted = true;
        emit CommentDeleted(threadId, commentIndex);
    }

    // Additional functions and checks as necessary...
}
