# By Barret (Discord: https://discord.gg/6VWmVgPTw9)
#
# Copyright 2023
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to
# deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import random
import re
import socket
import struct
import time
import torch
import torch.nn.functional as F
from sympy import symbols, lambdify, Abs, sin, cos, tan, sinh, cosh, tanh, exp, log, sqrt, atan, asin, acos, cbrt
import numpy as np

MANIFEST = {
    "name": "ZSuite",
    "version": (2, 0, 0),
    "author": "TheBarret",
    "project": "https://github.com/TheBarret/",
    "description": "A suite of useful nodes for ComfyUI",
}

# Initializing variables and instances
random.seed()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Constants
MAX_SEED = 2 ** 31 - 1

# Cheat sheet:
#Gain values    :  0.0 0.9 1.4 2.7 3.7 7.7 8.7 12.5 14.4 15.7 16.6 19.7 20.7 22.9 25.4
#                  28.0 29.7 32.8 33.8 36.4 37.2 38.6 40.2 42.1 43.4 43.9 44.5 48.0 49.6
#Sample rates   :  0.25, 1.024, 1.536, 1.792, 1.92, 2.048, 2.16, 2.56, 2.88, 3.2 MSps

DEVICE_FREQUENCY    = 100000000
DEVICE_IQ           = 1024000
DEVICE_TUNER        = 1
DEVICE_GAIN         = 40.2

class ZSuitePrompter:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        Define input types for the ZSuite Prompter node.
        """
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "__preamble__ painting made by __artist__"}),
                "trigger": ("INT", {"default": 0}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "process_text"
    CATEGORY = "Prompt"

    @classmethod
    def process_text(cls, text, trigger):
        """
        Process the input text by replacing placeholders with random words from corresponding text files.
        """
        import re

        # Extract placeholders between double underscores
        placeholders = re.findall(r'__([^_]+)__', text)
        print(f"[ZSuite] Signal [{trigger}]")
        print(f"[ZSuite] Replacing: {placeholders}")

        # Replace each placeholder with a random word from its corresponding text file
        for placeholder in placeholders:
            file_path = os.path.join("blocks", f"{placeholder}.txt")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    words = [line.strip() for line in file.readlines() if line.strip()]
                    if words:
                        replacement = random.choice(words)
                        text = text.replace(f"__{placeholder}__", replacement)

        print(f"[ZSuite] Finished: {text}")
        return (text,)

# Seed Modifier Node
class ZSuiteSeedMod:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        """
        Define input types for the Seed Modifier node.
        """
      
        # Assign default preset
        preset_default = "abs(seed * tan(trigger) + 0.1 * abs(seed))"
        
        return {
            "required": {
                "seed": ("INT", {"default": 0}),
                "expression": ("STRING", {"multiline": True, "default": preset_default}),
                "trigger": ("INT", {"default": 0}),
            },
        }

    @classmethod
    def OUTPUT_TYPES(cls):
        """
        Define output types for the Seed Modifier node.
        """
        return {
            "sum": ("INT", {}),
            "dec": ("FLOAT", {}),
        }

    RETURN_TYPES = ("INT", "FLOAT")

    FUNCTION = "modify_seed"
    CATEGORY = "Math"

    def modify_seed(self, seed, expression, trigger):
        """
        Modify the seed based on the selected expression, while retaining its essence with overflow check.
        """
        print(f"[ZSuite] Signal [{trigger}]")

        # Define symbols for the expression
        sym_seed, sym_trigger = symbols('seed trigger')

        # Create a lambda function from the expression
        expr_function = lambdify((sym_seed, sym_trigger), expression, modules=['numpy'])

        # Evaluate the expression using provided seed and trigger
        modification_amount = expr_function(seed, trigger)
        
         # Save both integer and decimal representations
        modification_amount_integer = int(modification_amount)
        modification_amount_decimal = float(modification_amount)
        # Save end product
        interpolated_value = modification_amount_integer

        # Use min and max to handle overflow with wraparound to 0
        interpolated_value = interpolated_value % (MAX_SEED + 1)
        
        print(f"[ZSuite] Input: {expression} [{seed},{trigger}]")
        print(f"[ZSuite] Output: {interpolated_value}")

        # Store the outcome for the next cycle
        self.last_sum = interpolated_value

        return (interpolated_value,modification_amount_decimal)


class ZSuiteNoise:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "latents": ("LATENT",),
                "rtl_tcp_host": ("STRING", {"default": "192.168.2.3", "multiline": False}),
                "rtl_tcp_port": ("INT", {"default": 10080, "min": 0, "max": 65535}),
                "duration": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 10.0, "step": 0.1}),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 200.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "inject_rtl_noise"
    CATEGORY = "latent/noise"

    def inject_rtl_noise(self, latents, rtl_tcp_host, rtl_tcp_port, duration, strength):
        print(f"[ZSuite] Addressing device [{rtl_tcp_host}:{rtl_tcp_port}]")
        noise = self.collect_rtl_noise(rtl_tcp_host, rtl_tcp_port, duration)
        return self.inject_noise(latents, noise, strength)

    def inject_noise(self, latents, noise, strength):
        s = latents.copy()
        if noise is None:
            return (s,)
        
        # Ensure noise is a NumPy array
        noise = np.array(noise)
        
        # Obtain min/max
        data_min = np.min(noise)
        data_max = np.max(noise)
        
        # Iterate elements and scale them
        print(f"[ZSuite] Injecting noise...")
        for i in range(s["samples"].numel()):
            raw = float(strength * float(noise[i % noise.size]))
            data_scaled = (raw - data_min) / (data_max - data_min)
            data_scaled = 2 * data_scaled - 1
            s["samples"].view(-1)[i] = data_scaled

        return (s,)
    
    def collect_rtl_noise(self, host, port, duration):
        print(f"[ZSuite] Opening connection...")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # Set a shorter timeout for testing
            try:
                s.connect((host, port))
            except Exception as e:
                print(f"[ZSuite] Error caught: {e}")
                return np.array([]), np.array([])
            print(f"[ZSuite] Sending parameters [{DEVICE_FREQUENCY},{DEVICE_IQ},{DEVICE_TUNER},{DEVICE_GAIN}]")
            self.send_command(s, 0x01, DEVICE_FREQUENCY)
            self.send_command(s, 0x02, DEVICE_IQ)
            self.send_command(s, 0x03, DEVICE_TUNER)
            self.send_command(s, 0x04, DEVICE_GAIN)

            noise_data = self.collect_data(s, duration)

        return self.prepare_noise(noise_data)

    def send_command(self, sock, opcode, value):
        if opcode in {0x01, 0x02}:                                  # Frequency and IQ Sample Rate commands
            cmd_bytes = struct.pack('>BI', opcode, value)
        elif opcode in {0x04, 0x05, 0x06, 0x0d}:                    # Gain, Frequency Correction, IF Gain, Tuner Gain Index commands
            cmd_bytes = struct.pack('>BHH', opcode, int(value), 0)  # Ensure value is an integer
        elif opcode in {0x03, 0x07, 0x08, 0x09, 0x0a, 0x0e}:        # Single uint8 value
            cmd_bytes = struct.pack('>BB', opcode, int(value))      # Ensure value is an integer
        else:
            raise ValueError(f"[ZSuite] Unsupported opcode {opcode}")

        sock.sendall(cmd_bytes)

    def collect_data(self, sock, duration):
        samples = []
        chunk_size = 4096
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
        combined_data = np.array(data)
        return combined_data

# NODE_CLASS_MAPPINGS
if "NODE_CLASS_MAPPINGS" not in globals():
    NODE_CLASS_MAPPINGS = {}

if "NODE_DISPLAY_NAME_MAPPINGS" not in globals():
    NODE_DISPLAY_NAME_MAPPINGS = {}

# FINALIZE
NODE_CLASS_MAPPINGS["ZSUITE_PROMPTER"]              = ZSuitePrompter
NODE_CLASS_MAPPINGS["ZSUITE_SEED_MODIFIER"]         = ZSuiteSeedMod
NODE_CLASS_MAPPINGS["ZSUITE_NOISE"]                 = ZSuiteNoise

NODE_DISPLAY_NAME_MAPPINGS["ZSUITE_PROMPTER"]       = "ZSuite Prompter"
NODE_DISPLAY_NAME_MAPPINGS["ZSUITE_SEED_MODIFIER"]  = "ZSuite Seed Modifier"
NODE_DISPLAY_NAME_MAPPINGS["ZSUITE_NOISE"]          = "ZSuite Noise"
