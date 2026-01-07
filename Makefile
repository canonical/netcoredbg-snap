# Makefile for netcoredbg snap packaging

# Variables with defaults (can be overridden via command line: make VERSION=X.X.X)
VERSION ?=
GRADE ?= stable
CONFINEMENT ?= classic
BUILD_TYPE ?= Release

# Paths
SNAP_DIR := snap
SNAPCRAFT_TEMPLATE := $(SNAP_DIR)/template.snapcraft.yaml
SNAPCRAFT_YAML := $(SNAP_DIR)/snapcraft.yaml

# Phony targets
.PHONY: all build clean fetch-version generate-snapcraft pack help

# Default target
all: build

# Main build target - depends on all steps
build: fetch-version generate-snapcraft pack
	@echo "Snap package build completed successfully!"

# Fetch latest version from GitHub if VERSION not provided
fetch-version:
ifeq ($(VERSION),)
	@echo "Fetching latest version from GitHub..."
	$(eval VERSION := $(shell curl -s https://api.github.com/repos/samsung/netcoredbg/releases/latest | jq -r '.tag_name'))
	@echo "Latest version: $(VERSION)"
else
	@echo "Using provided version: $(VERSION)"
endif

# Generate snapcraft.yaml from template
generate-snapcraft:
	@echo "Generating snapcraft.yaml with version $(VERSION), grade $(GRADE), confinement $(CONFINEMENT), build type $(BUILD_TYPE)..."
	@cp $(SNAPCRAFT_TEMPLATE) $(SNAPCRAFT_YAML)
	@sed -i 's/{{VERSION}}/$(VERSION)/g' $(SNAPCRAFT_YAML)
	@sed -i 's/{{GRADE}}/$(GRADE)/g' $(SNAPCRAFT_YAML)
	@sed -i 's/{{CONFINEMENT}}/$(CONFINEMENT)/g' $(SNAPCRAFT_YAML)
	@sed -i 's/{{BUILD_TYPE}}/$(BUILD_TYPE)/g' $(SNAPCRAFT_YAML)
	@echo "Generated $(SNAPCRAFT_YAML)"

# Run snapcraft pack
pack:
	@echo "Running snapcraft pack --verbose..."
	snapcraft pack --verbose
	@echo "Snapcraft pack completed!"

# Clean generated files
clean:
	snapcraft clean
	@rm -f $(SNAPCRAFT_YAML)
	@rm -f *.snap
	@echo "Cleaned generated files"

# Help target
help:
	@echo "NetCoreDbg Snap Build System"
	@echo ""
	@echo "Usage:"
	@echo "  make                                    # Build with latest GitHub version"
	@echo "  make VERSION=3.1.3-1062                 # Build with specific version"
	@echo "  make VERSION=3.1.3-1062 GRADE=devel    # Build with custom grade"
	@echo "  make clean                              # Remove generated files"
	@echo ""
	@echo "Variables:"
	@echo "  VERSION     - NetCoreDbg version (default: fetched from GitHub)"
	@echo "  GRADE       - Snap grade (default: stable)"
	@echo "  CONFINEMENT - Snap confinement (default: classic)"
