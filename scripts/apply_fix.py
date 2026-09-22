import os

with open("main.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

config_lines = []
new_main = []
in_config = False

for line in lines:
    if line.startswith("APP_NAME  ="):
        in_config = True
        config_lines.append("import os\n")
        config_lines.append("import json\n")
        config_lines.append("from pathlib import Path\n")
        config_lines.append("from utils.logger import AstaLogger\n")
        config_lines.append("from utils.updates_asta import CURRENT_VERSION\n\n")

    # Stop config extraction when we reach the LicenseWindow class
    if in_config and line.startswith("class LicenseWindow("):
        in_config = False
        new_main.append("from core.config import *\n\n")

    if in_config:
        config_lines.append(line)
    else:
        new_main.append(line)

# Write core/config.py
os.makedirs("core", exist_ok=True)
with open("core/config.py", "w", encoding="utf-8") as f:
    f.writelines(config_lines)

# Write main.py
with open("main.py", "w", encoding="utf-8") as f:
    f.writelines(new_main)

print("Extraction to core/config.py done safely.")
