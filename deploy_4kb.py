from web3 import Web3
from web3 import HTTPProvider
import sys

# w3 = Web3(HTTPProvider(
#     "https://ropsten.infura.io/v3/529aa367cbba407a98c67577f8b986a0"))


def deploy_4kb():

    w3 = Web3(HTTPProvider(
            "http://localhost:8545"))
    blocks = w3.eth.block_number
    # print(blocks)

    contract = w3.eth.contract(
        abi='[{"name": "BidAdded", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidIncreased", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidRemoved", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}], "anonymous": false, "type": "event"}, {"name": "AuctionPaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionUnpaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionClosed", "inputs": [], "anonymous": false, "type": "event"}, {"name": "TokensMinted", "inputs": [{"name": "_minTokenId", "type": "uint256", "indexed": false}, {"name": "_mintedQty", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidPromoted", "inputs": [{"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_height", "type": "int128", "indexed": false}], "anonymous": false, "type": "event"}, {"stateMutability": "view", "type": "function", "name": "contractVersion", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 426}, {"stateMutability": "view", "type": "function", "name": "getState", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 13776}, {"stateMutability": "nonpayable", "type": "function", "name": "test", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 39924}, {"stateMutability": "view", "type": "function", "name": "contractOwner", "inputs": [], "outputs": [{"name": "", "type": "address"}], "gas": 2616}, {"stateMutability": "view", "type": "function", "name": "minimumBid", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2646}, {"stateMutability": "view", "type": "function", "name": "open", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 2676}, {"stateMutability": "view", "type": "function", "name": "paused", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 2706}, {"stateMutability": "view", "type": "function", "name": "startDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2736}, {"stateMutability": "view", "type": "function", "name": "endDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2766}, {"stateMutability": "view", "type": "function", "name": "extendedEnd", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2796}, {"stateMutability": "view", "type": "function", "name": "extendingTime", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2826}, {"stateMutability": "view", "type": "function", "name": "minTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2856}, {"stateMutability": "view", "type": "function", "name": "maxTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2886}, {"stateMutability": "view", "type": "function", "name": "tokenQty", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2916}, {"stateMutability": "view", "type": "function", "name": "bidCount", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2946}, {"stateMutability": "view", "type": "function", "name": "bidAverage", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 2976}, {"stateMutability": "view", "type": "function", "name": "highestBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3006}, {"stateMutability": "view", "type": "function", "name": "lowWinningBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3036}, {"stateMutability": "view", "type": "function", "name": "levels", "inputs": [{"name": "arg0", "type": "uint256"}, {"name": "arg1", "type": "uint256"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "value", "type": "uint256"}, {"name": "prevBid", "type": "uint256"}, {"name": "nextBid", "type": "uint256"}]}], "gas": 7507}, {"stateMutability": "view", "type": "function", "name": "bidders", "inputs": [{"name": "arg0", "type": "address"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "lastSequence", "type": "uint256"}]}], "gas": 3413}, {"stateMutability": "view", "type": "function", "name": "testCount", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 3126}]',
        bytecode='0x6103dd56600436101561000d576102c3565b60046000601c37600051346103d45763a0a8e46081141561003757620f4241610140526020610140f35b631865c57d81141561005d5761004e610140610343565b61014051610160526020610160f35b63f8a8fd6d8114156100985760148054600180820180607f1d8160801d14156103d45780905090509050815550601454610140526020610140f35b63ce606ee08114156100b257600054610140526020610140f35b63d3a863868114156100cc57600254610140526020610140f35b63fcfff16f8114156100e657600354610140526020610140f35b635c975abb81141561010057600454610140526020610140f35b630b97bc8681141561011a57600554610140526020610140f35b63c24a0f8b81141561013457600654610140526020610140f35b6301f28d0381141561014e57600754610140526020610140f35b6366894fc881141561016857600854610140526020610140f35b63ce6e23b281141561018257600954610140526020610140f35b6391ba317a81141561019c57600a54610140526020610140f35b631eac06918114156101b657600b54610140526020610140f35b63b40a56278114156101d057600c54610140526020610140f35b63ecdde1aa8114156101ea57600d54610140526020610140f35b63cdb010a381141561020457600e54610140526020610140f35b63ebca293281141561021e57600f54610140526020610140f35b63aefb343481141561026a57600360243560068110156103d45702601060043560e05260c052604060c02001805461014052600181015461016052600281015461018052506060610140f35b63fcc8f7938114156102a7576004358060a01c6103d4578090506101405260116101405160e05260c052604060c020805461016052506020610160f35b639590d4b98114156102c157601454610140526020610140f35b505b60006000fd5b6101405160601b610180526101605161018051176101a0526101a0518152505660116101c05160e05260c052604060c0208054600181818301106103d457808201905090508155506101c0516101405260116101c05160e05260c052604060c020546101605261033a6101e06102c9565b6101e051815250565b6007544210156103585760016003541461035b565b60005b156103c757600454156103765760028152506103d2566103c2565b60055442106103b7576006546008548082106103d457808203905090504210156103a85760038152506103d2566103b2565b60048152506103d2565b6103c1565b60018152506103d2565b5b6103d1565b60058152506103d2565b5b565b600080fd5b6100046103dd036100046000396100046103dd036000f3'
    )

    acct = w3.eth.account.privateKeyToAccount(
            '0cc944d13eed9b4250a122bc2a953a44cc8741a4467f2cd4cb42daed1d960aad')
    # print(acct.address)

    construct_txn = contract.constructor("0x4E64373CAD46Ee4078126B9d7b1Bc2f1F1c61Dd2", 0, 1, 10, "0x4E64373CAD46Ee4078126B9d7b1Bc2f1F1c61Dd2", 10, 1638346670, 16383469999, 3000).buildTransaction({
            'from': acct.address,
            'nonce': w3.eth.getTransactionCount(acct.address),
            'value': 10,
            'gas': 9000000,
            # 'gasPrice': w3.toWei('21', 'gwei')})
            'gasPrice': 30000000000})

    signed = acct.signTransaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    # print(tx_receipt)
    return tx_receipt.contractAddress


sys.modules[__name__] = deploy_4kb
