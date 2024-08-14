const { expect } = require("chai");

   describe("TodoList", function () {
     let TodoList;
     let todoList;
     let owner;
     let addr1;
   
     beforeEach(async function () {
       TodoList = await ethers.getContractFactory("TodoList");
       [owner, addr1] = await ethers.getSigners();
       todoList = await TodoList.deploy();
       await todoList
     });
   
     it("Should create a new task", async function () {
       await todoList.createTask("Test task");
       const taskCount = await todoList.getTaskCount();
       expect(taskCount).to.equal(1);
   
       const task = await todoList.getTask(0);
       expect(task.content).to.equal("Test task");
       expect(task.isCompleted).to.equal(false);
     });
   
     it("Should mark a task as completed", async function () {
       await todoList.createTask("Test task");
       await todoList.completeTask(0);
       const task = await todoList.getTask(0);
       expect(task.isCompleted).to.equal(true);
     });
   
     it("Should revert when trying to complete non-existent task", async function () {
       await expect(todoList.completeTask(0)).to.be.revertedWith("Task does not exist");
     });
   
     it("Should return correct task count", async function () {
       await todoList.createTask("Task 1");
       await todoList.createTask("Task 2");
       const taskCount = await todoList.getTaskCount();
       expect(taskCount).to.equal(2);
     });
   });
   