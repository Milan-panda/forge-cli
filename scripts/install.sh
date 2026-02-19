#!/bin/bash

set -e

# Configuration
BINARY_NAME="forge"
DOWNLOAD_URL_BASE="https://github.com/Milan-panda/forge-cli/releases/download/v1.0.0/forge"
INSTALL_DIR="/usr/local/bin"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

printf "${GREEN}Installing Forge...${NC}\n"

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     OS_TYPE=linux;;
    Darwin*)    OS_TYPE=mac;;
    *)          printf "${RED}OS not supported: ${OS}${NC}\n"; exit 1;;
esac

echo "Detected OS: ${OS_TYPE}"

# Construct Download URL (Assumes binaries are named forge-linux or forge-mac)
DOWNLOAD_URL="${DOWNLOAD_URL_BASE}/${BINARY_NAME}-${OS_TYPE}"

# Check for curl
if ! command -v curl >/dev/null 2>&1; then
    printf "${RED}Error: curl is required to install Forge.${NC}\n"
    exit 1
fi

# Download
echo "Downloading binary from ${DOWNLOAD_URL}..."
# In a real scenario, use -f to fail on 404, but for now we might fail since URL is placeholder
curl -fsSL "${DOWNLOAD_URL}" -o "${BINARY_NAME}" || { printf "${RED}Download failed. Check the URL.${NC}\n"; exit 1; }

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
if command -v "${BINARY_NAME}" >/dev/null 2>&1; then
    printf "${GREEN}Success! Forge installed.${NC}\n"
    echo "Run '${BINARY_NAME}' to start."
else
    printf "${RED}Installation failed. '${BINARY_NAME}' not found in PATH.${NC}\n"
    exit 1
fi
