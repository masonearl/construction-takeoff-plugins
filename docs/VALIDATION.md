# Release candidate validation — October 7, 2026

- Claude Code strict plugin and marketplace validation passed.
- Anthropic MCPB 2.1.2 manifest validation passed. Icon accepted; validator emitted a recommended-size notice.
- Codex CLI installed and enabled construction-takeoff@construction-takeoff-plugins using an isolated temporary configuration; existing user installation unchanged.
- All four generated launchers completed MCP initialize and tools/list against the installed companion: 32 tools. Temporary empty project root remained unchanged.
- Three distribution tests passed, covering all four launchers' missing-companion diagnostics, stdio forwarding, forced legacy-write disablement, paths with spaces, exit-code propagation, archive integrity and reproducible builds.
- Workflow skill validator passed. Shared AI guidance library refresh indexed active sources with no conflicts; repository workflow instruction content is unchanged from the previously installed Construction Takeoff skill.
- Repository created under masonearl and GitHub private=true verified.

Not yet verified: actual Desktop extension installation/directory picker, Cowork host access, fresh Cursor UI installation of this package, complete proposal/review/apply/Undo in each host, store review and public download/onboarding. The prior local plugin installation is not evidence of directory approval.

Rebuild and revalidate if files change. Tests do not establish estimating completeness or accuracy on real construction projects.

## 0.1.1 follow-up

- Updated submission route: Anthropic no longer accepts new MCPB directory listings. Claude plugin submission is at claude.ai/directory/manage; MCPB remains a manual local option. Chat ignores local MCP plugin entries.
- Replaced Claude inline shell configuration with a packaged readable Node launcher and explicit plugin-root path. Strict Claude validation passes; the external companion dependency remains subject to directory review.
- Added per-platform packaged README files so installed package documentation contains no broken repository-relative links or incorrect install targets.
- Added scripts/smoke.py. All four packages passed health, capabilities, model inspection, proposal creation, stale-revision rejection and saved-project immutability against a synthetic fixture through stdio.
- Claude Desktop preview successfully opened the 0.1.1 MCPB and reported all runtime requirements met. Installation is awaiting user confirmation of the host's computer-access prompt; this is not yet an installed-host pass.
- Claude publisher portal opened, but the browser requires account login. GitHub CLI access as masonearl remains authenticated with repository admin/push permissions.

## 0.1.2 naming correction

Mason requested Construction Takeoff (not the prior product name). Updated plugin IDs, display names, marketplace IDs, artifact filenames, prompts and documentation. The companion executable remains ~/.local/bin/takeoff-mcp for installation compatibility. Older local marketplace references remain only in migration guidance.

Seven distribution/submission tests passed; all four synthetic proposal workflows passed. Codex connection check exposed 32 tools with legacy writes disabled. The user installed the prior 0.1.1 Desktop preview; it remains unconfigured, and the renamed build still needs host installation/configuration.

## 0.1.5 plan import (October 7, 2026)

Natural gas stress test (Enbridge La Hacienda 25-260144, Draper/Sandy Canal Bridge 25-260160) found no way to load plan PDFs through the plugin: `create_project` is a disabled legacy write that never attaches a PDF. Tracked as MAS-59…64 in Linear (label MCP).

- Skill: new "Load plans into a new project" workflow. It searches for an existing project first, stages with `propose_project_import` when the companion provides it, and otherwise falls back to File → New Document… in the app. It never enables legacy writes, and warns that imported pages start uncalibrated and that the scale bar wins over conflicting notes.
- Audit: `EXPECTED` workflows report a warning when the companion predates plan import; `--require-plan-import` makes that a release failure. Fixed `${CLAUDE_PLUGIN_ROOT}` expansion so the Claude package can be audited.
- Smoke: when the tool exists, each package stages a generated rotated PDF, checks that the bundle stays in the temporary proposals folder, that no project package is created, and that the duplicate guard works.
- Results against the installed companion (32 tools): all four packages pass; plan import is reported as not in the companion; the default audit passes with a warning; the strict audit fails as intended.
- Results against companion branch `feature/mcp-project-import` (33 tools, via a temporary HOME): all four packages pass, including plan import; the strict audit passes. The companion's own 70 unit tests pass. Real-plan dry run: La Hacienda staged 8 pages in 0.7 s; Canal Bridge staged 4 files / 21 pages in 2.8 s.
- Claude strict validation and MCPB 2.1.2 validation pass; 9 distribution tests pass.

Not yet available: the app's File → Review AI Project Import… sheet that applies the bundle (MAS-59 part B). Until it ships, a staged bundle cannot be applied, so do not ship 0.1.5 publicly before that app build.
