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
