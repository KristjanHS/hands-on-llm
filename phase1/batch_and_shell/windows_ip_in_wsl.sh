#!/bin/bash
# This script retrieves the Windows host's private IP address from WSL using the `ip route` command.
# It checks if the IP is a private address (10.x.x.x, 172.16.x.x - 172.31.x.x, or 192.168.x.x) and returns it.
# In WSL, the windows host IP is typically in the range 172.16.x.x - 172.31.x.x, but this can vary based on your network configuration.

get_windows_host_ip() {
    # Extract the IP address from the default route
    local ip
    ip=$(ip route | awk '/^default via/ {print $3}')

    if [[ -z "$ip" ]]; then
        echo "No default route found" >&2
        return 1
    fi

    # Manual private IP range check (same logic as Python version)
    if [[ "$ip" =~ ^10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ||
          "$ip" =~ ^172\.(1[6-9]|2[0-9]|3[0-1])\.[0-9]{1,3}\.[0-9]{1,3}$ ||
          "$ip" =~ ^192\.168\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        echo "$ip"
        return 0
    else
        echo "Invalid or non-private IP: $ip" >&2
        return 2
    fi
}

# Example usage
host_ip=$(get_windows_host_ip)
if [[ $? -eq 0 ]]; then
    echo "Windows Host IP: $host_ip"
else
    echo "Failed to get valid Windows IP."
fi
