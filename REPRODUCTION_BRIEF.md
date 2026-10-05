# Reproduce the Original 2024 τ-bench Before Modifying It

## Project context

I am extending research on **Human API / human over-acquisition in agentic systems**.

The long-term research question is about how an LLM agent acquires information from a human while also having access to backend tools. In particular, I eventually want to study when an agent:

- asks a human for information that is unnecessary for the task,
- actually acquires unnecessary information from the human,
- asks the human for information that could have been obtained from a backend tool instead,
- continues collecting information after a valid task subgoal has already been satisfied.

However, **do not implement any of those research modifications yet**.

The immediate objective is narrower:

> **Reproduce the original 2024 τ-bench setup as faithfully as possible, understand exactly how it works, and produce a clean reproducibility record before we modify anything.**

The original repository is:

- https://github.com/sierra-research/tau-bench

The original paper is:

- **τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains**
- arXiv: https://arxiv.org/abs/2406.12045

There is also a newer repository:

- https://github.com/sierra-research/tau2-bench

That newer repository now contains later τ² / τ³ development, updated tasks, voice, knowledge retrieval, task fixes, and refactored infrastructure.

For this phase, **do not start from τ² or τ³**.

We first want to reproduce the original 2024 benchmark as closely as possible.

---

# 1. Primary objective

Your job is to create a **faithful, documented reproduction of the original 2024 τ-bench retail setup**.

The purpose is not yet to reproduce every number in the paper at full scale.

The purpose is to:

1. identify the code version that most closely corresponds to the original paper,
2. understand the architecture,
3. run a small number of retail tasks successfully,
4. inspect complete trajectories,
5. verify the scoring and user simulation behavior,
6. document all deviations from the original setup,
7. only then attempt a larger reproduction.

Do not optimize, clean up, modernize, or reinterpret the benchmark unless required to make the historical code run.

---

# 2. Non-negotiable constraints

## 2.1 Do not silently use the latest version

The current `main` branch of `sierra-research/tau-bench` is not necessarily the exact paper version.

The repository continued to change after publication.

You must inspect the Git history and determine a defensible **paper-era commit**.

Do not simply clone `main` and assume it corresponds to the paper.

---

## 2.2 Do not use τ² / τ³ for this reproduction phase

Do not use:

- `sierra-research/tau2-bench`
- τ²-specific code
- τ³-specific code
- voice functionality
- knowledge-retrieval functionality
- banking domains
- newer task fixes
- newer orchestration abstractions

Those may be useful later, but not in this phase.

---

## 2.3 Do not modify task semantics

Do not change:

- retail policies,
- task definitions,
- user instructions,
- gold actions,
- backend state,
- evaluation criteria,
- prompts,
- tool APIs,
- scoring rules,

unless a change is strictly necessary to make the old code execute in the current environment.

If any change is necessary, document it explicitly.

---

## 2.4 Do not add Human API / over-acquisition logic yet

Do **not** add:

- over-acquisition metrics,
- privacy scores,
- information-gain scores,
- required/surplus knowledge annotations,
- user burden measures,
- solicitation labels,
- acquisition labels,
- minimum-scope scoring,
- matched perturbation cases.

We first need an uncontaminated baseline.

---

## 2.5 Do not silently substitute models

If the exact original model is unavailable, do not just replace it.

Instead:

1. identify what the original paper/code used,
2. try to use it if still available,
3. if unavailable, choose a substitute,
4. document the substitution prominently,
5. separate:
   - **code reproduction**
   - **behavioral reproduction**
   - **numerical reproduction**

A newer model may make the code run, but it is not a faithful numerical reproduction of the original paper.

---

# 3. Repository setup

Create a local working copy of:

```bash
git clone https://github.com/sierra-research/tau-bench.git
cd tau-bench
```

Before installing anything, inspect:

```bash
git log --oneline --decorate --all
git log --reverse --oneline
git tag
git branch -a
```

Also inspect commit dates around:

- June 2024
- the arXiv release date
- the first public paper release
- any repository changes immediately before and after that period

Create a branch for the reproduction work:

```bash
git checkout -b reproduce-tau-2024
```

Do not do research modifications on this branch.

---

# 4. Identify the correct paper-era commit

This is the first substantive task.

Determine which commit best corresponds to the code used for the original 2024 paper.

Use evidence from:

- commit dates,
- paper release date,
- README history,
- paper commands,
- paper appendix,
- experiment scripts,
- model names,
- task counts,
- file structure,
- historical trajectories,
- any release notes or tags if they exist.

Do not guess.

Create a section in `REPRODUCTION_NOTES.md` called:

```md
## Paper-era commit selection
```

Include:

- selected commit hash,
- commit date,
- commit message,
- why it was selected,
- alternative nearby commits considered,
- any uncertainty.

If the exact paper commit cannot be established, say so clearly and choose the closest defensible version.

---

# 5. Create a reproducibility log

Create:

```text
REPRODUCTION_NOTES.md
```

This file is mandatory.

It should be updated throughout the work.

Use at least the following structure:

```md
# τ-bench 2024 Reproduction Notes

## Goal

## Paper and repository

## Paper-era commit selection

## Original environment assumptions

## Original models

## Original agent strategy

## Original user simulator

## Retail task structure

## Retail policy structure

## Backend tools

## Scoring and reward

## Installation issues

## Compatibility changes

## API/model substitutions

## Small pilot runs

## Observed trajectories

## Reproduction of published results

## Deviations from the paper

## Open questions
```

Never silently fix something.

Every compatibility modification must be recorded here.

---

# 6. Inspect the architecture before running anything

Before modifying or running code, map the system.

I want a clear description of:

```text
User simulator
      ↕
LLM agent
      ↕
Backend tools / environment
```

Identify the exact files implementing each component.

Specifically locate and document:

## Agent

Find:

- agent base class,
- tool-calling agent,
- ReAct agent if present,
- prompts,
- system messages,
- turn logic,
- tool-call parsing,
- termination logic.

Answer:

- What does the agent see at turn 0?
- Does the agent receive the full policy?
- Does the agent see the user task directly, or only the conversation?
- Does the agent see backend database state?
- Does the agent see tool outputs?
- Can the agent choose freely between speaking to the user and calling a tool?
- Is there any explicit turn limit?

---

## User simulator

Find:

- LLM user simulator,
- user system prompt,
- user task representation,
- any `known_info` / `unknown_info` or equivalent,
- conversation-history handling,
- user simulator strategies.

Answer:

- What information is supplied to the simulated user?
- What information can the user answer?
- What happens if the agent asks for information not explicitly supplied?
- Can the user volunteer information?
- Can the user refuse?
- Can the user hallucinate?
- Does the user see tool calls?
- Does the user see tool outputs?
- Does the user see the backend database?
- Does the user receive the entire conversation history?
- Does the user know the policy?

This part is especially important for our later research.

---

## Tools / backend environment

Find:

- retail tool definitions,
- backend database,
- state transition logic,
- read tools,
- write tools,
- tool execution wrapper.

Answer:

- Which information can the agent retrieve without asking the user?
- Which information is only available from the user?
- Which tools mutate state?
- Which tools only read state?
- Are tool calls always visible in the trajectory?
- Are tool results stored in the agent context?

---

## Policy

Locate the retail policy.

Document:

- authentication requirements,
- return rules,
- cancellation rules,
- exchange rules,
- address modification rules,
- payment-related requirements,
- any alternative valid procedures.

We will later use these procedural rules to define necessity, so understanding them exactly is important.

---

## Tasks

Locate the retail task definitions.

For at least 5 example tasks, document:

- user goal,
- starting database state,
- user-known information,
- expected behavior,
- expected backend action,
- expected final response,
- success criteria.

Do not reinterpret the task.

Describe what the benchmark actually encodes.

---

# 7. Determine the original experimental configuration

Extract the original experiment settings from both the paper and repository.

Create a table in `REPRODUCTION_NOTES.md`:

| Component | Original setting | Evidence | Reproduction setting | Deviation |
|---|---|---|---|---|
| Agent model | | | | |
| User model | | | | |
| Agent strategy | | | | |
| User strategy | | | | |
| Temperature | | | | |
| Max turns | | | | |
| Concurrency | | | | |
| Number of trials | | | | |
| Retail task count | | | | |
| Reward metric | | | | |

Verify everything from source.

Do not infer missing values without labeling them as inference.

---

# 8. Understand the scoring exactly

Before doing a large run, trace the scoring code.

I need a precise answer to:

1. What is the reward for one task?
2. What conditions cause reward = 1?
3. What conditions cause reward = 0?
4. Is backend state compared to a gold state?
5. Is final natural-language output scored?
6. Is an LLM judge involved?
7. Are intermediate actions scored?
8. Can multiple trajectories be correct?
9. What is `pass^k`?
10. How is `pass^1` computed?
11. How are failed API calls treated?
12. How are malformed tool calls treated?
13. How are user simulator failures treated?

Follow the code path from:

```text
trajectory
→ evaluator
→ reward
→ aggregate metric
```

Document exact filenames and functions.

---

# 9. Install the historical environment

Try to reproduce the original dependency setup as faithfully as practical.

If the original install command works, use it.

For example, if the repository expects:

```bash
pip install -e .
```

try that first inside an isolated environment.

Use a dedicated environment.

For example:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

If the historical dependencies fail on current Python, determine the oldest/current Python version that can reasonably run them.

Do not immediately rewrite the project.

Prefer:

1. selecting a compatible Python version,
2. pinning old dependencies,
3. minimal compatibility patching.

Every modification must be documented.

---

# 10. Preserve the historical code

Before any compatibility patch:

```bash
git status
git diff
```

After every patch:

```bash
git diff
```

Keep compatibility changes small.

Commit them separately, for example:

```text
compat: support current Python without changing benchmark semantics
```

Never mix compatibility changes with experimental modifications.

---

# 11. API keys and secrets

Do not commit API keys.

Use environment variables or `.env` only if supported.

Confirm `.env` / secret files are ignored by Git.

Before committing anything, check:

```bash
git status
```

Never print secrets into logs or `REPRODUCTION_NOTES.md`.

---

# 12. First execution: one retail task

Do not begin with the full benchmark.

First run:

- retail domain,
- one task,
- one trial,
- original tool-calling agent if available,
- original user simulator strategy if available.

The exact command should be derived from the paper-era code.

If the historical README command is applicable, it may look conceptually like:

```bash
python run.py \
  --agent-strategy tool-calling \
  --env retail \
  --model <AGENT_MODEL> \
  --model-provider <PROVIDER> \
  --user-model <USER_MODEL> \
  --user-model-provider <PROVIDER> \
  --user-strategy llm \
  --task-ids <ONE_TASK_ID>
```

Do not blindly use this command if the selected paper-era commit differs.

Verify the arguments from that commit.

---

# 13. Inspect the first trajectory manually

Once one task runs, do not scale immediately.

Inspect the full trajectory.

Produce a short structured trace like:

```text
Turn 0
USER:
...

Turn 1
AGENT:
...

Turn 2
TOOL CALL:
...

TOOL RESULT:
...

Turn 3
AGENT:
...

Turn 4
USER:
...
```

For the first successful trajectory, explicitly identify:

- every user message,
- every agent message,
- every tool call,
- every tool result,
- final response,
- backend state change,
- final reward.

Also answer:

> Can we mechanically distinguish information obtained from the human from information obtained from backend tools?

If yes, explain exactly how.

If not, explain what would need to be instrumented later.

---

# 14. Pilot run: 3–5 retail tasks

After one task works, run approximately:

```text
3–5 retail tasks
×
1 trial each
```

Choose tasks with different transaction types if possible, for example:

- order status,
- cancellation,
- return,
- exchange,
- address/account modification.

Do not yet optimize model performance.

The purpose is to inspect behavior.

For each trajectory, record:

- success/failure,
- number of user turns,
- number of tool calls,
- whether authentication occurred,
- whether the agent requested customer information,
- whether the user answered,
- whether similar information was available through tools.

Do not call anything “over-acquisition” yet.

Just record what happened.

---

# 15. Questions the pilot must answer

After the 3–5 task pilot, give explicit answers to all of these:

## Interaction

- Is the conversation strictly sequential?
- Can the agent choose between asking the user and calling tools?
- Can the agent call several tools consecutively?
- Can the user initiate new information?
- Is conversation state persistent across turns?

## Human information

- What customer facts exist?
- Which facts are explicitly given to the simulated user?
- Which facts exist only in the backend?
- Can the user answer questions beyond its original task specification?
- If asked for an unspecified fact, does the user say “I don't know,” invent something, refuse, or behave inconsistently?

## Authentication

- How exactly does retail authentication work?
- Are there alternative valid authentication paths?
- Once one path succeeds, does the policy require or permit additional authentication information?
- Is authentication state represented explicitly?

## Tools

- Can the agent retrieve customer email, address, order ID, ZIP code, etc. through tools?
- Which facts can only come from the user?
- Which facts can come from either source?

## Evaluation

- Does task success depend only on final backend state?
- Does final language matter?
- Does asking unnecessary questions reduce reward?
- Does taking extra read actions reduce reward?
- Does asking the user for redundant information reduce reward?

This last group will tell us whether τ-bench already contains any implicit information-minimization incentive.

---

# 16. Reproduce a larger baseline only after the pilot works

Once:

- installation is stable,
- scoring is understood,
- trajectories look correct,
- user simulation is understood,

then run a larger subset.

Do not immediately run the entire benchmark if API cost is high.

Suggested progression:

```text
1 task × 1 trial
↓
5 tasks × 1 trial
↓
20 tasks × 1 trial
↓
full retail × 1 trial
↓
multiple trials if needed
```

At each stage, inspect failure modes.

---

# 17. Published-result reproduction

Only after the environment is stable should you attempt to reproduce a published result.

Identify one result from the original paper that is feasible to reproduce.

Prefer:

- retail,
- tool-calling agent,
- a model still available or a historically equivalent configuration.

Report separately:

## Exact reproduction

Only if the exact original model and configuration are available.

## Approximate reproduction

If using a substitute model or changed API.

Do not claim numerical reproduction when using a different model.

---

# 18. Do not chase exact leaderboard numbers prematurely

The main success criterion for this phase is **not**:

> “our pass^1 exactly matches the paper.”

The important success criteria are:

- the historical environment runs,
- the architecture is understood,
- trajectories are interpretable,
- reward computation is verified,
- retail tasks behave as expected,
- the user simulator behavior is understood,
- deviations are documented.

Numerical replication is useful but secondary if model endpoints have changed.

---

# 19. Required deliverables

When this reproduction phase is complete, I want the following.

## Deliverable 1 — `REPRODUCTION_NOTES.md`

Complete and detailed.

---

## Deliverable 2 — `ARCHITECTURE.md`

Create:

```text
ARCHITECTURE.md
```

It should explain:

```text
user simulator
↕
agent
↕
tools / environment
↕
retail database
```

Include exact source files and important functions/classes.

Also include the lifecycle of one turn.

---

## Deliverable 3 — `PAPER_CONFIGURATION.md`

Create:

```text
PAPER_CONFIGURATION.md
```

Record the original paper settings and the settings actually used in our reproduction.

Clearly mark unknown or inferred values.

---

## Deliverable 4 — pilot trajectories

Save the complete outputs for the 3–5 pilot tasks.

Do not only save aggregate scores.

Preserve full trajectories.

---

## Deliverable 5 — compatibility patch list

Provide a concise list of every code/dependency change required to make the old benchmark run.

For each one state:

- file changed,
- reason,
- whether semantics changed,
- whether it could affect benchmark results.

---

## Deliverable 6 — baseline summary

Write:

```text
BASELINE_SUMMARY.md
```

It should answer:

1. Did the original benchmark run?
2. Which commit was used?
3. Which model(s) were used?
4. Which retail tasks were run?
5. What success rates were observed?
6. How does scoring work?
7. How does the user simulator behave?
8. What customer information is available?
9. What information can tools retrieve?
10. What aspects of the environment will need modification for a future human-over-acquisition experiment?

Do not implement those modifications yet.

---

# 20. Future phase — context only, do not implement now

The eventual research extension will likely introduce a richer user information model.

A future task may distinguish:

```text
required_user_information
surplus_user_information
already_known_information
backend_available_information
```

We may eventually distinguish:

```text
over-solicitation
=
agent requests unnecessary human-held information

over-acquisition
=
user actually reveals unnecessary information

unnecessary human sourcing
=
information is task-relevant,
but asking the human was unnecessary because another valid source was available
```

We may also later create controlled matched pairs such as:

```text
Condition A:
email is necessary

Condition B:
email has already been supplied

Condition C:
email can be retrieved from backend
```

But again:

> **Do not implement any of this in the reproduction branch.**

The purpose of the baseline is to understand the unmodified system first.

---

# 21. Research integrity requirements

Throughout the reproduction:

- distinguish what the paper says from what the code does,
- distinguish what the historical code does from what current APIs force us to do,
- never silently change task definitions,
- never silently substitute models,
- never silently alter prompts,
- never silently fix benchmark logic,
- preserve raw trajectories,
- preserve exact commands,
- record package versions,
- record Git commit hashes,
- record model identifiers,
- record run dates.

The final reproduction must be auditable.

---

# 22. Suggested working sequence

Use this order:

```text
1. Clone original τ-bench
2. Inspect Git history
3. Identify paper-era commit
4. Create reproduction branch
5. Map architecture
6. Inspect paper configuration
7. Inspect retail tasks/policy/tools
8. Trace scoring
9. Build compatible environment
10. Run 1 retail task
11. Inspect full trajectory
12. Run 3–5 retail pilot tasks
13. Answer pilot questions
14. Run larger retail subset
15. Attempt one published-result reproduction
16. Finish documentation
17. Stop before research modifications
```

---

# 23. Stop conditions

Stop and report before proceeding if any of these occur:

- exact paper-era commit cannot be identified,
- repository cannot run without substantial semantic changes,
- original model API is unavailable,
- user simulator behavior is inconsistent with the paper,
- reward implementation differs materially from the paper,
- task files appear to have changed significantly around the paper date,
- reproducibility requires importing logic from τ² or τ³,
- more than minimal compatibility patches are required.

Do not solve these silently.

Report them.

---

# 24. Final report format

At the end of the reproduction phase, give me a concise report with these headings:

```md
# τ-bench 2024 Reproduction Report

## Status

## Selected commit

## Environment

## Models

## Agent configuration

## User simulator configuration

## Retail pilot results

## Scoring behavior

## Key architectural observations

## Compatibility changes

## Differences from the paper

## Reproducibility limitations

## What this implies for the Human API extension

## Recommended next step
```

The recommended next step should still **not** implement the Human API experiment unless the reproduction phase is complete.

---

# 25. Core principle

The guiding rule for this entire phase is:

> **Reproduce first. Understand second. Modify third.**

Do not let convenience collapse those stages into one.
