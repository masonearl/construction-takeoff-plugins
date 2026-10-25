# Grok Bot / Cursor marketplace submission packet

Grok Bot installs Cursor-format plugins. There is no separate grok-only schema for this local stdio companion. Use `packages/grok-bot` (same manifest shape as `packages/cursor`) plus the x.ai bot marketplace form if a shareable bot template is desired later.

Do not submit from this packet. Mason must complete portal login, publisher identity and the x.ai form.

Version in the package: 0.1.6.

## Listing fields

Name:

```
Construction Takeoff
```

Short description (27 characters):

```
Takeoffs with native review
```

Long description:

```
Load plan sets, inspect Construction Takeoff projects and prepare reviewed takeoff and estimating changes. Requires the separately installed macOS app and MCP companion. Changes use native review and Undo. Reads reflect saved project state. Cloud-only Grok Bot sessions cannot reach the Mac companion.
```

Category:

```
Productivity
```

Website:

```
https://www.masonearl.com/pages/documentation.html#construction-takeoff
```

Setup:

```
https://www.masonearl.com/pages/construction-takeoff/plugin.html
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

Homepage (App Store):

```
https://apps.apple.com/us/app/construction-takeoff/id6751007895?mt=12
```

Repository:

```
https://github.com/masonearl/construction-takeoff-plugins
```

Contact:

```
hi@masonearl.com
```

Logo (1:1 PNG, 512 x 512, packaged at `packages/grok-bot/assets/icon.png` and `shared/assets/icon.png`):

```
https://raw.githubusercontent.com/masonearl/construction-takeoff-plugins/main/shared/assets/icon.png
```

If the x.ai form rejects a GitHub raw URL, host the same file on masonearl.com. MASON must confirm the hosted URL.

Cursor marketplace publish:

```
https://cursor.com/marketplace/publish
```

Cursor catalog in this repository:

```
.cursor-plugin/marketplace.json
```

Cursor plugin folder:

```
packages/cursor
```

Grok Bot plugin folder (Cursor-format):

```
packages/grok-bot
```

## x.ai submit-a-plugin form

Source: https://x.ai/bot/marketplace/submit-a-plugin

Organization handle (no spaces or capitalization). Suggested:

```
masonearl
```

MASON: confirm this handle is available and is the one you want listed.

Website URL:

```
masonearl.com
```

Logotype URL (required, 1:1 SVG or PNG with a background plate):

```
https://raw.githubusercontent.com/masonearl/construction-takeoff-plugins/main/shared/assets/icon.png
```

Where do you want to be listed? Suggested:

```
Grok Bot and Cursor
```

MASON: the live form may use checkboxes. Pick Grok Bot and Cursor. Do not claim Grok cloud until a bridge exists. Grok (coming soon) is optional.

## Example prompts for reviewers

1.

```
Use Construction Takeoff health and capabilities, then list my saved projects. Do not make changes.
```

2.

```
Load the Willow Creek Canal Crossing 25-100002 plan PDFs into a new takeoff project and tell me how to apply the import in native review.
```

3.

```
Inspect calibration and quantities in Construction Takeoff Reviewer Demo, then prepare one reviewed change. Do not apply it.
```

## Release notes

```
0.1.6 ships a Cursor-format Construction Takeoff plugin for local Grok Bot and Cursor sessions. Requires the separately installed macOS companion. Cloud Grok Bot sessions are not supported.
```

## Reviewer test instructions

Use only fictional sample data.

Sample data:

- Saved project: Construction Takeoff Reviewer Demo
- Demo plan set A: Cedar Ridge Pump Station 25-100001
- Demo plan set B: Willow Creek Canal Crossing 25-100002
- Companion: `~/.local/bin/takeoff-mcp` on the review Mac

Steps:

1. Install Construction Takeoff for Mac, export AI setup and save Construction Takeoff Reviewer Demo.
2. Install `packages/grok-bot` (or `packages/cursor`) as a local Cursor-format plugin. Reload.
3. In a local Grok Bot or Cursor session on that Mac, run prompt 1. Confirm health, capabilities and the demo project.
4. Stage an import of Willow Creek Canal Crossing. Confirm a proposal bundle only. Apply in File, Review AI Project Import, then save.
5. Inspect calibration and native quantities. Prepare one proposal. Apply and Undo in the app.
6. From a cloud-only Grok Bot session, confirm the companion is unreachable and that the plugin reports that limit instead of claiming success.
7. Confirm no bid is submitted and nothing is written into old estimating software and old systems.

Cursor publisher terms to keep true in the listing: the plugin is free, MIT (permissive), descriptions are accurate, and it does not collect Plugin Data beyond disclosed takeoff inspection and local proposals. See https://cursor.com/marketplace-publisher-terms.

## Demo video script outline

1. Title card: Construction Takeoff on Grok Bot / Cursor, local Mac only, fictional demo project.
2. Show companion install and Construction Takeoff Reviewer Demo.
3. Show `packages/grok-bot/.cursor-plugin/plugin.json` and the 512 x 512 logo.
4. Install the plugin and run health plus list projects.
5. Import Willow Creek Canal Crossing through native review.
6. Inspect quantities and stage one change. Apply and Undo.
7. Show a cloud-only session failing to reach the companion.
8. Close on RC status: not marketplace-approved, no cloud bridge.

## Human-only checklist (Mason)

- [ ] MASON: Cursor publisher login at https://cursor.com/marketplace/publish. A publisher application was already submitted October 7, 2026. Continue that review. Do not file a second publisher identity.
- [ ] MASON: Confirm the public GitHub repository, root marketplace file and `packages/cursor` path in the Cursor form.
- [ ] MASON: Identity verification for Cursor / Anysphere review.
- [ ] MASON: x.ai form at https://x.ai/bot/marketplace/submit-a-plugin. Confirm organization handle, logo URL and listing surfaces.
- [ ] MASON: If x.ai requires a background plate and the current PNG reads as transparent, composite the 512 x 512 icon onto an opaque plate and host that file. Rebuild packages after replacing `shared/assets/icon.png`.
- [ ] MASON: Record the demo video from fictional data. Host a reviewer URL.
- [ ] MASON: Do not advertise cloud Grok Bot support.
- [ ] MASON: Do not submit, publish, tag or release from this packet.
