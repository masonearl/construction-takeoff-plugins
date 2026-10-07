import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]

class DistributionTests(unittest.TestCase):
    def launch(self, target, home, data=''):
        env = dict(os.environ, HOME=str(home), TAKEOFF_MCP_ENABLE_LEGACY_WRITES='1', TAKEOFF_PROJECTS_DIR=str(home / 'Library with spaces'))
        if target == 'desktop':
            command = ['node', str(ROOT / 'packages/desktop/server/index.cjs')]
        else:
            config = json.loads((ROOT / f'packages/{target}/.mcp.json').read_text())['mcpServers']['takeoff-x']
            command = [config['command'], *config['args']]
        return subprocess.run(command, env=env, input=data, capture_output=True, text=True, timeout=10)

    def test_missing_companion_is_actionable_stderr_only(self):
        with tempfile.TemporaryDirectory(prefix='takeoff absent ') as d:
            for target in ('cursor','claude','codex','desktop'):
                with self.subTest(target=target):
                    p = self.launch(target, Path(d))
                    self.assertEqual(p.returncode, 69)
                    self.assertEqual(p.stdout, '')
                    self.assertIn('companion', p.stderr)
                    self.assertIn('AI setup', p.stderr)

    def test_transparent_stdio_environment_and_exit_status(self):
        with tempfile.TemporaryDirectory(prefix='takeoff home ') as d:
            home = Path(d)
            companion = home / '.local/bin/takeoff-mcp'
            companion.parent.mkdir(parents=True)
            companion.write_text('#!/bin/sh\n[ "$TAKEOFF_MCP_ENABLE_LEGACY_WRITES" = 0 ] || exit 91\n[ "$TAKEOFF_PROJECTS_DIR" = "$HOME/Library with spaces" ] || exit 92\ncat\nexit 17\n')
            companion.chmod(0o755)
            message = '{"jsonrpc":"2.0","id":1,"method":"initialize"}\n'
            for target in ('cursor','claude','codex','desktop'):
                with self.subTest(target=target):
                    p = self.launch(target, home, message)
                    self.assertEqual(p.returncode, 17, p.stderr)
                    self.assertEqual(p.stdout, message)
                    self.assertEqual(p.stderr, '')

    def test_archive_contents_and_reproducibility(self):
        archives = sorted((ROOT / 'dist').glob('takeoff-x-*'))
        self.assertEqual(len(archives), 4)
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

if __name__ == '__main__':
    unittest.main()
