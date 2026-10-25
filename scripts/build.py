#!/usr/bin/env python3
"""Generate platform packages from shared plugin-only sources; no app checkout needed."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://github.com/masonearl/construction-takeoff-plugins'
WEBSITE = 'https://www.masonearl.com/pages/documentation.html#construction-takeoff'
SUPPORT = 'https://www.masonearl.com/pages/construction-takeoff/support.html'
PRIVACY = 'https://www.masonearl.com/pages/construction-takeoff/privacy.html'
TERMS = 'https://www.masonearl.com/pages/construction-takeoff/terms.html'
SETUP = 'https://www.masonearl.com/pages/construction-takeoff/plugin.html'
APP_URL = 'https://apps.apple.com/us/app/construction-takeoff/id6751007895?mt=12'
VERSION = (ROOT / 'VERSION').read_text().strip()
DISPLAY_NAME = 'takeoff.bid'
KEBAB_ID = 'takeoff-bid'
MARKETPLACE_ID = 'takeoff-bid-plugins'
CODEX_DOWNLOAD_ID = 'takeoff-bid-download'
MCP_SERVER = 'takeoff.bid'
ARCHIVE_PREFIX = 'takeoff-bid'
DESCRIPTION = 'Load plan sets, inspect takeoff.bid projects and prepare reviewed takeoff and estimating changes. Requires the separately installed macOS app and MCP companion.'


def machine_name(target):
    """Claude and Codex reject dots in plugin ids; Cursor, Grok Bot, and MCPB accept takeoff.bid."""
    if target in ('claude', 'codex'):
        return KEBAB_ID
    return DISPLAY_NAME


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n')

def package_readme(target):
    requirements = 'takeoff.bid for macOS and its separately installed MCP companion are required.'
    if target == 'desktop':
        requirements += ' The launcher uses Node.js 18 or newer (Claude Desktop supplies Node for extensions).'
    notes = {
        'cursor': f'Install this package through Cursor or copy the folder into ~/.cursor/plugins/local/{DISPLAY_NAME}. Reload Cursor.',
        'claude': f'Install the {KEBAB_ID} plugin from the {MARKETPLACE_ID} marketplace, or upload this ZIP in Claude Customize → Plugins → Add. In Claude Code 2.1.275 or later: `/plugin install {KEBAB_ID} --marketplace masonearl/construction-takeoff-plugins`. The tools work only where the session can launch the Mac companion. Claude chat ignores local MCP entries; the optional Desktop extension is available for local chat use. Cowork host access needs verification.',
        'codex': f'For the downloaded ZIP, unzip it and run `codex plugin marketplace add .` from its folder, then `codex plugin add {KEBAB_ID}@{CODEX_DOWNLOAD_ID}`. Keep that folder for updates. Repository users can install {KEBAB_ID} from the {MARKETPLACE_ID} marketplace in a local Mac session. Public directory submission still requires a supported remote endpoint or OpenAI approval for local MCP.',
        'grok-bot': 'Install the takeoff.bid companion first. Then install this Cursor-format plugin from packages/grok-bot or via Cursor Marketplace / Grok Bot Plugins once public. Grok Bot uses .cursor-plugin/plugin.json (no separate grok-only schema). Cloud-only Grok Bot sessions cannot reach the Mac companion without a separately supported bridge.',
        'desktop': 'Install this MCPB from Claude Desktop Settings → Extensions → Advanced settings, then select your saved project directory. This is an optional local installer, not a new directory submission: Anthropic no longer accepts Desktop extension listings.'
    }
    return f"""# takeoff.bid

Load plan PDFs into new projects through native review, inspect saved construction projects, review quantities and calibration, trace plan linework, and prepare model, calculation and estimate proposals. Supported changes are reviewed and applied inside takeoff.bid with Undo. Proposal creation does not submit a bid or modify the saved project.

## Setup

{requirements} In takeoff.bid, open 3D Model → AI tools, export AI setup and follow its companion instructions. The expected executable is ~/.local/bin/takeoff-mcp. [Get takeoff.bid for Mac]({APP_URL}) · [Documentation]({WEBSITE}). Plugin workflows require a build that includes AI setup/companion export; compatibility with the current App Store release has not yet been verified.

{notes[target]}

Save your project before asking the AI to inspect it. Start with: “Use takeoff.bid health and capabilities, then list my saved projects. Do not make changes.” Prefer native quantity exports and report calibration, source revisions and coverage gaps.

## Reviewed gas workflows

Guidance covers reviewed PDF import, scale proposals, paged results, project metadata proposals, gas-line tracing and the natural-gas calculation library. Availability depends on the tools and argument schemas returned by the installed companion. If a workflow is missing, update the app, reinstall its exported companion, update this plugin and reload the client. `companion-requirements.json` records the expected interfaces for release checks. Native Apply/Undo and plan accuracy require separate testing.

## What runs and what is shared

The package starts the separately installed companion. The launcher does not download code, send network requests or collect analytics. MCP results are sent to your chosen AI client and may be processed by its provider. The companion reads saved projects and creates local proposals/outputs. An updated app may additionally advertise local live reads and project-detail changes with approval choice, history and Undo; inspect capabilities first. The launcher disables legacy direct writes. Native app transactions or review own project changes and Undo. See [privacy](PRIVACY.md).

This preview has not been approved by any store. Disable any older local plugin that registers the same companion before enabling this package, so tools are not duplicated. Website: {WEBSITE}. Source and release status: {URL}. Contact: hi@masonearl.com. MIT applies to plugin files only; the app and companion remain separately licensed.
"""

def build():
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    hashes = []
    for old in list(dist.glob(f'{ARCHIVE_PREFIX}-*')) + list(dist.glob('construction-takeoff-*')):
        if old.suffix in ('.zip', '.mcpb'):
            old.unlink()
    for target in ('cursor', 'claude', 'codex', 'grok-bot', 'desktop'):
        root = ROOT / 'packages' / target
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        for name in ('LICENSE', 'NOTICE', 'PRIVACY.md'):
            shutil.copyfile(ROOT / name, root / name)
        shutil.copytree(ROOT / 'shared/assets', root / 'assets')
        shutil.copyfile(ROOT / 'shared/companion-requirements.json', root / 'companion-requirements.json')
        (root / 'README.md').write_text(package_readme(target))
        plugin_name = machine_name(target)
        manifest = dict(name=plugin_name, version=VERSION, description=DESCRIPTION,
                        author={'name': 'Mason Earl', 'email': 'hi@masonearl.com'},
                        homepage=APP_URL, repository=URL, license='MIT',
                        keywords=['construction', 'takeoff', 'estimating'],
                        skills='./skills/', mcpServers='./.mcp.json')
        if target == 'desktop':
            (root / 'server').mkdir()
            shutil.copyfile(ROOT / 'shared/desktop.cjs', root / 'server/index.cjs')
            dump(root / 'package.json', {'name': 'takeoff.bid-desktop', 'version': VERSION, 'private': True, 'license': 'MIT'})
            dump(root / 'manifest.json', {
                'manifest_version': '0.3', 'name': DISPLAY_NAME, 'display_name': DISPLAY_NAME,
                'version': VERSION, 'description': DESCRIPTION, 'author': manifest['author'],
                'repository': {'type': 'git', 'url': URL}, 'homepage': APP_URL,
                'documentation': SETUP, 'support': SUPPORT,
                'privacy_policies': [PRIVACY], 'license': 'MIT',
                'icon': 'assets/icon.png', 'tools_generated': True,
                'compatibility': {'platforms': ['darwin'], 'runtimes': {'node': '>=18.0.0'}},
                'server': {'type': 'node', 'entry_point': 'server/index.cjs',
                           'mcp_config': {'command': 'node', 'args': ['${__dirname}/server/index.cjs'],
                                          'env': {'TAKEOFF_PROJECTS_DIR': '${user_config.projects_directory}', 'TAKEOFF_MCP_ENABLE_LEGACY_WRITES': '0'}}},
                'user_config': {'projects_directory': {'type': 'directory', 'title': 'takeoff.bid project library',
                               'description': 'Select the folder containing your saved takeoff.bid projects.', 'required': True}}
            })
        else:
            shutil.copytree(ROOT / 'shared/skills', root / 'skills')
            # Inline the same shell source so hosts need no incompatible plugin-root expansion.
            dump(root / '.mcp.json', {'mcpServers': {MCP_SERVER: {
                'command': '/bin/sh', 'args': ['-c', (ROOT / 'shared/start.sh').read_text()],
                'env': {'TAKEOFF_MCP_ENABLE_LEGACY_WRITES': '0'}
            }}})
            if target == 'claude':
                manifest['displayName'] = DISPLAY_NAME
                manifest['privacyPolicyUrl'] = PRIVACY
                manifest['supportUrl'] = SUPPORT
                manifest['documentationUrl'] = SETUP
                manifest['termsOfServiceUrl'] = TERMS
                (root / 'server').mkdir()
                shutil.copyfile(ROOT / 'shared/start.sh', root / 'server/start.sh')
                (root / 'server/start.sh').chmod(0o755)
                dump(root / '.mcp.json', {'mcpServers': {MCP_SERVER: {
                    'command': '${CLAUDE_PLUGIN_ROOT}/server/start.sh', 'args': [],
                    'env': {'TAKEOFF_MCP_ENABLE_LEGACY_WRITES': '0'}
                }}})
            if target == 'codex':
                dump(root / '.agents/plugins/marketplace.json', {
                    'name': CODEX_DOWNLOAD_ID,
                    'interface': {'displayName': f'{DISPLAY_NAME} download'},
                    'plugins': [{'name': plugin_name, 'source': {'source': 'local', 'path': './'},
                        'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'category': 'Productivity'}]
                })
                manifest['interface'] = {
                    'displayName': DISPLAY_NAME, 'shortDescription': 'Takeoffs with native review',
                    'developerName': 'Mason Earl', 'category': 'Productivity',
                    'capabilities': ['Load plan sets for review', 'Inspect saved takeoffs', 'Trace plan linework', 'Prepare reviewed changes'],
                    'logo': './assets/icon.png', 'composerIcon': './assets/icon.png',
                    'longDescription': DESCRIPTION + ' Changes use native review and Undo. Reads reflect saved project state.',
                    'defaultPrompt': ['Check my takeoff.bid connection.', 'Load these plan PDFs into a new takeoff project.', 'Inspect calibration and quantities in my saved takeoff.'],
                    'websiteURL': APP_URL,
                    'supportURL': SUPPORT, 'privacyPolicyURL': PRIVACY, 'termsOfServiceURL': TERMS
                }
                shutil.copytree(ROOT / 'shared/codex/skills/get-started', root / 'skills/get-started')
                manifest['extensions'] = {'com.openai': {
                    'onboardingSkill': './skills/get-started/SKILL.md',
                    'review': json.loads((ROOT / 'shared/codex/review.json').read_text()),
                    'publication': {'release_notes': 'Renames the listing to takeoff.bid and documents local versus remote tools. Local macOS companion 0.9.1-dev or later required.'}
                }}
            if target in ('cursor', 'grok-bot'):
                manifest['displayName'] = DISPLAY_NAME
                manifest['logo'] = 'assets/icon.png'
            # Grok Bot installs Cursor-format plugins; no separate official grok-bot schema.
            plugin_kind = 'cursor' if target == 'grok-bot' else target
            dump(root / f'.{plugin_kind}-plugin/plugin.json', manifest)
        filename = f'{ARCHIVE_PREFIX}-{target}-{VERSION}' + ('.mcpb' if target == 'desktop' else '.zip')
        archive = dist / filename
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for path in sorted(root.rglob('*')):
                if path.is_file():
                    info = zipfile.ZipInfo(path.relative_to(root).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = (0o100755 if path.stat().st_mode & 0o111 else 0o100644) << 16
                    z.writestr(info, path.read_bytes())
        hashes.append(f'{hashlib.sha256(archive.read_bytes()).hexdigest()}  {filename}')
    (dist / 'SHA256SUMS').write_text('\n'.join(hashes) + '\n')
    dump(ROOT / '.claude-plugin/marketplace.json', {
        'name': MARKETPLACE_ID, 'owner': {'name': 'Mason Earl'},
        'metadata': {'description': DESCRIPTION},
        'plugins': [{'name': machine_name('claude'), 'displayName': DISPLAY_NAME, 'source': './packages/claude', 'description': DESCRIPTION}]
    })
    dump(ROOT / '.cursor-plugin/marketplace.json', {
        'name': MARKETPLACE_ID, 'owner': {'name': 'Mason Earl'},
        'metadata': {'description': DESCRIPTION},
        'plugins': [{'name': machine_name('cursor'), 'source': './packages/cursor', 'description': DESCRIPTION}]
    })
    dump(ROOT / '.agents/plugins/marketplace.json', {
        'name': MARKETPLACE_ID, 'interface': {'displayName': DISPLAY_NAME},
        'plugins': [{'name': machine_name('codex'), 'source': {'source': 'local', 'path': './packages/codex'},
                     'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'category': 'Productivity'}]
    })
    print('\n'.join(hashes))

if __name__ == '__main__':
    build()
