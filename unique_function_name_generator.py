
for i in range(20):
    string_i = "1_"+str(i)
    print(f"""@internal
@view
def getLevel{string_i}(_bidId: uint256, _sender: address, _randSeed: uint256) -> int128:
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
def getBidId{string_i}(_bidder: address, _bidSequence: uint256) -> uint256:
    msbs: uint256 = shift(convert(_bidder, uint256), 96)
    bidId: uint256 = bitwise_or(msbs, _bidSequence)

    return bidId


@internal
def getNewBidId{string_i}(_bidder: address) -> uint256:
    self.bidders[_bidder].lastSequence += 1
    return self.getBidId(_bidder, self.bidders[_bidder].lastSequence)


@internal
@view
def _getState{string_i}() -> uint256:
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
def getState{string_i}() -> uint256:
    return self._getState()



##### Assertion ####

@internal
@view
def bidOwner{string_i}(_sender: address, _bidId: uint256) -> bool:
    return shift(_bidId, -96) == convert(_sender, uint256)


@internal
@view
def _getNewAverageChangingN{string_i}(
        old_mean: int128,
        _value: uint256,
        temp_bid_count: uint256,
        _count: int128) -> int128:
    return old_mean + ((convert(_value, int128) * _count) - (old_mean * _count)) / (convert(temp_bid_count, int128) + _count)


@internal
@view
def _getNewAverageConstN{string_i}(
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
def _updateBidsAverage{string_i}(_value: uint256, _count: int128):
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
def _getLowerBidBound{string_i}() -> int128:
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
def getLowerBidBound{string_i}() -> int128:
    return self._getLowerBidBound()


@internal
@view
def validBidValue{string_i}(_value: uint256) -> bool:
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
def _bidOutOfTheMoney{string_i}(_bidId : uint256) -> bool:
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
    """)
