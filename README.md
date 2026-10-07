# Takeoff X plugins

Plugin distribution source for construction takeoffs and estimating in Cursor, Codex, Claude Code/Cowork, and Claude Desktop. This repository contains workflow instructions, client manifests and launchers. The Takeoff X app and MCP companion are separately installed and licensed.

**Release candidate: packages prepared; no public directory listing or host certification yet.** macOS local sessions only. Installing a plugin does not install Takeoff X. Cloud agents and Cowork sandbox access to the Mac companion have not been verified.

## Requirements and setup

1. Install Takeoff X. Open **3D Model → AI tools**, export AI setup, and follow its companion installation instructions. This installs `~/.local/bin/takeoff-mcp` with its runtime. The app is currently a prerequisite supplied separately; a public download/onboarding route must be established before store submission.
2. Save a project in the Takeoff project library. Unsaved changes are not visible to the companion.
3. Install the client package below. For Desktop, choose the saved project library directory when prompted. Other clients use the companion's configured/default library (`TAKEOFF_PROJECTS_DIR` can override it in a local launch environment).
4. Reload the client. Ask: “Use Takeoff X health and capabilities, then list my saved projects. Do not make changes.”

| Client | Package | Preview installation |
|---|---|---|
| Cursor | `packages/cursor` | Copy this directory into `~/.cursor/plugins/local/takeoff-x` after backing up any existing plugin; reload Cursor. Public marketplace submission uses this repository's catalog. |
| Claude Code | `packages/claude` | From the repository: `claude plugin marketplace add .` then `claude plugin install takeoff-x@takeoff-x-plugins`. |
| Claude Cowork | Same Claude plugin | Intended for the plugin directory; host access to the separately installed Mac companion still needs verification. |
| Codex | `packages/codex` | From the repository: `codex plugin marketplace add .` then `codex plugin add takeoff-x@takeoff-x-plugins`. Public directory submission is blocked on remote MCP or approved local support. |
| Claude Desktop chat | `dist/takeoff-x-desktop-0.1.1.mcpb` | Open Desktop Settings → Extensions and install the bundle; set the project directory. Optional local installer only; new Desktop extension directory listings are deprecated. It exposes tools but does not install the Code/Cowork skill. |

Avoid enabling the existing `takeoff-x-local` plugin and this preview simultaneously; both register the same companion. Do not overwrite custom settings during migration.

## Workflow

Inspect saved projects, sheets, calibration and quantities; trace plan linework; prepare model, calculation and estimate proposals. Takeoff X's native review applies changes and supplies Undo. The launcher forces legacy direct writes off. A staged proposal is not an applied project change or submitted bid. Use native exported quantities when available and report calibration and coverage gaps.

## Build and verify

Requires Python 3 for packaging/tests; Node 18+ for Desktop launcher tests (the Desktop host provides its runtime).

```sh
python3 scripts/build.py
python3 -m unittest discover -s tests -v
python3 scripts/smoke.py  # requires the separately installed companion
npx --yes @anthropic-ai/mcpb@2.1.2 validate packages/desktop/manifest.json
claude plugin validate packages/claude --strict
```

`dist/` contains three ZIPs, a Desktop MCPB ZIP, and SHA256SUMS. Archives use deterministic timestamps and include only generated package files. Edit `shared/` and rebuild; do not edit `packages/` directly. No private application source, sample customer projects or credentials belong here. The synthetic smoke test creates isolated temporary projects, checks proposal and stale-revision behavior, and removes only its own temporary data. It does not exercise native review/Undo.

See [submission checklist](docs/SUBMISSION.md) and [privacy](PRIVACY.md). Report issues at https://github.com/masonearl/construction-takeoff-plugins/issues or hi@masonearl.com. MIT applies to plugin code and instructions only; see NOTICE.
