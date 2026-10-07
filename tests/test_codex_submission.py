import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('preflight', ROOT / 'scripts/check_codex_submission.py')
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


class CodexSubmissionTests(unittest.TestCase):
    def test_local_package_cannot_be_mistaken_for_store_ready(self):
        report = preflight.check(ROOT / 'packages/codex')
        self.assertFalse(report['offline_checks_passed'])
        self.assertTrue(any('local stdio' in issue for issue in report['issues']))
        self.assertTrue(any('private source repository' in issue for issue in report['issues']))
        self.assertFalse(report['store_approved'])

    def test_complete_metadata_still_requires_manual_review(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / 'plugin'
            shutil.copytree(ROOT / 'packages/codex', package)
            path = package / '.codex-plugin/plugin.json'
            manifest = json.loads(path.read_text())
            for name in ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL'):
                manifest['interface'][name] = 'https://takeoff.test/' + name
            manifest['interface']['screenshots'] = ['./assets/icon.png']
            manifest['extensions']['com.openai']['review']['demo_recording_url'] = 'https://takeoff.test/demo'
            path.write_text(json.dumps(manifest))
            (package / '.mcp.json').write_text(json.dumps({'mcpServers': {'construction-takeoff': {'url': 'https://takeoff.test/mcp'}}}))
            report = preflight.check(package)
            self.assertTrue(report['offline_checks_passed'], report['issues'])
            self.assertFalse(report['store_approved'])
            self.assertTrue(report['manual_checks_required'])
            manifest['extensions']['com.openai']['onboardingSkill'] = './../outside.md'
            path.write_text(json.dumps(manifest))
            self.assertFalse(preflight.check(package)['offline_checks_passed'])

    def test_unsafe_or_placeholder_urls_rejected(self):
        for url in ('http://takeoff.test', 'https://example.com/mcp', 'https://localhost/mcp', 'https://user:password@takeoff.test', 'https://[broken'):
            with self.subTest(url=url):
                self.assertFalse(preflight.https_url(url))

    def test_review_metadata_is_preserved_in_package(self):
        review = json.loads((ROOT / 'shared/codex/review.json').read_text())
        self.assertEqual(len(review['test_cases']['positive']), 5)
        self.assertEqual(len(review['test_cases']['negative']), 3)
        manifest = json.loads((ROOT / 'packages/codex/.codex-plugin/plugin.json').read_text())
        self.assertEqual(manifest['extensions']['com.openai']['review'], review)


if __name__ == '__main__':
    unittest.main()
