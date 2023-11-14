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
import importlib

# NODE_CLASS_MAPPINGS
if "NODE_CLASS_MAPPINGS" not in globals():
    NODE_CLASS_MAPPINGS = {}

if "NODE_DISPLAY_NAME_MAPPINGS" not in globals():
    NODE_DISPLAY_NAME_MAPPINGS = {}

for node in os.listdir(os.path.dirname(__file__) + os.sep + 'nodes'):
    if node.startswith('ZS_'):
        node = node.split('.')[0]
        node_import = importlib.import_module('custom_nodes.Zephys.nodes.' + node)
        print(f"[ZSuite] Loading {node}...")
        NODE_CLASS_MAPPINGS.update(node_import.NODE_CLASS_MAPPINGS)