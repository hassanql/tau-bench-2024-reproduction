# τ-bench 2024 Paper Configuration

Audit date: 2026-10-05. Evidence: supplied `../2406.12045v1.pdf` (arXiv v1, June 17, 2024) and initial release `6f4b718037db619539b8b692060e6686f3f0dcc9`. This is a source-grounded proposed live configuration. Offline backend/scorer verification ran; no live model experiment has run.

| Component | Original setting | Evidence | Reproduction setting | Deviation |
|---|---|---|---|---|
| Agent model | `gpt-4o` for the selected FC baseline | Paper §5, Table 2; historical README | Proposed `gpt-4o`; no calls made | Exact paper agent snapshot is not specified; alias identity must be recorded |
| User model | `gpt-4-0613` in paper; code default `gpt-4` | Paper §3; `run.py:main`; `envs/user.py` | Pending decision: historical `gpt-4` alias or explicit `gpt-4-0613` | Explicit snapshot is accepted by CLI but missing from user cost dictionaries |
| Agent strategy | Function calling | Paper §5; README | `--agent_strategy function_calling --think 0` | None proposed |
| User strategy | LLM simulator with instruction and dialogue history | Paper §3; `NaiveUserSimulationEnv` | Hardcoded `naive` in historical runner | Later `--user-strategy llm` does not exist |
| Temperature | Agent 0.0; user 1.0 | Paper §5; GPT/user wrappers | `--temperature 0.0`; user hardcoded 1.0 | None proposed |
| Max turns | 30 agent actions | Paper §5; `GPTFunctionCallingAgent.act` | Hardcoded 30 | Counts speech and tool actions, not dialogue pairs |
| User token cap | Not specified in paper passages inspected; code 150 | `NaiveUserSimulationEnv.reset/step` | Hardcoded 150 | Code evidence only |
| Concurrency | Paper value unknown; README example 10; CLI default 1 | README; `run.py:main` | Proposed `--max_concurrency 1` | Pilot execution setting, not claimed paper setting |
| Number of trials | At least 3 per task for Table 2; larger experiments vary | Paper §5 and §5.1 | Proposed `--num_trials 1` for pilot | Insufficient for multi-trial reliability reproduction |
| Retail task count | 115 evaluation tasks | Paper Table 1; literal extraction of `tasks.py` | Same 115 test tasks, proposed pilot IDs 0, 2, 16, 22, 24 | Pilot subset only; historical defects preserved |
| Retail data | 500 users, 50 products, 1,000 orders | Paper Table 1; source JSON | Identical source files | None |
| Tools | 7 write, 8 non-write | Paper Table 1; tool list with `think` filtered | Same 15 exposed functions | None proposed |
| Reward | Binary final-state equality AND required output substrings | Paper §3; `BaseEnv.calculate_reward` | Historical evaluator unchanged | Does not independently verify all policy compliance |
| pass^1 | Mean task success probability | Paper §3 | Historical runner mean reward | One trial per task is only a pilot estimate |
| pass^k | Task mean `C(c,k)/C(n,k)` | Paper §3 | Not calculated yet | Aggregation code absent from initial release |
| Python | Original exact version unknown; code requires ≥3.10 syntax | `match` in retail environment | Offline venv: Miniforge Python 3.12.11; initial Framework 3.12.0 venv install failed | Installation compatibility not tested |
| Dependencies | Lower bounds, no exact lock | `setup.py` | Partial editable install with inherited modern packages; see frozen evidence | Full provider requirements not installed; offline fallback is not the historical environment |
| Seed | Paper value unknown; code default 10 | `run.py:main` | Proposed `--seed 10 --shuffle 0` | Python RNG seed does not fix model sampling |

## Commands derived from the historical runner

These commands are planned only. Do not use later hyphenated flags or `--task-ids`, `--model-provider`, or `--user-strategy`; this commit does not expose them. `--end_index` is exclusive.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .
.venv/bin/python -m pip freeze > evidence/installed-packages.txt

# One-task pilot using historical CLI defaults for the user alias:
.venv/bin/python run.py --env retail --task_split test \
  --agent_strategy function_calling --think 0 --model gpt-4o \
  --user_model gpt-4 --temperature 0.0 --max_concurrency 1 \
  --num_trials 1 --start_index 0 --end_index 1 \
  --seed 10 --shuffle 0 --log_dir results/pilot --verbose
```

After the first trajectory has been inspected, run each of the other selected indices separately using `[2,3)`, `[16,17)`, `[22,23)`, `[24,25)`. Task 16 was amended after release to supply a cancellation reason; preserving the original is intentional, and its ambiguity must be reported, not fixed. Task 24 changes its cancellation goal into an information request. Do not run all tasks between indices 0 and 25 as a substitute for these five.

## Snapshot and cost-accounting issue

The paper names the user snapshot but only names the agent alias. Passing `--user_model gpt-4-0613` to the unchanged code would fail after generation when it indexes `prompt_price_per_million[model]`. The tenacity wrapper then retries, potentially spending on ten successful generations that cannot be returned. A minimal separately documented cost-table patch is needed before requesting this snapshot directly. No patch has been made. Actual historical dollar constants are not current invoice estimates.

The paper-era agent snapshot `gpt-4o-2024-05-13` is a candidate inferred from chronology, not explicitly stated in the paper. It is not accepted by the original model choices and is absent from agent cost dictionaries. Using it needs an explicit configuration/accounting patch and documented inference; it cannot silently be labeled the exact published setting.

## Current endpoint evidence

The [OpenAI deprecation page](https://developers.openai.com/api/docs/deprecations), consulted 2026-10-05, lists an October 23, 2026 shutdown for `gpt-4-0613` (and its `gpt-4` alias) and `gpt-4o-2024-05-13`. This indicates possible availability before that date, not verified access in this account. No real OpenAI key has been loaded and no endpoint has been called; the offline verifier uses a dummy placeholder only for import-time client construction. Historical model names shown in documentation do not prove reproducible backend behavior.

## Published result target

The original paper's Table 2 reports GPT-4o FC retail pass^1 = 61.2%, with at least three trials per task. A five-task, one-trial pilot does not reproduce that statistic. Code reproduction, behavioral reproduction, and numerical reproduction will be reported separately. Any unavailable endpoint or substitute requires reporting before continuing, per the brief.
