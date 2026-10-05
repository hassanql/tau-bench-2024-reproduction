"""Extract historical source evidence without importing or executing benchmark code."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = '6f4b718037db619539b8b692060e6686f3f0dcc9'
OUT = ROOT / 'evidence'
OUT.mkdir(exist_ok=True)

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True)

def literal_tasks(name):
    tree = ast.parse((ROOT / 'tau_bench/envs/retail' / name).read_text())
    return ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'tasks' for t in n.targets)))

for name, args in {
    'git-log-all.txt': ['log', '--oneline', '--decorate', '--all'],
    'git-log-reverse.txt': ['log', '--all', '--reverse', '--format=%H %aI %cI %s'],
    'git-tags.txt': ['tag'],
    'git-branches.txt': ['branch', '-a'],
    'initial-commit.txt': ['show', '--no-patch', '--format=fuller', '6f4b718'],
    'july-task-fixes.diff': ['diff', '6f4b718', 'a8f3cf5', '--', 'tau_bench/envs/retail/tasks.py'],
}.items():
    (OUT / name).write_text(git(*args))

tasks = literal_tasks('tasks.py')
data = {name: json.loads((ROOT / f'tau_bench/envs/retail/data/{name}.json').read_text()) for name in ['users', 'orders', 'products']}
manifest = {'commit': BASE_COMMIT, 'task_counts': {split: len(literal_tasks(file)) for split, file in [('test','tasks.py'), ('train','tasks_train.py'), ('dev','tasks_dev.py')]}, 'database_counts': {k: len(v) for k,v in data.items()}, 'sha256': {}}
for relative in git('ls-tree','-r','--name-only',BASE_COMMIT).splitlines():
    p = ROOT / relative
    if p.is_file():
        manifest['sha256'][relative] = hashlib.sha256(subprocess.check_output(['git', 'show', f'{BASE_COMMIT}:{relative}'], cwd=ROOT)).hexdigest()
(OUT / 'source-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
examples = []
for index in [0, 2, 16, 22, 24]:
    task = tasks[index]
    user = data['users'][task['user_id']]
    examples.append({'task_id': index, 'task': task, 'starting_user': user, 'starting_orders': {oid: data['orders'][oid] for oid in user['orders']}, 'note': 'Static source extraction; this is not an agent run or trajectory. All tasks start from the full shared database.'})
(OUT / 'task-examples.json').write_text(json.dumps(examples, indent=2) + '\n')
print(json.dumps({k:v for k,v in manifest.items() if k!='sha256'}, indent=2))
