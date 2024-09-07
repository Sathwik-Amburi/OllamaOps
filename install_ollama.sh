#!/bin/bash

# Define variables
OLLAMA_TGZ="ollama-linux-amd64.tgz"
INSTALL_DIR="/usr"
SERVICE_FILE="/etc/systemd/system/ollama.service"

# Check if the TGZ file exists
if [ ! -f "$OLLAMA_TGZ" ]; then
  echo "Error: $OLLAMA_TGZ not found in the current directory."
  exit 1
fi

# Extract the package to the specified directory
echo "Extracting $OLLAMA_TGZ to $INSTALL_DIR..."
sudo tar -C $INSTALL_DIR -xzf $OLLAMA_TGZ

# Create a user and group for Ollama
echo "Creating a user and group for Ollama..."
sudo useradd -r -s /bin/false -U -m -d /usr/share/ollama ollama
sudo usermod -a -G ollama $(whoami)

# Create systemd service file
echo "Creating Ollama service file at $SERVICE_FILE..."
sudo bash -c "cat > $SERVICE_FILE <<EOL
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment=\"PATH=\$PATH\"

[Install]
WantedBy=default.target
EOL"

# Reload systemd, enable and start Ollama service
echo "Reloading systemd daemon and enabling Ollama service..."
sudo systemctl daemon-reload
sudo systemctl enable ollama

echo "Starting Ollama service..."
sudo systemctl start ollama

# Verify if Ollama is running
echo "Checking Ollama status..."
sudo systemctl status ollama

echo "Ollama installation and service setup completed."
