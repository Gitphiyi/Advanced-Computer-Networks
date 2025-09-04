# The Design Philosophy of the DARPA Internet Protocols
Paper Link: https://courses.cs.duke.edu/fall25/compsci514/readings/darpa.pdf 
<br>
Author: David Clark - Chief Protocol Architect of Internet & Dr. Yang's PHD advisor
<br>
Motivation of Paper: No documentation of what the DARPA protocol is as it is


## Goal of DARPA Internet Architecture:
Create general framework for communication across many different pre-existing networks. This framework would allow multiple applications to use the same network concurrently.

### Pre DARPA vs Post DARPA:
Before DARPA, many networks existed i.e. ARPANET, SATNET, PRNET, etc. Rather than replace them DARPA connects them together as one uniform network. i.e. the details of the underlying networks that make up the big network are abstracted away.

### Why not make a unified system?
While a new unified network system would be more performant, it is in the nature of the Internet to want to integrate "seperate entities into one common utility." 

### How networks were connected?
Via a layer of Internet packet switches called gateway. These gateways implement a store and forward packet forwarding algo

## Survivability in Face of Failure
Goal:
- Synchronization would never be lost unless there was no physical path over which any sort of communication could be achieved
- On transport layer, anything failures below it unless total failure shouldn't effect synchronization

Solution:
- State info of ongoing conversation needs to be protected (# transmitted packets, # packet ACKs, routing tables, etc)
- State information is replicated if state is stored in intermediate packet switching nodes (i.e. router). Robust replication is hard to build because distributed nature of replication. Basically it is hard for all computers to agree on a truth at a given time as failures can happen at any node, messages can be lost, etc.
- Alt Solution: take info and gather it at endpoints of the network or the entity using the service of network. Basis is that it is acceptable to lose state of info if the entity using it doesn't exist anymore

 -- why is it replicated if state is stored in intermediate packet switching node?