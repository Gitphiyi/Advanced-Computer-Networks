# CUBIC: A New TCP-Friendly High-Speed TCP Variant
## Author: Sangtae Ha, Injong Rhee, Lisong Xu
Paper Link: https://courses.cs.duke.edu/fall25/compsci514/readings/cubic.pdf

## Main Point
With TCP Reno and TCP Sack the network was severely underutilized, and due to over-aggressive congestion control, takes a while to get to capacity. With this issue, the introduction of high speed protocols were created. This includes BIC-TCP and CUBIC.

## Aim of Paper:
- Introduction to BIC-TCP and CUBIC
- Related Works
- Details of CUBIC
- Fairness policy of CUBIC
- Experimental Results

# Introduction to BIC-TCP and CUBIC
- binary search between last max window size before packet loss and last window size it did not have loss for one RTT period
- Window function is a logarithm concave function to keep congestion window much longer at staturation point
- If network has more capacity than before, cwnd allowed to grow exponentially beyond prev max
    - exponential functions grow slowly at first which make the system more stable around critical operating point
    - also means could be sluggish to find new saturation point since the steps are so large later
- Reacts fast to reduced capacity
- CUBIC merely simplifies window adjustment agorithm to a cubic function
    - window growth only depends on the real time between two consecutive congestion events
    - Removal of window clamping
    - Replaced BIC-TCP as default TCP algorithm in 2006

## Related Work:
- Scalable TCP (STCP) = make recovery time from loss events be constant regardless of the window size
- HighSpeed TCP (HSTCP) = Uses Additive Increase Multiplicative Decrease (AIMD) where the linear increase factor and multiplicative decrease factor are adjusted by a convex function of the current congestion window
- HTCP = Uses elapsed time since last congestion event for calculating current congestion window size
    - window growht function is quadratic relative to elapsed time
    - adjust decrease factor by function of RTTs to estimate queue size in network path of current flow
- TCP Vegas = measure the difference between actual and expected throughput based on round trip delays
- FAST = determines current congestion window size based on both round trip delays and packet loses over path
- TCP-Westwood = Estiamtes end-to-end available bandwidth by accounting rate of returning ACKs
- TCP-Illinois = use queuing delay to determine and increase factor $\alpha$ and multiplicaive decrease factor $\beta$ instantaneously during the window increment phase.
- TCP-Hybla = scales window increment rule to ensure fairness among flows with different RTTs
- TCP-Veno = determine congestion window size using delay info of TCP-Vegas to differentiate non congestion losses

## CUBIC Congestion Control
### BIC-TCP