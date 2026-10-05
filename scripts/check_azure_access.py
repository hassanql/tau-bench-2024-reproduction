"""Read-only Azure endpoint/authentication check; never logs the API key."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

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
        print(json.dumps(data, indent=2)[:14000])
    else:
        print(row['error'][:800])
