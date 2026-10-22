# William Keilsohn
# August 14 2026

# Import Packages
import os
import subprocess
import sys

# Declare Variables

# Define Functions

# Run Application
if __name__=="__main__":
    subprocess.run([sys.executable, '-m', 'flask','--app', 'app', 'run'])
    # python -m flask --app app.py run --debug