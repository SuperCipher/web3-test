from vyper.interfaces import ERC20


struct Bid:
    value: uint256
    prevBid: uint256 # Bid with lower or equal value to current bid
    nextBid: uint256 # Bid with greater or equal value to current bid

struct Bidder:
    lastSequence: uint256


# External Contracts
interface ABC:
    def mintNonFungibleToken(
            _tokenType: uint256,
            _to: address[100],
            _indexes: uint256[100]): payable


########### Events ###############
event BidAdded:
    _operator: indexed(address)
    _bidId: indexed(uint256)
    _value: uint256

event BidIncreased:
    _operator: indexed(address)
    _bidId: indexed(uint256)
    _value: uint256

event BidRemoved:
    _operator: indexed(address)
    _bidId: indexed(uint256)

event AuctionPaused: pass

event AuctionUnpaused: pass

event AuctionClosed: pass

event TokensMinted:
    _minTokenId: uint256
    _mintedQty: uint256

event BidPromoted:
    _bidId: indexed(uint256)
    _height: int128


CONTRACT_VERSION : constant(uint256) = 1000001

BASE_BID_ID: constant(uint256) = 0
DEEPEST_LEVEL: constant(int128) = 0

# ABC token
MAX_BATCH_SIZE: constant(uint256) = 100

# Bid retrieval batch size
BID_RETRIEVAL_BATCH_SIZE: constant(uint256) = 35

# Contract configuration
MAX_AUCTION_ITEMS: constant(uint256) = 5000000
MAX_BID_QTY: constant(uint256) = 5000000 * 10
MAX_WHITELIST_OPS: constant(uint256) = 10
MAX_LEVEL: constant(int128) = 6
# promote probability = 2 ^ PROMOTION_CONSTANT
PROMOTION_CONSTANT: constant(int128) = 3
UNPROMOTE_PROB: constant(int128) = (2 ** 3) - 1

PENDING_STATE: constant(uint256) = 1
PAUSED_STATE: constant(uint256) = 2
OPEN_STATE: constant(uint256) = 3
SUDDEN_DEATH_STATE: constant(uint256) = 4
CLOSED_STATE: constant(uint256) = 5


contractOwner: public(address)
currencyAddress: address
minimumBid: public(uint256)

open: public(bool)
paused: public(bool)
startDate: public(uint256)
endDate: public(uint256)
extendedEnd: public(uint256)
extendingTime: public(uint256)

minTokenId: public(uint256)
maxTokenId: public(uint256)
# Total number of tokenIds actually in the tokenIds list.
tokenQty: public(uint256)

bidCount: public(uint256)
bidAverage: public(int128)
highestBidId: public(uint256)
lowWinningBidId: public(uint256)

levels: public(HashMap[uint256, Bid[MAX_LEVEL]])

# bidders: public(HashMap(address, Bidder))  # Map between address and Bidder object
bidders: public(HashMap[address, Bidder])  # Map between address and Bidder object

tokenContract: address
tokenType: uint256
testCount: public(int128)

@external
@view
def contractVersion() -> uint256:
    """
    auction.vy -    Auction Contract for Ordered Sequential Non-Fungible Tokens
                    Given a descending ordered (by value) list of tokens with unique ids,
                    this auction contract will assign the top bids to the most valuable
                    tokens when the auction ends.

                    ITEMS - Tokens must be in our ERC-1155 contract and be optioned to this
                    auction contract. (Or should the auction mint the tokens? Probably so.)
                    List of items should be in descending order of value and one item may
                    only be in the list once.

                    KYC - Bids must come from wallets that are in a whitelist managed by
                    a KYCProvider.

                    KYC_CANCEL - Bidders removed from the whitelist have all their bids
                    'cancelled'. They may no longer add or update bids. Their bids will not
                    be matched with tokens should they be 'in the money' post auction.
                    (WARNING - if we don't remove the bids right away this could mess up our
                    'in the money' calculations for future bids and cancellation. Probably
                    should disallow kyc cancellations for our initial implementation and
                    perhaps add this later.)

                    MULTI_BID - Bidders may create multiple bids in order to bid on
                    multiple tokens.

                    ETHER - All bids are denominated in Ethereum wei.

                    SAME_VALID - Bids can be for the same bid value as a pre-existing bid
                    as long as the number of active bids is lower than the number of
                    available tokens OR the bid value is higher than the bid value of the
                    current lowest winning bid.

                    INCREASE - Bidders may update existing bids by increasing their value.

                    CANCELLOSER - Bidders may cancel existing bids only if their bid is
                    'out of the money'.

                    FAIR_PRECEDENCE - Pre-existing bids of the same bid value have
                    precedence over new bids of the same value.

                    TIMED_AUCTION - Bidding may commence on or after 'start' time so long
                    as 'pause' is False, and normal bidding ends upon 'end' time. Contract
                    owner may pause the bidding at any time.

                    FINAL_AUCTION - Final auction bidding model is TBD. Sudden death
                    extended bids from a more restricted set of bidding wallets is anticipated.

                    WIN_MATCH - Upon auction completion, the top bids will be matched to
                    their respective most valuable tokens.

                    LOSER_REFUND - All non-matched bids will be eligible for refund
                    requests from their bidding wallets. Owner can push refunds optionally.

                    DESTRUCT - After the auction is completed, owner may self destruct the
                    contract. Remaining value will be returned to auction owner or wallet
                    designated by owner.
    """
    return CONTRACT_VERSION


@external
def __init__(
    _tokenContract: address,
    _tokenType: uint256,
    _minTokenId: uint256,
    _maxTokenId: uint256,
    _currencyAddress: address,
    _minimumBid: uint256,
    _startDate: uint256,
    _endDate: uint256,
    _extendingTime: uint256
):
    """
    _tokenContract - address of token contract.

    _tokenType - type of ABC token.

    _minTokneId - an index of token with minimum sequence number that make
    it be the most valuable token of the auction.

    _minTokneId - an index of token with maximum sequence number that make
    it be the least valuable token of the auction.

    _currencyAddress - ERC20 contract address that going to be main
    currency of the auction contract

    _minimumBid - Minimium acceptable bid of the acution

    _startDate - the datetime when the auction can accept bids.

    _endDate - the datetime when the auction ends normal bidding activities.

    _extendingTime - the timedelta to extend the auction end time
    """
    assert _maxTokenId >= _minTokenId, "Max token id is less than minimum one"
    assert block.timestamp < _endDate, \
           "End of the auction is earlier than current time"
    assert _startDate < _endDate, \
           "End of the auction is earlier than its start date"
    quantity: uint256 = _maxTokenId - _minTokenId + 1
    assert quantity <= MAX_AUCTION_ITEMS, \
           "Total quantity of tokens exceeded maximum allowance"

    # Check currency address is ERC20 contract

    self.minTokenId = _minTokenId
    self.maxTokenId = _maxTokenId

    self.tokenContract = _tokenContract
    self.tokenType = _tokenType

    self.tokenQty = quantity
    self.bidAverage = 0

    self.contractOwner = msg.sender
    self.currencyAddress = _currencyAddress
    self.minimumBid = _minimumBid

    self.open = True
    self.startDate = _startDate
    self.endDate = _endDate
    self.extendedEnd = _endDate
    self.extendingTime = _extendingTime
    self.testCount = 0

@external
def layer2call(arg1: int128) -> int128:
    return arg1

@external
@view
def getBids(
       _startBid: uint256,
       _size: int128) -> uint256[2][BID_RETRIEVAL_BATCH_SIZE]:
   assert _size > 0

   # bids: uint256[2][BID_RETRIEVAL_BATCH_SIZE]
   bids: uint256[2][BID_RETRIEVAL_BATCH_SIZE] = empty(uint256[2][BID_RETRIEVAL_BATCH_SIZE])
   bid: Bid = self.levels[_startBid][DEEPEST_LEVEL]
   bidId: uint256 = _startBid

   for i in range(BID_RETRIEVAL_BATCH_SIZE):
       if bidId == 0 or i >= _size:
           break
       bid = self.levels[bidId][DEEPEST_LEVEL]
       bids[i] = [bidId, bid.value]
       bidId = bid.prevBid
   return bids

@external
def test() -> int128:
    self.testCount += 1
    return self.testCount


@external
def foo1() -> bool:
    return True


@external
def foo2() -> bool:
    return True


@external
def foo3() -> bool:
    return True


@external
def foo4() -> bool:
    return True


@external
def foo5() -> bool:
    return True


@external
def foo6() -> bool:
    return True


@external
def foo7() -> bool:
    return True


@external
def foo8() -> bool:
    return True


@external
def foo9() -> bool:
    return True


@external
def foo10() -> bool:
    return True

@internal
@view
def getLevel(_bidId: uint256, _sender: address, _randSeed: uint256) -> int128:
    level: int128 = 0
    xor_result: uint256 = bitwise_xor(
        bitwise_xor(
            bitwise_xor(
                convert(_sender, uint256), _bidId),
                convert(block.prevhash, uint256)
        ),
        _randSeed
    )
    random: uint256 = convert(keccak256(convert(xor_result, bytes32)), uint256)
    for i in range(MAX_LEVEL - 1):
        if bitwise_and(
                random,
                shift(UNPROMOTE_PROB, PROMOTION_CONSTANT * i)
                ) == 0:
            level += 1
        else:
            break

    return level



#### Auction utilities ####

@internal
@view
def getBidId(_bidder: address, _bidSequence: uint256) -> uint256:
    msbs: uint256 = shift(convert(_bidder, uint256), 96)
    bidId: uint256 = bitwise_or(msbs, _bidSequence)

    return bidId


@internal
def getNewBidId(_bidder: address) -> uint256:
    self.bidders[_bidder].lastSequence += 1
    return self.getBidId(_bidder, self.bidders[_bidder].lastSequence)


@internal
@view
def _getState() -> uint256:
    if block.timestamp < self.extendedEnd and self.open == True:
        if self.paused:
            return PAUSED_STATE
        else:
            if block.timestamp >= self.startDate:
                if block.timestamp < self.endDate - self.extendingTime:
                    return OPEN_STATE
                else:
                    return SUDDEN_DEATH_STATE
            else:
                return PENDING_STATE
    else:
        return CLOSED_STATE


@external
@view
def getState() -> uint256:
    return self._getState()



##### Assertion ####

@internal
@view
def bidOwner(_sender: address, _bidId: uint256) -> bool:
    return shift(_bidId, -96) == convert(_sender, uint256)


@internal
@view
def _getNewAverageChangingN(
        old_mean: int128,
        _value: uint256,
        temp_bid_count: uint256,
        _count: int128) -> int128:
    return old_mean + ((convert(_value, int128) * _count) - (old_mean * _count)) / (convert(temp_bid_count, int128) + _count)


@internal
@view
def _getNewAverageConstN(
        old_mean: int128,
        token_qty: uint256,
        _value: uint256,
        _count: int128) -> int128:
    value_pushed: uint256  = 0
    temp_bid_id: uint256 = self.lowWinningBidId
    for i in range(MAX_BATCH_SIZE):
        if i >= _count:
            break
#        value_pushed += self.levels[DEEPEST_LEVEL][temp_bid_id].value
#        temp_bid_id = self.levels[DEEPEST_LEVEL][temp_bid_id].nextBid
        value_pushed += self.levels[temp_bid_id][DEEPEST_LEVEL].value
        temp_bid_id = self.levels[temp_bid_id][DEEPEST_LEVEL].nextBid
    return old_mean + (
            (convert(_value, int128) * _count - convert(value_pushed, int128)) / convert(token_qty, int128))


@internal
def _updateBidsAverage(_value: uint256, _count: int128):
   old_av: int128 = self.bidAverage
   temp_bid_count: uint256 = self.bidCount
   temp_token_qty: uint256 = self.tokenQty
   # Total amount of bids in the money will be increased
   if ( (convert(temp_bid_count, int128) + _count) <=
           convert(temp_token_qty, int128) ):
       self.bidAverage = self._getNewAverageChangingN(
           old_av,
           _value,
           temp_bid_count,
           _count
       )
   else:
       # Total amount of bids will be PARTIALLY increased
       if ( temp_bid_count < temp_token_qty ):
           amount_diff: int128 = (convert(temp_bid_count, int128) + _count) - convert(temp_token_qty, int128)
           temp_mean: int128 = self._getNewAverageChangingN(
                   old_av,
                   _value,
                   temp_bid_count,
                   _count - amount_diff
           )
           self.bidAverage = self._getNewAverageConstN(
               temp_mean,
               temp_token_qty,
               _value,
               amount_diff
           )
       # Total amount of bids in the money will NOT be increased
       else:
           self.bidAverage = self._getNewAverageConstN(
               old_av,
               temp_token_qty,
               _value,
               _count
           )


@internal
@view
def _getLowerBidBound() -> int128:
    # Comparison is by date because we are out control on the Paused state
    if block.timestamp < self.endDate - self.extendingTime:
#        return convert(
#                self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value,
#                int128)
        return convert(
            self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value,
            int128)
    return self.bidAverage


@external
@view
def getLowerBidBound() -> int128:
    return self._getLowerBidBound()


@internal
@view
def validBidValue(_value: uint256) -> bool:
    if self.minimumBid > _value:
        return False
    if self._getState() == OPEN_STATE:
#        return (self.bidCount < self.tokenQty or
#               _value > self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value)
        return (self.bidCount < self.tokenQty or
               _value > self.levels[self.lowWinningBidId][DEEPEST_LEVEL].value)
    if self._getState() == SUDDEN_DEATH_STATE:
        return convert(_value, int128) > self.bidAverage
    return False


@internal
@view
def _bidOutOfTheMoney(_bidId : uint256) -> bool:
   # currentBid: Bid = self.levels[DEEPEST_LEVEL][self.lowWinningBidId]
#    value: uint256 = self.levels[DEEPEST_LEVEL][_bidId].value
    # currentBid: Bid = self.levels[self.lowWinningBidId]
    currentBid: Bid = self.levels[self.lowWinningBidId][DEEPEST_LEVEL]
    value: uint256 = self.levels[_bidId][DEEPEST_LEVEL].value
    result: bool = False

    if currentBid.value == value:
        for i in range(MAX_BID_QTY):
            if currentBid.prevBid == _bidId:
                result = True
                break
            if currentBid.value != value: break
#            currentBid = self.levels[DEEPEST_LEVEL][currentBid.prevBid]
            currentBid = self.levels[currentBid.prevBid][DEEPEST_LEVEL]
        return result
    else:
        return currentBid.value > value


@internal
@view
def getLevel0(_bidId: uint256, _sender: address, _randSeed: uint256) -> int128:
    level: int128 = 0
    xor_result: uint256 = bitwise_xor(
        bitwise_xor(
            bitwise_xor(
                convert(_sender, uint256), _bidId),
                convert(block.prevhash, uint256)
        ),
        _randSeed
    )
    random: uint256 = convert(keccak256(convert(xor_result, bytes32)), uint256)
    for i in range(MAX_LEVEL - 1):
        if bitwise_and(
                random,
                shift(UNPROMOTE_PROB, PROMOTION_CONSTANT * i)
                ) == 0:
            level += 1
        else:
            break

    return level



#### Auction utilities ####

@internal
@view
def getBidId0(_bidder: address, _bidSequence: uint256) -> uint256:
    msbs: uint256 = shift(convert(_bidder, uint256), 96)
    bidId: uint256 = bitwise_or(msbs, _bidSequence)

    return bidId


@internal
def getNewBidId0(_bidder: address) -> uint256:
    self.bidders[_bidder].lastSequence += 1
    return self.getBidId(_bidder, self.bidders[_bidder].lastSequence)


@internal
@view
def _getState0() -> uint256:
    if block.timestamp < self.extendedEnd and self.open == True:
        if self.paused:
            return PAUSED_STATE
        else:
            if block.timestamp >= self.startDate:
                if block.timestamp < self.endDate - self.extendingTime:
                    return OPEN_STATE
                else:
                    return SUDDEN_DEATH_STATE
            else:
                return PENDING_STATE
    else:
        return CLOSED_STATE


@external
@view
def getState0() -> uint256:
    return self._getState()



##### Assertion ####

@internal
@view
def bidOwner0(_sender: address, _bidId: uint256) -> bool:
    return shift(_bidId, -96) == convert(_sender, uint256)


@internal
@view
def _getNewAverageChangingN0(
        old_mean: int128,
        _value: uint256,
        temp_bid_count: uint256,
        _count: int128) -> int128:
    return old_mean + ((convert(_value, int128) * _count) - (old_mean * _count)) / (convert(temp_bid_count, int128) + _count)


@internal
@view
def _getNewAverageConstN0(
        old_mean: int128,
        token_qty: uint256,
        _value: uint256,
        _count: int128) -> int128:
    value_pushed: uint256  = 0
    temp_bid_id: uint256 = self.lowWinningBidId
    for i in range(MAX_BATCH_SIZE):
        if i >= _count:
            break
#        value_pushed += self.levels[DEEPEST_LEVEL][temp_bid_id].value
#        temp_bid_id = self.levels[DEEPEST_LEVEL][temp_bid_id].nextBid
        value_pushed += self.levels[temp_bid_id][DEEPEST_LEVEL].value
        temp_bid_id = self.levels[temp_bid_id][DEEPEST_LEVEL].nextBid
    return old_mean + (
            (convert(_value, int128) * _count - convert(value_pushed, int128)) / convert(token_qty, int128))


@internal
def _updateBidsAverage0(_value: uint256, _count: int128):
   old_av: int128 = self.bidAverage
   temp_bid_count: uint256 = self.bidCount
   temp_token_qty: uint256 = self.tokenQty
   # Total amount of bids in the money will be increased
   if ( (convert(temp_bid_count, int128) + _count) <=
           convert(temp_token_qty, int128) ):
       self.bidAverage = self._getNewAverageChangingN(
           old_av,
           _value,
           temp_bid_count,
           _count
       )
   else:
       # Total amount of bids will be PARTIALLY increased
       if ( temp_bid_count < temp_token_qty ):
           amount_diff: int128 = (convert(temp_bid_count, int128) + _count) - convert(temp_token_qty, int128)
           temp_mean: int128 = self._getNewAverageChangingN(
                   old_av,
                   _value,
                   temp_bid_count,
                   _count - amount_diff
           )
           self.bidAverage = self._getNewAverageConstN(
               temp_mean,
               temp_token_qty,
               _value,
               amount_diff
           )
       # Total amount of bids in the money will NOT be increased
       else:
           self.bidAverage = self._getNewAverageConstN(
               old_av,
               temp_token_qty,
               _value,
               _count
           )


@internal
@view
def _getLowerBidBound0() -> int128:
    # Comparison is by date because we are out control on the Paused state
    if block.timestamp < self.endDate - self.extendingTime:
#        return convert(
#                self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value,
#                int128)
        return convert(
            self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value,
            int128)
    return self.bidAverage


@external
@view
def getLowerBidBound0() -> int128:
    return self._getLowerBidBound()


@internal
@view
def validBidValue0(_value: uint256) -> bool:
    if self.minimumBid > _value:
        return False
    if self._getState() == OPEN_STATE:
#        return (self.bidCount < self.tokenQty or
#               _value > self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value)
        return (self.bidCount < self.tokenQty or
               _value > self.levels[self.lowWinningBidId][DEEPEST_LEVEL].value)
    if self._getState() == SUDDEN_DEATH_STATE:
        return convert(_value, int128) > self.bidAverage
    return False


@internal
@view
def _bidOutOfTheMoney0(_bidId : uint256) -> bool:
   # currentBid: Bid = self.levels[DEEPEST_LEVEL][self.lowWinningBidId]
#    value: uint256 = self.levels[DEEPEST_LEVEL][_bidId].value
    # currentBid: Bid = self.levels[self.lowWinningBidId]
    currentBid: Bid = self.levels[self.lowWinningBidId][DEEPEST_LEVEL]
    value: uint256 = self.levels[_bidId][DEEPEST_LEVEL].value
    result: bool = False

    if currentBid.value == value:
        for i in range(MAX_BID_QTY):
            if currentBid.prevBid == _bidId:
                result = True
                break
            if currentBid.value != value: break
#            currentBid = self.levels[DEEPEST_LEVEL][currentBid.prevBid]
            currentBid = self.levels[currentBid.prevBid][DEEPEST_LEVEL]
        return result
    else:
        return currentBid.value > value

@internal
@view
def getLevel1(_bidId: uint256, _sender: address, _randSeed: uint256) -> int128:
    level: int128 = 0
    xor_result: uint256 = bitwise_xor(
        bitwise_xor(
            bitwise_xor(
                convert(_sender, uint256), _bidId),
                convert(block.prevhash, uint256)
        ),
        _randSeed
    )
    random: uint256 = convert(keccak256(convert(xor_result, bytes32)), uint256)
    for i in range(MAX_LEVEL - 1):
        if bitwise_and(
                random,
                shift(UNPROMOTE_PROB, PROMOTION_CONSTANT * i)
                ) == 0:
            level += 1
        else:
            break

    return level



#### Auction utilities ####

@internal
@view
def getBidId1(_bidder: address, _bidSequence: uint256) -> uint256:
    msbs: uint256 = shift(convert(_bidder, uint256), 96)
    bidId: uint256 = bitwise_or(msbs, _bidSequence)

    return bidId


@internal
def getNewBidId1(_bidder: address) -> uint256:
    self.bidders[_bidder].lastSequence += 1
    return self.getBidId(_bidder, self.bidders[_bidder].lastSequence)


@internal
@view
def _getState1() -> uint256:
    if block.timestamp < self.extendedEnd and self.open == True:
        if self.paused:
            return PAUSED_STATE
        else:
            if block.timestamp >= self.startDate:
                if block.timestamp < self.endDate - self.extendingTime:
                    return OPEN_STATE
                else:
                    return SUDDEN_DEATH_STATE
            else:
                return PENDING_STATE
    else:
        return CLOSED_STATE


@external
@view
def getState1() -> uint256:
    return self._getState()



##### Assertion ####

@internal
@view
def bidOwner1(_sender: address, _bidId: uint256) -> bool:
    return shift(_bidId, -96) == convert(_sender, uint256)


@internal
@view
def _getNewAverageChangingN1(
        old_mean: int128,
        _value: uint256,
        temp_bid_count: uint256,
        _count: int128) -> int128:
    return old_mean + ((convert(_value, int128) * _count) - (old_mean * _count)) / (convert(temp_bid_count, int128) + _count)


@internal
@view
def _getNewAverageConstN1(
        old_mean: int128,
        token_qty: uint256,
        _value: uint256,
        _count: int128) -> int128:
    value_pushed: uint256  = 0
    temp_bid_id: uint256 = self.lowWinningBidId
    for i in range(MAX_BATCH_SIZE):
        if i >= _count:
            break
#        value_pushed += self.levels[DEEPEST_LEVEL][temp_bid_id].value
#        temp_bid_id = self.levels[DEEPEST_LEVEL][temp_bid_id].nextBid
        value_pushed += self.levels[temp_bid_id][DEEPEST_LEVEL].value
        temp_bid_id = self.levels[temp_bid_id][DEEPEST_LEVEL].nextBid
    return old_mean + (
            (convert(_value, int128) * _count - convert(value_pushed, int128)) / convert(token_qty, int128))


@internal
def _updateBidsAverage1(_value: uint256, _count: int128):
   old_av: int128 = self.bidAverage
   temp_bid_count: uint256 = self.bidCount
   temp_token_qty: uint256 = self.tokenQty
   # Total amount of bids in the money will be increased
   if ( (convert(temp_bid_count, int128) + _count) <=
           convert(temp_token_qty, int128) ):
       self.bidAverage = self._getNewAverageChangingN(
           old_av,
           _value,
           temp_bid_count,
           _count
       )
   else:
       # Total amount of bids will be PARTIALLY increased
       if ( temp_bid_count < temp_token_qty ):
           amount_diff: int128 = (convert(temp_bid_count, int128) + _count) - convert(temp_token_qty, int128)
           temp_mean: int128 = self._getNewAverageChangingN(
                   old_av,
                   _value,
                   temp_bid_count,
                   _count - amount_diff
           )
           self.bidAverage = self._getNewAverageConstN(
               temp_mean,
               temp_token_qty,
               _value,
               amount_diff
           )
       # Total amount of bids in the money will NOT be increased
       else:
           self.bidAverage = self._getNewAverageConstN(
               old_av,
               temp_token_qty,
               _value,
               _count
           )


@internal
@view
def _getLowerBidBound1() -> int128:
    # Comparison is by date because we are out control on the Paused state
    if block.timestamp < self.endDate - self.extendingTime:
#        return convert(
#                self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value,
#                int128)
        return convert(
            self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value,
            int128)
    return self.bidAverage


@external
@view
def getLowerBidBound1() -> int128:
    return self._getLowerBidBound()


@internal
@view
def validBidValue1(_value: uint256) -> bool:
    if self.minimumBid > _value:
        return False
    if self._getState() == OPEN_STATE:
#        return (self.bidCount < self.tokenQty or
#               _value > self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value)
        return (self.bidCount < self.tokenQty or
               _value > self.levels[self.lowWinningBidId][DEEPEST_LEVEL].value)
    if self._getState() == SUDDEN_DEATH_STATE:
        return convert(_value, int128) > self.bidAverage
    return False


@internal
@view
def _bidOutOfTheMoney1(_bidId : uint256) -> bool:
   # currentBid: Bid = self.levels[DEEPEST_LEVEL][self.lowWinningBidId]
#    value: uint256 = self.levels[DEEPEST_LEVEL][_bidId].value
    # currentBid: Bid = self.levels[self.lowWinningBidId]
    currentBid: Bid = self.levels[self.lowWinningBidId][DEEPEST_LEVEL]
    value: uint256 = self.levels[_bidId][DEEPEST_LEVEL].value
    result: bool = False

    if currentBid.value == value:
        for i in range(MAX_BID_QTY):
            if currentBid.prevBid == _bidId:
                result = True
                break
            if currentBid.value != value: break
#            currentBid = self.levels[DEEPEST_LEVEL][currentBid.prevBid]
            currentBid = self.levels[currentBid.prevBid][DEEPEST_LEVEL]
        return result
    else:
        return currentBid.value > value

@internal
@view
def getLevel2(_bidId: uint256, _sender: address, _randSeed: uint256) -> int128:
    level: int128 = 0
    xor_result: uint256 = bitwise_xor(
        bitwise_xor(
            bitwise_xor(
                convert(_sender, uint256), _bidId),
                convert(block.prevhash, uint256)
        ),
        _randSeed
    )
    random: uint256 = convert(keccak256(convert(xor_result, bytes32)), uint256)
    for i in range(MAX_LEVEL - 1):
        if bitwise_and(
                random,
                shift(UNPROMOTE_PROB, PROMOTION_CONSTANT * i)
                ) == 0:
            level += 1
        else:
            break

    return level



#### Auction utilities ####

@internal
@view
def getBidId2(_bidder: address, _bidSequence: uint256) -> uint256:
    msbs: uint256 = shift(convert(_bidder, uint256), 96)
    bidId: uint256 = bitwise_or(msbs, _bidSequence)

    return bidId


@internal
def getNewBidId2(_bidder: address) -> uint256:
    self.bidders[_bidder].lastSequence += 1
    return self.getBidId(_bidder, self.bidders[_bidder].lastSequence)


@internal
@view
def _getState2() -> uint256:
    if block.timestamp < self.extendedEnd and self.open == True:
        if self.paused:
            return PAUSED_STATE
        else:
            if block.timestamp >= self.startDate:
                if block.timestamp < self.endDate - self.extendingTime:
                    return OPEN_STATE
                else:
                    return SUDDEN_DEATH_STATE
            else:
                return PENDING_STATE
    else:
        return CLOSED_STATE


@external
@view
def getState2() -> uint256:
    return self._getState()



##### Assertion ####

@internal
@view
def bidOwner2(_sender: address, _bidId: uint256) -> bool:
    return shift(_bidId, -96) == convert(_sender, uint256)


@internal
@view
def _getNewAverageChangingN2(
        old_mean: int128,
        _value: uint256,
        temp_bid_count: uint256,
        _count: int128) -> int128:
    return old_mean + ((convert(_value, int128) * _count) - (old_mean * _count)) / (convert(temp_bid_count, int128) + _count)


@internal
@view
def _getNewAverageConstN2(
        old_mean: int128,
        token_qty: uint256,
        _value: uint256,
        _count: int128) -> int128:
    value_pushed: uint256  = 0
    temp_bid_id: uint256 = self.lowWinningBidId
    for i in range(MAX_BATCH_SIZE):
        if i >= _count:
            break
#        value_pushed += self.levels[DEEPEST_LEVEL][temp_bid_id].value
#        temp_bid_id = self.levels[DEEPEST_LEVEL][temp_bid_id].nextBid
        value_pushed += self.levels[temp_bid_id][DEEPEST_LEVEL].value
        temp_bid_id = self.levels[temp_bid_id][DEEPEST_LEVEL].nextBid
    return old_mean + (
            (convert(_value, int128) * _count - convert(value_pushed, int128)) / convert(token_qty, int128))


@internal
def _updateBidsAverage2(_value: uint256, _count: int128):
   old_av: int128 = self.bidAverage
   temp_bid_count: uint256 = self.bidCount
   temp_token_qty: uint256 = self.tokenQty
   # Total amount of bids in the money will be increased
   if ( (convert(temp_bid_count, int128) + _count) <=
           convert(temp_token_qty, int128) ):
       self.bidAverage = self._getNewAverageChangingN(
           old_av,
           _value,
           temp_bid_count,
           _count
       )
   else:
       # Total amount of bids will be PARTIALLY increased
       if ( temp_bid_count < temp_token_qty ):
           amount_diff: int128 = (convert(temp_bid_count, int128) + _count) - convert(temp_token_qty, int128)
           temp_mean: int128 = self._getNewAverageChangingN(
                   old_av,
                   _value,
                   temp_bid_count,
                   _count - amount_diff
           )
           self.bidAverage = self._getNewAverageConstN(
               temp_mean,
               temp_token_qty,
               _value,
               amount_diff
           )
       # Total amount of bids in the money will NOT be increased
       else:
           self.bidAverage = self._getNewAverageConstN(
               old_av,
               temp_token_qty,
               _value,
               _count
           )


@internal
@view
def _getLowerBidBound2() -> int128:
    # Comparison is by date because we are out control on the Paused state
    if block.timestamp < self.endDate - self.extendingTime:
#        return convert(
#                self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value,
#                int128)
        return convert(
            self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value,
            int128)
    return self.bidAverage


@external
@view
def getLowerBidBound2() -> int128:
    return self._getLowerBidBound()


@internal
@view
def validBidValue2(_value: uint256) -> bool:
    if self.minimumBid > _value:
        return False
    if self._getState() == OPEN_STATE:
#        return (self.bidCount < self.tokenQty or
#               _value > self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value)
        return (self.bidCount < self.tokenQty or
               _value > self.levels[self.lowWinningBidId][DEEPEST_LEVEL].value)
    if self._getState() == SUDDEN_DEATH_STATE:
        return convert(_value, int128) > self.bidAverage
    return False


@internal
@view
def _bidOutOfTheMoney2(_bidId : uint256) -> bool:
   # currentBid: Bid = self.levels[DEEPEST_LEVEL][self.lowWinningBidId]
#    value: uint256 = self.levels[DEEPEST_LEVEL][_bidId].value
    # currentBid: Bid = self.levels[self.lowWinningBidId]
    currentBid: Bid = self.levels[self.lowWinningBidId][DEEPEST_LEVEL]
    value: uint256 = self.levels[_bidId][DEEPEST_LEVEL].value
    result: bool = False

    if currentBid.value == value:
        for i in range(MAX_BID_QTY):
            if currentBid.prevBid == _bidId:
                result = True
                break
            if currentBid.value != value: break
#            currentBid = self.levels[DEEPEST_LEVEL][currentBid.prevBid]
            currentBid = self.levels[currentBid.prevBid][DEEPEST_LEVEL]
        return result
    else:
        return currentBid.value > value

@internal
@view
def getLevel3(_bidId: uint256, _sender: address, _randSeed: uint256) -> int128:
    level: int128 = 0
    xor_result: uint256 = bitwise_xor(
        bitwise_xor(
            bitwise_xor(
                convert(_sender, uint256), _bidId),
                convert(block.prevhash, uint256)
        ),
        _randSeed
    )
    random: uint256 = convert(keccak256(convert(xor_result, bytes32)), uint256)
    for i in range(MAX_LEVEL - 1):
        if bitwise_and(
                random,
                shift(UNPROMOTE_PROB, PROMOTION_CONSTANT * i)
                ) == 0:
            level += 1
        else:
            break

    return level



#### Auction utilities ####

@internal
@view
def getBidId3(_bidder: address, _bidSequence: uint256) -> uint256:
    msbs: uint256 = shift(convert(_bidder, uint256), 96)
    bidId: uint256 = bitwise_or(msbs, _bidSequence)

    return bidId


@internal
def getNewBidId3(_bidder: address) -> uint256:
    self.bidders[_bidder].lastSequence += 1
    return self.getBidId(_bidder, self.bidders[_bidder].lastSequence)


@internal
@view
def _getState3() -> uint256:
    if block.timestamp < self.extendedEnd and self.open == True:
        if self.paused:
            return PAUSED_STATE
        else:
            if block.timestamp >= self.startDate:
                if block.timestamp < self.endDate - self.extendingTime:
                    return OPEN_STATE
                else:
                    return SUDDEN_DEATH_STATE
            else:
                return PENDING_STATE
    else:
        return CLOSED_STATE


@external
@view
def getState3() -> uint256:
    return self._getState()



##### Assertion ####

@internal
@view
def bidOwner3(_sender: address, _bidId: uint256) -> bool:
    return shift(_bidId, -96) == convert(_sender, uint256)


@internal
@view
def _getNewAverageChangingN3(
        old_mean: int128,
        _value: uint256,
        temp_bid_count: uint256,
        _count: int128) -> int128:
    return old_mean + ((convert(_value, int128) * _count) - (old_mean * _count)) / (convert(temp_bid_count, int128) + _count)


@internal
@view
def _getNewAverageConstN3(
        old_mean: int128,
        token_qty: uint256,
        _value: uint256,
        _count: int128) -> int128:
    value_pushed: uint256  = 0
    temp_bid_id: uint256 = self.lowWinningBidId
    for i in range(MAX_BATCH_SIZE):
        if i >= _count:
            break
#        value_pushed += self.levels[DEEPEST_LEVEL][temp_bid_id].value
#        temp_bid_id = self.levels[DEEPEST_LEVEL][temp_bid_id].nextBid
        value_pushed += self.levels[temp_bid_id][DEEPEST_LEVEL].value
        temp_bid_id = self.levels[temp_bid_id][DEEPEST_LEVEL].nextBid
    return old_mean + (
            (convert(_value, int128) * _count - convert(value_pushed, int128)) / convert(token_qty, int128))


@internal
def _updateBidsAverage3(_value: uint256, _count: int128):
   old_av: int128 = self.bidAverage
   temp_bid_count: uint256 = self.bidCount
   temp_token_qty: uint256 = self.tokenQty
   # Total amount of bids in the money will be increased
   if ( (convert(temp_bid_count, int128) + _count) <=
           convert(temp_token_qty, int128) ):
       self.bidAverage = self._getNewAverageChangingN(
           old_av,
           _value,
           temp_bid_count,
           _count
       )
   else:
       # Total amount of bids will be PARTIALLY increased
       if ( temp_bid_count < temp_token_qty ):
           amount_diff: int128 = (convert(temp_bid_count, int128) + _count) - convert(temp_token_qty, int128)
           temp_mean: int128 = self._getNewAverageChangingN(
                   old_av,
                   _value,
                   temp_bid_count,
                   _count - amount_diff
           )
           self.bidAverage = self._getNewAverageConstN(
               temp_mean,
               temp_token_qty,
               _value,
               amount_diff
           )
       # Total amount of bids in the money will NOT be increased
       else:
           self.bidAverage = self._getNewAverageConstN(
               old_av,
               temp_token_qty,
               _value,
               _count
           )


@internal
@view
def _getLowerBidBound3() -> int128:
    # Comparison is by date because we are out control on the Paused state
    if block.timestamp < self.endDate - self.extendingTime:
#        return convert(
#                self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value,
#                int128)
        return convert(
            self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value,
            int128)
    return self.bidAverage


@external
@view
def getLowerBidBound3() -> int128:
    return self._getLowerBidBound()


@internal
@view
def validBidValue3(_value: uint256) -> bool:
    if self.minimumBid > _value:
        return False
    if self._getState() == OPEN_STATE:
#        return (self.bidCount < self.tokenQty or
#               _value > self.levels[DEEPEST_LEVEL][self.lowWinningBidId].value)
        return (self.bidCount < self.tokenQty or
               _value > self.levels[self.lowWinningBidId][DEEPEST_LEVEL].value)
    if self._getState() == SUDDEN_DEATH_STATE:
        return convert(_value, int128) > self.bidAverage
    return False


@internal
@view
def _bidOutOfTheMoney3(_bidId : uint256) -> bool:
   # currentBid: Bid = self.levels[DEEPEST_LEVEL][self.lowWinningBidId]
#    value: uint256 = self.levels[DEEPEST_LEVEL][_bidId].value
    # currentBid: Bid = self.levels[self.lowWinningBidId]
    currentBid: Bid = self.levels[self.lowWinningBidId][DEEPEST_LEVEL]
    value: uint256 = self.levels[_bidId][DEEPEST_LEVEL].value
    result: bool = False

    if currentBid.value == value:
        for i in range(MAX_BID_QTY):
            if currentBid.prevBid == _bidId:
                result = True
                break
            if currentBid.value != value: break
#            currentBid = self.levels[DEEPEST_LEVEL][currentBid.prevBid]
            currentBid = self.levels[currentBid.prevBid][DEEPEST_LEVEL]
        return result
    else:
        return currentBid.value > value
