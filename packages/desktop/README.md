# Construction Takeoff

Inspect saved construction projects, review quantities and calibration, trace plan linework, and prepare model, calculation and estimate proposals. Supported changes are reviewed and applied inside Construction Takeoff with Undo. Proposal creation does not submit a bid or modify the saved project.

## Setup

Construction Takeoff for macOS and its separately installed MCP companion are required. The launcher uses Node.js 18 or newer (Claude Desktop supplies Node for extensions). In Construction Takeoff, open 3D Model → AI tools, export AI setup and follow its companion instructions. The expected executable is ~/.local/bin/takeoff-mcp. A public app download is not included in this preview.

Install this MCPB from Claude Desktop Settings → Extensions → Advanced settings, then select your saved project directory. This is an optional local installer, not a new directory submission: Anthropic no longer accepts Desktop extension listings.

Save your project before asking the AI to inspect it. Start with: “Use Construction Takeoff health and capabilities, then list my saved projects. Do not make changes.” Prefer native quantity exports and report calibration, source revisions and coverage gaps.

## What runs and what is shared

The package starts the separately installed companion. The launcher does not download code, send network requests or collect analytics. MCP results are sent to your chosen AI client and may be processed by its provider. The companion reads saved projects and creates local proposals/outputs. The launcher disables legacy direct writes; native review owns project changes and Undo. See [privacy](PRIVACY.md).

This preview has not been approved by any store. Disable any older takeoff-x-local installation before enabling this package to avoid duplicate tools. Source, support and current status: https://github.com/masonearl/construction-takeoff-plugins. Contact: hi@masonearl.com. MIT applies to plugin files only; the app and companion remain separately licensed.
