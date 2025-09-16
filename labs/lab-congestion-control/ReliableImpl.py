from collections import deque
import Congestion
from Util import *


def checkInWrapRange(head, tail, index):  # index in [head, tail)
    if head <= tail and (index < head or tail <= index):
        return False
    if tail < head and (tail <= index and index < head):
        return False
    return True


def wrapdist(head, tail):
    if head <= tail:
        return tail-head
    else:
        return SeqNumSpace-head+tail


def checkAcked(seqNum, payloadlen, ackNum):
    dist = wrapdist(seqNum, ackNum)
    if dist > HalfSeqNumSpace:
        return False
    return dist >= payloadlen


class ReliableImpl:
    def __init__(self, reli=None, seqNum=None, srvSeqNum=None):
        super().__init__()
        self.reli = reli
        self.lastByteSent = seqNum
        # srvAckNum remains unchanged in this lab
        self.nextByteExpected = (srvSeqNum+1) % SeqNumSpace

        self.lastByteAcked = seqNum
        # lastAckNum = lastByteAcked + 1
        self.lastAckNum = (self.lastByteAcked+1) % SeqNumSpace
        self.swnd = deque()
        self.state = {}
        self.timestamps = {}
        self.retransmitted = set()

        self.rto = Congestion.MinRTO
        self.srtt = None
        self.rttvar = None

        self.FRCount = 0

    @staticmethod
    def checksum(s):
        n = len(s)
        res = 0
        for i in range(0, n-1, 2):
            res += struct.unpack('=H', s[i:i+2])[0]
        if (n & 1) == 1:
            res += struct.unpack('=H', bytes([s[n-1], 0]))[0]
        while (res >> 16) > 0:
            res = (res & 0xffff)+(res >> 16)
        return (1 << 16)-1-res  # ~res

    def recvAck(self, seg):
        if seg.ackNum == self.lastAckNum:
            self.FRCount += 1
            if self.FRCount == 3 and len(self.swnd) > 0:
                (seqNum, payloadlen) = self.swnd[0]
                self.fastRetransmission(seqNum, payloadlen)
            elif self.FRCount > 3:
                Congestion.updateCWND(
                    self.reli, self, fast=True)
            return 0

        if not checkInWrapRange((self.lastAckNum+1) % SeqNumSpace, (self.lastByteSent+2) % SeqNumSpace, seg.ackNum):
            return 0
        self.FRCount = 0

        fbytesReduce = wrapdist(self.lastAckNum, seg.ackNum)
        self.lastByteAcked = (seg.ackNum-1) % SeqNumSpace
        self.lastAckNum = seg.ackNum
        if seg.ackNum not in self.retransmitted and seg.ackNum in self.timestamps:
            Congestion.updateRTO(self.reli, self, self.timestamps[seg.ackNum])

        while len(self.swnd) > 0:
            (seqNum, payloadlen) = self.swnd[0]
            if checkAcked(seqNum, payloadlen, self.lastAckNum):
                self.state[seqNum][1].cancel()
                self.state.pop(seqNum, None)
                self.swnd.popleft()
                ackNum = (seqNum+payloadlen) % SeqNumSpace
                self.retransmitted.discard(ackNum)
                self.timestamps.pop(ackNum, None)
                Congestion.updateCWND(self.reli, self, acked=True)
                continue
            break
        self.reli.updateRWND(seg.rwnd)

        return fbytesReduce

    def sendData(self, payload, isFin):
        seqNum = (self.lastByteSent+1) % SeqNumSpace
        temp = Segment.pack(seqNum, 0, 0, 0, 0, int(isFin), 0, payload)
        seg = Segment.pack(seqNum, 0, 0, 0, 0, int(
            isFin), ReliableImpl.checksum(temp), payload)
        payloadlen = max(len(payload), 1)

        timer = self.reli.setTimer(
            self.rto, self.retransmission, [seqNum, payloadlen])
        self.state[seqNum] = [seg, timer, self.rto]
        self.timestamps[(seqNum+payloadlen) % SeqNumSpace] = time.time()
        self.swnd.append((seqNum, payloadlen))
        self.lastByteSent = (self.lastByteSent+payloadlen) % SeqNumSpace

        self.reli.sendto(seg)
        return payloadlen

    def retransmission(self, seqNum, payloadlen):
        if checkAcked(seqNum, payloadlen, self.lastAckNum):
            return
        [seg, timer, rto] = self.state[seqNum]
        if rto >= MaxRTO:
            ErrorHandler("Ack time out.")
        rto = min(MaxRTO, rto*2)
        timer = self.reli.setTimer(
            rto, self.retransmission, [seqNum, payloadlen])
        self.state[seqNum][1] = timer
        self.state[seqNum][2] = rto

        ackNum = (seqNum+payloadlen) % SeqNumSpace
        self.retransmitted.add(ackNum)

        if seqNum == self.lastAckNum:  # avoid continuous reducing cwnd
            Congestion.updateCWND(self.reli, self, timeout=True)

        self.reli.sendto(seg)

    def fastRetransmission(self, seqNum, payloadlen):
        if checkAcked(seqNum, payloadlen, self.lastAckNum):
            return
        [seg, timer, rto] = self.state[seqNum]
        rto = min(MaxRTO, rto*2)
        timer.cancel()  # cancel previous timer and call self.retransmission for later retransmission
        timer = self.reli.setTimer(
            rto, self.retransmission, [seqNum, payloadlen])
        self.state[seqNum][1] = timer
        self.state[seqNum][2] = rto

        ackNum = (seqNum+payloadlen) % SeqNumSpace
        self.retransmitted.add(seqNum)

        Congestion.updateCWND(self.reli, self, fast=True)

        self.reli.sendto(seg)
