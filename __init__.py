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
import numpy as np

MANIFEST = {
    "name": "ZSuite",
    "version": (2, 0, 0),
    "author": "TheBarret",
    "project": "https://github.com/TheBarret/",
    "description": "A suite of useful nodes for ComfyUI",
}

# Initialize seed and change directory
random.seed()
os.chdir(os.path.dirname(os.path.abspath(__file__)))


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
                "trigger": ("STRING", {"default": ""}),
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
        self.last_sum = 1  # Initialize with a default value

    @classmethod
    def INPUT_TYPES(cls):
        """
        Define input types for the Seed Modifier node.
        """
        return {
            "required": {
                "seed": ("INT", {"default": 0}),
                "modifier": ("FLOAT", {"default": 0.3, "min": 0, "max": 1, "step": 0.1}),
            },
        }

    @classmethod
    def OUTPUT_TYPES(cls):
        """
        Define output types for the Seed Modifier node.
        """
        return {
            "sum": ("INT", {}),
        }

    RETURN_TYPES = ("INT",)

    FUNCTION = "modify_seed"
    CATEGORY = "Math"

    def modify_seed(self, seed, modifier):
        """
        Modify the seed while retaining its essence with overflow check.
        """
        # Calculate the modification amount
        modification_amount = int(modifier * seed)

        # Linear interpolation between the last stored value and the new one
        interpolated_value = int(np.interp(random.random(), [0, 1], [self.last_sum, seed + modification_amount]))

        # Check for overflow
        max_int = 2**31 - 1  # Assuming 32-bit signed integer, adjust if needed
        if interpolated_value > max_int:
            interpolated_value = max_int
        elif interpolated_value < -max_int:
            interpolated_value = -max_int

        # Store the outcome for the next cycle
        self.last_sum = interpolated_value

        return (interpolated_value,)



# NODE_CLASS_MAPPINGS
if "NODE_CLASS_MAPPINGS" not in globals():
    NODE_CLASS_MAPPINGS = {}

if "NODE_DISPLAY_NAME_MAPPINGS" not in globals():
    NODE_DISPLAY_NAME_MAPPINGS = {}

# FINALIZE
NODE_CLASS_MAPPINGS["ZSUITE_PROMPTER"] = ZSuitePrompter
NODE_DISPLAY_NAME_MAPPINGS["ZSUITE_PROMPTER"] = "ZSuite Prompter"
NODE_CLASS_MAPPINGS["ZSUITE_SEED_MODIFIER"] = ZSuiteSeedMod
NODE_DISPLAY_NAME_MAPPINGS["ZSUITE_SEED_MODIFIER"] = "ZSuite Seed Modifier"
