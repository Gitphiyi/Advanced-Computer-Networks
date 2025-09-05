# DNS (Domain Name System)
**Goal:** Associate domain name with IP address. Think of it like a phonebook where you can find people's phone number based on their name
**How to make DNS query:** dig on MAC, nslookup on Windows
- Is a distributed tree-structured database
- Uses UDP port 53 for lightweight and fast exchange of queries. In the case that the response is too long, DNS will fall back to TCP
- Original DNS is insecure, so new DNSSEC adds security

## Protocol:
1. Local Lookup
2. Recursive Resolver
3. Iterative Resolver
4. Return Answer: 
Host first sends request to local DNS server. The resolver IP address is found using DHCP

Local DNS server is doing recursive resolution
Server types
Resolving DNS servers - sending queries, collecting info, forwarding back to client
Authoritative DNS servers - know who are authoritative name servers for sub domains and within their own domain
DNS resolver caches all the mappings of domain name to IP address with long TTL
dig www.website.com A
A tag means we want IP address record associated with name
Requests are tagged with ID to match up with reply from request
Response repeats initial question
Answer (A record): TTL in seconds, IP address, domain name
Authority section: tells us NS (name servers) responsible for finding the answer. The Resource Records (RR) in the Authority section give host names of various NS for names in website.com. Cache record for 11,088 seconds
Additional section: contains A records for the name servers, which contains IP address for NS domain name.
DNS poisoning = can put wrong domain name in Authority section and stuff in the Additional section a MIT IP address for the wrong domain name. If accepted in cache future record, future record requests for the wrong domain name will go to the wrong place
Solution: Don’t accept Additional records that don’t have domains that end correctly
DNS eavesdropping = can allow attackers to substitute different IP’s for each record since the UDP packet is unencrypted
DNS blind spoofing
Say we look up mail.google.com; how can an off-path attacker feed us a bogus A answer before the legitimate server replies? How can such a remote attacker even know we are looking up mail.google.com?
Suppose we visit a page under their control with tag <img src=”http://mail.google.com”>
Once attacker knows where we are going, they can just guess what number is in the UDP header identification field and reply before legit server. If ID field is randomized it becomes very hard to guess
The Kaminsky attack is to make victim look at a bunch of <img src=”http://rando1.mail.google.com”> that don’t exist, but the browser will DNS lookup for every single one. Since the true response will cache nothing as these domains don’t exist, the attacker can try multiple times

## Local Lookup
- Browser Cache
    - The browser frequently will cache common DNS lookups. If you search up "about:networking#dns" on Firefox it will actually take you to common DNS Queries
- OS Resolver Cache
    - OS also maintains a cache. Can search it up via sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder on MacOS
- Host Files
    - On MacOS/Linux checking the etc/hosts folder will also give a list of IP addresses mapped to domain names

## Recursive Resolver
- 

Solution to blind spoofing: 
Make the source port a random number to further reduce probability of spoofing
DNS over HTTPS

## DNSSEC
Compare public key from root and intermediate DNS servers so resolver knows the DNS response is valid


DNSSEC PKI (Public key infra)
Prevent DNS cache poisoning. Disjoint from SSL PKI. Checking is rare for client. Used for .com, .edu, .net, .gov, .mil top-level domains
