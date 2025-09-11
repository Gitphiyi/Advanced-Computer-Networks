# Congestion Control

## Dynamic Window Sizing
- Sending Speed: $W / RTT$
    - Adjust $W$ based on available bandwidth
    - Increase $W$ in no congestion
    - Decrease $W$ in congestion
- Sender has 2 internal params:
    - Congestion Window (cwnd)
    - Slow-start threshold Value (ssthresh)
