---
name: get-started
description: Connect and troubleshoot the Construction Takeoff macOS companion in Codex. Use on first installation or when the user asks to connect Construction Takeoff, verify its connection, or fix unavailable Construction Takeoff tools.
---

# Connect Construction Takeoff

1. Call `health` and `get_capabilities`. These are read-only. Check the reported
   transport, companion version, project-library availability, and capability gaps.
   An installed plugin or successful file export alone does not verify a connection.
2. If tools are unavailable, explain that this package requires a local macOS
   session and the separately installed Construction Takeoff companion. In Construction Takeoff open
   **AI → Connect your AI tools → Export AI setup**, run the exported Codex
   installation command, then start a new Codex chat. Do not install dependencies
   silently, edit client credentials, or enable legacy direct writes.
3. If health succeeds, report that this chat reached the companion. Explain that
   it reads saved projects; ask the user to save in the app before inspecting
   recent edits. An empty library can mean the configured folder is wrong. Do not
   create, move, reset, or delete project storage to repair discovery.
4. For a connection-only request, stop after reporting the result and any missing
   prerequisites. When the user asks to inspect projects, call `list_projects`,
   resolve the requested project, and follow the takeoff-workflow skill.

Local stdio does not provide cloud access. Do not claim cloud compatibility,
store approval, live unsaved state, or complete estimating coverage from health.
Proposals require native review; connection setup does not authorize project edits.
Never include project names, drawing content, credentials, or full local paths in
public support reports unless the user explicitly requests those details.
