import os
import sys
import time
import struct

UDPDatagramSize = 1024
SegmentSize = UDPDatagramSize - 8
PayloadSize = SegmentSize-16
MaxBandwidth = int(50*1024*1024/8)  # 50Mbps
MaxDelay = 0.5  # 500ms
MaxRTO = 60
MaxBDP = int(MaxBandwidth*MaxDelay)
SeqNumSpace = (1 << 32)
HalfSeqNumSpace = (1 << 31)
BufferSize = int(10*MaxBDP/PayloadSize)


def ErrorHandler(msg):
    print(msg, file=sys.stderr)
    os._exit(1)


class Segment:

    def __init__(self, seg):
        self.seqNum = struct.unpack('!L', seg[:4])[0]
        self.ackNum = struct.unpack('!L', seg[4:8])[0]
        self.rwnd = struct.unpack('!L', seg[8:12])[0]
        flags = struct.unpack('!H', seg[12:14])[0]
        self.ack = ((flags & 4) == 4)
        self.syn = ((flags & 2) == 2)
        self.fin = ((flags & 1) == 1)
        self.checksum = struct.unpack('=H', seg[14:16])[0]
        self.payload = seg[16:]

    @staticmethod
    def pack(seqNum, ackNum, rwnd, ack, syn, fin, checksum, payload):
        return struct.pack('!L', seqNum)+struct.pack('!L', ackNum)+struct.pack('!L', rwnd) +\
            bytes([0, ack*4+syn*2+fin])+struct.pack('=H', checksum)+payload

    def Print(self):
        print(self.seqNum, self.ackNum, self.rwnd)
        print(self.ack, self.syn, self.fin)


class Timer:

    def __init__(self, timesec, callback, args):
        self.timestamp = time.time()+timesec
        self.enable = True
        self.__callback = callback
        self.__args = args

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def cancel(self):
        self.enable = False

    def run(self):
        return self.__callback(*self.__args)
