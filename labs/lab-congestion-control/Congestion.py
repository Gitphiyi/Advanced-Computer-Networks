import time
import math
from Util import *

G = 0.1 #clock granularity
MinRTO = 0.3
MaxRTO = 5
alpha = 0.125 # RTT smoothing

BETA = 0.6
C = 0.4

# cubic state
last_crash = time.time() # time elapsed since last window reduction
MSS = PayloadSize
ssthresh = MSS * 50
phase = ""
W_last_max = 0
K = 0
acks_received = 0


# updateCWND: Update reli.cwnd according to the congestion control algorithm.
# 'reli' provides an interface to access class Reliable.
# 'reliImpl' provides an interface to access class ReliableImpl.
# 'acked'=True when a segment is acked.
# 'timeout'=True when a segment is timeout
# 'fast'=True when more than three duplicated acks are received (fast retransmission).

def updateCWND(reli, reliImpl, acked=False, timeout=False, fast=False):
    cubic_impl(reli, reliImpl, acked, timeout, fast)
    #reno_impl(reli, reliImpl, acked, timeout, fast)
    
def cubic_impl(reli, reliImpl, acked=False, timeout=False, fast=False):
    global W_last_max, MSS, phase, K, ssthresh, last_crash, acks_received
    cwnd = reli.cwnd
    T = time.time() - last_crash
    # Slow start
    if acked:
        acks_received += 1
        if cwnd <= ssthresh:
            phase = "slow"
            reli.cwnd += MSS
        else:
            phase = "cubic"
            # Only increase cubicly after receiving multiple ACKS
            if acks_received > 10:
                K = (abs(W_last_max - cwnd) / C) ** (1/3)
                new_cwnd = max(C * (T - K) ** 3 + W_last_max, cwnd+MSS)
                reli.cwnd = min(new_cwnd, reli.rwnd)
        print(f"ACK {phase}: cwnd={reli.cwnd}, ssthresh={ssthresh}, rwnd={reli.rwnd}, Wmax={W_last_max}, rto={reliImpl.rto}, K={K}")
    if fast: 
        last_crash = time.time()
        W_last_max = cwnd
        ssthresh = max(cwnd * (1 - BETA), MSS)
        reli.cwnd = max(cwnd * 0.8, MSS)
        acks_received = 0
        print(f"FAST RECOVERY: cwnd={reli.cwnd}, ssthresh={ssthresh}, rwnd={reli.rwnd}, Wmax={W_last_max}, rto={reliImpl.rto}") 

    if timeout:
        reli.cwnd = max(MSS, cwnd * BETA)
        ssthresh = max(MSS, cwnd * BETA)
        K = 0
        last_crash = time.time()
        acks_received = 0
        reliImpl.rto = reliImpl.rto * 2 # exponential backoff
        print(f"TIMEOUT: cwnd={reli.cwnd}, ssthresh={ssthresh}, rwnd={reli.rwnd}, Wmax={W_last_max}, rto={reliImpl.rto}") 

def reno_impl(reli, reliImpl, acked=False, timeout=False, fast=False):
    global ssthresh, MSS
    prev_cwnd = reli.cwnd

    if acked:
        # Slow start
        if prev_cwnd < ssthresh:
            reli.cwnd = prev_cwnd + MSS
        else:
            # Congestion avoidance
            ssthresh = prev_cwnd
            reli.cwnd = prev_cwnd + ((MSS / prev_cwnd) * 0.5 * MSS)
        print(f"ACK {phase}: cwnd={reli.cwnd}, ssthresh={ssthresh}, rwnd={reli.rwnd}, rto={reliImpl.rto}")

    if timeout:
        ssthresh = max(prev_cwnd * 0.5, MSS)
        reli.cwnd = max(prev_cwnd * alpha, MSS)

    if fast:
        ssthresh = max(prev_cwnd * 0.5, MSS)
        reli.cwnd = max(prev_cwnd * 0.8, MSS)
        print(f"FAST RECOVERY: cwnd={reli.cwnd}, ssthresh={ssthresh}, rwnd={reli.rwnd}, rto={reliImpl.rto}") 


# updateRTO: Run RTT estimation and update RTO.
# You can use time.time() to get current timestamp.
# 'reli' provides an interface to access class Reliable.
# 'reliImpl' provides an interface to access class ReliableImpl.
# 'timestamp' indicates the time when the sampled packet is sent out.
def updateRTO(reli, reliImpl, timestamp):
    alpha = 0.125
    beta = 0.25
    g = 0.2 # gain constant
    m = (time.time() - timestamp) # new rtt sample
    if reliImpl.srtt is None or reliImpl.rttvar is None:
        reliImpl.rttvar = m / 2
        reliImpl.srtt = m 
    else:
        err = m - reliImpl.srtt
        reliImpl.srtt += g*err
        reliImpl.rttvar += g * (abs(err) - reliImpl.rttvar)
        # reliImpl.rttvar = (1 - beta) * reliImpl.rttvar + beta * abs(reliImpl.srtt - rtt)
        # reliImpl.srtt = (1-alpha)*reliImpl.srtt + alpha * rtt 

    reliImpl.rto = reliImpl.srtt + 4 * reliImpl.rttvar # rto = avg RTT + 4 * variance of rtt
    reliImpl.rto = max(reliImpl.rto, MinRTO)
    reliImpl.rto = min(reliImpl.rto, MaxRTO)
        
"""
    This function is in charge of returning # of 
"""