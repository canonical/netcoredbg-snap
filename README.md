# NetCoreDbg Snap

[![Get it from the Snap Store](https://snapcraft.io/en/dark/install.svg)](https://snapcraft.io/netcoredbg)

This repository contains the snap packaging for [NetCoreDbg](https://github.com/Samsung/netcoredbg), a managed code debugger with GDB/MI, VSCode DAP and CLI interfaces for CoreCLR.

## Supported Architectures

This snap supports the following architectures:
- **amd64** (x86_64)
- **arm64** (aarch64)

## Repository Structure

- `snap/` - Snap packaging files
  - `snapcraft.yaml.template` - Template snapcraft YAML file with placeholders for dynamic values
- `.github/workflows/` - CI/CD automation
  - `build-stable-snap.yml` - Builds and publishes stable releases for both architectures
  - `build-edge-snap.yml` - Builds and publishes edge releases from upstream master
- `eng/` - Engineering scripts
  - `snap_store_has_latest.py` - Version checking script for Snap Store channels
- `Makefile` - Build automation for snap packaging

## Prerequisites

- **make** - Build automation tool
- **snapcraft** - Snap packaging tool
- **curl** - For fetching latest version from GitHub
- **jq** - For parsing JSON responses

Install dependencies on Ubuntu:
```bash
sudo apt install make snapcraft curl jq
```

## Building the Snap

### Build with Latest Version from GitHub

The build system will automatically fetch the latest release version from GitHub:

```bash
make
```

### Build with Specific Version

Override the version using make variables:

```bash
make VERSION=3.1.3-1062
```

### Customize Snap Grade and Confinement

You can also override the snap grade, confinement, and build type:

```bash
make GRADE=devel CONFINEMENT=devmode BUILD_TYPE=Debug
```

**Default values:**
- `VERSION`: Fetched automatically from GitHub
- `GRADE`: `stable`
- `CONFINEMENT`: `classic`
- `BUILD_TYPE`: `Release`

### Build Examples

Development build with all options:
```bash
make VERSION=3.2.0-1100 GRADE=devel CONFINEMENT=devmode BUILD_TYPE=Debug
```

Production build (uses defaults):
```bash
make
```

## Build Process

The build system performs the following steps:

1. **fetch-version** - Queries GitHub API for the latest release tag (if version not specified)
2. **generate-snapcraft** - Generates `snap/snapcraft.yaml` from the template with token replacements:
   - `{{VERSION}}` → NetCoreDbg version
   - `{{GRADE}}` → Snap grade (stable/devel)
   - `{{CONFINEMENT}}` → Snap confinement (classic/devmode/strict)
   - `{{BUILD_TYPE}}` → CMake build type (Release/Debug)
3. **pack** - Runs `snapcraft pack --verbose` to build the snap package

The generated snapcraft.yaml includes platform definitions for both amd64 and arm64 architectures.

## Cleaning Generated Files

Remove generated files:

```bash
make clean
```

## Manual Snap Build

If you prefer to build without make:

1. Edit `snap/snapcraft.yaml.template` and replace tokens manually
2. Save as `snap/snapcraft.yaml`
3. Run `snapcraft pack`

## Installing the Built Snap

After building, install the snap locally:

```bash
sudo snap install --dangerous --classic netcoredbg_*.snap
```

## License

This packaging follows the same license as NetCoreDbg (MIT License).
