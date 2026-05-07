module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 8545, // default port of Ganache GUI/CLI
      network_id: "*" // Match any network id
    },
  },
  compilers: {
    solc: {
      version: "0.8.11" // your contract uses this version
    }
  }
};
