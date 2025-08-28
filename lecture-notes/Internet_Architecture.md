
# Internet Architecture
The Internet is layered abstractions to reduce complexity by dividing and conquering tasks into layers
## What happens when you press Google.com
DNS asks for IP of www.google.com from DNS server and returns IP 
<br>
Application Layer   -> HTTP GET request for it
<br>
Transport Layer     -> break HTTP message into segments. Use TCP to have reliable and in-order delivery
<br>
Network Layer       -> Find destination IP via routing
<br>
Link Layer          -> Who gets to talk, Framing, Error Detection
<br>
Physical Layer      -> Bits are sent as signals over wifi, cellular, fiber, coaxial cables etc.