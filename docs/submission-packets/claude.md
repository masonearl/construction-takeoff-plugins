# Claude directory submission packet

Copy these values into https://claude.ai/directory/manage. Do not submit from this packet. Mason must sign in, validate in the portal, and submit.

Version in the package: 0.1.7. Plugin path: `packages/claude`.

The directory listing name comes from `displayName` in `.claude-plugin/plugin.json`. That field is takeoff.bid. The machine id `name` is takeoff-bid because Claude requires kebab-case (`^[a-z][a-z0-9]*(-[a-z0-9]+)*$`) and rejects dots.

Local stdio MCP runs in Claude Code and Cowork, not claude.ai.

## Listing fields

Name (displayName):

```
takeoff.bid
```

Plugin id (`name`):

```
takeoff-bid
```

Short description (plugin.json `description`):

```
Load plan sets, inspect takeoff.bid projects and prepare reviewed takeoff and estimating changes. Requires the separately installed macOS app and MCP companion.
```

Long description (README listing text):

```
Load plan PDFs into new projects through native review, inspect saved construction projects, review quantities and calibration, trace plan linework, and prepare model, calculation and estimate proposals. Supported changes are reviewed and applied inside takeoff.bid with Undo. Proposal creation does not submit a bid or modify the saved project. Requires macOS, takeoff.bid for Mac, and its separately installed MCP companion. Saved project state only.
```

Category:

```
Productivity
```

Website / documentation:

```
https://www.masonearl.com/pages/construction-takeoff/plugin.html
```

Support:

```
https://www.masonearl.com/pages/construction-takeoff/support.html
```

Privacy:

```
https://www.masonearl.com/pages/construction-takeoff/privacy.html
```

Terms:

```
https://www.masonearl.com/pages/construction-takeoff/terms.html
```

Homepage (App Store):

```
https://apps.apple.com/us/app/construction-takeoff/id6751007895?mt=12
```

Contact email:

```
hi@masonearl.com
```

Author:

```
Mason Earl
```

Repository:

```
https://github.com/masonearl/construction-takeoff-plugins
```

Plugin path in the repository:

```
packages/claude
```

License:

```
MIT
```

## Three example prompts

1.

```
Use takeoff.bid health and capabilities, then list my saved projects. Do not make changes.
```

2.

```
Load the Cedar Ridge Pump Station 25-100001 plan PDFs into a new takeoff project and tell me how to apply the import in native review.
```

3.

```
Inspect calibration and quantities in takeoff.bid Reviewer Demo, then prepare one reviewed model change. Do not apply it.
```

## Release notes

```
0.1.7 lists as takeoff.bid and documents local versus remote tool names, the takeoff-then-estimate loop, and live helpers from companion 0.9.1-dev. Local macOS companion required. This version does not add a hosted MCP service.
```

## Data handling answers

Use these on the Data handling step. They match PRIVACY.md.

- Does the plugin read personal data? Yes. Tool results can include project names, client names, site addresses, quantities, model data, drawings or file paths from saved takeoff.bid projects.
- Does the plugin store personal data? Yes, locally. The companion writes proposal and output files on the user's Mac. Those files have no automatic retention limit and remain until the user deletes them.
- Does the plugin send data to services other than its declared connectors? No additional developer-operated service is called. MCP results enter the user's Claude conversation and may be processed by Anthropic under Claude settings.
- How long is data kept? Local proposals and outputs remain until deleted. Uninstalling the plugin does not delete projects, proposals or the separately installed app.
- Intended for people under 18? No. Professional construction estimating use.

## Reviewer test instructions

Use only the fictional sample library below. Never attach customer drawings.

Sample data:

- Saved project name: takeoff.bid Reviewer Demo
- Demo plan set A: Cedar Ridge Pump Station 25-100001 (synthetic multi-page PDF)
- Demo plan set B: Willow Creek Canal Crossing 25-100002 (synthetic multi-page PDF)
- Expected companion executable: `~/.local/bin/takeoff-mcp`
- Minimum companion version: 0.9.1-dev
- Project library: the saved takeoff.bid library on the review Mac

Steps:

1. Install takeoff.bid for Mac from the App Store. Open 3D Model, AI tools, export AI setup, and install the companion.
2. Save takeoff.bid Reviewer Demo in the project library. Unsaved edits are not visible.
3. Install this plugin from `packages/claude` (marketplace add of this repository, or ZIP upload). Reload Claude Code.
4. Run example prompt 1. Confirm health, capabilities and `list_projects`. The saved demo project should appear. No files should change.
5. Run example prompt 2 with the Cedar Ridge Pump Station PDFs. If `propose_project_import` exists, a checksummed bundle is staged only. Tell the reviewer to apply it in File, Review AI Project Import, then save. If the tool is missing, the plugin must report the gap and must not enable legacy writes.
6. Inspect a sheet. Report calibration, missing quantities and coverage gaps. Do not invent lengths on an uncalibrated sheet.
7. Prepare one supported model or calculation proposal against the inspected revision. Confirm the saved project is unchanged until native review.
8. In takeoff.bid, review, apply, Undo, save, then reread. Send a stale proposal and confirm rejection.
9. Confirm no action submits a bid or writes a bid into old estimating software and old systems.

## Demo video script outline

1. Title card: takeoff.bid Claude plugin, local macOS preview, fictional demo data.
2. Show the App Store app, AI setup export and `takeoff-mcp` present.
3. Install the plugin and reload Claude Code.
4. Prompt 1: health, capabilities, list projects. Show takeoff.bid Reviewer Demo.
5. Prompt 2: stage Cedar Ridge Pump Station import. Show the bundle path and that no project package was created.
6. Apply the bundle in the native Review AI Project Import sheet. Save.
7. Inspect calibration and the native quantity export.
8. Stage one model height change. Show Review AI changes, Apply, Undo.
9. Negative: ask to submit the bid. The plugin refuses.
10. Close on limitations: local Mac only, Cowork host access unverified, not store-approved.

## Human-only checklist (Mason)

- [ ] MASON: Sign in at https://claude.ai/directory/manage on the organization that should own the listing.
- [ ] MASON: Connect the GitHub account that can push to masonearl/construction-takeoff-plugins.
- [ ] MASON: Start or continue the existing draft. Do not create a duplicate submission.
- [ ] MASON: Source: this public repository, plugin path `packages/claude`, default branch unless you choose otherwise.
- [ ] MASON: Run portal Validate. Fix any Blocking findings. Re-validate after each push.
- [ ] MASON: Executable policy hold. `.mcp.json` starts `${CLAUDE_PLUGIN_ROOT}/server/start.sh`, and that script execs the separately installed `~/.local/bin/takeoff-mcp`. Directory rules hold plugins that run a file the validator cannot follow, or an executable outside the plugin folder. Disclose this in reviewer notes. Do not bundle the licensed companion.
- [ ] MASON: Answer data handling and compliance acknowledgements.
- [ ] MASON: Identity, plan and role (Pro, Max, Team Owner, or Directory permission).
- [ ] MASON: Record a demo video from the fictional project and host a reviewer-accessible URL.
- [ ] MASON: Confirm Cowork can or cannot reach the Mac companion before advertising Cowork.
- [ ] MASON: Submit for review only after portal Validate is clean enough to send. Do not publish, tag or release from this packet.
