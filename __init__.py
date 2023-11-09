# Import necessary modules
import os
import random

random.seed()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class TFWN:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        # Get the list of files in the 'blocks' folder
        block_files = [file for file in os.listdir('blocks') if file.endswith('.txt')]

        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "__preamble__ painting made by __artist__"}),
                "trigger": ("STRING", {"default": ""}),                                   # Re-execution trigger
                "file_list": ("STRING", {"display": "dropdown", "options": block_files})  # List of available files
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    FUNCTION = "process_text"
    CATEGORY = "Prompt"

    def process_text(self, text, trigger, file_list):
        import re

        # Extract placeholders between double underscores
        placeholders = re.findall(r'__([^_]+)__', text)
        print(f"[Zephys] Prompt input: {text}")
        print(f"[Zephys] Found: {placeholders}")
        print(f"[Zephys] Selected File: {file_list}")

        # Replace each placeholder with a random word from its corresponding text file
        for placeholder in placeholders:
            file_path = f"blocks/{placeholder}.txt"
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    words = [line.strip() for line in file.readlines() if line.strip()]
                    if words:
                        replacement = random.choice(words)
                        text = text.replace(f"__{placeholder}__", replacement)

        print(f"[Zephys] Processed: {text}")

        return (text,)


# Check if NODE_CLASS_MAPPINGS is defined, if not, define it as an empty dictionary
if "NODE_CLASS_MAPPINGS" not in globals():
    NODE_CLASS_MAPPINGS = {}

# Check if NODE_DISPLAY_NAME_MAPPINGS is defined, if not, define it as an empty dictionary
if "NODE_DISPLAY_NAME_MAPPINGS" not in globals():
    NODE_DISPLAY_NAME_MAPPINGS = {}

# Add the new class to the NODE_CLASS_MAPPINGS dictionary
NODE_CLASS_MAPPINGS["Zephys"]           = TFWN
NODE_DISPLAY_NAME_MAPPINGS["Zephys"]    = "Zephy's Prompt Machine"
