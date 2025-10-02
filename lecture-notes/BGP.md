# Inter-Domain Routing Protocol (BGP)
## Terms
Routing = Finding a path from a source and destination without loops. Can be also called process of learning which next hop to forward a packet

Route: a network prefix + path attributes

Transit Service: If A advertises a route to B, it implies that A will forward packets coming from B to any destination in the advertised prefix

Control Plane:

Data Plane:
 
Background:
- Expensive Routers to communicate outside of an AS and switches are used inside
- 152.3.0.0/16 means the IP prefix is 16 bits long
- Routers exchange routing protocol messages to building routing table

## Autonomous Systems (AS)

Autonomous System (AS): group of IP prefixes under common management. Identifiable by a 16 bit number
\\
**Transit AS vs Stub AS:** Transit AS let traffic pass through it to reach a seperate destination. Stub AS only allows traffic to originate from it or end up there.

### Tiers of ISPs
ISPs are not equal and some are bigger or more connected than others 
\\
- Tier 1: Only a handful that have global scope b/c their routing table have explicit routes to all current reachable Internet prefixes. They cannot have default route to big ISP. All tier-1 providers MUST peer with each other b/c they have no other provider.
- Tier 2: state-wide or region-wide scope
- Tier 3: small # of local customers
\\
From here on out assume that the Internet is made up of ASes and each implement some set of policies to decide which routes to accept and export. Within the AS, there are different routping procols called Interior Gateway Protocols (IGP) which include RIP, OSPF, IS-IS, E-IGRP. IGP is normally concerned with optimizing a path metric and doesn't scale as well as BGP does. 

### Common AS relationships
- Provider-Customer = pay you to carry my packets to destination
- Peering = For free, I carry your packets to my customers only

### Peering
Customer always pays provider. For Peering there is free peering because if free peering didn't happen then they would have to pay for sending traffic rather than just let them do it for free.
\\
**When to Peer:** There are better performances, lower costs, or more efficient routing.

## BGP
The Internet is made up of peers, customers, and providers, and each has their own preferences to who they want to send.

### Protocol Description
**Initialization**:
BGP runs on TCP over port 179. To start a BGP session, router sends an OPEN message. After OPEN is completed, routers exchange tables of all routes they want to send. Router then uses info from neighbors into the new routing table. Takes a couple of minutes.

### #BGP Messages
- OPEN
- UPDATE
    - Announcements
        - Dest Next-hop AS Path ... other attributes ...
    - Withdrawals
- KEEPALIVE
\\
**The key is Next Hop**
**Update**:
UPDATE messages come in 2 kinds: announcements = changes to existing routes or new routes & withdrawals = named route doesn't exist anymore
\\
Run keep-alive timer such that during a BGP sesion a router will send at least 1 BGP message (UPDATE or KEEPALIVE) within the timer to keep alive. The absence of KEEPALIVE messages means the session will be terminated, and this is configurable by hold timer.
\\

### eBGP & iBGP
- eBGP sessions between BGP-speaking routers in different ASes
- iBGP sessions between BGP routers in same AS
- eBGP = standard mode in BGP. most AS have more than 1 router that participates in eBGP and thus much disseminate routes to external prefixes to other routers in the AS.
- 2 main goals:
    - loop free forwarding
    - complete visibility
- iBGP disseminates externally learned routes to internal routers
- iBGP != IGP. iBGP sessions run over TCP as well and provide a way for routers inside AS to use BGP to exchange info about external routes.
- iBGP sessions are themselves routed between BGP routersin the IGP
- use iBGP vs IGP bc it is inconvenient and doesn't scale well as BGP with respect to # of routes sent. IGP relies more on preiodic routing announcements and IGP doesn't have rich set of attributes present in BGP.

### Route Attributes
- Next Hop
- AS path
- Local Preference
- Multiple-Exit Discriminator

### Path Vector
- ASPATH Attribute
Records what ASes a route went through. This prevents loops such that a route can be discarded if a loop is detected. There is also the shortest path heuristic which basically says if the AS path length is not long then the distance is probably short which is not true and results in issues.