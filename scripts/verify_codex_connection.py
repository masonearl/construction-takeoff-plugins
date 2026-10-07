#!/usr/bin/env python3
"""Smoke-test a plugin's real launcher over stdio with an empty isolated project root."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile


def verify(plugin):
    config=json.loads((plugin/'.mcp.json').read_text())['mcpServers']['takeoff-x']
    with tempfile.TemporaryDirectory(prefix='takeoff-plugin-check-') as temporary:
        requests=[
            {'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'plugin-verifier','version':'1.0'}}},
            {'jsonrpc':'2.0','method':'notifications/initialized'},
            {'jsonrpc':'2.0','id':2,'method':'tools/list'},
            {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'health','arguments':{}}},
            {'jsonrpc':'2.0','id':4,'method':'tools/call','params':{'name':'get_capabilities','arguments':{}}},
        ]
        env={**os.environ,**config.get('env',{}),'TAKEOFF_PROJECTS_DIR':temporary,'TAKEOFF_MCP_PROPOSALS_DIR':temporary}
        result=subprocess.run([config['command'],*config.get('args',[])],env=env,
            input=''.join(json.dumps(r)+'\n' for r in requests),text=True,capture_output=True,timeout=20,check=True)
        responses={r['id']:r for r in map(json.loads,result.stdout.splitlines())}
        assert set(responses)=={1,2,3,4}, responses
        assert all('error' not in r for r in responses.values()), responses
        tools=responses[2]['result']['tools']
        manifest=json.loads((plugin/'.codex-plugin/plugin.json').read_text())
        cases=manifest.get('extensions',{}).get('com.openai',{}).get('review',{}).get('test_cases',{}).get('positive',[])
        expected={'health','get_capabilities','propose_estimate_change'}
        for case in cases: expected.update(name.strip() for name in case['tools_triggered'].split(','))
        assert expected <= {t['name'] for t in tools}, 'Reviewer scenario references an unavailable tool'
        for identifier in (3,4): assert not responses[identifier]['result'].get('isError'), responses[identifier]
        health=json.loads(responses[3]['result']['content'][0]['text'])
        assert health['project_count']==0 and health['writes_allowed'] is False, health
        assert list(Path(temporary).iterdir())==[], 'Smoke test modified isolated projects directory'
        print(json.dumps({'plugin':str(plugin),'tools':len(tools),'version':health['helper_version'],'stdio':'passed','legacy_writes':False,'client_ui_verified':False,'store_approved':False}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plugin',nargs='?',type=Path,default=Path(__file__).resolve().parents[1]/'packages/codex')
    verify(parser.parse_args().plugin)
