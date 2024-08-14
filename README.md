# TodoList Blockchain Project 🚀

Ever felt like your ToDo list needed a bit more... permanence?

Me either haha but as a courtesy of Antrhopic and my recent urge to get back into web3 I decided to do a little refresher.

So here I bring you the TodoList... as an Ethereum smart contract.

## Features 📋

- Create tasks (because what's a todo list without tasks?)
- Mark tasks as complete (oh, the satisfaction!)
- View your tasks (in case you forget what you're supposed to be doing)
- All of this... on the blockchain! (because why not?)

## Tech Stack 🛠

- Solidity: For writing our smart contracts
- Hardhat: Our trusty development environment
- Ethers.js: To interact with our contracts
- Node.js: Because JavaScript all the things!

## Getting Started 🏁

1. Clone this repo:
2. Install dependencies:
   ```javascript
   npm install
   ```
3. Fire up a local node:
   ```javascript
   npx hardhat node
   ```
4. Deploy the contract:
   ```javascript
   npx hardhat run scripts/deploy.js
   // deploy locally with flag --network localhost
   ```
5. Interact with your contract:
   ```javascript
   npx hardhat run scripts/interact.js
   // or `npx hardhat run scripts/interact.js --network localhost`
   ```

## Project Structure 🏗

- `contracts/`
- `scripts/`
- `test/`

## Testing 🧪

Run the tests and pray to the blockchain gods:

```
npx hardhat test
```



Built with ❤️ and several cups of joe 🍵.