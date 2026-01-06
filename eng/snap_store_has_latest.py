#!/usr/bin/env python3
"""
Check if the Snap Store version matches the latest GitHub version for a given channel.
Returns EXIT_SUCCESS (0) if versions match, EXIT_FAILURE (1) otherwise.
"""

import sys
import json
import urllib.request
import urllib.error
import socket
import http.client
import argparse


def get_github_latest_release():
    """Fetch the latest release version from GitHub."""
    url = "https://api.github.com/repos/samsung/netcoredbg/releases/latest"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data.get("tag_name", "").strip()
    except urllib.error.URLError as e:
        print(f"Error fetching GitHub release: {e}", file=sys.stderr)
        return None


def get_github_latest_commit():
    """Fetch the latest commit SHA from Samsung/netcoredbg master branch."""
    url = "https://api.github.com/repos/Samsung/netcoredbg/commits/master"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            # Get short SHA (7 chars) to match snap version format
            return data.get("sha", "")[:7]
    except urllib.error.URLError as e:
        print(f"Error fetching upstream commit: {e}", file=sys.stderr)
        return None


class UnixSocketHTTPConnection(http.client.HTTPConnection):
    """HTTP connection over Unix socket."""

    def __init__(self, socket_path):
        super().__init__("localhost")
        self.socket_path = socket_path

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.socket_path)


def get_snap_store_version(channel):
    """Fetch the current version from Snap Store using snapd API find endpoint."""
    socket_path = "/run/snapd.socket"

    try:
        conn = UnixSocketHTTPConnection(socket_path)
        conn.request("GET", "/v2/find?name=netcoredbg")
        response = conn.getresponse()

        if response.status != 200:
            print(f"Error: snapd API returned status {response.status}", file=sys.stderr)
            return None

        data = json.loads(response.read().decode())

        # Get the snap info from store
        if data.get("type") == "sync" and "result" in data:
            results = data["result"]

            # Find netcoredbg snap (exact match)
            for snap in results:
                if snap.get("name") == "netcoredbg":
                    # Get channel information
                    channels = snap.get("channels", {})

                    # Look for the specific channel (e.g., "latest/stable", "latest/edge")
                    channel_key = f"latest/{channel}"
                    if channel_key in channels:
                        version = channels[channel_key].get("version", "").strip()
                        return version
                    else:
                        print(f"Channel {channel_key} not found in store", file=sys.stderr)
                        return None

            print("netcoredbg snap not found in store", file=sys.stderr)
            return None

        return None
    except (socket.error, OSError) as e:
        print(f"Error connecting to snapd socket: {e}", file=sys.stderr)
        return None
    except (json.JSONDecodeError, http.client.HTTPException) as e:
        print(f"Error fetching Snap info: {e}", file=sys.stderr)
        return None


def main():
    """Main function to compare versions."""
    parser = argparse.ArgumentParser(
        description="Check if Snap Store has the latest netcoredbg version for a given channel"
    )
    parser.add_argument(
        "--channel",
        choices=["stable", "edge"],
        default="stable",
        help="Snap channel to check (default: stable)"
    )
    args = parser.parse_args()

    # Get expected version based on channel
    if args.channel == "stable":
        print("Fetching latest GitHub release version...")
        expected_version = get_github_latest_release()
        version_type = "GitHub release"
    else:  # edge
        print("Fetching latest upstream master commit SHA...")
        expected_version = get_github_latest_commit()
        version_type = "Upstream master SHA"

    if not expected_version:
        print(f"Failed to fetch {version_type}", file=sys.stderr)
        return 1

    print(f"{version_type}: {expected_version}")

    print(f"Fetching Snap Store {args.channel} channel version...")
    snap_version = get_snap_store_version(args.channel)

    if not snap_version:
        print(f"Failed to fetch snap version from {args.channel} channel", file=sys.stderr)
        return 1

    print(f"Snap Store {args.channel} version: {snap_version}")

    if expected_version == snap_version:
        print(f"✓ Versions match - Snap Store {args.channel} has the latest netcoredbg version")
        return 0

    print(f"✗ Versions differ - Snap Store {args.channel} does NOT have the latest netcoredbg version")
    return 1


if __name__ == "__main__":
    sys.exit(main())
