# Store submission preparation

Status: release candidate, not submitted. Publisher: Mason Earl / GitHub masonearl. MIT covers plugin files only. Keep the repository private during preparation; Cursor submission requires making this plugin-only repository public. Never publish the application repository.

## Listing copy

Name: Takeoff X

Short description: Construction takeoffs and estimates with native review.

Description: Inspect saved Takeoff X projects, review quantities and calibration, trace plan linework, and prepare model, calculation and estimate proposals. Apply supported changes through Takeoff X's native review with Undo. Requires macOS, the separately installed Takeoff X app, and its MCP companion. Saved project state only; no automatic bid submission.

Support: hi@masonearl.com and repository Issues. Icon: shared/assets/icon.png. Privacy: repository PRIVACY.md. Screenshots must come from a synthetic demonstration project, never customer drawings.

## Submission routes

- Cursor: https://cursor.com/marketplace/publish — public GitHub repository, root `.cursor-plugin/marketplace.json`, plugin at `packages/cursor`. Confirm current form fields before submission. [Official reference](https://prod.cursor.com/docs/reference/plugins).
- Claude Code/Cowork: https://clau.de/plugin-directory-submission — root `.claude-plugin/marketplace.json`, plugin at `packages/claude`. Validate Code and Cowork independently; a schema-valid package does not prove Cowork can reach the Mac's companion. [Official guide](https://claude.com/resources/articles/build-plugins-for-claude).
- Claude Desktop chat: submit the `.mcpb` via the Desktop extension directory submission route linked from [Anthropic's local server guide](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop). It wraps an external companion dependency, which must be disclosed to reviewers. Schema validation is not directory approval.
- Codex: [OpenAI plugin submission](https://developers.openai.com/plugins/deploy/submission). The current package is local stdio. Public directory requirements currently call for a remote HTTPS endpoint or contact with OpenAI for local MCP support. Do not submit this as skills-only: that would omit its core dependency. A hosted endpoint requires a separate authenticated service design and verified developer/domain identity. [Packaging rules](https://developers.openai.com/plugins/build/plugins).

## Required before submission

- [ ] Stable Takeoff X app/companion release, public onboarding/download URL and minimum compatible version.
- [ ] Reviewer access to the app plus a synthetic sample project.
- [ ] In each host: install from clean user state, health, capabilities, project list, inspect quantities, create proposal, native review/apply, Undo, save and stale-revision rejection.
- [ ] Desktop: first-run directory picker, paths with spaces, disconnect/reconnect, missing companion error, uninstall.
- [ ] Cowork: establish actual host filesystem/process access or implement a supported remote connection. Do not advertise support before this passes.
- [ ] Fresh screenshots and publisher verification in each directory portal.
- [ ] Codex: remote HTTPS deployment and authentication OR explicit provider approval for local MCP.
- [ ] Make plugin-only repository public after reviewing its exact committed contents; submit and record receipt IDs/status.

## Reviewer script

1. Install the separately supplied Takeoff X app/companion and save a synthetic project.
2. Install this plugin. Ask to run health, capabilities and list_projects. Confirm missing prerequisites produce actionable errors without corrupting the protocol stream.
3. Ask to inspect a sheet and explain its calibration and missing quantities.
4. Ask to prepare one supported edit using the inspected revision. Confirm the project remains unchanged before native review.
5. Review/apply in Takeoff X, Undo, save and reread. Try a stale proposal and confirm rejection.
6. Inspect generated outputs for correct units and source evidence. Confirm no action submits a bid externally.

Do not mark the Linear work complete until Mason confirms QA. Package preparation and public store availability are separate milestones.
