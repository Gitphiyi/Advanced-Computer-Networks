import time
import math
from Util import *

G = 0.1 #clock granularity
K = 4
MinRTO = 0.3
alpha = 0.125 # RTT smoothing

# cubic state
last_crash = time.time() # time elapsed since last window reduction
Wmax = 0.0 # window size before last reduction
MSS = PayloadSize
ssthresh = float("inf")
phase = ""

# updateCWND: Update reli.cwnd according to the congestion control algorithm.
# 'reli' provides an interface to access class Reliable.
# 'reliImpl' provides an interface to access class ReliableImpl.
# 'acked'=True when a segment is acked.
# 'timeout'=True when a segment is timeout
# 'fast'=True when more than three duplicated acks are received (fast retransmission).
def updateCWND(reli, reliImpl, acked=False, timeout=False, fast=False):
    global Wmax, last_crash, MSS, ssthresh, phase, K
    
    C = 0.4 #scaling constant
    beta = 0.7
    
    curr_cwnd = reli.cwnd
    T = (time.time() - last_crash) # time since last crash in SECONDS
    # Receiver got data so can increase congestion window    
    if acked:
        # slow start
        if curr_cwnd <= ssthresh:
            curr_phase = "slow start"
            curr_cwnd += MSS

            reli.cwnd = min(curr_cwnd, reli.rwnd)
            
        #cubic growth
        else:
            curr_phase = "cubic"
            curr_cwnd += 1/curr_cwnd
            reli.cwnd = min(curr_cwnd, reli.rwnd)
            # if Wmax > 0:
            #     K = ((Wmax - curr_cwnd) / C) ** (1/3)
            #     new_cwnd = C * (T - K) ** 3 + Wmax
            #     reli.cwnd = max(MSS, min(int(new_cwnd), reli.rwnd))
            # else:
            #     reli.cwnd += MSS
            
            
        print(f"ACK {curr_phase}: cwnd={reli.cwnd}, ssthresh={ssthresh}, rwnd={reli.rwnd}, Wmax={Wmax}, rto={reliImpl.rto}, T={T}, K={K}") 
                    
    # Severe Congestion
    if timeout:
        Wmax = 0
        last_crash = time.time()
        reliImpl.rto = min(reliImpl.rto * 2, 20.0) # exponential backoff
        reli.cwnd = MSS # set cwnd to 1 packet
        print(f"TIMEOUT: cwnd={reli.cwnd}, ssthresh={ssthresh}, rwnd={reli.rwnd}, Wmax={Wmax}, rto={reliImpl.rto}, T={T}, K={K}") 
        
    # Enter Fast recovery and reduce window. indicates a packet was lost but later packets arrived
    if fast:
        Wmax = reli.cwnd
        ssthresh = max(int(reli.cwnd * beta), 2*MSS)
        reli.cwnd = ssthresh
        last_crash = time.time()
        print(f"FAST RECOVERY: cwnd={reli.cwnd}, ssthresh={ssthresh}, rwnd={reli.rwnd}, Wmax={Wmax}, rto={reliImpl.rto}, T={T}, K={K}") 


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
    reliImpl.rto = min(reliImpl.rto, 10)