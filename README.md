# NetCoreDbg Snap

This repository contains the snap packaging for [NetCoreDbg](https://github.com/Samsung/netcoredbg), a managed code debugger with GDB/MI, VSCode DAP and CLI interfaces for CoreCLR.

## Repository Structure

- `snap/` - Snap packaging files
  - `snapcraft.yaml.template` - Template snapcraft YAML file with placeholders for dynamic values
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

You can also override the snap grade and confinement:

```bash
make GRADE=devel CONFINEMENT=devmode
```

**Default values:**
- `VERSION`: Fetched automatically from GitHub
- `GRADE`: `stable`
- `CONFINEMENT`: `classic`

### Build Examples

Development build with all options:
```bash
make VERSION=3.2.0-1100 GRADE=devel CONFINEMENT=devmode
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
3. **pack** - Runs `snapcraft pack --verbose` to build the snap package

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
