import os

with open("main.py", "r", encoding="utf-8") as f:
    main_lines = f.readlines()

with open("core/config.py", "r", encoding="utf-8") as f:
    config_lines = f.readlines()

# The config file has 6 lines of new imports at the top:
# import os
# from pathlib import Path
# ...
# APP_NAME = "Asta Académie"
# We want to keep everything from APP_NAME onwards.
start_idx = 0
for i, line in enumerate(config_lines):
    if line.startswith("APP_NAME  ="):
        start_idx = i
        break

rest_of_main = config_lines[start_idx:]

with open("main.py", "w", encoding="utf-8") as f:
    f.writelines(main_lines)
    f.writelines(rest_of_main)

print("Restored main.py successfully.")
