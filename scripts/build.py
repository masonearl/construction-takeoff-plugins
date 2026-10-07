#!/usr/bin/env python3
"""Generate platform packages from shared plugin-only sources; no app checkout needed."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://github.com/masonearl/construction-takeoff-plugins'
VERSION = (ROOT / 'VERSION').read_text().strip()
DESCRIPTION = 'Inspect Takeoff X projects and prepare reviewed takeoff and estimating changes. Requires the separately installed macOS app and MCP companion.'

def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n')

def build():
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    hashes = []
    for target in ('cursor', 'claude', 'codex', 'desktop'):
        root = ROOT / 'packages' / target
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        for name in ('LICENSE', 'NOTICE', 'README.md', 'PRIVACY.md'):
            shutil.copyfile(ROOT / name, root / name)
        shutil.copytree(ROOT / 'shared/assets', root / 'assets')
        manifest = dict(name='takeoff-x', version=VERSION, description=DESCRIPTION,
                        author={'name': 'Mason Earl', 'email': 'hi@masonearl.com'},
                        homepage=URL, repository=URL, license='MIT',
                        keywords=['construction', 'takeoff', 'estimating'],
                        skills='./skills/', mcpServers='./.mcp.json')
        if target == 'desktop':
            (root / 'server').mkdir()
            shutil.copyfile(ROOT / 'shared/desktop.cjs', root / 'server/index.cjs')
            dump(root / 'package.json', {'name': 'takeoff-x-desktop', 'version': VERSION, 'private': True, 'license': 'MIT'})
            dump(root / 'manifest.json', {
                'manifest_version': '0.3', 'name': 'takeoff-x', 'display_name': 'Takeoff X',
                'version': VERSION, 'description': DESCRIPTION, 'author': manifest['author'],
                'repository': {'type': 'git', 'url': URL}, 'homepage': URL,
                'documentation': URL + '#readme', 'support': URL + '/issues',
                'privacy_policies': [URL + '/blob/main/PRIVACY.md'], 'license': 'MIT',
                'icon': 'assets/icon.png', 'tools_generated': True,
                'compatibility': {'platforms': ['darwin'], 'runtimes': {'node': '>=18.0.0'}},
                'server': {'type': 'node', 'entry_point': 'server/index.cjs',
                           'mcp_config': {'command': 'node', 'args': ['${__dirname}/server/index.cjs'],
                                          'env': {'TAKEOFF_PROJECTS_DIR': '${user_config.projects_directory}', 'TAKEOFF_MCP_ENABLE_LEGACY_WRITES': '0'}}},
                'user_config': {'projects_directory': {'type': 'directory', 'title': 'Takeoff project library',
                               'description': 'Select the folder containing your saved Takeoff X projects.', 'required': True}}
            })
        else:
            shutil.copytree(ROOT / 'shared/skills', root / 'skills')
            # Inline the same shell source so hosts need no incompatible plugin-root expansion.
            dump(root / '.mcp.json', {'mcpServers': {'takeoff-x': {
                'command': '/bin/sh', 'args': ['-c', (ROOT / 'shared/start.sh').read_text()],
                'env': {'TAKEOFF_MCP_ENABLE_LEGACY_WRITES': '0'}
            }}})
            if target == 'codex':
                manifest['interface'] = {
                    'displayName': 'Takeoff X', 'shortDescription': 'Construction takeoffs and estimates with native review',
                    'developerName': 'Mason Earl', 'category': 'Productivity',
                    'capabilities': ['Read', 'Write'], 'logo': './assets/icon.png',
                    'supportURL': URL + '/issues', 'privacyPolicyURL': URL + '/blob/main/PRIVACY.md'
                }
            if target == 'cursor':
                manifest['logo'] = 'assets/icon.png'
            dump(root / f'.{target}-plugin/plugin.json', manifest)
        filename = f'takeoff-x-{target}-{VERSION}' + ('.mcpb' if target == 'desktop' else '.zip')
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
            'name': 'takeoff-x-plugins', 'owner': {'name': 'Mason Earl'},
            'metadata': {'description': DESCRIPTION},
            'plugins': [{'name': 'takeoff-x', 'source': f'./packages/{client}', 'description': DESCRIPTION}]
        })
    dump(ROOT / '.agents/plugins/marketplace.json', {
        'name': 'takeoff-x-plugins', 'interface': {'displayName': 'Takeoff X'},
        'plugins': [{'name': 'takeoff-x', 'source': {'source': 'local', 'path': './packages/codex'},
                     'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'category': 'Productivity'}]
    })
    print('\n'.join(hashes))

if __name__ == '__main__':
    build()
