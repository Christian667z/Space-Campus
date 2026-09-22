import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Lines to add at the top (after existing imports)
new_imports = """
import sys
import pathlib
import time as _t
from PIL import Image, ImageTk
import customtkinter as _ctk
"""

# Insert new imports after 'from datetime import datetime'
content = content.replace("from datetime import datetime\n", "from datetime import datetime\n" + new_imports + "\n")

# Remove nested imports by replacing them with empty strings
nested_imports = [
    r"^\s*import sys\n",
    r"^\s*from PIL import Image, ImageTk\n",
    r"^\s*from PIL import Image\n",
    r"^\s*import customtkinter as _ctk\n",
    r"^\s*import pathlib\n",
    r"^\s*import time as _t\n"
]

for pattern in nested_imports:
    content = re.sub(pattern, "", content, flags=re.MULTILINE)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Imports cleaned up in main.py")
