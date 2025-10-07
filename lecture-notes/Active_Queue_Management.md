# Active Queue Management
How to determine the best size of the Router Buffer

## Issue with DropTail Queue
- large buffer increases latency b/c TCP will increase cwnd until loss
- large buffeer is expensive

## Random Early Detection (RED)
Goal: operate at the "knee"
Router measures avg queue length using exponential weighted averaging algorithm when packet arrives

$$
AvgLen = (1-Weight)*AvgLen + Weight * q
$$

The drop based on some threshold
- $AvgLen \leq MinThreshold$: enqueue packet
- $MinThreshold < AvgLen < MaxThreshold$: calc dropping probability P and drop arriving packets with that probability P
- $MaxThreshold \leq AvgLen$: drop arriving packets

The average queue length smooths out the stuff and is better for measuring how big the queue should be because some stuff can just be instantaneous bursts.

### Limitations of RED
- Parameters are hard to tune
    - leads to low utilization if minThresh, maxThresh, max_p aren't set correctly
    - Does not directly control latency
        - High speed

### Explicit Congestion Notification (ECN)
**Goal:** Notify congestion exists instead of drop packets
<br>
- 
- 2 bits in IP (00 NO ECN support) (01/10) ECN support enabled (11 Congestion experienced)
<br>
Receiver will echo back returned signal:
- 2 TCP flags
- ECE: congestion experienced
- CWR: cwnd reduced
The goal is not only flag congestion but also have router tell exactly how much to reduce cwnd and stuff.



## Proportional Integral Enhanced
Adjusting queue length is the key to the problem. Follow up from RED. Drop packets depending on what latency is desired and if packets will allow for it
**Goal:** Directly control latency and drive "error" or queuing delay to zero
- based on a PID controller
randomely drop incoming packets when congestion occurs
- detect congestion based on the derivative of queuing latency


### Little's Law
avg_arrival_rate = 
queueing delay = queue_len / avg_departure_rate
## CoDel
FQ-CoDel in Linux kernel
## Optimal Router Buffer Size
- Buffer empty means link is idle
- What is the min buffer to keep link busy at all times?