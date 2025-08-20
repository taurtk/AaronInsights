# This script creates a new virtual environment, activates it, and installs the required packages.

# 1. Create the virtual environment using Python 3.11
py -3.11 -m venv .venv

# 2. Activate the virtual environment
. .\.venv\Scripts\Activate.ps1

# 3. Install the packages from requirements.txt
pip install -r requirements.txt

Write-Host "Virtual environment setup is complete. You can now run your application."