# Internet Architecture
The Internet is characterized by the general framework known as the OSI model, which is a standard created by the ISO to allow different vendors to interoperate with each other. The current internet doesn't utilize the entire OSI Model, but instead only uses 4 of the layers (Application, Transport, Network, Data Link, & Physical).

## What is OSI Model?
- Application
- Presentation
- Session
- Transport
- Network
- Data Link
- Physical

## Why Use OSI Model?
- Modularity: Each layer is in charge of 1 set of tasks, so changing one layer of the OSI model does not affect the other layers. For example, using Wifi vs. Ethernet doesn't affect TCP (part of the transport layer) in any way
- Abstraction: Each layer hides the details away from another layer.
- Interoperability: In the past, vendors and systems used to design their own network stack that bundled all functions into it, meaning if you used a certain stack like IBM's SNA then you were trapped into it. With the OSI model, systems can implement different technologies as long as they conform to the layer’s standard.
- Scalability: New technologies can replace current ones in layers. For example, fiber optics helped replace ethernet in certain cases without disrupting the Data Link Layer at all.