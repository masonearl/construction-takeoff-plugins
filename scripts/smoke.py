#!/usr/bin/env python3
"""Exercise installed companion through each package using synthetic temporary data only."""
import json
import os
from pathlib import Path
import queue
import subprocess
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]
PID = '10000000-0000-4000-8000-000000000001'
EID = '20000000-0000-4000-8000-000000000001'

def fixture():
    data = {'id': PID, 'name': 'Plugin synthetic review', 'clientName': '', 'projectNumber': 'DEMO',
            'description': 'Generated test data. Not a real construction project.',
            'dateCreated': '2026-10-07T00:00:00Z', 'lastModified': '2026-10-07T00:00:00Z',
            'documentURL': None, 'preferredWorkspace': 'takeoff', 'units': 'ft', 'precision': 1,
            'currency': 'USD', 'notes': 'Synthetic fixture only.', 'allPageDocumentScales': {},
            'documentScale': {'realWorldUnits': 1, 'realWorldUnit': 'ft', 'drawingUnits': 72, 'calibrated': True, 'precision': 1}}
    for key in ('measurements','markupAnnotations','textBoxes','signatures','simpleTexts','imageOverlays','takeoffItems','groups','rollPlots'):
        data[key] = []
    data['measurements'] = [{'id': EID, 'name': 'Synthetic concrete slab', 'type': 'Area',
        'startPoint': [0,0], 'endPoint': [1,1], 'points': [[0,0],[1,0],[1,1],[0,1]],
        'documentSize': [720,720], 'pageNumber': 1, 'createdAt': '2026-10-07T00:00:00Z',
        'areaDepth': 1, 'model3D': {'kind': 'slab', 'height': 1, 'width': 1, 'elevation': 0,
        'unit': 'ft', 'material': 'Concrete', 'sourcePointsPerFoot': 72}}]
    return data

class Session:
    def __init__(self, target, directory):
        if target == 'desktop':
            command = ['node', str(ROOT / 'packages/desktop/server/index.cjs')]
        else:
            cfg = json.loads((ROOT / f'packages/{target}/.mcp.json').read_text())['mcpServers']['takeoff-x']
            command = [cfg['command'], *[arg.replace('${CLAUDE_PLUGIN_ROOT}',str(ROOT / f'packages/{target}')) for arg in cfg['args']]]
        self.stderr = tempfile.TemporaryFile(mode='w+')
        self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.stderr, text=True,
            env=dict(os.environ, TAKEOFF_PROJECTS_DIR=str(directory), TAKEOFF_MCP_PROPOSALS_DIR=str(directory/'proposals'), TAKEOFF_MCP_ENABLE_LEGACY_WRITES='1'))
        self.responses = queue.Queue()
        self.next_id = 0
        def reader():
            for line in self.proc.stdout:
                self.responses.put(line)
        self.reader = threading.Thread(target=reader, daemon=True)
        self.reader.start()
        self.call('initialize', {'protocolVersion': '2024-11-05','capabilities': {},'clientInfo': {'name':'takeoff-package-smoke','version':'1'}})
        self.proc.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n');self.proc.stdin.flush()

    def call(self, method, params):
        self.next_id += 1
        self.proc.stdin.write(json.dumps({'jsonrpc':'2.0','id':self.next_id,'method':method,'params':params})+'\n');self.proc.stdin.flush()
        while True:
            message = json.loads(self.responses.get(timeout=15))
            if message.get('id') == self.next_id:
                assert 'error' not in message, message
                return message['result']

    def tool(self, name, arguments, error=False):
        result = self.call('tools/call', {'name':name,'arguments':arguments})
        if error:
            assert result.get('isError'), result
            return result
        assert not result.get('isError'), result
        return json.loads(next(item['text'] for item in result['content'] if item['type']=='text'))

    def close(self):
        self.proc.stdin.close()
        try: self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired: self.proc.terminate();self.proc.wait(timeout=5)
        self.proc.stdout.close();self.stderr.close()

def main():
    for target in ('cursor','claude','codex','desktop'):
        with tempfile.TemporaryDirectory(prefix='takeoff synthetic ') as td:
            directory = Path(td)
            package = directory / f'{PID}.takeoffxpkg';package.mkdir()
            project = package / 'project.json';project.write_text(json.dumps(fixture()))
            before = project.read_bytes()
            session = Session(target,directory)
            try:
                tools = session.call('tools/list',{})['tools']
                health = session.tool('health',{})
                assert health['project_count']==1 and not health['writes_allowed'], health
                session.tool('get_capabilities',{})
                context = session.tool('get_model_context',{'project_id':PID})
                session.tool('get_model_element',{'project_id':PID,'element_id':EID})
                args = {'project_id':PID,'expected_revision':context['revision'],'element_ids':[EID],
                        'title':'Synthetic review','reason':'Test an 18 inch slab proposal','unit':'in','changes':{'height':18}}
                proposal = session.tool('propose_model_edit',args)
                assert not proposal['applied']
                proposal_path = Path(proposal['proposal_path'])
                assert proposal_path.is_relative_to(directory) and proposal_path.is_file()
                session.tool('propose_model_edit',{**args,'expected_revision':'0'*64},error=True)
                assert project.read_bytes()==before, 'Project changed before native review'
                print(f'{target}: {len(tools)} tools; health, capabilities, model inspection, proposal, stale rejection and unchanged project PASS')
            finally:
                session.close()

if __name__ == '__main__':
    main()
