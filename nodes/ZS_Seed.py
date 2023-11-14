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

# Constants
MAX_SEED = 2 ** 31 - 1

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
        
NODE_CLASS_MAPPINGS = { "ZSuite: SeedMod": ZSuiteSeedMod }