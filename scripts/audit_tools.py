#!/usr/bin/env python3
"""Check required release workflows against the real packaged MCP launcher."""
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
FILE_WRITERS = {'propose_model_edit', 'save_traced_measurement', 'propose_calculation_change', 'propose_estimate_change', 'prepare_rendering_revision', 'propose_rendering_review', 'propose_rendering_visibility', 'export_rendering', 'render_sheet_region'}


def audit(plugin):
    config = json.loads((plugin / '.mcp.json').read_text())['mcpServers']['construction-takeoff']
    with tempfile.TemporaryDirectory(prefix='construction-tool-audit-') as folder:
        env = {**os.environ, **config.get('env', {}), 'TAKEOFF_PROJECTS_DIR': folder, 'TAKEOFF_MCP_PROPOSALS_DIR': folder}
        requests = [
            {'jsonrpc':'2.0', 'id':1, 'method':'initialize', 'params':{'protocolVersion':'2025-06-18', 'capabilities':{}, 'clientInfo':{'name':'construction-release-audit','version':'1.0'}}},
            {'jsonrpc':'2.0', 'method':'notifications/initialized'},
            {'jsonrpc':'2.0', 'id':2, 'method':'tools/list'},
            {'jsonrpc':'2.0', 'id':3, 'method':'tools/call', 'params':{'name':'get_capabilities','arguments':{}}},
        ]
        result = subprocess.run([config['command'], *config.get('args', [])], input=''.join(json.dumps(r)+'\n' for r in requests), env=env, capture_output=True, text=True, timeout=30, check=True)
        replies = {r['id']:r for r in map(json.loads, result.stdout.splitlines())}
        if any('error' in r or r.get('result', {}).get('isError') for r in replies.values()):
            raise ValueError('MCP returned an error during capability audit')
        tools = {t['name']:t for t in replies[2]['result']['tools']}
        caps = json.loads(replies[3]['result']['content'][0]['text'])
        missing = {domain:[name for name in names if name not in tools] for domain,names in REQUIRED.items()}
        missing = {domain:names for domain,names in missing.items() if names}
        errors = [f'Missing workflow tools: {missing}'] if missing else []
        for name in FILE_WRITERS & tools.keys():
            if tools[name].get('annotations',{}).get('readOnlyHint') is not False:
                errors.append(f'{name} creates files but is marked read-only; update the companion.')
        if list(Path(folder).iterdir()):
            errors.append('Read-only discovery modified its isolated project root.')
        return {'passed':not errors, 'errors':errors, 'tool_count':len(tools), 'required_workflows':REQUIRED,
                'transport':caps.get('transport'), 'remaining_gaps':caps.get('gaps'),
                'native_app_required':['Sheet import and calibration', 'Project creation and Hardhat job linking', 'Review/apply/Undo and fresh native exports'],
                'acceptance_tests_executed':False}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plugin', type=Path, default=ROOT/'packages/codex')
    report=audit(parser.parse_args().plugin)
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if report['passed'] else 1)
