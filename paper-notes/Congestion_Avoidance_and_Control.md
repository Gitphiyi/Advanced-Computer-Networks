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

### RFC793 Algorithm
- **Algorithm to estimate mean round trip time**
- Simplest example of a class of estimators called stochastic gradient algorithms
$$
a \leftarrow (1-g)a+gm 
\Rightarrow
a \leftarrow a + g(m-a)
$$
a = current RTT estimate  
m = new RTT sample (measured when an ACK returns)  
g = gain (0 < g < 1). Typically g = 0.1-0.2
m-a = prediction error. This is the sum of error due to noise in the measurement and error due to a bad choice of a 
- In other words, the new estimate a moves a fraction g of the way towards the new measurement
#### Rewritten Equation
$$
a \leftarrow a + gE_r + gE_e
$$
$E_r$ = random error
$E_e$ = estimation error
- $gE_e$ kicks a in right direction
- $gE_r$ kicks a into a random direction
- Over time the random kicks cancel each other out and the algorithm converges to correct average
#### Tradeoff in choosing g
- Large $g$: Estimates react quickly to new samples but is more sensitive to noise
- Small $g$: Estimates are slower but smoother

#### Variation Estimation
- How to measure RTT variability for setting RTO?
    - Usually use varince or standard deviation, but variance requires squaring which is computationally expensive. Instead use mean deviation (mdev)
$$
mdev = \text{avg of } |m-a|
\\
mdev^2 = (\sum |m-a|)^2 \geq \sum |m-a|^2 = \sigma^2
$$
mdev = mean deviation

#### Fast Estimator for RTT average and variation
$$
Err \equiv m-a \\
a \leftarrow a+g*Err \\
v \leftarrow v+g(|Err| - v)
$$
$a$ = RTT avg estimate  
$v$ = RTT deviation estimate
$g$ = gain (same one as before)
- To be computed quickly the above equation should be done in integer arithmetic but $g < 1$, so the numbers need to be scaled. If $g$ is a reciprocal power of 2 then the scaling can be implemented with bit shifts.
- To minimize round off error keep scaled versions of $a$ and $v$ 
- Unnecessary to use same gain for $a$ and $v$. $1/g$ should be as large as window size in packets for $a$ estimator. $1/g$ should be less than window size for $v$ estimator

## Congestion Avoidance
How packets get lost:
- damaged in transit, but this is rare
- network is congested and somewhere on path there was insufficient buffer capacity
### What a Congestion Avoidance Strategy consists of:
- Network can signal transport endpoints that congestion is or will occur
    - Explicit Signaling: Routers set a special bit in the packet header if queues are building (DECbit or ECN)
    - Implicit Signaling: Assume that packet loss almost always means congestion. No need to modify routers
- Endpoints have policy that decreases utilization if this signal is received and increase utilization if signal isn't received
### Queue Length Model:
- Uncongested Case: 
$$
L_i = N
$$  
- Congested Case:
$$
L_i = N + \gamma L_{i-1}
$$
- $L_i$ = load at interval $i$. Network load measured by avg queue length / fixed interval (something near RTT)
- $N$ = constant base load. accounts for avg arrival rate of new traffic and intrinisc delay
- $\gamma$ = how much leftover traffic from previous interval spills into the next. if $\gamma$ is too large the queue length starts growing exponentially as the queues never drain. Consider this a 1st order taylor expansion.
- System will stabilize only if traffic sources throttle back as quickly as the queues are growing
### Sender Policy: (Multiplicative Decrease)
#### On Congestion 
$$
W_i = dW_{i-1} \quad (d<1)
$$
- $W$ = size of window
- $d = multiplicative factor 
- When congestion is detected the sender reduces its congestion window by a multiplicative amount. This becomes exponential as congestion persists
#### No Congestion (Additive Increase)
- If there is no congestion then $gamma$ is near zero and load is approximately constant
- Can only determine when traffic is excessive, but cannot know that the connection is underutilizing network capacity. To find out network capacity, increase bandwidth utilization
- Using a symmetric multiplicative increase is a mistake as the window will oscillate wildly and on average be worse
$$
W_i = W_{i-1} + u \quad (u \ll W_{max})
$$
- $W_{max}$ = pipesize
- $u$ = additive constant. Usually $u = \frac{1}{W_i}$
- Thus on each ack for new data, increase cwnd by 1/cwnd
- When sending, send min of receivers advertised window and cwnd

## Gateway Side of Congestion Control
- Multiplicative Decrease and Additive Increase only prevents network capacity from being exceeded but doesn't ensure fair sharing of the network capacity. 
- Gateways can control sharing and fair allocation as all network flow must go through it
    - Gateway should signal congestion at the right time. Too late means queues are full and too early means the queue is empty and network is underutilized
- Solution:
Continue using packet drops as congestion signal. When a host sends more than its fair share the gateway will drop its packets. A misbehaving host  that ignores the congestion control will get most of its packets dropped. Hosts that do implement congestion avoidance get their fair share of bandwidth and don't suffer as many packet drops

### Challenge: Networks are bursty
- Because traffic is bursty detecting congestion early is hard
#### Current Solution: Jain's Scheme
- Based on averaging queue lengths between points when queue drains fully
- Concern: may have convergence issues under heavy load or traffic has 2nd order dynamics
#### Proposed Solution: ARMAX models
- These models predict round-trip time and queue length using past data which detects exponential growth patterns in RTT/queue length earlier and more reliably. 
- Results: preliminary results show it works well at high load and is immune to 2nd order effects in traffic. It is also computationally cheap


