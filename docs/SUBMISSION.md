# Store submission preparation

Status: release candidate, not submitted. Publisher: Mason Earl / GitHub masonearl. MIT covers plugin files only. Keep both repositories private. A directory requiring public source needs Mason’s explicit exception for this specific repository before changing visibility. OpenAI accepts ZIP submission; do not publish source just to provide listing pages.

## Listing copy

Name: Construction Takeoff

Short description: Construction takeoffs and estimates with native review.

Description: Inspect saved Construction Takeoff projects, review quantities and calibration, trace plan linework, and prepare model, calculation and estimate proposals. Apply supported changes through Construction Takeoff's native review with Undo. Requires macOS, the separately installed Construction Takeoff app, and its MCP companion. Saved project state only; no automatic bid submission.

Support: hi@masonearl.com and repository Issues. Icon: shared/assets/icon.png. Privacy: repository PRIVACY.md. Screenshots must come from a synthetic demonstration project, never customer drawings.

## Submission routes

- Cursor: https://cursor.com/marketplace/publish — public GitHub repository, root `.cursor-plugin/marketplace.json`, plugin at `packages/cursor`. Confirm current form fields before submission. [Official reference](https://prod.cursor.com/docs/reference/plugins).
- Claude Code/Cowork: https://clau.de/plugin-directory-submission — root `.claude-plugin/marketplace.json`, plugin at `packages/claude`. Validate Code and Cowork independently; a schema-valid package does not prove Cowork can reach the Mac's companion. [Official guide](https://claude.com/resources/articles/build-plugins-for-claude).
- Claude Desktop chat: `.mcpb` is an optional local installer only. [Current Anthropic directory rules](https://claude.com/docs/directory/publish) no longer accept Desktop extension submissions. Submit the Claude plugin bundle through https://claude.ai/directory/manage instead. Local MCP entries are ignored by chat; full cross-surface tools require a remote MCP service.

- Codex: [OpenAI plugin submission](https://developers.openai.com/plugins/deploy/submission). The current package is local stdio. Public directory requirements currently call for a remote HTTPS endpoint or contact with OpenAI for local MCP support. Do not submit this as skills-only: that would omit its core dependency. A hosted endpoint requires a separate authenticated service design and verified developer/domain identity. [Packaging rules](https://developers.openai.com/plugins/build/plugins).

## Required before submission

- [ ] Stable Construction Takeoff app/companion release, public onboarding/download URL and minimum compatible version.
- [ ] Reviewer access to the app plus a synthetic sample project.
- [ ] In each host: install from clean user state, health, capabilities, project list, inspect quantities, create proposal, native review/apply, Undo, save and stale-revision rejection.
- [ ] Desktop: first-run directory picker, paths with spaces, disconnect/reconnect, missing companion error, uninstall.
- [ ] Cowork: establish actual host filesystem/process access or implement a supported remote connection. Do not advertise support before this passes.
- [ ] Fresh screenshots and publisher verification in each directory portal.
- [ ] Codex: remote HTTPS deployment and authentication OR explicit provider approval for local MCP.
- [ ] Submit the appropriate artifact and record receipt IDs/status. Keep repositories private unless Mason explicitly authorizes a visibility exception for that repository.

## Reviewer script

1. Install the separately supplied Construction Takeoff app/companion and save a synthetic project.
2. Install this plugin. Ask to run health, capabilities and list_projects. Confirm missing prerequisites produce actionable errors without corrupting the protocol stream.
3. Ask to inspect a sheet and explain its calibration and missing quantities.
4. Ask to prepare one supported edit using the inspected revision. Confirm the project remains unchanged before native review.
5. Review/apply in Construction Takeoff, Undo, save and reread. Try a stale proposal and confirm rejection.
6. Inspect generated outputs for correct units and source evidence. Confirm no action submits a bid externally.

Do not mark the Linear work complete until Mason confirms QA. Package preparation and public store availability are separate milestones.

## Updated portal findings

Claude permits validation/submission from a private GitHub repo but requires public visibility before listing. Connect GitHub with push access in the intended Claude organization. The organization that first submits this repository/folder owns the listing. Team plans require Owner or Directory permission.

The Claude package now starts a readable Node launcher through `${CLAUDE_PLUGIN_ROOT}` rather than an inline shell command, addressing a blocking subfolder command rule. External companion execution still requires transparent disclosure and reviewer acceptance. CLI schema validation cannot replace portal validation.

Sources: https://claude.com/docs/plugins/pre-submission-checklist and https://claude.com/docs/plugins/platform-support.
