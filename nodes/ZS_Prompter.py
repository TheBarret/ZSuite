import os
import random
import re
import socket
import struct
import time
import torch
import numpy as np

# Initializing variables and instances
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

NODE_CLASS_MAPPINGS = { "ZSuite: Prompter": ZSuitePrompter }