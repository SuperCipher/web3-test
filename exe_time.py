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
                "http://10.66.67.6:8545"))
            blocks = w3.eth.block_number
            print("blocknumber >>> ", blocks)
            print("--------------------------------------" + "Iterations: " + str(i) + "--------------------------------------")
            greeter = w3.eth.contract(
                address='0xE9e0dE58870FF5c4B21272cdF1Ec30eF57Da00B6',
                abi='[{"name": "BidAdded", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidIncreased", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidRemoved", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}], "anonymous": false, "type": "event"}, {"name": "AuctionPaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionUnpaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionClosed", "inputs": [], "anonymous": false, "type": "event"}, {"name": "TokensMinted", "inputs": [{"name": "_minTokenId", "type": "uint256", "indexed": false}, {"name": "_mintedQty", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidPromoted", "inputs": [{"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_height", "type": "int128", "indexed": false}], "anonymous": false, "type": "event"}, {"stateMutability": "view", "type": "function", "name": "contractVersion", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 426}, {"stateMutability": "view", "type": "function", "name": "getState", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 13776}, {"stateMutability": "nonpayable", "type": "function", "name": "test", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 39924}, {"stateMutability": "view", "type": "function", "name": "getLowerBidBound", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 11887}, {"stateMutability": "view", "type": "function", "name": "bidOutOfTheMoney", "inputs": [{"name": "_bidId", "type": "uint256"}], "outputs": [{"name": "", "type": "bool"}], "gas": 338950011956}, {"stateMutability": "nonpayable", "type": "constructor", "inputs": [{"name": "_tokenContract", "type": "address"}, {"name": "_tokenType", "type": "uint256"}, {"name": "_minTokenId", "type": "uint256"}, {"name": "_maxTokenId", "type": "uint256"}, {"name": "_currencyAddress", "type": "address"}, {"name": "_minimumBid", "type": "uint256"}, {"name": "_startDate", "type": "uint256"}, {"name": "_endDate", "type": "uint256"}, {"name": "_extendingTime", "type": "uint256"}], "outputs": []}, {"stateMutability": "view", "type": "function", "name": "getBids", "inputs": [{"name": "_startBid", "type": "uint256"}, {"name": "_size", "type": "int128"}], "outputs": [{"name": "", "type": "uint256[2][400]"}], "gas": 2798067}, {"stateMutability": "nonpayable", "type": "function", "name": "addBids", "inputs": [{"name": "_value", "type": "uint256"}, {"name": "_count", "type": "int128"}], "outputs": [], "gas": 59584200928229}, {"stateMutability": "nonpayable", "type": "function", "name": "increaseBids", "inputs": [{"name": "_bidIds", "type": "uint256[100]"}, {"name": "_value", "type": "uint256"}], "outputs": [], "gas": 93479253083874}, {"stateMutability": "nonpayable", "type": "function", "name": "removeBid", "inputs": [{"name": "_bidId", "type": "uint256"}], "outputs": [], "gas": 338950922982}, {"stateMutability": "nonpayable", "type": "function", "name": "batchRemoveBid", "inputs": [{"name": "_bidIds", "type": "uint256[100]"}], "outputs": [], "gas": 33895090925545}, {"stateMutability": "nonpayable", "type": "function", "name": "pauseAuction", "inputs": [], "outputs": [], "gas": 52909}, {"stateMutability": "nonpayable", "type": "function", "name": "resumeAuction", "inputs": [], "outputs": [], "gas": 37904}, {"stateMutability": "nonpayable", "type": "function", "name": "closeAuction", "inputs": [], "outputs": [], "gas": 26725}, {"stateMutability": "nonpayable", "type": "function", "name": "mintTokens", "inputs": [{"name": "_size", "type": "int128"}], "outputs": [], "gas": 50903752}, {"stateMutability": "nonpayable", "type": "function", "name": "promoteBid", "inputs": [{"name": "_bidId", "type": "uint256"}, {"name": "_height", "type": "int128"}], "outputs": [], "gas": 9046400034885}, {"stateMutability": "nonpayable", "type": "function", "name": "destroyContract", "inputs": [], "outputs": [], "gas": 45840}, {"stateMutability": "view", "type": "function", "name": "contractOwner", "inputs": [], "outputs": [{"name": "", "type": "address"}], "gas": 3006}, {"stateMutability": "view", "type": "function", "name": "minimumBid", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3036}, {"stateMutability": "view", "type": "function", "name": "open", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 3066}, {"stateMutability": "view", "type": "function", "name": "paused", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 3096}, {"stateMutability": "view", "type": "function", "name": "startDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3126}, {"stateMutability": "view", "type": "function", "name": "endDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3156}, {"stateMutability": "view", "type": "function", "name": "extendedEnd", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3186}, {"stateMutability": "view", "type": "function", "name": "extendingTime", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3216}, {"stateMutability": "view", "type": "function", "name": "minTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3246}, {"stateMutability": "view", "type": "function", "name": "maxTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3276}, {"stateMutability": "view", "type": "function", "name": "tokenQty", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3306}, {"stateMutability": "view", "type": "function", "name": "bidCount", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3336}, {"stateMutability": "view", "type": "function", "name": "bidAverage", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 3366}, {"stateMutability": "view", "type": "function", "name": "highestBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3396}, {"stateMutability": "view", "type": "function", "name": "lowWinningBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3426}, {"stateMutability": "view", "type": "function", "name": "levels", "inputs": [{"name": "arg0", "type": "uint256"}, {"name": "arg1", "type": "uint256"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "value", "type": "uint256"}, {"name": "prevBid", "type": "uint256"}, {"name": "nextBid", "type": "uint256"}]}], "gas": 7897}, {"stateMutability": "view", "type": "function", "name": "bidders", "inputs": [{"name": "arg0", "type": "address"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "lastSequence", "type": "uint256"}]}], "gas": 3803}, {"stateMutability": "view", "type": "function", "name": "testCount", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 3516}]'
            )

            start_time = time.time()
            contract_return = greeter.functions.test().call()
            print("contract_return >>> ", contract_return)
            exe_time = time.time() - start_time
            print(exe_time)


            greeter2 = w3.eth.contract(
                address='0x1Bb4A26115F8F24af48b23382549fF38153CF41D',
                abi='[{"name": "BidAdded", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidIncreased", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidRemoved", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}], "anonymous": false, "type": "event"}, {"name": "AuctionPaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionUnpaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionClosed", "inputs": [], "anonymous": false, "type": "event"}, {"name": "TokensMinted", "inputs": [{"name": "_minTokenId", "type": "uint256", "indexed": false}, {"name": "_mintedQty", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidPromoted", "inputs": [{"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_height", "type": "int128", "indexed": false}], "anonymous": false, "type": "event"}, {"stateMutability": "view", "type": "function", "name": "contractVersion", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 426}, {"stateMutability": "view", "type": "function", "name": "getState", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 13776}, {"stateMutability": "nonpayable", "type": "function", "name": "test", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 39924}, {"stateMutability": "view", "type": "function", "name": "getLowerBidBound", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 11887}, {"stateMutability": "view", "type": "function", "name": "bidOutOfTheMoney", "inputs": [{"name": "_bidId", "type": "uint256"}], "outputs": [{"name": "", "type": "bool"}], "gas": 338950011956}, {"stateMutability": "nonpayable", "type": "constructor", "inputs": [{"name": "_tokenContract", "type": "address"}, {"name": "_tokenType", "type": "uint256"}, {"name": "_minTokenId", "type": "uint256"}, {"name": "_maxTokenId", "type": "uint256"}, {"name": "_currencyAddress", "type": "address"}, {"name": "_minimumBid", "type": "uint256"}, {"name": "_startDate", "type": "uint256"}, {"name": "_endDate", "type": "uint256"}, {"name": "_extendingTime", "type": "uint256"}], "outputs": []}, {"stateMutability": "view", "type": "function", "name": "getBids", "inputs": [{"name": "_startBid", "type": "uint256"}, {"name": "_size", "type": "int128"}], "outputs": [{"name": "", "type": "uint256[2][400]"}], "gas": 2798067}, {"stateMutability": "nonpayable", "type": "function", "name": "addBids", "inputs": [{"name": "_value", "type": "uint256"}, {"name": "_count", "type": "int128"}], "outputs": [], "gas": 59584200928229}, {"stateMutability": "nonpayable", "type": "function", "name": "increaseBids", "inputs": [{"name": "_bidIds", "type": "uint256[100]"}, {"name": "_value", "type": "uint256"}], "outputs": [], "gas": 93479253083874}, {"stateMutability": "nonpayable", "type": "function", "name": "removeBid", "inputs": [{"name": "_bidId", "type": "uint256"}], "outputs": [], "gas": 338950922982}, {"stateMutability": "nonpayable", "type": "function", "name": "batchRemoveBid", "inputs": [{"name": "_bidIds", "type": "uint256[100]"}], "outputs": [], "gas": 33895090925545}, {"stateMutability": "nonpayable", "type": "function", "name": "pauseAuction", "inputs": [], "outputs": [], "gas": 52909}, {"stateMutability": "nonpayable", "type": "function", "name": "resumeAuction", "inputs": [], "outputs": [], "gas": 37904}, {"stateMutability": "nonpayable", "type": "function", "name": "closeAuction", "inputs": [], "outputs": [], "gas": 26725}, {"stateMutability": "nonpayable", "type": "function", "name": "mintTokens", "inputs": [{"name": "_size", "type": "int128"}], "outputs": [], "gas": 50903752}, {"stateMutability": "nonpayable", "type": "function", "name": "promoteBid", "inputs": [{"name": "_bidId", "type": "uint256"}, {"name": "_height", "type": "int128"}], "outputs": [], "gas": 9046400034885}, {"stateMutability": "nonpayable", "type": "function", "name": "destroyContract", "inputs": [], "outputs": [], "gas": 45840}, {"stateMutability": "view", "type": "function", "name": "contractOwner", "inputs": [], "outputs": [{"name": "", "type": "address"}], "gas": 3006}, {"stateMutability": "view", "type": "function", "name": "minimumBid", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3036}, {"stateMutability": "view", "type": "function", "name": "open", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 3066}, {"stateMutability": "view", "type": "function", "name": "paused", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 3096}, {"stateMutability": "view", "type": "function", "name": "startDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3126}, {"stateMutability": "view", "type": "function", "name": "endDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3156}, {"stateMutability": "view", "type": "function", "name": "extendedEnd", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3186}, {"stateMutability": "view", "type": "function", "name": "extendingTime", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3216}, {"stateMutability": "view", "type": "function", "name": "minTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3246}, {"stateMutability": "view", "type": "function", "name": "maxTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3276}, {"stateMutability": "view", "type": "function", "name": "tokenQty", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3306}, {"stateMutability": "view", "type": "function", "name": "bidCount", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3336}, {"stateMutability": "view", "type": "function", "name": "bidAverage", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 3366}, {"stateMutability": "view", "type": "function", "name": "highestBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3396}, {"stateMutability": "view", "type": "function", "name": "lowWinningBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3426}, {"stateMutability": "view", "type": "function", "name": "levels", "inputs": [{"name": "arg0", "type": "uint256"}, {"name": "arg1", "type": "uint256"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "value", "type": "uint256"}, {"name": "prevBid", "type": "uint256"}, {"name": "nextBid", "type": "uint256"}]}], "gas": 7897}, {"stateMutability": "view", "type": "function", "name": "bidders", "inputs": [{"name": "arg0", "type": "address"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "lastSequence", "type": "uint256"}]}], "gas": 3803}, {"stateMutability": "view", "type": "function", "name": "testCount", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 3516}]'
            )

            start_time2 = time.time()
            contract_return = greeter2.functions.test().call()
            print("contract_return >>> ", contract_return)
            exe_time2 = time.time() - start_time2
            print(exe_time2)

            exe_dict = {
                '4kb':exe_time,
                '56kb':exe_time2
            }

            writer.writerow(exe_dict)

            i+=1

if __name__ == "__main__":
    typer.run(main)

