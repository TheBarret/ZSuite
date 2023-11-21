# ZSuite

![afbeelding](https://github.com/TheBarret/ZSuite/assets/25234371/309a5f2c-81cb-496c-bb79-a34b56d08807)


Version: 2.0.0
- 10-11-2023 - Initial Release
- 11-11-2023 - Added Seed Modifier
- 12-11-2023 - Modified Seed node to accept expressions
- 13-11-2023 - Added Latent Noise Provider (Transforming Ambient RF Signals using `RTL_TCP` as noise)


# ZSuite - Prompter

This node uses files to randomize pre-defined sorted subjects of random things.

Example line:

`__preamble__ painting by __artist__`

This prompt will be processed with random line form the file called `preamble.txt` and `artists.txt` in the folder:

`.\comfyui\custom_nodes\Zephys\nodes\blocks\.*txt`

You can create new or change any `txt` files in this folder to customize your wishes

The node uses a `trigger` as input from any `integer` value type, to enforce a new prompt output.
I often myself use a `Counter` node that comes almost by default for math operations, it allows
me to make sure the `Prompter` gets processed each time you hit `Generate`.


# ZSuite - RF Node

*This section explains the functioning of the RF Node within ZSuite, emphasizing the need for an RTL-SDR device, server setup, and predefined configurations.
the rtl_tcp is an I/Q spectrum server for RTL2832 based DVB-T receivers*

**Server Hosting and RTL_TCP Service:**

To facilitate communication with the RTL-SDR device, a server must be set up. The RTL_TCP service is employed for this purpose. Here's a breakdown of the setup:

1. **RTL_TCP Installation:**
   - Follow the Debian-specific instructions provided in the [RTL_TCP Manpage](https://manpages.debian.org/testing/rtl-sdr/rtl_tcp.1.en.html).
   - Execute the command: `rtl_tcp -a <ip> -p <port> -d 0` to initiate the service on the specified IP and port.

![afbeelding](https://github.com/TheBarret/ZSuite/assets/25234371/fd5e517c-c3bd-4ad6-a219-c61648bf757c)

![afbeelding](https://github.com/TheBarret/ZSuite/assets/25234371/c333f042-ff4c-41f7-9581-c667fe02db82)

**Why Server Setup is Necessary:**

The RTL-SDR device communicates via TCP/IP, necessitating the establishment of a server. This server acts as an intermediary, allowing ZSuite to access the data stream from the RTL-SDR device. The specified IP and port parameters ensure a seamless connection between the RF Node in ZSuite and the RTL-SDR device.

**Predefined Configurations and Latent Noise Processing:**

Within the ZSuite framework, the RF Node operates on pre-defined configurations and processes data using the following steps:

1. **Data Capture Parameters:**
   - The RF Node captures data at a rate of (default) `4096 bytes per cycle`.
   - The duration parameter governs capture length of the capturing.

![afbeelding](https://github.com/TheBarret/ZSuite/assets/25234371/b13f7ca0-5b76-4210-9c2d-0636c4400721)


2. **Latent Noise Processing:**
   - If the captured data length is smaller than the specified Latent shape, it resets to index 0.
   - The captured data undergoes processing using the `numpy` library to perform normalization.
   - Normalization involves scaling and injecting noise into latent samples, ensuring the data is in a workable format.

**Configurability:**

Users can customize default device parameters by editing the `ZS_Rtlsdr.py` file located at `.\comfyui\custom_nodes\Zephys\nodes\`.

The constant definition header in this file contains configurable settings for the RF Node.

By following these steps and understanding the underlying processes, users can effectively set up and utilize the RF Node in ZSuite for their specific needs.
