# TCP CUBIC
## Why does it work?
## Design Goals
- Congestion Control: making system operate left of the cliff to avoid congestion collapse
- Congestion Avoidance: making system operate around the knee to obtain low latency and high throughput
    - Efficiency: closeness of total load on resource of its knee: $\sum x_i \approx \text{capacity}$
    - Fairness: $F(x) = \frac{(\sum x_i)^2}{n(\sum x_i^2)}$
        - When all $x_i$ are equal, $F(x) = 1$
    - Distributedness
        - A centralized scheme requires complete knowledge of the state of  the system
    - Convergence
        - System approach goal state from any starting state
- High Throughput/Utilization
- Low Latency
- Fairness
- Fast Convergence

## Model of the System
- A feedback control systems
- Sum the loads from all the users going into the system

### Linear Control System
$$
\begin{equation}
x_i(t+1) =
\begin{cases}
a_I + b_I x_i(t), & \text{if } y(t) = 0 \;\Rightarrow\; \text{Increase}, \\
a_D + b_D x_i(t), & \text{if } y(t) = 1 \;\Rightarrow\; \text{Decrease}.
\end{cases}
\end{equation}
$$
Depending on linear combo of $a_I, b_I, a_D, b_D$ 4 sample types of control arrive
- Additive Increase Additive Decrease (AIAD)
    - $b_I = b_D = 1$
    - $a_I >0, a_D < 0$
- Additive Increase Multiplicative Decrease (AIMD)
    - $b_I = 1, a_D = 0$
    - $a_I > 0, 0 <b_D < 1$
- Multiplicative Increase Additive Decrease (MIAD)
- Multiplicative Increase Multiplicative Decrease (MIMD)

### Why not use AIAD?
- Assumption RTT is the same between X2 and X1 (2 users)
- line going down is efficiency line 
- line going up is $x_1 = x_2$
- want to operate where the lines intersect because that is where system is efficient and fair
#### AIAD Example
- Suppose starting point was not efficient and not fair
- Then system would tell both users to increase capacity. This would make the point move parallel to the fairness line
- This means that if the starting point never starts where $x_1 = x_2$ then the system will never be fair
#### AIMD Example
- Below capacity is the same as AIAD
- Once point of exceeding capacity then suppose the constants for multiplicatively decreasing $x_1$ and $x_2$ is 1/2
- This makes it so eventually it is possible to reache the fair line since going down by 1/2 in both ways is not a parallel line to the fairness line

### RTT Unfairness
- Long RTT flows obtain smaller bandwidth shares because they can't reach efficiency as fast as shorter RTT flows
- For every ACK received $W+= 1/W$ and every packet lost $W/=2$ (W = min window size)
- Only true in unit of RTT and this add decrease is a sawtooth behavior

## Metrics to measure convergence
- Responsiveness
- Smoothness