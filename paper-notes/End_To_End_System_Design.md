# End-To-End System Design Argument

## Main Point = Many functions (like error detection, encryption, delivery guarantees) can only be completely and correctly implemented at the application layer, because only the application knows what "correct" means.

## Aim of Paper
- Give examples why end-to-end system design makes sense
- Different functions the end-to-end argument can be applied to (encryption, duplicate
message detection, message sequencing, guaranteed message delivery, detecting host crashes,
and delivery receipts)
- the argument applies to many more applications like OS

## Why End-To-End Makes Sense?
- Trying to apply functions in the middle doesn't reduce burden at the end. Example 1 displays this
- Applications that do not need function but use middle layer subsystems have to pay performance degradation for function implemented at that level
- Applicable to encryption
    - Do not want middle man to know what message is
    - If not end-to-end data will be vulnerable in the middle
    - Authenticity of message must be checked by two ends

## Caveats to End-To-End
- Ensuring reliability on lower levels still needed as it reduces # of retries. Doesn't require FULL reliability though
- End-To-End doesn't know where the failure occured, and thus where to place early retry checks
- Cannot have useless acknowledgement that message is received. Want to know the messsage is acted upon.
- Depending on how necessary the packets have to be pristine from end to end determines whether there should be more effort spent on creating reliable middle-layer subsystems

## History of End to End
- First questioned in MIT Compatible Time-Sharing System
- End to End in regards to encryption first mentioned in 1973 by Branstad
    - Diffie and Hellman expanded on the necessity for end to end. Needham and Schroder devised protocols
- 2 phase commit data update protocol devised by Gray, Lampson, Sturgis, and Reed use end to end


## Example 1: Reliable Data Transmission
Goal: Move file from A to B without damage
- Computer A & B are linked via data communication network
- Both computeres have file systems and disk
Steps that are taken:
1. Computer A's file transfer program calls file system to read file from disk. The file system passes the file to the program via fixed-size blocks (disk-format independent)
2. Computer A's program asks data communication network to transmit file via some protocol which splits file into packets.
3. Network moves packet from A to B
4. Computer B's program takes packets from protocol and hands the data to a 2nd transfer application
5. Computer B's program asks file system to write data to disk
### Threats:
1. file on computer A can be read with errors due to disk storage hardware faults
2. software of filesystem, file transfer program, or data communication system can mess up in buffering or copying data to file
3. hardware processor or local memory might have transient errors
4. communication system can drop or modify packets accidentally
5. a host might crash
### Approaches to fix this:
- reinforce each step via duplicate copies, timeouts, retries, etc. 
- verify at the end of the process that the file is correct via checksum or hash. If it is wrong then retry process.
### Supposition 1: communication system guarantees reliable data transmission
- Threat 4 eliminated, but rest of threats remain
- Extra effort to guarantee communication system reliability only reduces # of retries needed
- Cannot confirm that data in the end is correct. Thus checksum is still needed at the end

## Example 2: Duplicate Message Suppression
Some networks make send messages multiple times. Even if network itself tries to suppress duplicates the application itself can send duplicates. The network wouldn't know these messages were duplicates as it is a layer above it. Thus, duplication suppression must be done at the application level.

## Example 3: Guarantee FIFO Delivery
FIFO usually used to ensure messages are delivered the same way they were sent, but messages sent across multple virtual circuit may be in a mixed order.

## Example 4: Practical application of End-To-End with SWALLOW
- SWALLOW has repositories (servers) where clients can read or write data
    - messages must include: which object, version, type of access (r/w), value to be written if a write
- underlying message communication doesn't suppress duplicates b/c version is attached, and duplicate message only results in duplicate response which can be discarded
- This results in a very simple low-level communication protocol
- Only application layer needs to deliver acknowledgements, so # of acknowledgements needed is halved
- Reads do not need acknowledgements

