# Physical Layer
**Goal:** Move bits between 2 nodes connected by a physical link
**Interface:** Specifies how to send one bit over physical link

## Devices
- Coaxial Cables
- Fiber Optics
- Ethernet
- WIFI
- Radio Frequency Transmitters

## Line Encoding
### NRZ - sample on clock rising edge (low to high)
Problems: long string of 0/1 cause dsynchronization (bitslip). Basically if there are no transitions between signals the receiver has a hard time knowing if its clock is in sync with the sender. Also, can’t tell if getting no signal at all or all 0s. Receiver and sender can synchronize clocks on transitions from 0 to 1.

Dsynchronization Example: The sender sends 8 bits, but because the receiver clock is slightly slower it only detects 7 bits. The receiver and sender only synchronize when the bits change from 0 to 1 or 1 to 0

### NRZI (Non return to Zero Inverted) - transition = 1. Samples every clock cycle. No transition = 0. Solves problem for repeated 1’s but not 0’s.
Solution: Change the data to prevented repeated 1/0s. Map all 4-bit sequences to 5-bit sequence that has no more than 1 leading 0 and 2 trailing 0 (won’t send 3 consecutive 0s). Efficiency drops to 80%.

### Manchester - high to low = 1. Low to high = 0. 
- Guarantees bit transition but takes 2 clock cycles for every bit transmission

## Clock Synchronization and Recovery


Vocab:
Bandwidth - # of bits that can be transmitted over the network in a certain period of time
Throughput - Empirical performance of a system; “average bandwidth”
Latency - delay
Line rate - speed at which individual devices have to be able to process data (Ethernet = 100GB/s)
Gateway Router - router that client uses as the first hop for all of its Internet traffic to remote hosts
