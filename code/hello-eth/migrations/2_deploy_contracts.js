const Cheque = artifacts.require("Cheque");

module.exports = function (deployer) {
  deployer.deploy(Cheque);
};
