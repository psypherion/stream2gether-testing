#!/bin/bash

# Ensure the script is run with superuser privileges
if [ "$(id -u)" -ne "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

# Update package list and install required packages
apt-get update
apt-get install -y python3 python3-venv python3-pip curl

# Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install necessary Python packages
pip install flask flask-socketio

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Install ngrok
curl -s https://ngrok.com/download | tar xvz -C /usr/local/bin

# Install Node.js dependencies
npm install


