#!/usr/bin/env python3
"""Check packaged launchers and report companion compatibility without modifying projects."""
import argparse
import json
import os
from pathlib import Path
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
FILE_WRITERS = {'propose_project_import', 'propose_page_scales', 'propose_project_metadata',
    'propose_calculation_library', 'propose_model_edit', 'save_traced_measurement',
    'propose_calculation_change', 'propose_estimate_change', 'prepare_rendering_revision',
    'propose_rendering_review', 'propose_rendering_visibility', 'export_rendering', 'render_sheet_region'}
UPGRADE = 'Update the app and reinstall its exported MCP companion, update the plugin, then reload the AI client.'


def launch_config(plugin):
    """Resolve each package's actual entry point, including Claude and Desktop roots."""
    plugin = plugin.resolve()
    if (plugin / '.mcp.json').is_file():
        config = json.loads((plugin / '.mcp.json').read_text())['mcpServers']['construction-takeoff']
    else:
        config = json.loads((plugin / 'manifest.json').read_text())['server']['mcp_config']
    command = [part.replace('${CLAUDE_PLUGIN_ROOT}', str(plugin)).replace('${__dirname}', str(plugin))
               for part in [config['command'], *config.get('args', [])]]
    return command, config.get('env', {})


def inspect_workflows(tools, caps, health, requirements):
    """Discovery-level checks only. A ready interface is not native acceptance."""
    registry = caps.get('capabilities', {})
    reports = {}
    for ticket, workflow in requirements['workflows'].items():
        issues = []
        for name, properties in workflow['tools'].items():
            if name not in tools:
                issues.append(f'Missing tool: {name}')
                continue
            missing = sorted(set(properties) - tools[name].get('inputSchema', {}).get('properties', {}).keys())
            if missing:
                issues.append(f'{name} lacks arguments: {", ".join(missing)}')
            entries = [cap for cap in registry.values() if name in cap.get('tools', [])]
            if not entries:
                issues.append(f'{name} is not registered in capabilities')
            elif not any(cap.get('available') is True for cap in entries):
                reasons = [cap.get('unavailable_reason') for cap in entries if cap.get('unavailable_reason')]
                issues.append(f'{name} has no confirmed available capability' + (f': {"; ".join(reasons)}' if reasons else ''))
        for name in workflow['proposal_tools']:
            if name in tools and tools[name].get('annotations', {}).get('readOnlyHint') is not False:
                issues.append(f'{name} creates proposal files but is marked read-only')
        reports[ticket] = {'name': workflow['name'], 'interface_ready': not issues, 'issues': issues}

    gates = reports['MAS-62']['issues']
    legacy = sorted({'create_project', 'link_hardhat_job'} & tools.keys())
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
    reports['MAS-62']['interface_ready'] = not gates
    return reports


def audit(plugin, require_expected=False, require_mcp_workflows=False):
    requirements = json.loads((plugin / 'companion-requirements.json').read_text())
    if requirements.get('schema_version') != 1:
        raise ValueError('Unsupported companion requirements format')
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
        workflows = inspect_workflows(tools, caps, health, requirements)
        missing_workflows = [ticket for ticket, report in workflows.items() if not report['interface_ready']]
        warnings = [f'Companion has incomplete MCP workflows: {", ".join(missing_workflows)}. {UPGRADE}'] if missing_workflows else []
        enforced = set(workflows) if require_mcp_workflows else {'MAS-59'} if require_expected else set()
        for ticket in sorted(enforced):
            if not workflows[ticket]['interface_ready']:
                errors.append(f'{ticket}: ' + '; '.join(workflows[ticket]['issues']))
        return {
            'passed': not errors, 'errors': errors, 'warnings': warnings,
            'companion_version': health.get('helper_version'), 'tool_count': len(tools),
            'transport': caps.get('transport'), 'legacy_writes': health.get('writes_allowed'),
            'mcp_workflow_interfaces_ready': not missing_workflows, 'workflows': workflows,
            'remaining_gaps': caps.get('gaps'),
            'native_app_required': ['Review/apply/Undo for proposals', 'Save and export fresh native quantities'],
            'acceptance_tests_executed': False,
        }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plugin', type=Path, default=ROOT/'packages/codex')
    parser.add_argument('--require-plan-import', action='store_true', help='require the reviewed import interface (MAS-59)')
    parser.add_argument('--require-mcp-workflows', action='store_true', help='release gate: require all six MAS-59–64 interfaces')
    options = parser.parse_args()
    try:
        report = audit(options.plugin, options.require_plan_import, options.require_mcp_workflows)
    except (OSError, ValueError, KeyError, StopIteration, subprocess.SubprocessError) as exc:
        report = {'passed': False, 'errors': [str(exc)], 'acceptance_tests_executed': False}
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['passed'] else 1)
