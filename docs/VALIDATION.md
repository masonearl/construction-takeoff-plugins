# Release candidate validation — October 7, 2026

- Claude Code strict plugin and marketplace validation passed.
- Anthropic MCPB 2.1.2 manifest validation passed. Icon accepted; validator emitted a recommended-size notice.
- Codex CLI installed and enabled takeoff-x@takeoff-x-plugins using an isolated temporary configuration; existing user installation unchanged.
- All four generated launchers completed MCP initialize and tools/list against the installed companion: 32 tools. Temporary empty project root remained unchanged.
- Three distribution tests passed, covering all four launchers' missing-companion diagnostics, stdio forwarding, forced legacy-write disablement, paths with spaces, exit-code propagation, archive integrity and reproducible builds.
- Workflow skill validator passed. Shared AI guidance library refresh indexed active sources with no conflicts; repository workflow instruction content is unchanged from the previously installed Takeoff X skill.
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
