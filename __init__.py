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
from sympy import symbols, lambdify, Abs, sin, cos, tan, sinh, cosh, tanh, exp, log, sqrt, atan, asin, acos, cbrt
import numpy as np

from sympy.parsing.sympy_parser import parse_expr
from sympy import Piecewise as piecewise

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

# NODE_CLASS_MAPPINGS
if "NODE_CLASS_MAPPINGS" not in globals():
    NODE_CLASS_MAPPINGS = {}

if "NODE_DISPLAY_NAME_MAPPINGS" not in globals():
    NODE_DISPLAY_NAME_MAPPINGS = {}

# FINALIZE
NODE_CLASS_MAPPINGS["ZSUITE_PROMPTER"]              = ZSuitePrompter
NODE_CLASS_MAPPINGS["ZSUITE_SEED_MODIFIER"]         = ZSuiteSeedMod

NODE_DISPLAY_NAME_MAPPINGS["ZSUITE_PROMPTER"]       = "ZSuite Prompter"
NODE_DISPLAY_NAME_MAPPINGS["ZSUITE_SEED_MODIFIER"]  = "ZSuite Seed Modifier"

