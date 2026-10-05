# τ-bench 2024 Retail Reproduction

A documented reproduction of the original [τ-bench paper](https://arxiv.org/abs/2406.12045v1), before any Human API research extensions.

**Status: historical-source audit and offline validation complete (11 controlled checks passed). Live LLM pilot trajectories and numerical results are pending.** Static task examples and gold replays must not be interpreted as model performance.

The baseline is Sierra Research's initial public release, **`6f4b718037db619539b8b692060e6686f3f0dcc9`**, committed June 17, 2024. This is the closest defensible public paper-era version; the exact internal experiment commit is not certified. The project owner approved this documented uncertainty. Later task fixes, τ²/τ³ infrastructure, and research modifications are excluded.

## Start here

| Document | Purpose |
|---|---|
| [Reproduction notes](REPRODUCTION_NOTES.md) | Commit evidence, progress, deviations and open questions |
| [Architecture](ARCHITECTURE.md) | Agent/user visibility, tools, policies, turn lifecycle and exact scoring |
| [Paper configuration](PAPER_CONFIGURATION.md) | Paper settings versus actual environment; historical CLI commands |
| [Task examples](TASK_EXAMPLES.md) | Five historical task definitions and starting-state references |
| [Baseline summary](BASELINE_SUMMARY.md) | Current status and next step |
| [Compatibility changes](COMPATIBILITY_PATCHES.md) | Every environment/code adjustment |
| [Original project brief](REPRODUCTION_BRIEF.md) | Scope, constraints and required deliverables |
| [Historical README](evidence/README.paper-era.md) | Unchanged release setup instructions |

Historical benchmark implementation is under `tau_bench/`, with its original `run.py` and `setup.py`. The [upstream repository](https://github.com/sierra-research/tau-bench) and original MIT [license](LICENSE) are retained. This README is reproduction documentation; historical prompts, tasks, policies, APIs, database and evaluator are unchanged.

## Reproduction commands

Use a dedicated environment on a machine with package-network access. The historical release uses underscore flags and `function_calling`; current upstream examples do not apply.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .
.venv/bin/python -m pip freeze > evidence/installed-packages.txt
```

Set `OPENAI_API_KEY` in the shell environment without adding it to Git. The code does not automatically load `.env`. See [model caveats](PAPER_CONFIGURATION.md) before invoking an endpoint: the paper's explicit user snapshot is missing from historical cost dictionaries and cannot safely be passed without a documented accounting patch.

Static source audit (no dependencies/model calls):

```bash
python3 scripts/audit_sources.py
```

Offline backend/reward verification (requires OpenAI SDK and tenacity, but makes no network or model calls):

```bash
python3 scripts/verify_offline.py
```

The offline verifier uses gold annotations and controlled synthetic scorer inputs. It verifies implementation behavior, not agent competence or user simulator behavior. Results belong in `evidence/`; actual agent trajectories will belong in `results/pilot/` once generated.

## Team review

Work is on `reproduce-tau-2024`. Review commit selection and model configuration first. Keep compatibility patches separate from documentation and experiments. Do not change task semantics, silently substitute models, or implement Human API metrics in this baseline.
