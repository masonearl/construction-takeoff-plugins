#!/bin/sh
set -eu
if [ "$(uname -s)" != Darwin ]; then
  echo 'Takeoff X requires a local macOS session with the Takeoff X companion installed.' >&2
  exit 69
fi
companion="$HOME/.local/bin/takeoff-mcp"
if [ ! -x "$companion" ]; then
  echo 'Takeoff X companion is missing. In Takeoff X open 3D Model > AI tools, export AI setup, and follow its installation instructions. Expected ~/.local/bin/takeoff-mcp.' >&2
  exit 69
fi
export TAKEOFF_MCP_ENABLE_LEGACY_WRITES=0
exec "$companion"
