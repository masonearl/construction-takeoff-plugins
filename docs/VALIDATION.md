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
