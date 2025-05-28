// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Donation {
    address public owner;

    event DonationReceived(address indexed donor, uint256 amount);

    constructor() {
        owner = msg.sender; // Set the contract deployer as the owner
    }

    // Function to accept donations
    function donate() public payable {
        require(msg.value > 0, "Donation must be greater than zero");
        emit DonationReceived(msg.sender, msg.value);
    }

    // Function to withdraw funds (only owner)
    function withdraw() public {
        require(msg.sender == owner, "Only the owner can withdraw");
        payable(owner).transfer(address(this).balance);
    }

    // Get contract balance
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
