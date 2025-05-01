#!/bin/bash
# Script to install TA-Lib C library and Python wrapper
# This script requires sudo privileges

# Exit on error
set -e

echo "Installing TA-Lib dependencies..."
sudo apt-get update
sudo apt-get install -y build-essential wget

echo "Downloading and extracting TA-Lib source..."
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/

echo "Configuring and building TA-Lib..."
./configure --prefix=/usr
make

echo "Installing TA-Lib to system..."
sudo make install

# Create symbolic link if needed
if [ ! -f /usr/lib/libta_lib.so ]; then
    echo "Creating symbolic link for libta_lib.so..."
    sudo ln -s /usr/lib/libta_lib.so.0 /usr/lib/libta_lib.so
fi

# Clean up downloaded files
cd ..
rm -rf ta-lib-0.4.0-src.tar.gz

echo "Installing Python TA-Lib wrapper..."
pip install ta-lib

echo "TA-Lib installation completed successfully!"