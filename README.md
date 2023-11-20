# ZSuite

![afbeelding](https://github.com/TheBarret/ZSuite/assets/25234371/309a5f2c-81cb-496c-bb79-a34b56d08807)


Version: 2.0
- 10-11-2023 - Initial Release
- 11-11-2023 - Added Seed Modifier
- 12-11-2023 - Modified Seed node to accept expressions
- 13-11-2023 - Added Latent Noise Provider (Transforming RF Signals) using `RTL_TCP`


# ZSuite - Prompter

This node uses files to randomize pre-defined sorted subjects of random things.

Example line:

`__preable__ painting by __artist__`

This prompt will be processed with random line form the file called `preamble.txt` in the folder:

`.\comfyui\custom_nodes\Zephys\nodes\blocks\.*txt`

The node uses a `trigger` as input from any `integer` value type, to enforce a new prompt output.

# ZSuite - RF Node

The data capture in the `RF Node` is `4096 bytes / cycle` governed by `duration` in seconds.
If the data length is smaller then the Latent shape it will reset to index 0.

Then the data is processed using `numpy` to normalize the data in workable format shown here:

```
        # Ensure noise is a NumPy array
        noise = np.array(noise)

        # Obtain min/max values from noise data
        data_min = np.min(noise)
        data_max = np.max(noise)

        # Scale and inject noise into latent samples
        print(f"[ZSuite] Injecting noise...")
        for i in range(s["samples"].numel()):
            raw = float(strength * float(noise[i % noise.size]))
            data_scaled = (raw - data_min) / (data_max - data_min)
            data_scaled = 2 * data_scaled - 1
            s["samples"].view(-1)[i] = data_scaled
```
Remark: Im sure this can be done better, feel free to tell me if so.

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
