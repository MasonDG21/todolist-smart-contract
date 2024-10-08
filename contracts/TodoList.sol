// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TodoList {
    struct Task {
        string content;
        bool isCompleted;
    }

    mapping(address => Task[]) private userTasks;

    event TaskCreated(address indexed user, uint256 taskId, string content);
    event TaskCompleted(address indexed user, uint256 taskId);

    function createTask(string memory _content) public {
        userTasks[msg.sender].push(Task(_content, false));
        emit TaskCreated(msg.sender, userTasks[msg.sender].length - 1, _content);
    }

    function completeTask(uint256 _taskId) public {
        require(_taskId < userTasks[msg.sender].length, "Task does not exist");
        userTasks[msg.sender][_taskId].isCompleted = true;
        emit TaskCompleted(msg.sender, _taskId);
    }

    function getTask(uint256 _taskId) public view returns (string memory content, bool isCompleted) {
        require(_taskId < userTasks[msg.sender].length, "Task does not exist");
        Task memory task = userTasks[msg.sender][_taskId];
        return (task.content, task.isCompleted);
    }

    function getTaskCount() public view returns (uint256) {
        return userTasks[msg.sender].length;
    }
}
