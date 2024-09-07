#!/bin/bash

# Define variables
SERVICE_FILE="/etc/systemd/system/ollama.service"
OLLAMA_BIN_PATH="$(which ollama)"
OLLAMA_INSTALL_DIR="/usr/share/ollama"

# Stop and disable the Ollama service
echo "Stopping and disabling Ollama service..."
sudo systemctl stop ollama
sudo systemctl disable ollama

# Remove the Ollama service file
if [ -f "$SERVICE_FILE" ]; then
    echo "Removing Ollama service file..."
    sudo rm "$SERVICE_FILE"
else
    echo "Ollama service file not found."
fi

# Reload systemd to apply changes
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Remove the Ollama binary
if [ -f "$OLLAMA_BIN_PATH" ]; then
    echo "Removing Ollama binary from $OLLAMA_BIN_PATH..."
    sudo rm "$OLLAMA_BIN_PATH"
else
    echo "Ollama binary not found."
fi

# Remove Ollama installation directory
if [ -d "$OLLAMA_INSTALL_DIR" ]; then
    echo "Removing Ollama installation directory at $OLLAMA_INSTALL_DIR..."
    sudo rm -r "$OLLAMA_INSTALL_DIR"
else
    echo "Ollama installation directory not found."
fi

# Remove the Ollama user and group
echo "Removing Ollama user and group..."
sudo userdel ollama
sudo groupdel ollama

echo "Ollama has been successfully removed."
