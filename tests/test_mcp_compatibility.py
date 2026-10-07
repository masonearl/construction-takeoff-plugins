import importlib.util
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit_tools', ROOT / 'scripts/audit_tools.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
CONTRACT = json.loads((ROOT / 'shared/companion-requirements.json').read_text())


def discovery():
    """Synthetic future companion; never represents a real implementation pass."""
    tools = {name: {'name': name, 'inputSchema': {'type': 'object', 'properties': {}},
                    'annotations': {'readOnlyHint': name not in audit.FILE_WRITERS}}
             for names in audit.REQUIRED.values() for name in names}
    for workflow in CONTRACT['workflows'].values():
        for name, properties in workflow['tools'].items():
            tool = tools.setdefault(name, {'name': name, 'inputSchema': {'type': 'object', 'properties': {}},
                                          'annotations': {'readOnlyHint': name not in audit.FILE_WRITERS}})
            tool['inputSchema']['properties'].update({key: {} for key in properties})
    caps = {'transport': 'local_stdio', 'capabilities': {
        'fixture': {'available': True, 'unavailable_reason': None, 'tools': list(tools)},
        'native_plan_analysis': {'available': False, 'unavailable_reason': 'No development helper', 'tools': ['analyze_plan_page']}}}
    health = {'helper_version': 'synthetic-test-only', 'project_count': 0, 'writes_allowed': False,
              'capabilities': {'native_plan_analysis': 'development_helper_not_configured'}}
    return tools, caps, health


def wire_result(tools, caps, health):
    replies = [
        {'id': 1, 'result': {'protocolVersion': '2025-06-18'}},
        {'id': 2, 'result': {'tools': list(tools.values())}},
        {'id': 3, 'result': {'content': [{'type': 'text', 'text': json.dumps(caps)}]}},
        {'id': 4, 'result': {'structuredContent': health}},
    ]
    return subprocess.CompletedProcess([], 0, '\n'.join(json.dumps(r) for r in replies), '')


class CompatibilityTests(unittest.TestCase):
    def test_interface_readiness_never_claims_native_acceptance(self):
        with patch.object(audit.subprocess, 'run', return_value=wire_result(*discovery())):
            report = audit.audit(ROOT / 'packages/codex', require_mcp_workflows=True)
        self.assertTrue(report['passed'], report)
        self.assertTrue(report['mcp_workflow_interfaces_ready'])
        self.assertFalse(report['acceptance_tests_executed'])

    def test_old_companion_connects_but_fails_full_workflow_gate(self):
        tools, caps, health = discovery()
        del tools['propose_calculation_library']
        caps['capabilities']['fixture']['tools'].remove('propose_calculation_library')
        with patch.object(audit.subprocess, 'run', return_value=wire_result(tools, caps, health)):
            diagnostic = audit.audit(ROOT / 'packages/codex')
            strict = audit.audit(ROOT / 'packages/codex', require_mcp_workflows=True)
            import_only = audit.audit(ROOT / 'packages/codex', require_expected=True)
        self.assertTrue(diagnostic['passed'])
        self.assertFalse(diagnostic['mcp_workflow_interfaces_ready'])
        self.assertIn('MAS-64', diagnostic['warnings'][0])
        self.assertFalse(strict['passed'])
        self.assertTrue(import_only['passed'])

    def test_tool_name_alone_does_not_establish_new_paging_support(self):
        tools, caps, health = discovery()
        del tools['list_sheets']['inputSchema']['properties']['summary_only']
        report = audit.inspect_workflows(tools, caps, health, CONTRACT)
        self.assertFalse(report['MAS-61']['interface_ready'])
        self.assertIn('summary_only', ' '.join(report['MAS-61']['issues']))

    def test_disabled_capability_reports_reason_even_if_tool_is_listed(self):
        tools, caps, health = discovery()
        caps['capabilities']['fixture']['available'] = False
        caps['capabilities']['fixture']['unavailable_reason'] = 'PDF dependency missing'
        report = audit.inspect_workflows(tools, caps, health, CONTRACT)
        self.assertFalse(report['MAS-59']['interface_ready'])
        self.assertIn('PDF dependency missing', ' '.join(report['MAS-59']['issues']))

    def test_proposal_writers_must_be_marked_as_mutating(self):
        for name in ('propose_project_import', 'propose_page_scales', 'propose_project_metadata', 'propose_calculation_library'):
            with self.subTest(tool=name):
                tools, caps, health = discovery()
                tools[name]['annotations']['readOnlyHint'] = True
                with patch.object(audit.subprocess, 'run', return_value=wire_result(tools, caps, health)):
                    report = audit.audit(ROOT / 'packages/codex')
                self.assertFalse(report['passed'])
                self.assertIn(name, ' '.join(report['errors']))

    def test_legacy_tools_and_unconfigured_helper_fail_availability_gate(self):
        tools, caps, health = discovery()
        for name in ('create_project', 'link_hardhat_job', 'analyze_plan_page'):
            tools[name] = {'name': name}
        report = audit.inspect_workflows(tools, caps, health, CONTRACT)
        errors = ' '.join(report['MAS-62']['issues'])
        for name in ('create_project', 'link_hardhat_job', 'analyze_plan_page'):
            self.assertIn(name, errors)
        self.assertFalse(report['MAS-62']['interface_ready'])

    def test_native_helper_health_and_registry_must_agree(self):
        tools, caps, health = discovery()
        caps['capabilities']['native_plan_analysis']['available'] = True
        report = audit.inspect_workflows(tools, caps, health, CONTRACT)
        self.assertIn('disagrees', ' '.join(report['MAS-62']['issues']))
        tools['analyze_plan_page'] = {'name': 'analyze_plan_page'}
        health['capabilities']['native_plan_analysis'] = 'configured_development_helper'
        report = audit.inspect_workflows(tools, caps, health, CONTRACT)
        self.assertTrue(report['MAS-62']['interface_ready'], report)

    def test_failed_health_or_incomplete_responses_are_not_success(self):
        result = wire_result(*discovery())
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        for broken in (responses[:-1], responses[:-1] + [{'id': 4, 'result': {'isError': True}}]):
            with self.subTest(responses=broken):
                result.stdout = '\n'.join(json.dumps(r) for r in broken)
                with patch.object(audit.subprocess, 'run', return_value=result):
                    with self.assertRaisesRegex(ValueError, 'missing or failed'):
                        audit.audit(ROOT / 'packages/codex')

    def test_unisolated_or_write_enabled_health_is_rejected(self):
        for key, value in (('project_count', 3), ('writes_allowed', True), ('writes_allowed', None)):
            tools, caps, health = discovery()
            health[key] = value
            with self.subTest(key=key, value=value):
                with patch.object(audit.subprocess, 'run', return_value=wire_result(tools, caps, health)):
                    self.assertFalse(audit.audit(ROOT / 'packages/codex')['passed'])

    def test_all_packages_include_contract_and_resolve_launchers(self):
        source = (ROOT / 'shared/companion-requirements.json').read_bytes()
        for target in ('cursor', 'claude', 'codex', 'grok-bot', 'desktop'):
            package = ROOT / 'packages' / target
            with self.subTest(target=target):
                self.assertEqual((package / 'companion-requirements.json').read_bytes(), source)
                command, env = audit.launch_config(package)
                self.assertNotIn('${CLAUDE_PLUGIN_ROOT}', ' '.join(command))
                self.assertNotIn('${__dirname}', ' '.join(command))
                self.assertEqual(env['TAKEOFF_MCP_ENABLE_LEGACY_WRITES'], '0')
                if target == 'claude':
                    self.assertTrue(Path(command[0]).is_file())
                if target == 'desktop':
                    self.assertEqual(command[0], 'node')
                    self.assertTrue(Path(command[1]).is_file())


if __name__ == '__main__':
    unittest.main()
