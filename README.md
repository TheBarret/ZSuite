# ZSuite

![afbeelding](https://github.com/TheBarret/ZSuite/assets/25234371/309a5f2c-81cb-496c-bb79-a34b56d08807)


Version: 2.0
- 10-11-2023 - Initial Release
- 11-11-2023 - Added Seed Modifier
- 12-11-2023 - Modified Seed node to accept expressions
- 13-11-2023 - Added Latent Noise Provider (Transforming RF Signals) using `RTL_TCP`

# RTL Device Setup

For debian:

https://manpages.debian.org/testing/rtl-sdr/rtl_tcp.1.en.html

Commandline for listening:

```user@server:~$ rtl_tcp -a <ip> -p <port> -d 0```

![afbeelding](https://github.com/TheBarret/ZSuite/assets/25234371/fd5e517c-c3bd-4ad6-a219-c61648bf757c)

After this you setup the `RF Noise` node to use this ip and port.
  
 Important:
 - You do need a RTL-SDR device for this node to work

![afbeelding](https://github.com/TheBarret/ZSuite/assets/25234371/c333f042-ff4c-41f7-9581-c667fe02db82)
