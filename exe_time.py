from web3 import Web3
from web3 import HTTPProvider
import time
import csv
import typer


def main(iteration: int = typer.Argument(1)):

    with open('exe_time.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            '4kb',
            '56kb'
        ])
        writer.writeheader()

        i = 1
        while(i <= iteration):
            w3 = Web3(HTTPProvider(
                "http://localhost:8545"))
            blocks = w3.eth.block_number
            print("blocknumber >>> ", blocks)
            print("--------------------------------------" + "Iterations: "
                  + str(i) + "--------------------------------------")
            w3 = Web3(HTTPProvider("http://localhost:8545"))
            print("Is connected?:", w3.isConnected())
            acct = w3.eth.account.privateKeyToAccount(
                '4698687ad012af87ab5aff4cf787b7324f36e09d9629b9bcd0eba7cbc1d3b327')
            print(acct.address)
            greeter = w3.eth.contract(
                address='0xBe047df53438E14F3eeABf260A866A6113728Aa4',
                abi='[{"name": "BidAdded", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidIncreased", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidRemoved", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}], "anonymous": false, "type": "event"}, {"name": "AuctionPaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionUnpaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionClosed", "inputs": [], "anonymous": false, "type": "event"}, {"name": "TokensMinted", "inputs": [{"name": "_minTokenId", "type": "uint256", "indexed": false}, {"name": "_mintedQty", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidPromoted", "inputs": [{"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_height", "type": "int128", "indexed": false}], "anonymous": false, "type": "event"}, {"stateMutability": "view", "type": "function", "name": "contractVersion", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 426}, {"stateMutability": "view", "type": "function", "name": "getState", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 13776}, {"stateMutability": "nonpayable", "type": "function", "name": "test", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 39924}, {"stateMutability": "view", "type": "function", "name": "contractOwner", "inputs": [], "outputs": [{"name": "", "type": "address"}], "gas": 2616}, {"stateMutability": "view", "type": "function", "name": "minimumBid", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2646}, {"stateMutability": "view", "type": "function", "name": "open", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 2676}, {"stateMutability": "view", "type": "function", "name": "paused", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 2706}, {"stateMutability": "view", "type": "function", "name": "startDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2736}, {"stateMutability": "view", "type": "function", "name": "endDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2766}, {"stateMutability": "view", "type": "function", "name": "extendedEnd", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2796}, {"stateMutability": "view", "type": "function", "name": "extendingTime", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2826}, {"stateMutability": "view", "type": "function", "name": "minTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2856}, {"stateMutability": "view", "type": "function", "name": "maxTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2886}, {"stateMutability": "view", "type": "function", "name": "tokenQty", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2916}, {"stateMutability": "view", "type": "function", "name": "bidCount", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2946}, {"stateMutability": "view", "type": "function", "name": "bidAverage", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 2976}, {"stateMutability": "view", "type": "function", "name": "highestBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3006}, {"stateMutability": "view", "type": "function", "name": "lowWinningBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3036}, {"stateMutability": "view", "type": "function", "name": "levels", "inputs": [{"name": "arg0", "type": "uint256"}, {"name": "arg1", "type": "uint256"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "value", "type": "uint256"}, {"name": "prevBid", "type": "uint256"}, {"name": "nextBid", "type": "uint256"}]}], "gas": 7507}, {"stateMutability": "view", "type": "function", "name": "bidders", "inputs": [{"name": "arg0", "type": "address"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "lastSequence", "type": "uint256"}]}], "gas": 3413}, {"stateMutability": "view", "type": "function", "name": "testCount", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 3126}]'
            )

            construct_txn = greeter.functions.test().buildTransaction({
                'from': acct.address,
                'nonce': w3.eth.getTransactionCount(acct.address),
                'gas': 10000000,
                'gasPrice': 30000000000
                })

            signed = acct.signTransaction(construct_txn)
            tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_receipt)
            # print(greeter.caller().test())

            start_time = time.time()
            contract_return = greeter.caller().test()
            print("contract_return >>> ", contract_return)
            exe_time = time.time() - start_time
            print(exe_time)

            greeter2 = w3.eth.contract(
                address='0x9dcB4c2Ae3dF68052061809310B2922EC2471b18',
                abi='[{"name": "BidAdded", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidIncreased", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidRemoved", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}], "anonymous": false, "type": "event"}, {"name": "AuctionPaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionUnpaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionClosed", "inputs": [], "anonymous": false, "type": "event"}, {"name": "TokensMinted", "inputs": [{"name": "_minTokenId", "type": "uint256", "indexed": false}, {"name": "_mintedQty", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidPromoted", "inputs": [{"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_height", "type": "int128", "indexed": false}], "anonymous": false, "type": "event"}, {"stateMutability": "view", "type": "function", "name": "contractVersion", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 426}, {"stateMutability": "nonpayable", "type": "constructor", "inputs": [{"name": "_tokenContract", "type": "address"}, {"name": "_tokenType", "type": "uint256"}, {"name": "_minTokenId", "type": "uint256"}, {"name": "_maxTokenId", "type": "uint256"}, {"name": "_currencyAddress", "type": "address"}, {"name": "_minimumBid", "type": "uint256"}, {"name": "_startDate", "type": "uint256"}, {"name": "_endDate", "type": "uint256"}, {"name": "_extendingTime", "type": "uint256"}], "outputs": []}, {"stateMutability": "view", "type": "function", "name": "getBids", "inputs": [{"name": "_startBid", "type": "uint256"}, {"name": "_size", "type": "int128"}], "outputs": [{"name": "", "type": "uint256[2][1000]"}], "gas": 7002644}, {"stateMutability": "nonpayable", "type": "function", "name": "test", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 39924}, {"stateMutability": "view", "type": "function", "name": "contractOwner", "inputs": [], "outputs": [{"name": "", "type": "address"}], "gas": 2616}, {"stateMutability": "view", "type": "function", "name": "minimumBid", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2646}, {"stateMutability": "view", "type": "function", "name": "open", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 2676}, {"stateMutability": "view", "type": "function", "name": "paused", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 2706}, {"stateMutability": "view", "type": "function", "name": "startDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2736}, {"stateMutability": "view", "type": "function", "name": "endDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2766}, {"stateMutability": "view", "type": "function", "name": "extendedEnd", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2796}, {"stateMutability": "view", "type": "function", "name": "extendingTime", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2826}, {"stateMutability": "view", "type": "function", "name": "minTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2856}, {"stateMutability": "view", "type": "function", "name": "maxTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2886}, {"stateMutability": "view", "type": "function", "name": "tokenQty", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2916}, {"stateMutability": "view", "type": "function", "name": "bidCount", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2946}, {"stateMutability": "view", "type": "function", "name": "bidAverage", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 2976}, {"stateMutability": "view", "type": "function", "name": "highestBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3006}, {"stateMutability": "view", "type": "function", "name": "lowWinningBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3036}, {"stateMutability": "view", "type": "function", "name": "levels", "inputs": [{"name": "arg0", "type": "uint256"}, {"name": "arg1", "type": "uint256"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "value", "type": "uint256"}, {"name": "prevBid", "type": "uint256"}, {"name": "nextBid", "type": "uint256"}]}], "gas": 7507}, {"stateMutability": "view", "type": "function", "name": "bidders", "inputs": [{"name": "arg0", "type": "address"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "lastSequence", "type": "uint256"}]}], "gas": 3413}, {"stateMutability": "view", "type": "function", "name": "testCount", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 3126}]'
            )

            construct_txn2 = greeter2.functions.test().buildTransaction({
                'from': acct.address,
                'nonce': w3.eth.getTransactionCount(acct.address),
                'gas': 10000000,
                'gasPrice': 30000000000
                })

            signed2 = acct.signTransaction(construct_txn2)
            tx_hash2 = w3.eth.sendRawTransaction(signed2.rawTransaction)
            tx_receipt2 = w3.eth.waitForTransactionReceipt(tx_hash2)
            print(tx_receipt2)
            start_time2 = time.time()
            contract_return2 = greeter2.caller().test()
            print("contract_return 2 >>> ", contract_return2)
            exe_time2 = time.time() - start_time2
            print(exe_time2)

            exe_dict = {
                '4kb': exe_time,
                '56kb': exe_time2
            }

            writer.writerow(exe_dict)

            i += 1


if __name__ == "__main__":
    typer.run(main)
