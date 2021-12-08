from web3 import Web3
from web3 import HTTPProvider

w3 = Web3(HTTPProvider(
    "http://10.66.67.6:8545"))
blocks = w3.eth.block_number
print("blocknumber >>> ", blocks)


greeter = w3.eth.contract(
    address='0xE9e0dE58870FF5c4B21272cdF1Ec30eF57Da00B6',
    abi='[{"name": "BidAdded", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidIncreased", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidRemoved", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}], "anonymous": false, "type": "event"}, {"name": "AuctionPaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionUnpaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionClosed", "inputs": [], "anonymous": false, "type": "event"}, {"name": "TokensMinted", "inputs": [{"name": "_minTokenId", "type": "uint256", "indexed": false}, {"name": "_mintedQty", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidPromoted", "inputs": [{"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_height", "type": "int128", "indexed": false}], "anonymous": false, "type": "event"}, {"stateMutability": "view", "type": "function", "name": "contractVersion", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 426}, {"stateMutability": "view", "type": "function", "name": "getState", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 13776}, {"stateMutability": "nonpayable", "type": "function", "name": "test", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 39924}, {"stateMutability": "view", "type": "function", "name": "contractOwner", "inputs": [], "outputs": [{"name": "", "type": "address"}], "gas": 2616}, {"stateMutability": "view", "type": "function", "name": "minimumBid", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2646}, {"stateMutability": "view", "type": "function", "name": "open", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 2676}, {"stateMutability": "view", "type": "function", "name": "paused", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 2706}, {"stateMutability": "view", "type": "function", "name": "startDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2736}, {"stateMutability": "view", "type": "function", "name": "endDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2766}, {"stateMutability": "view", "type": "function", "name": "extendedEnd", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2796}, {"stateMutability": "view", "type": "function", "name": "extendingTime", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2826}, {"stateMutability": "view", "type": "function", "name": "minTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2856}, {"stateMutability": "view", "type": "function", "name": "maxTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2886}, {"stateMutability": "view", "type": "function", "name": "tokenQty", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2916}, {"stateMutability": "view", "type": "function", "name": "bidCount", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2946}, {"stateMutability": "view", "type": "function", "name": "bidAverage", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 2976}, {"stateMutability": "view", "type": "function", "name": "highestBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3006}, {"stateMutability": "view", "type": "function", "name": "lowWinningBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3036}, {"stateMutability": "view", "type": "function", "name": "levels", "inputs": [{"name": "arg0", "type": "uint256"}, {"name": "arg1", "type": "uint256"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "value", "type": "uint256"}, {"name": "prevBid", "type": "uint256"}, {"name": "nextBid", "type": "uint256"}]}], "gas": 7507}, {"stateMutability": "view", "type": "function", "name": "bidders", "inputs": [{"name": "arg0", "type": "address"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "lastSequence", "type": "uint256"}]}], "gas": 3413}, {"stateMutability": "view", "type": "function", "name": "testCount", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 3126}]'
)

contract_return = greeter.functions.test().call()
print("contract_return >>> ", contract_return)