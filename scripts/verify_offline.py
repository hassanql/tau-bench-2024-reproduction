"""Verify historical backend/reward behavior without LLM calls.

Gold-action replay and controlled scoring checks are NOT agent pilot trajectories.
A placeholder key only permits the historical import-time OpenAI constructor.
Human mode plus obs=False prevents all user-model and stdin interaction.
"""
import json
import os
import sys
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('OPENAI_API_KEY', 'offline-placeholder-not-a-real-key')
from tau_bench.envs.retail import MockRetailDomainEnv

ROOT = Path(__file__).resolve().parents[1]

def prepare(index, omit_auth=False, add_outputs=True):
    env = MockRetailDomainEnv(user_mode='human')
    env.reset(index=index, obs=False)
    errors = []
    for action in env.task['actions']:
        if action['name'] in env.terminate_tools or (omit_auth and action['name'].startswith('find_user_id')):
            continue
        observation, _, done, _ = env.step(deepcopy(action))
        if observation.startswith('Error:') or done:
            errors.append({'action': action, 'observation': observation})
    if add_outputs and env.task.get('outputs'):
        # Controlled scorer input only, not generated user-facing language.
        env.actions.append({'name':'respond','arguments':{'content':' '.join(env.task['outputs'])}})
    return env, errors

rows=[]
for index in range(115):
    env, errors = prepare(index)
    agent_data = deepcopy(env.data)
    reward, info = env.calculate_reward()
    rows.append({'task_id':index,'reward':reward,'gold_tool_errors':errors,'pre_scoring_data_hash':info['data_hash'],'gold_data_hash':info['gt_data_hash']})

checks=[]
def record(name, actual, expected):
    checks.append({'check':name,'actual':actual,'expected':expected,'passed':actual==expected})

for index in [0,2,16,22,24]:
    env, errors = prepare(index)
    pre = deepcopy(env.data)
    reward, info = env.calculate_reward()
    record(f'gold state and required substrings task {index}',reward,1)
    (ROOT/f'evidence/offline-gold-task-{index}.json').write_text(json.dumps({'kind':'offline gold replay, not a pilot trajectory','task_id':index,'tool_errors':errors,'state_before_scoring':pre,'reward':reward,'reward_info':info},indent=2)+'\n')

env,_=prepare(24,add_outputs=False)
record('correct state but missing required words fails',env.calculate_reward()[0],0)
env,_=prepare(0)
env.data['orders']['#W2378156']['status']='delivered'
pre_hash=env.get_data_hash()
reward,info=env.calculate_reward()
record('incorrect final database fails',reward,0)
record('evaluation records actual pre-replay hash',info['data_hash'],pre_hash)
record('evaluation leaves database at gold hash',env.get_data_hash(),info['gt_data_hash'])
env,_=prepare(0,omit_auth=True)
record('authentication sequence not independently enforced by reward',env.calculate_reward()[0],1)
env,_=prepare(0)
env.step({'name':'get_user_details','arguments':{'user_id':'yusuf_rossi_9620'}})
env.actions.append({'name':'respond','arguments':{'content':'Please tell me your email again.'}})
record('extra read and unrequired question have no direct reward penalty',env.calculate_reward()[0],1)
report={'kind':'offline gold replay and controlled scorer checks; no LLM or user behavior sampled','utc':datetime.now(timezone.utc).isoformat(),'task_count':len(rows),'tasks_with_gold_tool_errors':[r['task_id'] for r in rows if r['gold_tool_errors']],'checks':checks,'tasks':rows}
(ROOT/'evidence/offline-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='tasks'},indent=2))
assert all(c['passed'] for c in checks)
