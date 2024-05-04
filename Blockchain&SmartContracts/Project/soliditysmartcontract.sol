// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DeveloperRewards {
    address public owner;
    mapping(address => uint) public balances;

    struct Developer {
        address account;
        uint score;
    }

    Developer[] public developers;
    uint public totalTokens;

    constructor(uint _totalTokens) {
        owner = msg.sender;
        totalTokens = _totalTokens;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    function addDeveloper(address _account, uint _score) public onlyOwner {
        developers.push(Developer(_account, _score));
    }

    function distributeTokens() public onlyOwner {
        uint totalScore = 0;
        for (uint i = 0; i < developers.length; i++) {
            totalScore += developers[i].score;
        }

        for (uint i = 0; i < developers.length; i++) {
            uint allocation = (developers[i].score * totalTokens) / totalScore;
            balances[developers[i].account] += allocation;
        }
    }

    function checkBalance(address _account) public view returns (uint) {
        return balances[_account];
    }
}
