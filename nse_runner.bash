#!/bin/bash

# Usage:
# ./nse_runner.sh <ip_address> <script_name>

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <ip_address> <script_name>"
    exit 1
fi

IP="$1"
SCRIPT="$2"

echo "Running NSE script '$SCRIPT' against $IP..."
nmap --script "$SCRIPT" "$IP"