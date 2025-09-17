import time
import math
from Util import *

# Constants
MinRTO = 0.3
G = 0.1 #clock granularity
K = 4
alpha = 0.125 # RTT smoothing

# cubic state
last_crash = time.time() # time elapsed since last window reduction
Wmax = 0.0 # window size before last reduction
mss = SegmentSize
ssthresh = float("inf")


# updateCWND: Update reli.cwnd according to the congestion control algorithm.
# 'reli' provides an interface to access class Reliable.
# 'reliImpl' provides an interface to access class ReliableImpl.
# 'acked'=True when a segment is acked.
# 'timeout'=True when a segment is timeout
# 'fast'=True when more than three duplicated acks are received (fast retransmission).
def updateCWND(reli, reliImpl, acked=False, timeout=False, fast=False):
    global Wmax, last_crash, mss, ssthresh
    C = 0.4 #scaling constant
    beta = 0.7
    
    curr_cwnd = reli.cwnd
    T = (time.time() - last_crash) # time since last crash
    print("prev cwnd: " + str(curr_cwnd))
    
    # Receiver got data so can increase congestion window    
    if acked:
        print("Sucessfully Acked")
        
        # slow start
        if curr_cwnd <= ssthresh:
            curr_cwnd += mss
        #cubic growth
        else:
            K = (Wmax*(1-beta)/C)**(1/3)
            new_cwnd = C * (T - K) ** 3 + Wmax
            print("prev cwnd: " + str(new_cwnd))
            reli.cwnd = new_cwnd

            
    # Severe Congestion
    if timeout:
        print("Did not receive ACK. Congestion is strong")
        Wmax = 0
        dMin = None
        reli.cwnd = mss

    
    # Enter Fast recovery and reduce window. indicates a packet was lost but later packets arrived
    if fast:
        print("Packet was lost but later packets arrived")
        Wmax = curr_cwnd
        ssthresh = curr_cwnd * (1-beta)
        reli.cwnd = ssthresh


# updateRTO: Run RTT estimation and update RTO.
# You can use time.time() to get current timestamp.
# 'reli' provides an interface to access class Reliable.
# 'reliImpl' provides an interface to access class ReliableImpl.
# 'timestamp' indicates the time when the sampled packet is sent out.
def updateRTO(reli, reliImpl, timestamp):
    alpha = 0.9
    beta = 2
    rtt = time.time() - timestamp
    if reliImpl.srtt is None or reliImpl.rttvar is None:
        reliImpl.rttvar = rtt / 2
        reliImpl.srtt = rtt 
    else:
        reliImpl.rttvar = (1 - 0.25) * reliImpl.rttvar + 0.25 * abs(reliImpl.srtt - rtt)
        reliImpl.srtt = (1-alpha)*reliImpl.srtt + alpha * rtt 

    print("old rto: " + str(reliImpl.rto))
    reliImpl.rto = reliImpl.srtt + max(G, 4*reliImpl.rttvar)
    
    #make sure it is always above min RTO
    reliImpl.rto = max(reliImpl.rto, MinRTO)
    print("new rto: " + str(reliImpl.rto))
