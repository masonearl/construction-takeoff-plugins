# Construction Takeoff

Load plan PDFs into new projects through native review, inspect saved construction projects, review quantities and calibration, trace plan linework, and prepare model, calculation and estimate proposals. Supported changes are reviewed and applied inside Construction Takeoff with Undo. Proposal creation does not submit a bid or modify the saved project.

## Setup

Construction Takeoff for macOS and its separately installed MCP companion are required. In Construction Takeoff, open 3D Model → AI tools, export AI setup and follow its companion instructions. The expected executable is ~/.local/bin/takeoff-mcp. [Get Construction Takeoff for Mac](https://apps.apple.com/us/app/construction-takeoff/id6751007895?mt=12) · [Documentation](https://www.masonearl.com/pages/documentation.html#construction-takeoff). Plugin workflows require a build that includes AI setup/companion export; compatibility with the current App Store release has not yet been verified.

Install this package through Cursor or copy the folder into ~/.cursor/plugins/local/construction-takeoff. Reload Cursor.

Save your project before asking the AI to inspect it. Start with: “Use Construction Takeoff health and capabilities, then list my saved projects. Do not make changes.” Prefer native quantity exports and report calibration, source revisions and coverage gaps.

## Reviewed gas workflows

Guidance covers reviewed PDF import, scale proposals, paged results, project metadata proposals, gas-line tracing and the natural-gas calculation library (MAS-59–64). Availability depends on the tools and argument schemas returned by the installed companion. If a workflow is missing, update the app, reinstall its exported companion, update this plugin and reload the client. `companion-requirements.json` records the expected interfaces for release checks. Native Apply/Undo and plan accuracy require separate testing.

## What runs and what is shared

The package starts the separately installed companion. The launcher does not download code, send network requests or collect analytics. MCP results are sent to your chosen AI client and may be processed by its provider. The companion reads saved projects and creates local proposals/outputs. The launcher disables legacy direct writes; native review owns project changes and Undo. See [privacy](PRIVACY.md).

This preview has not been approved by any store. Disable any older takeoff-x-local installation before enabling this package to avoid duplicate tools. Website: https://www.masonearl.com/pages/documentation.html#construction-takeoff. Source and release status: https://github.com/masonearl/construction-takeoff-plugins. Contact: hi@masonearl.com. MIT applies to plugin files only; the app and companion remain separately licensed.
