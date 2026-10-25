#!/usr/bin/env python3
"""Check packaged launchers and report companion compatibility without modifying projects."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    'connection': ['health', 'get_capabilities'],
    'projects': ['list_projects', 'get_project'],
    'plans': ['list_sheets', 'summarize_linework', 'trace_linework', 'render_sheet_region', 'measure_geometry', 'save_traced_measurement'],
    'models': ['get_model_context', 'search_model_elements', 'get_model_element', 'propose_model_edit'],
    'quantities': ['read_native_quantity_export', 'export_quantities'],
    'calculations': ['list_calculation_types', 'evaluate_calculation_type', 'propose_calculation_change', 'export_calculation_results'],
    'estimates': ['read_estimate_context', 'propose_estimate_change', 'export_estimate_bid_sheet'],
    'renderings': ['get_rendering_context', 'validate_rendering', 'prepare_rendering_revision', 'propose_rendering_review', 'propose_rendering_visibility', 'export_rendering'],
}
FILE_WRITERS = {
    'propose_project_import', 'propose_page_scales', 'propose_project_metadata',
    'propose_calculation_library', 'propose_model_edit', 'save_traced_measurement',
    'propose_calculation_change', 'propose_estimate_change', 'prepare_rendering_revision',
    'propose_rendering_review', 'propose_rendering_visibility', 'export_rendering', 'render_sheet_region',
    'apply_estimate_commands', 'apply_pay_item_matches', 'stamp_takeoff',
    'update_live_project_metadata', 'import_live_project', 'stage_and_import_plans',
    'undo_live_changes', 'export_live_estimate',
}
UPGRADE = 'Update the app and reinstall its exported MCP companion, update the plugin, then reload the AI client.'


def load_contract(path=None):
    source = Path(path) if path else ROOT / 'shared/companion-requirements.json'
    return json.loads(source.read_text())


def profile_of(contract, name=None):
    name = name or contract.get('default_profile') or 'local'
    profiles = contract.get('profiles') or {}
    if name not in profiles:
        raise ValueError(f'Unknown audit profile: {name}')
    return name, profiles[name]


def version_tuple(value):
    core = str(value or '').split('-', 1)[0]
    parts = re.findall(r'\d+', core)
    if not parts:
        return None
    return tuple(int(part) for part in parts)


def version_at_least(actual, minimum):
    left, right = version_tuple(actual), version_tuple(minimum)
    if left is None or right is None:
        return None
    width = max(len(left), len(right))
    left += (0,) * (width - len(left))
    right += (0,) * (width - len(right))
    return left >= right


def launch_config(plugin):
    """Resolve each package's actual entry point, including Claude and Desktop roots."""
    plugin = plugin.resolve()
    if (plugin / '.mcp.json').is_file():
        servers = json.loads((plugin / '.mcp.json').read_text())['mcpServers']
        config = servers.get('takeoff.bid') or next(iter(servers.values()))
    else:
        config = json.loads((plugin / 'manifest.json').read_text())['server']['mcp_config']
    command = [part.replace('${CLAUDE_PLUGIN_ROOT}', str(plugin)).replace('${__dirname}', str(plugin))
               for part in [config['command'], *config.get('args', [])]]
    return command, config.get('env', {})


def inspect_workflows(tools, caps, health, requirements, profile_name='local'):
    """Discovery-level checks only. A ready interface is not native acceptance."""
    _, profile = profile_of(requirements, profile_name)
    registry = caps.get('capabilities', {})
    reports = {}
    for name, workflow in profile.get('workflows', {}).items():
        issues = []
        for tool_name, properties in workflow['tools'].items():
            if tool_name not in tools:
                issues.append(f'Missing tool: {tool_name}')
                continue
            missing = sorted(set(properties) - tools[tool_name].get('inputSchema', {}).get('properties', {}).keys())
            if missing:
                issues.append(f'{tool_name} lacks arguments: {", ".join(missing)}')
            entries = [cap for cap in registry.values() if tool_name in cap.get('tools', [])]
            if not entries:
                issues.append(f'{tool_name} is not registered in capabilities')
            elif not any(cap.get('available') is True for cap in entries):
                reasons = [cap.get('unavailable_reason') for cap in entries if cap.get('unavailable_reason')]
                issues.append(f'{tool_name} has no confirmed available capability' + (f': {"; ".join(reasons)}' if reasons else ''))
        for tool_name in workflow['proposal_tools']:
            if tool_name in tools and tools[tool_name].get('annotations', {}).get('readOnlyHint') is not False:
                issues.append(f'{tool_name} creates proposal files but is marked read-only')
        reports[name] = {'name': workflow['name'], 'interface_ready': not issues, 'issues': issues}

    if profile_name == 'local' and 'project-metadata' in reports:
        gates = reports['project-metadata']['issues']
        legacy = sorted(set(profile.get('legacy_disabled_tools', [])) & tools.keys())
        if legacy:
            gates.append(f'Plugin advertises disabled legacy tools: {", ".join(legacy)}')
        configured = health.get('capabilities', {}).get('native_plan_analysis') == 'configured_development_helper'
        if 'analyze_plan_page' in tools and not configured:
            gates.append('analyze_plan_page is advertised without a configured native helper')
        for name, capability in registry.items():
            if type(capability.get('available')) is not bool or 'unavailable_reason' not in capability:
                gates.append(f'{name} lacks runtime availability/reason metadata')
            if capability.get('available') is True:
                missing = sorted(set(capability.get('tools', [])) - tools.keys())
                if missing:
                    gates.append(f'{name} claims available tools absent from discovery: {", ".join(missing)}')
        native_capability = registry.get('native_plan_analysis')
        if native_capability and type(native_capability.get('available')) is bool:
            if native_capability['available'] != configured:
                gates.append('Native helper availability disagrees between health and capabilities')
        reports['project-metadata']['interface_ready'] = not gates
    return reports


def inspect_unknown_tools(tools, profile):
    known = set(profile.get('known_tools', []))
    return sorted(set(tools) - known)


def inspect_remote_inventory(requirements):
    _, profile = profile_of(requirements, 'remote')
    return {
        'passed': True,
        'profile': 'remote',
        'planned': True,
        'ship_remote_manifest': False,
        'known_tools': list(profile.get('known_tools', [])),
        'collisions': profile.get('collisions', {}),
        'note': 'Do not enable the local companion and a remote MCP server under the same name. A remote-MCP plugin manifest is a planned option only.',
        'acceptance_tests_executed': False,
    }


def audit(plugin, require_expected=False, require_mcp_workflows=False, profile='local',
          require_companion_version=False):
    requirements = json.loads((plugin / 'companion-requirements.json').read_text())
    if requirements.get('schema_version') not in (1, 2):
        raise ValueError('Unsupported companion requirements format')
    if requirements.get('schema_version') == 1:
        requirements = {
            'schema_version': 2,
            'minimum_companion_version': requirements.get('minimum_companion_version'),
            'default_profile': 'local',
            'profiles': {'local': {'transport': 'local_stdio', 'workflows': requirements.get('workflows', {}),
                                   'legacy_disabled_tools': ['create_project', 'link_hardhat_job'],
                                   'known_tools': []}},
        }
    profile_name, selected = profile_of(requirements, profile)
    if profile_name == 'remote':
        return inspect_remote_inventory(requirements)

    command, configured_env = launch_config(plugin)
    with tempfile.TemporaryDirectory(prefix='construction-tool-audit-') as folder:
        env = {**os.environ, **configured_env, 'TAKEOFF_PROJECTS_DIR': folder, 'TAKEOFF_MCP_PROPOSALS_DIR': folder}
        requests = [
            {'jsonrpc':'2.0', 'id':1, 'method':'initialize', 'params':{'protocolVersion':'2025-06-18', 'capabilities':{}, 'clientInfo':{'name':'construction-release-audit','version':'1.1'}}},
            {'jsonrpc':'2.0', 'method':'notifications/initialized'},
            {'jsonrpc':'2.0', 'id':2, 'method':'tools/list'},
            {'jsonrpc':'2.0', 'id':3, 'method':'tools/call', 'params':{'name':'get_capabilities','arguments':{}}},
            {'jsonrpc':'2.0', 'id':4, 'method':'tools/call', 'params':{'name':'health','arguments':{}}},
        ]
        result = subprocess.run(command, input=''.join(json.dumps(r)+'\n' for r in requests), env=env,
                                capture_output=True, text=True, timeout=30, check=True)
        replies = {r['id']:r for r in map(json.loads, result.stdout.splitlines()) if 'id' in r}
        if set(replies) != {1, 2, 3, 4} or any('error' in r or r.get('result', {}).get('isError') for r in replies.values()):
            raise ValueError('MCP returned missing or failed discovery responses')
        tools = {t['name']:t for t in replies[2]['result']['tools']}

        def payload(identifier):
            result = replies[identifier]['result']
            return result.get('structuredContent') or json.loads(next(c['text'] for c in result['content'] if c['type'] == 'text'))

        caps, health = payload(3), payload(4)
        errors = []
        warnings = []
        missing = {domain:[name for name in names if name not in tools] for domain,names in REQUIRED.items()}
        missing = {domain:names for domain,names in missing.items() if names}
        if missing:
            errors.append(f'Missing baseline workflow tools: {missing}')
        if health.get('writes_allowed') is not False:
            errors.append('Plugin companion did not confirm legacy writes are disabled')
        if health.get('project_count') != 0 or list(Path(folder).iterdir()):
            errors.append('Read-only discovery did not preserve the isolated empty project root')
        for name in FILE_WRITERS & tools.keys():
            if tools[name].get('annotations', {}).get('readOnlyHint') is not False:
                errors.append(f'{name} creates files but is marked read-only')
        workflows = inspect_workflows(tools, caps, health, requirements, profile_name)
        missing_workflows = [name for name, report in workflows.items() if not report['interface_ready']]
        if missing_workflows:
            warnings.append(f'Companion has incomplete MCP workflows: {", ".join(missing_workflows)}. {UPGRADE}')
        enforced = set(workflows) if require_mcp_workflows else {'plan-import'} if require_expected else set()
        for name in sorted(enforced):
            if not workflows[name]['interface_ready']:
                errors.append(f'{name}: ' + '; '.join(workflows[name]['issues']))
        unknown = inspect_unknown_tools(tools, selected)
        if unknown:
            warnings.append(f'Unknown tools not in the {profile_name} known-tools list: {", ".join(unknown)}')
        minimum = requirements.get('minimum_companion_version')
        helper_version = health.get('helper_version')
        version_ok = version_at_least(helper_version, minimum) if minimum else None
        if minimum and version_ok is False:
            message = f'Companion helper_version {helper_version} is older than minimum {minimum}'
            if require_companion_version or require_mcp_workflows:
                errors.append(message)
            else:
                warnings.append(message)
        elif minimum and version_ok is None:
            warnings.append(f'Could not compare helper_version {helper_version!r} to minimum {minimum}')
        return {
            'passed': not errors, 'errors': errors, 'warnings': warnings,
            'profile': profile_name,
            'companion_version': helper_version,
            'minimum_companion_version': minimum,
            'companion_version_ok': version_ok,
            'tool_count': len(tools),
            'unknown_tools': unknown,
            'transport': caps.get('transport'), 'legacy_writes': health.get('writes_allowed'),
            'mcp_workflow_interfaces_ready': not missing_workflows, 'workflows': workflows,
            'remaining_gaps': caps.get('gaps'),
            'collisions': selected.get('collisions', {}),
            'native_app_required': ['Review/apply/Undo for proposals', 'Save and export fresh native quantities'],
            'acceptance_tests_executed': False,
        }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plugin', type=Path, default=ROOT/'packages/codex')
    parser.add_argument('--profile', choices=('local', 'remote'), default='local')
    parser.add_argument('--require-plan-import', action='store_true', help='require the reviewed plan-import interface')
    parser.add_argument('--require-mcp-workflows', action='store_true', help='release gate: require all six reviewed workflow interfaces')
    parser.add_argument('--require-companion-version', action='store_true', help='fail when helper_version is older than the contract minimum')
    options = parser.parse_args()
    try:
        report = audit(options.plugin, options.require_plan_import, options.require_mcp_workflows,
                       options.profile, options.require_companion_version)
    except (OSError, ValueError, KeyError, StopIteration, subprocess.SubprocessError) as exc:
        report = {'passed': False, 'errors': [str(exc)], 'acceptance_tests_executed': False}
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['passed'] else 1)
