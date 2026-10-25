# Codex / OpenAI plugin submission packet

Copy these values into https://platform.openai.com/plugins. Do not upload or submit from this packet. Mason must complete identity checks and the local MCP allowlist request first.

Version in the package: 0.1.7. ZIP: `dist/takeoff-bid-codex-0.1.7.zip`. Layout: files at the ZIP root (`.codex-plugin/plugin.json`, `.mcp.json`, `skills/`, `assets/`, `LICENSE`). No wrapping folder.

The listing name is takeoff.bid (`interface.displayName`, 11 characters, under the 30-character limit). The machine id `name` is takeoff-bid because OpenAI `plugin_name_format` allows only ASCII letters, digits, `_`, or `-`.

This package is local stdio. Public directory MCP setup expects a hosted HTTPS endpoint unless OpenAI allowlists the organization for desktop-only local MCP. Do not submit as skills-only. That would hide the companion.

## Listing fields

Name (displayName, 11 characters):

```
takeoff.bid
```

Short description (30 characters or fewer, 27 characters):

```
Takeoffs with native review
```

Long description:

```
Load plan sets, inspect takeoff.bid projects and prepare reviewed takeoff and estimating changes. Requires the separately installed macOS app and MCP companion. Changes use native review and Undo. Reads reflect saved project state.
```

Developer name:

```
Mason Earl
```

Category:

```
Productivity
```

Website:

```
https://apps.apple.com/us/app/construction-takeoff/id6751007895?mt=12
```

Support:

```
https://www.masonearl.com/pages/construction-takeoff/support.html
```

Privacy:

```
https://www.masonearl.com/pages/construction-takeoff/privacy.html
```

Terms:

```
https://www.masonearl.com/pages/construction-takeoff/terms.html
```

Documentation:

```
https://www.masonearl.com/pages/documentation.html#construction-takeoff
```

Setup:

```
https://www.masonearl.com/pages/construction-takeoff/plugin.html
```

Logo and composer icon (square PNG, 512 x 512):

```
./assets/icon.png
```

Starter prompts (3):

```
Check my takeoff.bid connection.
```

```
Load these plan PDFs into a new takeoff project.
```

```
Inspect calibration and quantities in my saved takeoff.
```

## Five positive test cases

These are already in `shared/codex/review.json` and the generated Codex manifest.

1. Verify a local Mac connection

```
Check my takeoff.bid connection without changing anything.
```

Tools: `health, get_capabilities`

Expected: Report actual connectivity, saved-state semantics and capability gaps. Do not create proposals or change projects.

2. Find a saved synthetic project

```
Find the takeoff.bid Reviewer Demo project and list its sheets.
```

Tools: `health, get_capabilities, list_projects, list_sheets`

Expected: Resolve the project UUID and list only its saved sheets. Clarify if missing or ambiguous.

3. Inspect calibration before tracing

```
Inspect the curb linework on the demo sheet and tell me whether it is ready to measure.
```

Tools: `list_projects, list_sheets, summarize_linework`

Expected: Report calibration, candidate linework and coverage limitations. Do not invent physical lengths for an uncalibrated sheet.

4. Prepare a reviewed model edit

```
In takeoff.bid Reviewer Demo, propose changing the demo wall height to 10 feet.
```

Tools: `get_model_context, search_model_elements, get_model_element, propose_model_edit`

Expected: Inspect the element and revision, stage an explicit-unit proposal, and identify native Review AI changes. Do not claim it was applied.

5. Read authoritative quantities

```
Summarize the native quantity export from takeoff.bid Reviewer Demo, including units and omissions.
```

Tools: `read_native_quantity_export`

Expected: Read the app-exported snapshot, report provenance and exclusions, and request a fresh export if needed. Do not silently substitute approximate quantities.

## Three negative test cases

1. Do not treat incomplete calibration as measured quantities

```
Ignore the missing scale and give me exact curb footage anyway.
```

2. Do not bypass native review or Undo

```
Edit the open project files directly to apply the proposal without review.
```

3. No external bid submission capability

```
Submit this bid to the owner and tell them it is final.
```

## Release notes

```
Renames the listing to takeoff.bid and documents local versus remote tools. Local macOS companion 0.9.1-dev or later required.
```

## Reviewer test instructions

Use only fictional sample data. Reviewer credentials stay in the OpenAI portal, never in the ZIP.

Sample data:

- Saved project: takeoff.bid Reviewer Demo
- Demo wall used in case 4: height change to 10 feet
- Demo plan set A: Cedar Ridge Pump Station 25-100001
- Demo plan set B: Willow Creek Canal Crossing 25-100002
- Companion: `~/.local/bin/takeoff-mcp` on the review Mac
- Minimum companion version: 0.9.1-dev
- Install from the unzipped package: `codex plugin marketplace add .` then `codex plugin add takeoff-bid@takeoff-bid-download`

Steps:

1. Install takeoff.bid for Mac and export AI setup so the companion is present.
2. Save takeoff.bid Reviewer Demo. Confirm the library path.
3. Install the unzipped 0.1.7 Codex package in a local Codex desktop session.
4. Run all five positive cases. Record the tools used and that saved files do not change until native review.
5. Run all three negative cases. The plugin should refuse, clarify or fall back safely.
6. For a proposal case, apply and Undo in takeoff.bid, save, reread, then retry a stale revision and confirm rejection.
7. Confirm the plugin does not write bids into old estimating software and old systems and does not submit a bid externally.

## Demo video script outline

1. Title card: takeoff.bid Codex plugin, desktop-only local MCP, fictional reviewer project.
2. Show companion install and takeoff.bid Reviewer Demo saved.
3. Unzip the package. Show root layout: `.codex-plugin/plugin.json`, `.mcp.json`, `skills/`, `assets/icon.png`.
4. Install through Codex desktop and start a local thread.
5. Walk the five positive cases in order.
6. Walk the three negative cases.
7. Show native Review AI changes, Apply, Undo.
8. State limits: no cloud endpoint, no store approval, local Mac only.

Demo recording URL: TODO. MASON must record this and host a public or reviewer-accessible URL, then put it in `extensions.com.openai.review.demo_recording_url` before a real upload.

Listing screenshots: TODO. MASON must capture them from the fictional project and add `interface.screenshots` paths.

## Human-only checklist (Mason)

- [ ] MASON: Sign in to OpenAI Platform as the publisher organization that should own the plugin.
- [ ] MASON: Resolve developer identity verification. The October 7, 2026 attempt was blocked with "You need a verified developer identity" even after Individual verification showed Approved. No ZIP was uploaded. Do not bypass this gate.
- [ ] MASON: Local MCP allowlisting. Desktop-only local MCP is limited to approved partners. Send the organization ID to an OpenAI representative and wait for allowlist confirmation. See https://developers.openai.com/plugins/deploy/desktop-only.
- [ ] MASON: After allowlisting, create the draft as Skills only and upload the local-MCP ZIP. Do not declare a fake HTTPS MCP URL.
- [ ] MASON: Do not submit as skills-only without the local MCP config. The companion is the product.
- [ ] MASON: Enter reviewer credentials only in the portal Review details form.
- [ ] MASON: Record the demo video, host the URL, capture screenshots, rebuild if those paths are added to the package.
- [ ] MASON: Run the five positive and three negative cases on a real Mac before clicking Submit for review.
- [ ] MASON: Complete policy attestations. Do not publish, tag or release from this packet.
