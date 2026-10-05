"""Tiny Azure chat/tool-calling probe; no benchmark or user simulation is run."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--deployment', default=os.environ.get('AZURE_OPENAI_DEPLOYMENT'))
parser.add_argument('--skip-tool-check', action='store_true')
args = parser.parse_args()
if not args.deployment:
    parser.error('Specify --deployment or AZURE_OPENAI_DEPLOYMENT.')
endpoint = os.environ['AZURE_OPENAI_ENDPOINT'].rstrip('/')
base = endpoint if endpoint.endswith('/openai/v1') else endpoint + '/openai/v1'
key = os.environ['AZURE_OPENAI_API_KEY']

def probe(label, payload):
    row = {'check': label, 'requested_deployment': args.deployment}
    try:
        request = Request(base + '/chat/completions', data=json.dumps(payload).encode(), headers={'api-key': key, 'Content-Type': 'application/json'}, method='POST')
        with urlopen(request, timeout=30) as response:
            data = json.loads(response.read())
            row.update(http_status=response.status, returned_model=data.get('model'), usage=data.get('usage'), response=data)
    except HTTPError as exc:
        row.update(http_status=exc.code, error=exc.read().decode(errors='replace').replace(key,'[REDACTED]'))
    except (URLError, OSError) as exc:
        row.update(http_status=None, error=str(exc).replace(key,'[REDACTED]'))
    print('Check:', label, '| HTTP:', row['http_status'])
    if row['http_status'] == 200:
        print('Returned model:', row['returned_model'])
        print('Usage:', json.dumps(row['usage']))
        print('Message:', json.dumps(row['response']['choices'][0]['message']))
    else:
        print(row['error'][:1000])
    return row

checks = [probe('chat', {'model': args.deployment, 'messages':[{'role':'user','content':'Reply with OK.'}], 'temperature':0, 'max_tokens':4})]
if checks[0]['http_status'] == 200 and not args.skip_tool_check:
    tool={'type':'function','function':{'name':'reproduction_probe','description':'Diagnostic function; no backend operation.','parameters':{'type':'object','properties':{'value':{'type':'string'}},'required':['value']}}}
    checks.append(probe('function_calling', {'model':args.deployment,'messages':[{'role':'user','content':'Call reproduction_probe with value OK.'}],'tools':[tool],'tool_choice':{'type':'function','function':{'name':'reproduction_probe'}},'temperature':0,'max_tokens':64}))
report={'kind':'bounded deployment diagnostic, not a benchmark trajectory','checked_utc':datetime.now(timezone.utc).isoformat(),'checks':checks}
path=Path(__file__).resolve().parents[1]/'evidence/azure-deployment-check.json'
path.write_text(json.dumps(report,indent=2)+'\n')
print('Saved diagnostic to evidence/azure-deployment-check.json')
