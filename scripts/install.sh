#!/bin/bash

set -e

# Configuration
BINARY_NAME="forge"
# REPLACE THIS WITH YOUR ACTUAL HOSTED BINARY URL
DOWNLOAD_URL_BASE="https://github.com/milan/forge/releases/latest/download"
INSTALL_DIR="/usr/local/bin"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Installing Forge...${NC}"

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     OS_TYPE=linux;;
    Darwin*)    OS_TYPE=mac;;
    *)          echo -e "${RED}OS not supported: ${OS}${NC}"; exit 1;;
esac

echo "Detected OS: ${OS_TYPE}"

# Construct Download URL (Assumes binaries are named forge-linux or forge-mac)
DOWNLOAD_URL="${DOWNLOAD_URL_BASE}/${BINARY_NAME}-${OS_TYPE}"

# Check for curl
if ! command -v curl &> /dev/null; then
    echo -e "${RED}Error: curl is required to install Forge.${NC}"
    exit 1
fi

# Download
echo "Downloading binary from ${DOWNLOAD_URL}..."
# In a real scenario, use -f to fail on 404, but for now we might fail since URL is placeholder
curl -fsSL "${DOWNLOAD_URL}" -o "${BINARY_NAME}" || { echo -e "${RED}Download failed. Check the URL.${NC}"; exit 1; }

# Make Executable
chmod +x "${BINARY_NAME}"

# Install
echo "Installing to ${INSTALL_DIR} (requires sudo)..."
if [ -w "${INSTALL_DIR}" ]; then
    mv "${BINARY_NAME}" "${INSTALL_DIR}/${BINARY_NAME}"
else
    sudo mv "${BINARY_NAME}" "${INSTALL_DIR}/${BINARY_NAME}"
fi

# Verification
if command -v "${BINARY_NAME}" &> /dev/null; then
    echo -e "${GREEN}Success! Forge installed.${NC}"
    echo "Run '${BINARY_NAME}' to start."
else
    echo -e "${RED}Installation failed. '${BINARY_NAME}' not found in PATH.${NC}"
    exit 1
fi
