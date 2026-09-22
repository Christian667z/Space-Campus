import os
import glob

# 1. Extract config from main.py
with open("main.py", "r", encoding="utf-8") as f:
    main_lines = f.readlines()

config_code = []
new_main_lines = []
in_config = False

for i, line in enumerate(main_lines):
    # Detect the start of constants
    if line.startswith("APP_NAME  ="):
        in_config = True
        config_code.append("import os\n")
        config_code.append("from pathlib import Path\n")
        config_code.append("import json\n")
        config_code.append("from utils.logger import AstaLogger\n")
        config_code.append("from utils.updates_asta import CURRENT_VERSION\n\n")
    
    # Detect the end of save_json (the last function)
    # The line after save_json ends usually has class AstaLicenseWindow
    if in_config and line.startswith("class AstaLicenseWindow"):
        in_config = False
        new_main_lines.append("from core.config import *\n\n")

    if in_config:
        config_code.append(line)
    else:
        new_main_lines.append(line)

# Create core/config.py
os.makedirs("core", exist_ok=True)
with open("core/config.py", "w", encoding="utf-8") as f:
    f.writelines(config_code)

# Write updated main.py
with open("main.py", "w", encoding="utf-8") as f:
    f.writelines(new_main_lines)

# 2. Update views/*.py
view_files = glob.glob("views/*.py")
for view in view_files:
    with open(view, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remplacer from main import PROFILE_FILE, ... par from core.config import ...
    if "from main import " in content:
        content = content.replace("from main import ", "from core.config import ")
        with open(view, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {view}")

print("Fix applied successfully.")
