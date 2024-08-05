#!/bin/bash

# Script for setting up the environment for your project

echo "Starting setup..."

# 1. Download ngrok
echo "Downloading ngrok..."
curl -s https://bin.equinox.io/c/4b8e4a0e39f0/ngrok-stable-linux-amd64.zip -o ngrok.zip
unzip ngrok.zip
rm ngrok.zip

# 2. Create ngrok multi-tunneling configuration
echo "Creating ngrok multi-tunneling configuration..."

mkdir -p ~/.ngrok
cat > ~/.ngrok/ngrok.yml <<EOL
tunnels:
  flask:
    addr: 5000
    proto: http
  nodejs:
    addr: 3000
    proto: http
EOL

sudo apt-get install jq

# 3. ngrok API key generation doc
echo "For ngrok API key generation, follow these steps:"
echo "1. Sign up or log in to ngrok at https://dashboard.ngrok.com"
echo "2. Go to the Auth section to get your API key."
echo "3. Replace <YOUR_NGROK_API_KEY> below with your actual API key."

# 4. Add ngrok API key
echo "Adding ngrok API key..."
read -p "Enter your ngrok API key: " NGROK_API_KEY
./ngrok authtoken $NGROK_API_KEY


# Create credentials.json if it doesn't exist and add the API key
echo "Creating credentials.json with the API key..."
CREDENTIALS_FILE="credentials.json"
if [ ! -f "$CREDENTIALS_FILE" ]; then
    echo "{}" > $CREDENTIALS_FILE
fi

# Add ngrok API key to credentials.json
jq --arg key "$NGROK_API_KEY" '.api_key = $key' $CREDENTIALS_FILE > tmp.$$.json && mv tmp.$$.json $CREDENTIALS_FILE

echo "API key added to credentials.json"

# 5. Install Node.js
echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 6. Node.js setup
echo "Setting up Node.js..."
npm install

# installing git
sudo apt install git

# Installing envtool
echo "Installing envtool..."

git clone https://github.com/ky13-troj/envtool.git

cd envtool

chmod +x run.sh

./run.sh

cd ../

# setting up python environment

echo "Setting up python environment..."
envtool -n venv

echo "Done!"

echo "Setup is complete now activate the virtual environment"

echo "Type this command : source venv/bin/activate"

