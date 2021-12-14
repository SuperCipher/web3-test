from web3 import Web3
from web3 import HTTPProvider
import time
import csv
import typer
import deploy_56kb
import deploy_4kb


def prepare_contract_4kb(w3, funding_account, contract_address_str):
    greeter = w3.eth.contract(
        address=contract_address_str,
        abi='[{"name": "BidAdded", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidIncreased", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidRemoved", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}], "anonymous": false, "type": "event"}, {"name": "AuctionPaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionUnpaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionClosed", "inputs": [], "anonymous": false, "type": "event"}, {"name": "TokensMinted", "inputs": [{"name": "_minTokenId", "type": "uint256", "indexed": false}, {"name": "_mintedQty", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidPromoted", "inputs": [{"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_height", "type": "int128", "indexed": false}], "anonymous": false, "type": "event"}, {"stateMutability": "view", "type": "function", "name": "contractVersion", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 426}, {"stateMutability": "nonpayable", "type": "constructor", "inputs": [{"name": "_tokenContract", "type": "address"}, {"name": "_tokenType", "type": "uint256"}, {"name": "_minTokenId", "type": "uint256"}, {"name": "_maxTokenId", "type": "uint256"}, {"name": "_currencyAddress", "type": "address"}, {"name": "_minimumBid", "type": "uint256"}, {"name": "_startDate", "type": "uint256"}, {"name": "_endDate", "type": "uint256"}, {"name": "_extendingTime", "type": "uint256"}], "outputs": []}, {"stateMutability": "view", "type": "function", "name": "getBids", "inputs": [{"name": "_startBid", "type": "uint256"}, {"name": "_size", "type": "int128"}], "outputs": [{"name": "", "type": "uint256[2][10]"}], "gas": 76959}, {"stateMutability": "nonpayable", "type": "function", "name": "test", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 39924}, {"stateMutability": "nonpayable", "type": "function", "name": "foo1", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 516}, {"stateMutability": "nonpayable", "type": "function", "name": "foo2", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 546}, {"stateMutability": "nonpayable", "type": "function", "name": "foo3", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 576}, {"stateMutability": "nonpayable", "type": "function", "name": "foo4", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 606}, {"stateMutability": "nonpayable", "type": "function", "name": "foo5", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 636}, {"stateMutability": "nonpayable", "type": "function", "name": "foo6", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 666}, {"stateMutability": "nonpayable", "type": "function", "name": "foo7", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 696}, {"stateMutability": "nonpayable", "type": "function", "name": "foo8", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 726}, {"stateMutability": "nonpayable", "type": "function", "name": "foo9", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 756}, {"stateMutability": "nonpayable", "type": "function", "name": "foo10", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 786}, {"stateMutability": "view", "type": "function", "name": "getState", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 14496}, {"stateMutability": "view", "type": "function", "name": "getLowerBidBound", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 12575}, {"stateMutability": "view", "type": "function", "name": "getState0", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 14556}, {"stateMutability": "view", "type": "function", "name": "getLowerBidBound0", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 12635}, {"stateMutability": "view", "type": "function", "name": "getState1", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 14616}, {"stateMutability": "view", "type": "function", "name": "getLowerBidBound1", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 12695}, {"stateMutability": "view", "type": "function", "name": "getState2", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 14676}, {"stateMutability": "view", "type": "function", "name": "getLowerBidBound2", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 12755}, {"stateMutability": "view", "type": "function", "name": "getState3", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 14736}, {"stateMutability": "view", "type": "function", "name": "getLowerBidBound3", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 12815}, {"stateMutability": "view", "type": "function", "name": "contractOwner", "inputs": [], "outputs": [{"name": "", "type": "address"}], "gas": 3216}, {"stateMutability": "view", "type": "function", "name": "minimumBid", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3246}, {"stateMutability": "view", "type": "function", "name": "open", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 3276}, {"stateMutability": "view", "type": "function", "name": "paused", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 3306}, {"stateMutability": "view", "type": "function", "name": "startDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3336}, {"stateMutability": "view", "type": "function", "name": "endDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3366}, {"stateMutability": "view", "type": "function", "name": "extendedEnd", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3396}, {"stateMutability": "view", "type": "function", "name": "extendingTime", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3426}, {"stateMutability": "view", "type": "function", "name": "minTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3456}, {"stateMutability": "view", "type": "function", "name": "maxTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3486}, {"stateMutability": "view", "type": "function", "name": "tokenQty", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3516}, {"stateMutability": "view", "type": "function", "name": "bidCount", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3546}, {"stateMutability": "view", "type": "function", "name": "bidAverage", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 3576}, {"stateMutability": "view", "type": "function", "name": "highestBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3606}, {"stateMutability": "view", "type": "function", "name": "lowWinningBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3636}, {"stateMutability": "view", "type": "function", "name": "levels", "inputs": [{"name": "arg0", "type": "uint256"}, {"name": "arg1", "type": "uint256"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "value", "type": "uint256"}, {"name": "prevBid", "type": "uint256"}, {"name": "nextBid", "type": "uint256"}]}], "gas": 8107}, {"stateMutability": "view", "type": "function", "name": "bidders", "inputs": [{"name": "arg0", "type": "address"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "lastSequence", "type": "uint256"}]}], "gas": 4013}, {"stateMutability": "view", "type": "function", "name": "testCount", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 3726}]'
    )
    ### uncomment if you want to increament the number
    # construct_txn = greeter.functions.test().buildTransaction({
    #     'from': funding_account.address,
    #     'nonce': w3.eth.getTransactionCount(funding_account.address),
    #     'gas': 10000000,
    #     'gasPrice': 30000000000
    #     })
    #
    # signed = funding_account.signTransaction(construct_txn)
    # tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return greeter

def prepare_contract_56kb(w3, funding_account, contract_address_str):
    greeter = w3.eth.contract(
        address=contract_address_str,
        abi='[{"name": "BidAdded", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidIncreased", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidRemoved", "inputs": [{"name": "_operator", "type": "address", "indexed": true}, {"name": "_bidId", "type": "uint256", "indexed": true}], "anonymous": false, "type": "event"}, {"name": "AuctionPaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionUnpaused", "inputs": [], "anonymous": false, "type": "event"}, {"name": "AuctionClosed", "inputs": [], "anonymous": false, "type": "event"}, {"name": "TokensMinted", "inputs": [{"name": "_minTokenId", "type": "uint256", "indexed": false}, {"name": "_mintedQty", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "BidPromoted", "inputs": [{"name": "_bidId", "type": "uint256", "indexed": true}, {"name": "_height", "type": "int128", "indexed": false}], "anonymous": false, "type": "event"}, {"stateMutability": "nonpayable", "type": "function", "name": "test", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 39864}, {"stateMutability": "view", "type": "function", "name": "contractVersion", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 456}, {"stateMutability": "view", "type": "function", "name": "getState", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 13836}, {"stateMutability": "view", "type": "function", "name": "getLowerBidBound", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 11887}, {"stateMutability": "view", "type": "function", "name": "bidOutOfTheMoney", "inputs": [{"name": "_bidId", "type": "uint256"}], "outputs": [{"name": "", "type": "bool"}], "gas": 338950011956}, {"stateMutability": "nonpayable", "type": "constructor", "inputs": [{"name": "_tokenContract", "type": "address"}, {"name": "_tokenType", "type": "uint256"}, {"name": "_minTokenId", "type": "uint256"}, {"name": "_maxTokenId", "type": "uint256"}, {"name": "_currencyAddress", "type": "address"}, {"name": "_minimumBid", "type": "uint256"}, {"name": "_startDate", "type": "uint256"}, {"name": "_endDate", "type": "uint256"}, {"name": "_extendingTime", "type": "uint256"}], "outputs": []}, {"stateMutability": "view", "type": "function", "name": "getBids", "inputs": [{"name": "_startBid", "type": "uint256"}, {"name": "_size", "type": "int128"}], "outputs": [{"name": "", "type": "uint256[2][450]"}], "gas": 3147599}, {"stateMutability": "nonpayable", "type": "function", "name": "addBids", "inputs": [{"name": "_value", "type": "uint256"}, {"name": "_count", "type": "int128"}], "outputs": [], "gas": 59584200931319}, {"stateMutability": "nonpayable", "type": "function", "name": "increaseBids", "inputs": [{"name": "_bidIds", "type": "uint256[100]"}, {"name": "_value", "type": "uint256"}], "outputs": [], "gas": 93479253083964}, {"stateMutability": "nonpayable", "type": "function", "name": "removeBid", "inputs": [{"name": "_bidId", "type": "uint256"}], "outputs": [], "gas": 338950923012}, {"stateMutability": "nonpayable", "type": "function", "name": "batchRemoveBid", "inputs": [{"name": "_bidIds", "type": "uint256[100]"}], "outputs": [], "gas": 33895090925575}, {"stateMutability": "nonpayable", "type": "function", "name": "pauseAuction", "inputs": [], "outputs": [], "gas": 52939}, {"stateMutability": "nonpayable", "type": "function", "name": "resumeAuction", "inputs": [], "outputs": [], "gas": 37934}, {"stateMutability": "nonpayable", "type": "function", "name": "closeAuction", "inputs": [], "outputs": [], "gas": 26725}, {"stateMutability": "nonpayable", "type": "function", "name": "mintTokens", "inputs": [{"name": "_size", "type": "int128"}], "outputs": [], "gas": 50903782}, {"stateMutability": "nonpayable", "type": "function", "name": "promoteBid", "inputs": [{"name": "_bidId", "type": "uint256"}, {"name": "_height", "type": "int128"}], "outputs": [], "gas": 9046400034885}, {"stateMutability": "nonpayable", "type": "function", "name": "destroyContract", "inputs": [], "outputs": [], "gas": 45870}, {"stateMutability": "view", "type": "function", "name": "contractOwner", "inputs": [], "outputs": [{"name": "", "type": "address"}], "gas": 3006}, {"stateMutability": "view", "type": "function", "name": "minimumBid", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3036}, {"stateMutability": "view", "type": "function", "name": "open", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 3066}, {"stateMutability": "view", "type": "function", "name": "paused", "inputs": [], "outputs": [{"name": "", "type": "bool"}], "gas": 3096}, {"stateMutability": "view", "type": "function", "name": "startDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3126}, {"stateMutability": "view", "type": "function", "name": "endDate", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3156}, {"stateMutability": "view", "type": "function", "name": "extendedEnd", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3186}, {"stateMutability": "view", "type": "function", "name": "extendingTime", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3216}, {"stateMutability": "view", "type": "function", "name": "minTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3246}, {"stateMutability": "view", "type": "function", "name": "maxTokenId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3276}, {"stateMutability": "view", "type": "function", "name": "tokenQty", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3306}, {"stateMutability": "view", "type": "function", "name": "bidCount", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3336}, {"stateMutability": "view", "type": "function", "name": "bidAverage", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 3366}, {"stateMutability": "view", "type": "function", "name": "highestBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3396}, {"stateMutability": "view", "type": "function", "name": "lowWinningBidId", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 3426}, {"stateMutability": "view", "type": "function", "name": "levels", "inputs": [{"name": "arg0", "type": "uint256"}, {"name": "arg1", "type": "uint256"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "value", "type": "uint256"}, {"name": "prevBid", "type": "uint256"}, {"name": "nextBid", "type": "uint256"}]}], "gas": 7897}, {"stateMutability": "view", "type": "function", "name": "bidders", "inputs": [{"name": "arg0", "type": "address"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "lastSequence", "type": "uint256"}]}], "gas": 3803}, {"stateMutability": "view", "type": "function", "name": "testCount", "inputs": [], "outputs": [{"name": "", "type": "int128"}], "gas": 3516}]'
    )

    # construct_txn2 = greeter2.functions.test().buildTransaction({
    #     'from': acct.address,
    #     'nonce': w3.eth.getTransactionCount(acct.address),
    #     'gas': 10000000,
    #     'gasPrice': 30000000000
    #     })
    #
    # signed2 = acct.signTransaction(construct_txn2)
    # tx_hash2 = w3.eth.sendRawTransaction(signed2.rawTransaction)
    # tx_receipt2 = w3.eth.waitForTransactionReceipt(tx_hash2)
    return greeter


def main(iteration: int = typer.Argument(1)):

    with open('exe_time.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            '4kb',
            '56kb'
        ])
        writer.writeheader()

        w3 = Web3(HTTPProvider(
            "http://localhost:8545"))
        blocks = w3.eth.block_number
        print("Blocknumber : ", blocks)

        w3 = Web3(HTTPProvider("http://localhost:8545"))
        print("Is connected? : ", w3.isConnected())
        acct = w3.eth.account.privateKeyToAccount(
            '7b771f71f1c861710dc8e214f426fed67a3b538c3b835d66015c8a08533ca68b')
        print("Account address : ", acct.address)

        i = 1
        while(i <= iteration):
            print("--------------------------------------" + "Iterations: "
                + str(i) + "--------------------------------------")
            contract_address_str_4kb = deploy_4kb()
            print("contract_address_str_4kb", contract_address_str_4kb)
            greeter = prepare_contract_4kb(w3,acct, contract_address_str_4kb)

            ### benchmark start
            start_time = time.time()
            contract_result = greeter.caller().test()
            exe_time = time.time() - start_time
            ### benchmark stop

            print("Contract result", contract_result)
            print("Execute time : ", exe_time)


            contract_address_str_56kb = deploy_56kb()
            print("contract_address_str_56kb : ",contract_address_str_56kb)
            greeter2 = prepare_contract_56kb(w3,acct, contract_address_str_56kb)

            ### benchmark start
            start_time2 = time.time()
            contract_result2 = greeter2.caller().test()
            exe_time2 = time.time() - start_time2
            ### benchmark stop

            print("Contract result2 :", contract_result2)
            print("Execute time : ", exe_time2)

            exe_dict = {
                '4kb': exe_time,
                '56kb': exe_time2
            }

            writer.writerow(exe_dict)

            i += 1


if __name__ == "__main__":
    typer.run(main)
