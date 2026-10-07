#!/usr/bin/env python3
"""Offline Codex submission preflight. Passing is not store approval or URL verification."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def https_url(value):
    try:
        url = urlsplit(value or '')
        return (url.scheme == 'https' and bool(url.hostname) and not url.username
                and not url.password and url.hostname not in ('localhost', 'example.com')
                and not url.hostname.endswith('.example.com'))
    except ValueError:
        return False


def check(package):
    manifest = json.loads((package / '.codex-plugin/plugin.json').read_text())
    servers = json.loads((package / '.mcp.json').read_text())['mcpServers']
    interface = manifest.get('interface', {})
    extension = manifest.get('extensions', {}).get('com.openai', {})
    review = extension.get('review', {})
    issues = []
    if len(servers) != 1 or not all(https_url(s.get('url')) and not s.get('command') for s in servers.values()):
        issues.append('Current package uses local stdio. Public MCP setup needs a hosted HTTPS connection; resolve local distribution eligibility with OpenAI before submitting this package.')
    for name in ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL'):
        if not https_url(interface.get(name)):
            issues.append(f'Missing valid public HTTPS listing field: {name}.')
    for kind, count in (('positive', 5), ('negative', 3)):
        cases = review.get('test_cases', {}).get(kind, [])
        required = ('description', 'prompt', 'tools_triggered', 'expected_behavior') if kind == 'positive' else ('description', 'prompt')
        if len(cases) < count or any(not all(c.get(k) for k in required) for c in cases):
            issues.append(f'Provide {count} complete {kind} reviewer test cases.')
    if not https_url(review.get('demo_recording_url')):
        issues.append('Provide an accessible video walkthrough URL after executing the reviewer scenarios.')
    screenshots = interface.get('screenshots', [])
    if not screenshots:
        issues.append('Capture listing screenshots from the synthetic reviewer project.')
    for value in [extension.get('onboardingSkill', ''), *screenshots]:
        relative = Path(value)
        resolved = (package / relative).resolve()
        if not value.startswith('./') or '..' in relative.parts or not resolved.is_relative_to(package.resolve()) or not resolved.is_file():
            issues.append(f'Missing or unsafe packaged asset: {value or "onboardingSkill"}.')
    return {
        'package': str(package), 'version': manifest['version'],
        'offline_checks_passed': not issues, 'issues': issues,
        'manual_checks_required': [
            'Publisher identity and organization permission verified in OpenAI portal.',
            'Public page reachability, endpoint authentication, domain ownership and project isolation verified.',
            'Stable app/companion download and minimum version published; reviewer has synthetic data.',
            'Five positive and three negative cases executed, including native review/apply/Undo and stale revisions.',
            'Automated portal checks and review completed; publication explicitly performed.'
        ],
        'submitted': False, 'store_approved': False
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, default=ROOT / 'packages/codex')
    args = parser.parse_args()
    report = check(args.package.resolve())
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['offline_checks_passed'] else 1)
