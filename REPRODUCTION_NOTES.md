# τ-bench 2024 Reproduction Notes

## Goal

Reproduce the original retail baseline before any Human API research modifications. This record is in progress: the source audit and offline backend/reward verification are complete; live execution awaits an OpenAI API key. No pilot scores or numerical reproduction claims exist.

## Paper and repository

- Paper: *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains*, [arXiv v1](https://arxiv.org/abs/2406.12045v1), submitted June 17, 2024, 19:33:08 UTC.
- Supplied paper: `../2406.12045v1.pdf`. Inspected through `pdftotext -layout`; extracted text initially saved to `/tmp/tau-paper-v1.txt`.
- Repository: https://github.com/sierra-research/tau-bench, cloned locally into this directory on 2026-10-05.
- τ²/τ³ code has not been imported.
- Audit helper: `python3 scripts/audit_sources.py`. It extracts literals without importing benchmark modules or invoking models. Git history, task fixes, original source hashes and task snapshots are saved under `evidence/`.

## Paper-era commit selection

Selected closest defensible public release: `6f4b718037db619539b8b692060e6686f3f0dcc9`, **Initial commit**.

Author date: June 6, 2024, 10:11:36 −07:00. Committer date: June 17, 2024, 10:30:45 −07:00 (17:30:45 UTC), roughly two hours before the arXiv v1 submission. Distinguishing these dates is essential: sorting by author date alone obscures its publication-day release.

Evidence supporting selection:

- This is the initial public history and the only commit committed by the paper release date.
- Source contains the 115 retail test tasks, 500 users, 1,000 orders and 50 products from paper Table 1.
- Full policy, naive user simulator, 30-action limit, agent temperature 0 and user temperature 1 agree with the paper descriptions.
- The release README runs `python run.py --env retail --model gpt-4o --max_concurrency 10`.
- There are no repository tags. Remote branch inventory is saved in `evidence/git-branches.txt`.

Alternatives considered:

| Commit | Date | Why not selected |
|---|---|---|
| `bcdeb61` | June 25, 2024 | Fixes Claude integration and adds Claude 3.5 after publication |
| `fa2a75f` | June 25, 2024 | Post-publication README update |
| `8c48def` | June 28, 2024 | Adds artifact ignore rules; useful housekeeping but not release code |
| `2d5b206` | July 10, 2024 | Changes a gold refund payment ID and two task instructions |
| `a8f3cf5` | July 11, 2024 | Changes task 9 gold variant and instructions for tasks 16, 20, 35 |
| `8d339ff` | July 28, 2024 | Adds pass^k aggregation absent at initial release |
| `043b544` | September 3, 2024 | Rewrites infrastructure; later CLI examples do not apply |
| Current `main` | March 2026 latest history | Includes subsequent task/evaluator changes and references newer benchmarks |

Uncertainty: the paper does not publish an experiment commit hash and the public repository has no certified paper release tag. Initial release correspondence is strongly supported, but the exact internal code used for Table 2 cannot be proved from this history. Per section 23 of the supplied brief, this has been reported to the user before installation or execution. On 2026-10-05 the user explicitly approved proceeding with the initial release and documented uncertainty (“ok”). This resolves the commit-selection stop condition without certifying exact experiment provenance.

The July changes are materially different task semantics, preserved in `evidence/july-task-fixes.diff`; they are excluded. They are after the June release, rather than evidence of an ambiguous series of publication-day task edits.

Local branch: `reproduce-tau-2024`, created from the selected release. Historical benchmark implementation remains unchanged. The README is now a team landing page; its original bytes are retained in `evidence/README.paper-era.md`.

## Original environment assumptions

Exact original OS, Python version and resolved dependency versions are unknown. Python ≥3.10 is required by `match` syntax. `setup.py` declares lower bounds: openai 1.13.3, mistralai 0.4.0, anthropic 0.26.1, google-generativeai 0.5.4, tenacity 8.3.0, termcolor 2.4.0, numpy 1.26.4. No lockfile exists. Editable installation is documented. `envs/user.py` creates an OpenAI client at import time, so a key is required even before CLI execution reaches task initialization. It does not load `.env` itself.

Local inspection environment: macOS. Shell Python varies with working directory: the workspace default is Miniforge Python 3.12.11, while the repository shell selected Framework Python 3.12.0. Explicit executable paths now avoid this ambiguity. `pdftotext` is available. `.venv` records the isolated failed installation attempt; `.venv-offline` uses Miniforge 3.12.11 with system packages exposed for offline verification.

## Original models

Paper §5 evaluates GPT, Claude, Gemini, Mistral and Llama families. Selected target is GPT-4o function calling; paper §3 names user `gpt-4-0613`, release defaults to `gpt-4`. See `PAPER_CONFIGURATION.md` for alias uncertainty, snapshot accounting incompatibilities and endpoint evidence. No models have been called or substituted.

## Original agent strategy

`GPTFunctionCallingAgent` receives full policy and tool schemas. It sees the user's generated conversation rather than the hidden task. It chooses one tool or spoken response per action and retains all observed results, up to 30 actions. Optional thinking is disabled in the default FC baseline. See `ARCHITECTURE.md` for exact functions.

## Original user simulator

`NaiveUserSimulationEnv` has the task instruction, simulator prompt and full speech history. It sees no tools, database or domain policy. The prompt prohibits fabricating missing information, but no mechanical validation enforces this. User intent may change conditionally, and personality instructions may discourage disclosure. Empirical compliance is untested.

## Retail task structure

Test: 115 tasks; dev: 20; train: 500. Tasks encode instruction, annotator, user ID, gold actions and optional outputs. Only the instruction is directly supplied to the simulator. All tasks use the full shared database with a fresh per-episode copy. Five examples (0, 2, 16, 22, 24) and their exact starting records are in `TASK_EXAMPLES.md` and `evidence/task-examples.json`. These are source evidence, not trajectories.

## Retail policy structure

Policy is `tau_bench/envs/retail/wiki.md`. Authenticate by email or name + ZIP, even when a user ID is supplied. Serve one user; explicitly confirm consequential changes; check pending/delivered status; obey one-use item modification/exchange and payment restrictions. Profile and pending shipping address updates use different tools. Detailed procedures and alternative lookup path are in `ARCHITECTURE.md`.

## Backend tools

Seven writes and eight non-writes are normally exposed. Profiles reveal email, full address/ZIP, payment methods and order IDs. Order details reveal items, status, fulfillment and payments; product details reveal variants and availability. New intent/preferences and confirmation come from speech. There is no explicit authentication state gate or structured required-human-fact representation.

## Scoring and reward

Binary reward: complete final database hash equality with the state produced by gold-action replay, AND all required agent response substrings. No LLM judge, intermediate action sequence matching or explicit penalty for extra questions/read actions exists. Missing constraints default to passing their respective component. Reward is evaluated only on termination; action-limit exhaustion stays zero.

The evaluator overwrites the live database with gold data during scoring. Raw pre-scoring state must therefore be captured separately for a faithful record. GPT trajectories retain tool calls as strings instead of structured arguments. See `ARCHITECTURE.md` for failures, retries, termination and provenance details.

## Installation issues

Attempted the original editable install in an isolated environment; PyPI DNS/network access failed while fetching build dependencies (`evidence/install.log`, `pip-upgrade.log`). This is an infrastructure failure, not proof of incompatible historical dependencies.

An initial offline fallback also failed: Framework Python had no SDK/build dependencies, and then modern setuptools `develop` tried a nested pip call that dropped build isolation flags. The successful fallback is explicitly partial:

```bash
/Users/salih/miniforge3/bin/python3 -m venv --system-site-packages .venv-offline
.venv-offline/bin/python -m pip install --use-pep517 --no-build-isolation --no-deps -e .
.venv-offline/bin/python -m pip freeze > evidence/installed-packages-system-fallback.txt
.venv-offline/bin/python scripts/verify_offline.py > evidence/offline-verification.log 2>&1
```

SDK 2.32.0, tenacity 9.1.4, termcolor 3.3.0, numpy 2.3.5 and setuptools 80.9.0 are inherited. Anthropic and Mistral SDKs are absent: this is sufficient for the offline retail/OpenAI path, not a complete historical installation. No dependency constraints were changed. Frozen inherited packages are an environment record, not a portable historical lock.

## Compatibility changes

No benchmark code patches. `.gitignore`, audit/verification helpers, evidence and documentation were added; see `COMPATIBILITY_PATCHES.md`. Exact snapshot support requires accounting/CLI changes identified there but not applied. No dependency pins yet. Modern packages exposed through a dedicated fallback venv are an explicitly recorded deviation.

## API/model substitutions

None. GitHub cloning and forking used existing authentication without copying credentials. Only environment-variable names were inspected in candidate project files; no values were printed or copied. No OpenAI key was found. A request to configure the key locally is pending. Environment files are ignored. Account access to historical model endpoints remains unverified.

## Small pilot runs

No live LLM pilot has run. Offline gold replay is complete and explicitly excluded from pilot results. Proposed first task: 0, one trial, FC GPT-4o, original naive user, concurrency 1. Exact historical commands are in `PAPER_CONFIGURATION.md`. Inspect that trajectory before remaining tasks 2, 16, 22, 24. Task 16's missing explicit cancellation reason is a known historical ambiguity, retained intentionally.

## Observed trajectories

No model trajectories yet. Offline backend/scorer records are under `evidence/offline-*` and contain no simulated conversation. Source inspection shows the role/channel distinction can identify human versus backend messages; it does not establish factual novelty or necessity. Planned records include all messages, tools, original task, pre-evaluation state, reward, exact commands, run date, model identifiers/metadata, and package versions. Authentication behavior and unspecified-fact responses remain empirical questions.

## Reproduction of published results

Not attempted. Candidate target: original Table 2 GPT-4o FC retail pass^1 61.2%, at least three trials per task. A small pilot cannot be compared as numerical replication. Scale only after execution, scoring and simulator behavior have been inspected; no large API spend has occurred.

## Deviations from the paper

- Exact experiment commit is unverified; closest public release selected provisionally.
- No original environment lock is available.
- Code's user alias differs in specificity from the paper's named snapshot.
- Agent snapshot is unspecified in paper; chronology-based pinning would be an inference.
- No execution, pilot success rate or result reproduction yet.
- New files only support evidence and documentation; policies/tasks/prompts/tools/scoring/data are unchanged.

## Open questions

1. Resolved: owner approved using the initial public release with explicit uncertainty.
2. Which user endpoint should be requested: unchanged historical alias or explicit paper snapshot with accounting-only patch?
3. Can this account access the historical models before shutdown, and what snapshot does the agent alias actually return?
4. Full installation remains untested beyond network failure; partial modern-dependency fallback runs offline checks on Python 3.12.11.
5. Does the simulator consistently respect supplied facts, conditional goals and nondisclosure instructions in actual trajectories?
6. How much do historical defective annotations affect later aggregate interpretation? Keep defects intact and report them.

## Offline verification results (2026-10-05)

`scripts/verify_offline.py` executes historical tools and scorer with human mode and `obs=False`; a dummy nonfunctional key permits import-time OpenAI client construction. It never calls the API or human input. Eleven controlled checks passed, including five gold-state/output cases, state mismatch, missing required words, scorer hash capture, gold-state overwrite, lack of independent authentication enforcement, and lack of a direct penalty for an added read/question.

All 115 gold sequences were replayed. Tool-error observations occurred in 22 task definitions: 2, 3, 4, 5, 9, 12, 13, 21, 34, 35, 36, 37, 38, 39, 46, 47, 54, 55, 64, 67, 68, 106. These are **not uniformly defects**: failed identity lookups can be intentional, and refusal scenarios can legitimately leave state unchanged. Nevertheless, task 5's invalid refund method and task 9's unavailable exchange variant were explicitly fixed after release; task 34's gold write passes `province` to a function accepting `state` and therefore fails. They remain unchanged.

Because the evaluator uses the same tools and error handling to construct its target state, a failed gold write can yield a no-op target. Gold replay plus supplied output substrings returning 1 is therefore a self-consistency check, **not a 100% agent success rate** or evidence that every annotation achieves the natural-language goal. This is a material limitation for numerical interpretation; report it before any larger run. Complete errors and checks: `evidence/offline-verification.json`.

## GitHub sharing

User requested uploading the reproduction to GitHub for team review. Created `hassanql/tau-bench-2024-reproduction` as a fork of the original repository, preserving upstream history/license. The reproduction branch is `reproduce-tau-2024`; `team` is its local remote, while `origin` still refers to Sierra's upstream. No collaborator invitations or messages have been sent. The README is a new documentation landing page; no historical benchmark code is changed. Live results are explicitly pending.

Published audit commit: `66a032f` on `reproduce-tau-2024`. Team entry point: https://github.com/hassanql/tau-bench-2024-reproduction/tree/reproduce-tau-2024 . The fork default branch remains upstream `main`: changing repository settings through the local CLI hit a network restriction. Share the reproduction branch URL.
