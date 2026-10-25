#!/bin/sh
set -eu
if [ "$(uname -s)" != Darwin ]; then
  echo 'takeoff.bid requires a local macOS session with the takeoff.bid companion installed.' >&2
  exit 69
fi
companion="$HOME/.local/bin/takeoff-mcp"
if [ ! -x "$companion" ]; then
  echo 'takeoff.bid companion is missing. In takeoff.bid open 3D Model > AI tools, export AI setup, and follow its installation instructions. Expected ~/.local/bin/takeoff-mcp.' >&2
  exit 69
fi
export TAKEOFF_MCP_ENABLE_LEGACY_WRITES=0
exec "$companion"
