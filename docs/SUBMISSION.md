# Store submission preparation

Status: Cursor publisher application submitted October 7, 2026; awaiting review. Publisher: Mason Earl / @masonearl. MIT covers plugin files only. The dedicated plugin repository is public; application source remains private. Claude and Codex submissions remain outstanding.

## Listing copy

Name: Construction Takeoff

Short description: Construction takeoffs and estimates with native review.

Description: Inspect saved Construction Takeoff projects, review quantities and calibration, trace plan linework, and prepare model, calculation and estimate proposals. Apply supported changes through Construction Takeoff's native review with Undo. Requires macOS, the separately installed Construction Takeoff app, and its MCP companion. Saved project state only; no automatic bid submission.

Support: hi@masonearl.com and repository Issues. Icon: shared/assets/icon.png. Privacy: repository PRIVACY.md. Screenshots must come from a synthetic demonstration project, never customer drawings.

## Submission routes

- Cursor: https://cursor.com/marketplace/publish — public GitHub repository, root `.cursor-plugin/marketplace.json`, plugin at `packages/cursor`. Confirm current form fields before submission. [Official reference](https://prod.cursor.com/docs/reference/plugins).
- Grok Bot: same Cursor marketplace publish — https://cursor.com/marketplace/publish — using this Cursor-format package (`packages/grok-bot`) or `packages/cursor`. Grok Bot installs marketplace plugins through Cursor in-app Plugins; there is no separate official grok-only plugin schema for this stdio companion. [x.ai/bot/marketplace](https://x.ai/bot/marketplace) is a Bot Template marketplace and is a later, separate step if a shareable bot template is desired. Cloud-only Grok Bot sessions cannot reach the Mac companion; do not advertise cloud support until a bridge exists. RC status; the separately installed Mac companion remains required.
- Claude Code/Cowork: https://clau.de/plugin-directory-submission — root `.claude-plugin/marketplace.json`, plugin at `packages/claude`. Validate Code and Cowork independently; a schema-valid package does not prove Cowork can reach the Mac's companion. [Official guide](https://claude.com/resources/articles/build-plugins-for-claude).
- Claude Desktop chat: `.mcpb` is an optional local installer only. [Current Anthropic directory rules](https://claude.com/docs/directory/publish) no longer accept Desktop extension submissions. Submit the Claude plugin bundle through https://claude.ai/directory/manage instead. Local MCP entries are ignored by chat; full cross-surface tools require a remote MCP service.

- Codex: [OpenAI plugin submission](https://developers.openai.com/plugins/deploy/submission). The current package is local stdio. Public directory requirements currently call for a remote HTTPS endpoint or contact with OpenAI for local MCP support. Do not submit this as skills-only: that would omit its core dependency. A hosted endpoint requires a separate authenticated service design and verified developer/domain identity. [Packaging rules](https://developers.openai.com/plugins/build/plugins).

## Required before submission

- [ ] Stable Construction Takeoff app/companion release, public onboarding/download URL and minimum compatible version.
- [ ] Reviewer access to the app plus a synthetic sample project.
- [ ] In each host: install from clean user state, health, capabilities, project list, inspect quantities, create proposal, native review/apply, Undo, save and stale-revision rejection.
- [ ] Desktop: first-run directory picker, paths with spaces, disconnect/reconnect, missing companion error, uninstall.
- [ ] Cowork: establish actual host filesystem/process access or implement a supported remote connection. Do not advertise support before this passes.
- [ ] Grok Bot: marketplace or in-app install from a local Mac session with the companion present. Do not claim cloud Grok Bot support without a verified bridge.
- [ ] Fresh screenshots and publisher verification in each directory portal.
- [ ] Codex: remote HTTPS deployment and authentication OR explicit provider approval for local MCP.
- [ ] Submit the appropriate artifact and record receipt IDs/status. Do not change application repository visibility.

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

## Public website

Published October 7, 2026:
- Documentation: https://www.masonearl.com/pages/documentation.html#construction-takeoff
- Setup: https://www.masonearl.com/pages/construction-takeoff/plugin.html
- Support: https://www.masonearl.com/pages/construction-takeoff/support.html
- Privacy: https://www.masonearl.com/pages/construction-takeoff/privacy.html
- Plugin license/terms: https://www.masonearl.com/pages/construction-takeoff/terms.html
- Local Codex preview: https://www.masonearl.com/assets/construction-takeoff-plugin/construction-takeoff-codex-0.1.3.zip

These describe local stdio honestly; no hosted service is advertised. The download
contains a local marketplace catalog so it can be installed without source-repo access.

## Submission attempt, October 7, 2026

Opened https://platform.openai.com/plugins under Mason Earl / Default project.
Upload was blocked before file selection with “You need a verified developer
identity before you can create or upload a plugin.” Organization settings showed
Individual verification Approved, but returning to the portal produced the same
block. No ZIP was uploaded, no submission ID exists, and no approval is claimed.
The publisher identity discrepancy needs resolution in OpenAI Platform. Do not
bypass the gate or submit as skills-only to hide the MCP dependency.

Remaining technical requirements: supported public MCP transport/connection,
synthetic native app review/apply/Undo acceptance, screenshots and video walkthrough.
The current local companion is not a cloud endpoint. A hosted bridge needs
user authentication, device pairing and explicit project scope before deployment.

## Tool coverage verification

`python3 scripts/audit_tools.py` checks the actual packaged launcher's inventory
against eight workflow groups: connection, projects, plans, models, quantities,
calculations, estimates and renderings. The current companion exposes 32 tools.
Sheet import/calibration and proposal application are native-app operations.
Legacy project creation/job linking are disabled by the plugin. Do not describe
the inventory as complete native UI parity or automatic full-plan takeoff.

66 companion unit tests, seven packaging tests, and official MCP SDK 2.2.0
negotiation/discovery/proposal/native-snapshot tests passed. The audit caught and
fixed false read-only annotations for rendering proposals/exports and sheet image
rendering in the companion source. This Mac's companion was backed up and updated;
those changes still need inclusion in the next signed app release. Full native
acceptance and public provider acceptance are not established by these tests.


## Claude review preparation — 2026-10-07

Version 0.1.4 replaces the Claude Node wrapper with `/bin/sh` and a literal
`${CLAUDE_PLUGIN_ROOT}/server/start.sh` argument. The shell script performs no
downloads or package installation and execs the separately installed companion.
That external executable can still require manual review; this is not a claim
that the directory policy hold is resolved.

The directory explains that documentationUrl, privacyPolicyUrl, supportUrl and
termsOfServiceUrl are listing-only fields and need no action. Keep all four.

Data disclosure: reads and stores (local proposals/outputs can retain personal
information from projects); no additional service called by skills; no
developer-operated service retains data; local outputs remain until deleted.
Explain local retention in reviewer notes rather than implying all data is
ephemeral. Intended for professional use, not specifically for under-18 users.
Continue the existing draft; do not create a duplicate submission.
