#!/bin/sh
set -eu
if [ "$(uname -s)" != Darwin ]; then
  echo 'Construction Takeoff requires a local macOS session with the Construction Takeoff companion installed.' >&2
  exit 69
fi
companion="$HOME/.local/bin/takeoff-mcp"
if [ ! -x "$companion" ]; then
  echo 'Construction Takeoff companion is missing. In Construction Takeoff open 3D Model > AI tools, export AI setup, and follow its installation instructions. Expected ~/.local/bin/takeoff-mcp.' >&2
  exit 69
fi
export TAKEOFF_MCP_ENABLE_LEGACY_WRITES=0
exec "$companion"
