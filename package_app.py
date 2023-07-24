import subprocess
import sys
import os

# Replace 'your_script.py' with the name of your existing script file
script_file = "media_downloader.py"
output_folder = "dist"

# Ensure that the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Package the script using PyInstaller
cmd = f"pyinstaller --onefile --windowed --distpath={output_folder} {script_file}"
subprocess.run(cmd, shell=True)

# Print a success message
print("Packaging completed!")