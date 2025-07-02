#!/usr/bin/env python3
# This script retrieves the Windows host's private IP address from WSL using the `ip route` command.
# It checks if the IP is a private address (10.x.x.x, 172.16.x.x - 172.31.x.x, or 192.168.x.x)
# and returns it.
# In WSL, the windows host IP is typically in the range 172.16.x.x - 172.31.x.x,
# but this can vary based on your network configuration.

import subprocess
import re


def get_windows_host_ip():
    try:
        # Run `ip route` and get the output
        result = subprocess.check_output(["ip", "route"]).decode("utf-8")

        # Look for the 'default via' line
        for line in result.splitlines():
            if line.startswith("default via"):
                parts = line.split()
                ip = parts[2]

                # Manual regex-based private IP check
                if (
                    re.match(r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)
                    or re.match(r"^172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}$", ip)
                    or re.match(r"^192\.168\.\d{1,3}\.\d{1,3}$", ip)
                ):
                    return ip
                else:
                    print(f"Rejected non-private IP: {ip}")
                    return None

        print("No 'default via' line found in `ip route` output.")
        return None

    except Exception as e:
        print(f"Error determining Windows host IP: {e}")
        return None


# Example usage:
"""
windows_ip = get_windows_host_ip()
if windows_ip:
    print(f"Windows Host IP: {windows_ip}")
else:
    print("Failed to find a valid private IP.")
"""
