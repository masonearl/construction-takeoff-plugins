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
DESCRIPTION = 'Inspect Construction Takeoff projects and prepare reviewed takeoff and estimating changes. Requires the separately installed macOS app and MCP companion.'

def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n')

def package_readme(target):
    requirements = 'Construction Takeoff for macOS and its separately installed MCP companion are required.'
    if target == 'desktop':
        requirements += ' The launcher uses Node.js 18 or newer (Claude Desktop supplies Node for extensions).'
    notes = {
        'cursor': 'Install this package through Cursor or copy the folder into ~/.cursor/plugins/local/construction-takeoff. Reload Cursor.',
        'claude': 'Install the construction-takeoff plugin from the construction-takeoff-plugins marketplace, or upload this ZIP in Claude Customize → Plugins → Add. The tools work only where the session can launch the Mac companion. Claude chat ignores local MCP entries; the optional Desktop extension is available for local chat use. Cowork host access needs verification.',
        'codex': 'For the downloaded ZIP, unzip it and run `codex plugin marketplace add .` from its folder, then `codex plugin add construction-takeoff@construction-takeoff-download`. Keep that folder for updates. Repository users can install construction-takeoff from the construction-takeoff-plugins marketplace in a local Mac session. Public directory submission still requires a supported remote endpoint or OpenAI approval for local MCP.',
        'grok-bot': 'Install the Construction Takeoff companion first. Then install this Cursor-format plugin from packages/grok-bot or via Cursor Marketplace / Grok Bot Plugins once public. Grok Bot uses .cursor-plugin/plugin.json (no separate grok-only schema). Cloud-only Grok Bot sessions cannot reach the Mac companion without a separately supported bridge.',
        'desktop': 'Install this MCPB from Claude Desktop Settings → Extensions → Advanced settings, then select your saved project directory. This is an optional local installer, not a new directory submission: Anthropic no longer accepts Desktop extension listings.'
    }
    return f"""# Construction Takeoff

Inspect saved construction projects, review quantities and calibration, trace plan linework, and prepare model, calculation and estimate proposals. Supported changes are reviewed and applied inside Construction Takeoff with Undo. Proposal creation does not submit a bid or modify the saved project.

## Setup

{requirements} In Construction Takeoff, open 3D Model → AI tools, export AI setup and follow its companion instructions. The expected executable is ~/.local/bin/takeoff-mcp. [Get Construction Takeoff for Mac]({APP_URL}) · [Documentation]({WEBSITE}). Plugin workflows require a build that includes AI setup/companion export; compatibility with the current App Store release has not yet been verified.

{notes[target]}

Save your project before asking the AI to inspect it. Start with: “Use Construction Takeoff health and capabilities, then list my saved projects. Do not make changes.” Prefer native quantity exports and report calibration, source revisions and coverage gaps.

## What runs and what is shared

The package starts the separately installed companion. The launcher does not download code, send network requests or collect analytics. MCP results are sent to your chosen AI client and may be processed by its provider. The companion reads saved projects and creates local proposals/outputs. The launcher disables legacy direct writes; native review owns project changes and Undo. See [privacy](PRIVACY.md).

This preview has not been approved by any store. Disable any older takeoff-x-local installation before enabling this package to avoid duplicate tools. Website: {WEBSITE}. Source and release status: {URL}. Contact: hi@masonearl.com. MIT applies to plugin files only; the app and companion remain separately licensed.
"""

def build():
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    hashes = []
    for old in dist.glob('construction-takeoff-*'):
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
        (root / 'README.md').write_text(package_readme(target))
        manifest = dict(name='construction-takeoff', version=VERSION, description=DESCRIPTION,
                        author={'name': 'Mason Earl', 'email': 'hi@masonearl.com'},
                        homepage=APP_URL, repository=URL, license='MIT',
                        keywords=['construction', 'takeoff', 'estimating'],
                        skills='./skills/', mcpServers='./.mcp.json')
        if target == 'desktop':
            (root / 'server').mkdir()
            shutil.copyfile(ROOT / 'shared/desktop.cjs', root / 'server/index.cjs')
            dump(root / 'package.json', {'name': 'construction-takeoff-desktop', 'version': VERSION, 'private': True, 'license': 'MIT'})
            dump(root / 'manifest.json', {
                'manifest_version': '0.3', 'name': 'construction-takeoff', 'display_name': 'Construction Takeoff',
                'version': VERSION, 'description': DESCRIPTION, 'author': manifest['author'],
                'repository': {'type': 'git', 'url': URL}, 'homepage': APP_URL,
                'documentation': SETUP, 'support': SUPPORT,
                'privacy_policies': [PRIVACY], 'license': 'MIT',
                'icon': 'assets/icon.png', 'tools_generated': True,
                'compatibility': {'platforms': ['darwin'], 'runtimes': {'node': '>=18.0.0'}},
                'server': {'type': 'node', 'entry_point': 'server/index.cjs',
                           'mcp_config': {'command': 'node', 'args': ['${__dirname}/server/index.cjs'],
                                          'env': {'TAKEOFF_PROJECTS_DIR': '${user_config.projects_directory}', 'TAKEOFF_MCP_ENABLE_LEGACY_WRITES': '0'}}},
                'user_config': {'projects_directory': {'type': 'directory', 'title': 'Takeoff project library',
                               'description': 'Select the folder containing your saved Construction Takeoff projects.', 'required': True}}
            })
        else:
            shutil.copytree(ROOT / 'shared/skills', root / 'skills')
            # Inline the same shell source so hosts need no incompatible plugin-root expansion.
            dump(root / '.mcp.json', {'mcpServers': {'construction-takeoff': {
                'command': '/bin/sh', 'args': ['-c', (ROOT / 'shared/start.sh').read_text()],
                'env': {'TAKEOFF_MCP_ENABLE_LEGACY_WRITES': '0'}
            }}})
            if target == 'claude':
                manifest['displayName'] = 'Construction Takeoff'
                manifest['privacyPolicyUrl'] = PRIVACY
                manifest['supportUrl'] = SUPPORT
                manifest['documentationUrl'] = SETUP
                manifest['termsOfServiceUrl'] = TERMS
                (root / 'server').mkdir()
                shutil.copyfile(ROOT / 'shared/start.sh', root / 'server/start.sh')
                dump(root / '.mcp.json', {'mcpServers': {'construction-takeoff': {
                    'command': '/bin/sh', 'args': ['${CLAUDE_PLUGIN_ROOT}/server/start.sh'],
                    'env': {'TAKEOFF_MCP_ENABLE_LEGACY_WRITES': '0'}
                }}})
            if target == 'codex':
                dump(root / '.agents/plugins/marketplace.json', {
                    'name': 'construction-takeoff-download',
                    'interface': {'displayName': 'Construction Takeoff download'},
                    'plugins': [{'name': 'construction-takeoff', 'source': {'source': 'local', 'path': './'},
                        'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'category': 'Productivity'}]
                })
                manifest['interface'] = {
                    'displayName': 'Construction Takeoff', 'shortDescription': 'Construction takeoffs and estimates with native review',
                    'developerName': 'Mason Earl', 'category': 'Productivity',
                    'capabilities': ['Inspect saved takeoffs', 'Trace plan linework', 'Prepare reviewed changes'],
                    'logo': './assets/icon.png', 'composerIcon': './assets/icon.png',
                    'longDescription': DESCRIPTION + ' Changes use native review and Undo. Reads reflect saved project state.',
                    'defaultPrompt': ['Check my Construction Takeoff connection.', 'Inspect calibration and quantities in my saved takeoff.', 'Prepare a takeoff change for native review.'],
                    'websiteURL': APP_URL,
                    'supportURL': SUPPORT, 'privacyPolicyURL': PRIVACY, 'termsOfServiceURL': TERMS
                }
                shutil.copytree(ROOT / 'shared/codex/skills/get-started', root / 'skills/get-started')
                manifest['extensions'] = {'com.openai': {
                    'onboardingSkill': './skills/get-started/SKILL.md',
                    'review': json.loads((ROOT / 'shared/codex/review.json').read_text()),
                    'publication': {'release_notes': 'Adds guided Codex connection setup and review scenarios. Local macOS companion required.'}
                }}
            if target in ('cursor', 'grok-bot'):
                manifest['logo'] = 'assets/icon.png'
            # Grok Bot installs Cursor-format plugins; no separate official grok-bot schema.
            plugin_kind = 'cursor' if target == 'grok-bot' else target
            dump(root / f'.{plugin_kind}-plugin/plugin.json', manifest)
        filename = f'construction-takeoff-{target}-{VERSION}' + ('.mcpb' if target == 'desktop' else '.zip')
        archive = dist / filename
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for path in sorted(root.rglob('*')):
                if path.is_file():
                    info = zipfile.ZipInfo(path.relative_to(root).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o100644 << 16
                    z.writestr(info, path.read_bytes())
        hashes.append(f'{hashlib.sha256(archive.read_bytes()).hexdigest()}  {filename}')
    (dist / 'SHA256SUMS').write_text('\n'.join(hashes) + '\n')
    for client in ('cursor', 'claude'):
        dump(ROOT / f'.{client}-plugin/marketplace.json', {
            'name': 'construction-takeoff-plugins', 'owner': {'name': 'Mason Earl'},
            'metadata': {'description': DESCRIPTION},
            'plugins': [{'name': 'construction-takeoff', **({'displayName': 'Construction Takeoff'} if client == 'claude' else {}), 'source': f'./packages/{client}', 'description': DESCRIPTION}]
        })
    dump(ROOT / '.agents/plugins/marketplace.json', {
        'name': 'construction-takeoff-plugins', 'interface': {'displayName': 'Construction Takeoff'},
        'plugins': [{'name': 'construction-takeoff', 'source': {'source': 'local', 'path': './packages/codex'},
                     'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'category': 'Productivity'}]
    })
    print('\n'.join(hashes))

if __name__ == '__main__':
    build()
