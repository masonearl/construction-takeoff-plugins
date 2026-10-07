# Codex release preparation — October 7, 2026

This is a tested local macOS plugin candidate, not an approved public listing.
The plugin-only repository is public for Cursor review; application source remains private. Other client packaging is being developed
in the same repository; preserve those changes.

## Added in this pass

- Codex first-run connection skill registered through `onboardingSkill`.
- Accurate capability labels, starter prompts and saved-state disclosure.
- Five positive and three negative reviewer scenarios embedded in the manifest.
- Reusable isolated stdio verification against the packaged launcher and installed
  companion; checks reviewer tool names, health and capability discovery.
- Offline submission preflight with nonzero exit when known requirements are missing.

## Verification

Seven distribution/preflight tests passed. A fresh temporary Codex configuration
accepted the marketplace and installed the package. That installed package completed
MCP initialization and discovered 32 tools with direct writes disabled. The empty
project test directory remained unchanged. The existing plugin in the active chat
also returned successful health and capabilities; this does not verify the new
onboarding skill's execution in the desktop UI.

Run from this repository:

```sh
python3 scripts/build.py
python3 -m unittest discover -s tests -v
python3 scripts/verify_codex_connection.py
python3 scripts/audit_tools.py --require-mcp-workflows
python3 scripts/check_codex_submission.py
```

The last command currently fails intentionally with concrete submission blockers.
The MCP workflow audit separately requires the MAS-59–64 companion interfaces.
A working connection with an older companion does not pass that feature gate;
see `docs/VALIDATION.md` for the installed-companion result. Update the app and
companion before retrying it; changing only the plugin cannot add missing tools.
Its offline success would not prove endpoint reachability, publisher identity,
reviewer acceptance, or store approval. It does not contact or submit to OpenAI.

## Work required for the public directory

1. Resolve the transport route: the documented MCP portal flow connects a hosted
   endpoint and verifies its domain. This package launches local stdio. Obtain
   explicit local-plugin distribution support or build a hosted authenticated
   bridge with user pairing and explicit project scope. A public tunnel to the
   current companion is not an authenticated multi-user integration.
2. Establish public product/download, support, privacy and terms pages. The plugin repository provides public support and privacy pages.
   A dedicated terms page remains required. OpenAI ZIP submission itself does not
   require public source.
3. Prepare a synthetic reviewer project and execute all scenarios. Record native
   proposal review/apply/Undo and stale-revision handling in the real Mac app.
4. Add genuine screenshots and walkthrough URL, then complete publisher/domain
   verification, upload the ZIP and resolve portal findings. Reviewer credentials
   belong only in the portal. Never package them.
5. Submit for review and publish after approval. A submission date is controllable;
   an approval date is not promised by the documentation.

Official source checked October 7, 2026:
https://developers.openai.com/plugins/deploy/submission

The scenarios describe expected behavior, not completed acceptance tests. The
fixture, video and hosted service have not been created by this packaging pass.
