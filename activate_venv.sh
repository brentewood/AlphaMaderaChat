#!/bin/bash

# Get the directory where the script is located
# This line gets the absolute path of the directory containing this script:
# 1. ${BASH_SOURCE[0]} is the path to this script
# 2. dirname gets the directory containing the script
# 3. cd changes to that directory
# 4. pwd prints the absolute path
# The result is stored in SCRIPT_DIR variable
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Path to the virtual environment
VENV_PATH="./venv"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/$VENV_PATH" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH"
    echo "Please ensure the virtual environment is created at scripts/venv"
    exit 1
fi

# Activate the virtual environment
source "$SCRIPT_DIR/$VENV_PATH/bin/activate"

# Print confirmation
echo "Virtual environment activated. Use 'deactivate' to exit."
echo "Python path: $(which python)"