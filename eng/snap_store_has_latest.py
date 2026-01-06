#!/usr/bin/env python3
"""
Check if the Snap Store version matches the latest GitHub release version.
Returns EXIT_SUCCESS (0) if versions match, EXIT_FAILURE (1) otherwise.
"""

import sys
import json
import urllib.request
import urllib.error
import socket
import http.client


def get_github_latest_version():
    """Fetch the latest release version from GitHub."""
    url = "https://api.github.com/repos/samsung/netcoredbg/releases/latest"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data.get("tag_name", "").strip()
    except urllib.error.URLError as e:
        print(f"Error fetching GitHub release: {e}", file=sys.stderr)
        return None


class UnixSocketHTTPConnection(http.client.HTTPConnection):
    """HTTP connection over Unix socket."""

    def __init__(self, socket_path):
        super().__init__("localhost")
        self.socket_path = socket_path

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.socket_path)


def get_snap_store_version():
    """Fetch the current version from Snap Store using snapd API."""
    socket_path = "/run/snapd.socket"

    try:
        conn = UnixSocketHTTPConnection(socket_path)
        conn.request("GET", "/v2/snaps/netcoredbg")
        response = conn.getresponse()

        if response.status != 200:
            print(f"Error: snapd API returned status {response.status}", file=sys.stderr)
            return None

        data = json.loads(response.read().decode())

        # Get the installed snap version
        if data.get("type") == "sync" and "result" in data:
            result = data["result"]
            version = result.get("version", "").strip()

            # Also check tracking channel
            channel = result.get("channel", "")
            print(f"Installed from channel: {channel}")

            return version

        return None
    except (socket.error, OSError) as e:
        print(f"Error connecting to snapd socket: {e}", file=sys.stderr)
        return None
    except (json.JSONDecodeError, http.client.HTTPException) as e:
        print(f"Error fetching Snap info: {e}", file=sys.stderr)
        return None


def main():
    """Main function to compare versions."""
    print("Fetching latest GitHub release version...")
    github_version = get_github_latest_version()

    if not github_version:
        print("Failed to fetch GitHub version", file=sys.stderr)
        return 1

    print(f"GitHub version: {github_version}")

    print("Fetching installed snap version...")
    snap_version = get_snap_store_version()

    if not snap_version:
        print("Failed to fetch snap version (is netcoredbg snap installed?)", file=sys.stderr)
        return 1

    print(f"Installed snap version: {snap_version}")

    if github_version == snap_version:
        print("✓ Versions match - Snap Store has the latest netcoredbg version")
        return 0

    print("✗ Versions differ - Snap Store does NOT have the latest netcoredbg version")
    return 1


if __name__ == "__main__":
    sys.exit(main())
