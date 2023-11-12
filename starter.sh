#!/bin/bash

_check_and_install_tkinter() {
    python3 -c "import tkinter" &> /dev/null
    if [ $? -ne 0 ]; then
        echo "Tkinter not found. Installing..."
        if ! brew install python-tk; then
            echo "Failed to install Tkinter. Please check your installation."
            exit 1
        fi
    fi
}

# Check and install Tkinter
_check_and_install_tkinter

# Run the Python script with parameters
python3 ./yolo_image_labeler.py 