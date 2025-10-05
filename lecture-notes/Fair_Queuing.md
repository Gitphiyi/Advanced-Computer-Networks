# Fair Queuing
Instead of FIFO there should be a fair queuing algorithm for buffer space, bandwidth, and latency amoung competing sources

## What is Fair?
- There is no satisfactory sol
    - Could be fairness for flow
    - What if a flow uses long path?
- Max-min fairness
    - many fq algos aim to achieve this def of fairness
    1. No user receives more than it requests
    2. No other allocation satisfies 1 and a higher min allocation (this is the largest min share allocation)
    3. Remove minimal users and reduce the total resources accordingly
- Max-min examples
    1. Increase all flows' rates equally until some users' requests are satisfied or some links are saturated. Remove these users, reduce the resources, and repeat

## Weighted Fair Queuing
### Design Constraints of Weighted Fair Queue
- Bandwidth: Which packets get transmitted
- Promptness: When do packets get transmitted
- Buffer: Which packets to discard

### Nagle's proposal
Have seperate queues for packets from each individual source and different queues are serviced in a round robin manner.
<br>

**Issues:**
- Flows can send different size of packets so it is not fair b/c larger packets take up more bandwidth
- If a packet arrives right after 1 departs it has to wait a long time before departing which is not prompt

### Ideal System
In the ideal world, we imagine that packets are infinitely divisible and each bit from each flow can be sent separately. This is obviously not practical, but WFQ tries to emulate this ideal system.

### Bit-by-Bit Round Robin
**Virtual clock:** the round number R(t) as the # of rounds made in a bit-by-bit round robin service up to time t. A packet with size P bits whose first bit serviced at round $R(t_0) will finish at round $R(t) = R(t_0) + P$ 
    - For a single flow, clock ticks when a bit is transmitted
    - For a multiple flow, clock ticks when a bit from ALL active flows is transmitted

**Finish Time:** 
<br>
$t_i^\alpha$ = real time arrival time of packet $i$ from flow $\alpha$

$P_i^\alpha$ = packet size

$S_i^\alpha$ = round number when packet starts service

$F_i^\alpha$ = finished round number

$F_i^\alpha$ = $S_i^\alpha + P_i^\alpha$ Basically, finish time = start time + packet length

$S_i^\alpha = max(F_{i-1}^\alpha, R(t_i^\alpha))$ Packet can only start service when previous packet from same flow is done and R(t) has caught up to the flow's arrival
<br>

#### Default Allocation
Schedule which packets get serviced based on the finished round number (use heap and get min each finish time)

#### Delay Allocation
- Reduce delay for flows using less than fair share
- Schedule based on $max(F_{i-1}, A_i - \delta)$
    - When $\delta = 0$ no effect
    - $\delta = inf$ means infrequent sender preempts frequent senders

#### Weighted Fair Queuing
- Different queues get different weights
- $w_i$ = # bits from queue in each round
- $F_i = S_i + P+i / w_i$

## FQ Variants
- Stochastic Fair Queuing = fixed number of queues rather than various number of queues
    - Hashes all the flows to fixed queues and round robins each queue. Drop packet from longest queue when no free buffers
    - aggressive flows steal traffic from other flows in same hash
- Deficit Round Robin
    - Dequeue cost: O(1) < O(log Q)
    - each queue is allowed to send Q bytes per round
    - If Q bytes are not sent bc packet is too large then use a deficit counter of each queue to keep track of unused portion
        - Unused quantum saved for next round to offset packet size unfairness
    - if queue is empty counter = 0
    - Use hash bins like stochastic FQ