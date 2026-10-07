---
name: get-started
description: Connect and troubleshoot the Construction Takeoff macOS companion in Codex. Use on first installation or when the user asks to connect Construction Takeoff, verify its connection, or fix unavailable Construction Takeoff tools.
---

# Connect Construction Takeoff

1. Call `health` and `get_capabilities`. These are read-only. Check the reported
   transport, companion version, capability `available`/`unavailable_reason` values,
   and gaps. Tools come from the installed companion, not the plugin version.
   An installed plugin or successful file export alone does not verify a connection.
2. If tools are unavailable, explain that this package requires a local macOS
   session and the separately installed Construction Takeoff companion. In Construction Takeoff open
   **AI → Connect your AI tools → Export AI setup**, run the exported Codex
   installation command, then start a new Codex chat. Updating the plugin alone
   cannot add tools to an older companion; update the app and companion too.
   Do not install dependencies
   silently, edit client credentials, or enable legacy direct writes.
3. If health succeeds, report that this chat reached the companion. Explain that
   it reads saved projects; ask the user to save in the app before inspecting
   recent edits. An empty library can mean the configured folder is wrong. Do not
   create, move, reset, or delete project storage to repair discovery.
4. For a connection-only request, stop after reporting the result and any missing
   prerequisites. When the user asks to inspect projects, call `list_projects`,
   resolve the requested project, and follow the takeoff-workflow skill. To load
   new plan PDFs, follow its plan-import section; if `propose_project_import` is
   missing, report the compatibility gap and update/re-export the companion.

For newer gas workflows, check the advertised tools before promising support:
`propose_project_import`, `suggest_page_scales`, `propose_page_scales`,
`propose_project_metadata`, `propose_calculation_library`, plus paging and gas-tracing
arguments on existing tools. Report missing workflows precisely; successful health
alone does not verify all six capabilities.

Local stdio does not provide cloud access. Do not claim cloud compatibility,
store approval, live unsaved state, or complete estimating coverage from health.
Proposals require native review; connection setup does not authorize project edits.
Never include project names, drawing content, credentials, or full local paths in
public support reports unless the user explicitly requests those details.

Official Mac application: [Construction Takeoff on the Mac App Store](https://apps.apple.com/us/app/construction-takeoff/id6751007895?mt=12). Documentation: https://www.masonearl.com/pages/documentation.html. If the installed version lacks AI setup export, report the compatibility gap instead of claiming installation is complete.
