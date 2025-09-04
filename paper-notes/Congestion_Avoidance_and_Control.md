# Congestion Avoidance and Control
## Author: Jacobson and Karels
Paper Link: https://courses.cs.duke.edu/fall25/compsci514/readings/vanjacobson-congavoid.pdf

## Main Point 
Because of large growth in computer networks, internet gateways drop ~10% of incoming packets due to buffer overflow.

## Aim of Paper:
- Examples of wrong behavior and simple algorithms to correct it
- How algorithms derive from "packet conservation" principle
- Explain 7 new algorithms in 4BSD (Berkeley Unix) TCP
    1. **Round-trip-time variance estimation**  
    2. **Exponential retransmit timer backoff**  
    3. **Slow-start**  
    4. **More aggressive receiver ACK policy**  
    5. **Dynamic window sizing on congestion**  
    6. **Karn’s clamped retransmit backoff**  
    7. **Fast retransmit**
- Explain rationale for algorithms 1-5

## Packet Conservation: 
Definition: In a stable, well-behaved TCP connection, the sender should only inject a new packet into the network when one leaves (i.e., when an ACK is received). This ensures that the number of packets in flight stays constant — like a steady flow of water through a pipe. Physicists would call this a conservative system: mass (or packets) is conserved, not arbitrarily created.  

## How Packet Conservation can be violated:  
1. Connection doesn't get to equilibrium (sender can ramp up too fast or timeouts prevent steady state)
2. Sender injects new packet before old packet exits
3. Equilibrium can't be reached because of resource limits along the path (buffer might be too small for bandwidth)


## Brief Overview of Algorithm:
- Algorithms 1-5 come from packet conservation principle. If "conservation of packets" was violated then thats where a lot of congestion would occur

## Slow Start
- **Algorithm to get to equilibrium by gradually increasing amount of data in transit**
- Usually not reaching equilibrium happens if the connection just started or is restarting after packet loss
- Having a system where the receiver cannot ACK until the sender sends packets means that the protocol is self-clocking. This is good for adjusting to delays and bandwidth variation, but it also means that self-clocked systems is very stable. This makes it hard to start or get data flowing into the system.
### Algorithm Process
- Add congestion window, cwnd, to per-connection state
- When starting or restarting after a loss, set cwnd to 1 packet
- On each ACK for new data, increase cwnd by 1 packet
- When sending, send minimum of receiver's advertised window and cwnd

## Round Trip Timing
- **Algorithm used to conserve equilibrium**
- Problem (2) frequently occurs when the retransmit timer is too short, meaning the sender assumes a packet is lost too quickly and retransmits unnecessarily
- Having a good RTT (round trip time) estimator is ESSENTIAL to surviving heavy load
- RTT estimation is difficult as it is not constant
$$
RTO = R + 4\sigma_R
$$
### Mistake 1: Not estimating the variation $\sigma_R$
- $\sigma_R$ = variation of avg round trip time $R$
- queuing theory states we know that $R$ and $\sigma_R$ increase quickly with load denoted as $\rho$. To be exact $R$ and $\sigma_R$ scale with $(1-\rho)^{-1}$
- Example: 
    - network running at 75% capacity
    - expect RTT to vary by a factor of 16 ($-2\sigma_R, 2\sigma_R$). This comes from $(1-\rho)^{-1} = (0.25)^{-1} = 16$
    - RTT can swing wildly. This means a packet that usually takes 100ms can sometimes take 1.6 seconds

### Initial Solution: Low Pass Filter
- 4BSD TCP protocol suggests estimation of $R$. It is called a low pass filter because when RTT sample spikes then the estimator only shifts a little bit. In essence, short term RTT spikes are ignored but long term trends are captured.
$$
R \leftarrow \alpha R + (1-\alpha)M
$$
R = avg RTT estimate  
M = round trip time measurement from most recently acked data packet  
$\alpha$ = filter gain constant (suggested val is 0.9)
    - higher alpha means slower reaction to changes. lower alpha means faster response to sudden changes
- Example of filter in practice:
    - Suppose $R = 100ms$ and $M = 500ms$ with suggested alpha value. Then new $R = 0.9*100 + 0.1*500 = 140ms$
- Once $R$ estimate is updated, transmit timeout interval $rto$ for next packet sent is set to $\beta R$ where $\beta$ = RTT variation. RTO basically says if I haven't gotten an ACK after this much time, assume the packet is lost and retransmit. $\beta$ just acts as a safety margin factor or the jitter due to queueing
- suggest $\beta = 2$ can adapt to loads up to at most 30%. Above 30% means useless work as connection will retransmit packets that have only been delayed
- Issue is $\beta$ is static and should change depending on load. For example as load increases, then $R$ and $\sigma_R$ both grow very fast, but $\beta$ is still constant.
- Thus, the solution to this issue is estimating $\beta$ which improves low and high load performance via Jacobson's later algorithm

### Mistake 2: Retransmit spacing
- If a packet has to be retransmitted more than once how should the retransmits be spaced
- Solution is exponential backoff
    - Wonky proof: network is approximately a linear systems composed of elements that behave like linear operators: integrators, delays, gain stages, etc. 
    - "Linear system theory says if a system is stable, the stability is exponential. Thus an unstable system can stabilize by adding exponential damping to its primary excitation (senders, traffic sources)"

## Congestion Avoidance
- How packets get lost
    - damaged in transit, but this is rare
    - network is congested and somewhere on path there was insufficient buffer capacity
- What a Congestion Avoidance Strategy consists of
    - Network can signal transport endpoints that congestion is or will occur
    - Endpoints have policy that decreases utilization if this signal is received and increase utilization if signal isn't received
    