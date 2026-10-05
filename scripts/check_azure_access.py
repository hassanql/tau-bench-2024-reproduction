"""Read-only Azure endpoint/authentication check; never logs the API key."""
import json
import os
from datetime import datetime, timezone
import argparse
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--full', action='store_true', help='Print full catalog JSON instead of a concise summary.')
args = parser.parse_args()
endpoint = os.environ['AZURE_OPENAI_ENDPOINT'].rstrip('/')
key = os.environ['AZURE_OPENAI_API_KEY']
checks = []
for path in ['/openai/v1/models', '/openai/models?api-version=2024-10-21']:
    row = {'route': path}
    try:
        request = Request(endpoint + path, headers={'api-key': key, 'Authorization': 'Bearer ' + key})
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read())
            row.update(status=response.status, data=payload)
    except HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        row.update(status=exc.code, error=body.replace(key, '[REDACTED]'))
    except (URLError, OSError) as exc:
        row.update(status=None, error=str(exc).replace(key, '[REDACTED]'))
    checks.append(row)
    if row['status'] == 200:
        break
report = {'checked_utc': datetime.now(timezone.utc).isoformat(), 'endpoint': endpoint, 'kind': 'read-only metadata/authentication check; no model generation', 'checks': checks}
p = Path(__file__).resolve().parents[1] / 'evidence/azure-access-check.json'
p.write_text(json.dumps(report, indent=2) + '\n')
for row in checks:
    print('Route:', row['route'], 'HTTP status:', row['status'])
    if 'data' in row:
        data = row['data']
        if args.full:
            print(json.dumps(data, indent=2))
        else:
            models = data.get('data', [])
            print(f'Authentication succeeded. Catalog entries: {len(models)}; this does not confirm deployed models.')
            for model in models:
                name = model.get('id', '')
                if name.startswith(('gpt-4-', 'gpt-4o-')) and model.get('capabilities', {}).get('chat_completion'):
                    stamp = model.get('deprecation', {}).get('inference')
                    date = datetime.fromtimestamp(stamp, timezone.utc).date().isoformat() if stamp else 'unknown'
                    print(name, '|', model.get('lifecycle_status', 'unknown'), '| catalog inference date:', date)
            print('Next: inspect deployment names and exact model versions in Foundry.')
    else:
        print(row['error'][:800])
