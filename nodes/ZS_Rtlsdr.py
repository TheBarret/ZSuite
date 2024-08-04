# #######################################################################################################################

# This node facilitates communication with an RTL-SDR device (Digital Radio Receiver) through a TCP connection.
# Once connected, it captures live ambient RF noise, which is then embedded into a latent vector.

# Protocol: https://hz.tools/rtl_tcp/ Paul Tagliamonte 2020-11-03

# Overview:
# - The node establishes a TCP connection with the RTL-SDR device.
# - Sends essential parameters such as frequency, IQ sample rate, tuner, and gain settings.
# - Collects ambient RF noise data from the device for a specified duration.
# - Scales and injects the noise into a given latent vector, adjusting its strength.
# - The injected latent vector is then returned for further processing.

# Cheat sheet:
# Frequnecy     : Depending device type but generally 5Khz ~ 1.7Ghz, in `Hz` unit notation
# Gain values   : 0.0, 0.9, 1.4, 2.7, 3.7, 7.7, 8.7, 12.5, 14.4, 15.7, 16.6, 19.7, 20.7, 22.9, 25.4,
#                 28.0, 29.7, 32.8, 33.8, 36.4, 37.2, 38.6, 40.2, 42.1, 43.4, 43.9, 44.5, 48.0, 49.6 (Default: 0 = auto)
# Samplerates   : 0.25, 1.024, 1.536, 1.792, 1.92, 2.048, 2.16, 2.56, 2.88, 3.2 MSps (Default:  1.024 MSps)

import os
import random
import re
import socket
import struct
import time
import torch
import numpy as np

# Settings for RTL-SDR device
DEVICE_HOST         = "192.168.2.3"
DEVICE_PORT         = 10080
DEVICE_BUFFER       = 4096
DEVICE_FREQUENCY    = 100000000
DEVICE_IQ           = 1024000
DEVICE_TUNER        = 1
DEVICE_GAIN         = 20.7

class ZSuiteNoise:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        # Define input types for the inject_rtl_noise function
        return {
            "required": {
                "latents": ("LATENT",),
                "rtl_tcp_host": ("STRING", {"default": DEVICE_HOST, "multiline": False}),
                "rtl_tcp_port": ("INT", {"default": DEVICE_PORT, "min": 0, "max": 65535}),
                "duration": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 10.0, "step": 0.1}),
                "strength": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "trigger": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "inject_rtl_noise"
    CATEGORY = "latent/noise"

    def inject_rtl_noise(self, latents, rtl_tcp_host, rtl_tcp_port, duration, strength, trigger):
        print(f"[ZSuite] Signal [{trigger}]")
        # Inject RTL-SDR noise into latent samples
        print(f"[ZSuite] Addressing device [{rtl_tcp_host}:{rtl_tcp_port}]")
        noise = self.collect_rtl_noise(rtl_tcp_host, rtl_tcp_port, duration)
        return self.inject_noise(latents, noise, strength)

    def inject_noise(self, latents, noise, strength):
        # Inject noise into latent samples
        s = latents.copy()
        if noise is None:
            return (s,)

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

        return (s,)

    def collect_rtl_noise(self, host, port, duration):
       try:
        # Collect RTL-SDR noise data from specified host and port
        print(f"[ZSuite] Opening connection...")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # Set a shorter timeout for testing
            try:
                s.connect((host, port))
            except Exception as e:
                print(f"[ZSuite] Error caught: {e}")
                return np.array([]), np.array([])

            # Send RTL-SDR parameters to the device
            print(f"[ZSuite] Sending parameters [{DEVICE_FREQUENCY},{DEVICE_IQ},{DEVICE_TUNER},{DEVICE_GAIN}]")
            self.send_command(s, 0x01, DEVICE_FREQUENCY)
            self.send_command(s, 0x02, DEVICE_IQ)
            self.send_command(s, 0x03, DEVICE_TUNER)
            self.send_command(s, 0x04, DEVICE_GAIN)

            # Collect noise data from the device
            noise_data = self.collect_data(s, duration)

        return self.prepare_noise(noise_data)
    except Exception as e:
        print(f"[ZSuite] Error caught: {e}")
        return np.array([]), np.array([])

    def send_command(self, sock, opcode, value):
        # Send command to the RTL-SDR device
        if opcode in {0x01, 0x02}:  # Frequency and IQ Sample Rate commands
            cmd_bytes = struct.pack('>BI', opcode, value)
        elif opcode in {0x04, 0x05, 0x06, 0x0d}:  # Gain, Frequency Correction, IF Gain, Tuner Gain Index commands
            cmd_bytes = struct.pack('>BHH', opcode, int(value), 0)  # Ensure value is an integer
        elif opcode in {0x03, 0x07, 0x08, 0x09, 0x0a, 0x0e}:  # Single uint8 value
            cmd_bytes = struct.pack('>BB', opcode, int(value))  # Ensure value is an integer
        else:
            raise ValueError(f"[ZSuite] Unsupported opcode {opcode}")

        sock.sendall(cmd_bytes)

    def collect_data(self, sock, duration):
        # Collect data from the RTL-SDR device for the specified duration
        samples = []
        chunk_size = DEVICE_BUFFER
        timer_start = time.time()
        while True:
            data = sock.recv(chunk_size)
            if not data:
                break

            samples.extend(struct.unpack('h' * (len(data) // 2), data))

            if time.time() - timer_start > duration:
                break
        print(f"[ZSuite] Captured {len(samples)} samples")
        return np.array(samples)

    def prepare_noise(self, data):
        # Prepare noise data for injection
        combined_data = np.array(data)
        return combined_data

# Mapping for the ZSuite: RF Noise node class
NODE_CLASS_MAPPINGS = {"ZSuite: RF Noise": ZSuiteNoise}

