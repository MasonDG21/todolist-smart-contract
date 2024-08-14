const hre = require("hardhat");

async function main() {
  const contractAddress = "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0"; // Use the address from your deployment
  const todoList = await hre.ethers.getContractAt("TodoList", contractAddress);

  console.log("\n--- TodoList Interaction Script ---\n");

  // Create a new task
  console.log("Creating a new task...");
  let tx = await todoList.createTask("Study Hardhat");
  await tx.wait(); 
  console.log("✅ Task created successfully!");

  // Get the number of tasks
  try {
    const taskCount = await todoList.getTaskCount();
    // taskCount = taskCount.toString()
    console.log(`\nTotal number of tasks: ${taskCount.toString()}`);
  } catch (error) {
    console.error("❌ Error fetching task count:", error.message);
  }

  // Get the first task
  try {
    const task = await todoList.getTask(0);
    console.log("\nTask Details:");
    console.log(`  Content: ${task[0]}`);
    console.log(`  Completed: ${task[1]}`);
  } catch (error) {
    console.error("❌ Error fetching task 0:", error.message);
  }

  // Complete the first task
  try {
    tx = await todoList.completeTask(0);
    await tx.wait();
    console.log("\nTask Completed:✔️");
  } catch (error) {
    console.error("❌ Error completing task 0:", error.message);
  }

  // Get the updated first task
  try {
    const updatedTask = await todoList.getTask(0);
    console.log("\nTask Updated: ♻️");
    console.log(`  Content: ${updatedTask[0]}`);
    console.log(`  Completed: ${updatedTask[1]}`);
  } catch (error) {
    console.error("❌ Error fetching updated task 0:", error.message);
  }

  console.log("\n--- End of Interaction Script ---");
}

main().catch((error) => {
  console.error("❌ An error occurred:", error);
  process.exitCode = 1;
});