import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / 'VERSION').read_text().strip()
LAUNCHERS = ('cursor', 'claude', 'codex', 'grok-bot', 'desktop')
DARWIN = platform.system() == 'Darwin'

class DistributionTests(unittest.TestCase):
    def launch(self, target, home, data=''):
        env = dict(os.environ, HOME=str(home), TAKEOFF_MCP_ENABLE_LEGACY_WRITES='1', TAKEOFF_PROJECTS_DIR=str(home / 'Library with spaces'))
        if target == 'desktop':
            command = ['node', str(ROOT / 'packages/desktop/server/index.cjs')]
        else:
            config = json.loads((ROOT / f'packages/{target}/.mcp.json').read_text())['mcpServers']['construction-takeoff']
            command = [config['command'].replace('${CLAUDE_PLUGIN_ROOT}', str(ROOT / f'packages/{target}')), *[arg.replace('${CLAUDE_PLUGIN_ROOT}', str(ROOT / f'packages/{target}')) for arg in config['args']]]
        return subprocess.run(command, env=env, input=data, capture_output=True, text=True, timeout=10)

    def test_missing_companion_is_actionable_stderr_only(self):
        with tempfile.TemporaryDirectory(prefix='takeoff absent ') as d:
            for target in LAUNCHERS:
                with self.subTest(target=target):
                    p = self.launch(target, Path(d))
                    self.assertEqual(p.returncode, 69)
                    self.assertEqual(p.stdout, '')
                    self.assertIn('companion', p.stderr)
                    if DARWIN:
                        self.assertIn('AI setup', p.stderr)
                    else:
                        self.assertIn('macOS', p.stderr)

    def test_transparent_stdio_environment_and_exit_status(self):
        with tempfile.TemporaryDirectory(prefix='takeoff home ') as d:
            home = Path(d)
            companion = home / '.local/bin/takeoff-mcp'
            companion.parent.mkdir(parents=True)
            companion.write_text('#!/bin/sh\n[ "$TAKEOFF_MCP_ENABLE_LEGACY_WRITES" = 0 ] || exit 91\n[ "$TAKEOFF_PROJECTS_DIR" = "$HOME/Library with spaces" ] || exit 92\ncat\nexit 17\n')
            companion.chmod(0o755)
            message = '{"jsonrpc":"2.0","id":1,"method":"initialize"}\n'
            for target in LAUNCHERS:
                with self.subTest(target=target):
                    p = self.launch(target, home, message)
                    if not DARWIN:
                        self.assertEqual(p.returncode, 69, p.stderr)
                        self.assertEqual(p.stdout, '')
                        self.assertIn('macOS', p.stderr)
                        continue
                    self.assertEqual(p.returncode, 17, p.stderr)
                    self.assertEqual(p.stdout, message)
                    self.assertEqual(p.stderr, '')

    def test_archive_contents_and_reproducibility(self):
        archives = sorted((ROOT / 'dist').glob('construction-takeoff-*'))
        self.assertEqual(len(archives), 5)
        self.assertIn(f'construction-takeoff-grok-bot-{VERSION}.zip', {p.name for p in archives})
        before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in archives}
        subprocess.run(['python3', str(ROOT / 'scripts/build.py')], check=True, capture_output=True)
        self.assertEqual(before, {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in archives})
        for archive in archives:
            with zipfile.ZipFile(archive) as z:
                self.assertIsNone(z.testzip())
                self.assertIn('LICENSE', z.namelist())
                self.assertIn('PRIVACY.md', z.namelist())
                for name in z.namelist():
                    self.assertFalse(name.startswith('/') or '..' in Path(name).parts)
                    self.assertNotIn('.DS_Store', name)
                    self.assertFalse(name.endswith(('.swift','.pdf','.takeoff','.pyc')))

    def test_grok_bot_uses_cursor_plugin_format(self):
        root = ROOT / 'packages/grok-bot'
        cursor_manifest = json.loads((ROOT / 'packages/cursor/.cursor-plugin/plugin.json').read_text())
        grok_manifest = json.loads((root / '.cursor-plugin/plugin.json').read_text())
        self.assertEqual(cursor_manifest, grok_manifest)
        self.assertEqual(grok_manifest['name'], 'construction-takeoff')
        for rel in ('.mcp.json', 'skills/takeoff-workflow/SKILL.md', 'LICENSE', 'NOTICE', 'README.md', 'PRIVACY.md', 'assets/icon.png'):
            self.assertTrue((root / rel).is_file(), rel)
        self.assertFalse((root / '.grok-bot-plugin').exists())
        marketplace = json.loads((ROOT / '.cursor-plugin/marketplace.json').read_text())
        self.assertEqual(marketplace['plugins'][0]['name'], 'construction-takeoff')
        self.assertEqual(marketplace['plugins'][0]['source'], './packages/cursor')
        grok_zip = ROOT / 'dist' / f'construction-takeoff-grok-bot-{VERSION}.zip'
        with zipfile.ZipFile(grok_zip) as z:
            names = z.namelist()
            for required in ('.cursor-plugin/plugin.json', '.mcp.json', 'skills/takeoff-workflow/SKILL.md', 'assets/icon.png'):
                self.assertIn(required, names)
            self.assertNotIn('.grok-bot-plugin/plugin.json', names)

if __name__ == '__main__':
    unittest.main()
