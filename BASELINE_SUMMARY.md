# τ-bench 2024 Reproduction Report

## Status

Historical source audit and offline verification complete. Owner approved the initial-release uncertainty. Reproduction remains incomplete: Azure authentication is confirmed by a user-run HTTP 200 metadata check; direct chat and function-calling probes now confirm deployment gpt-4o-2 returns GPT-4o-2024-11-20; live pilot awaits an explicit model-configuration decision; full isolated installation now succeeds after enabling network access. Five static task examples are preserved; they are not pilot trajectories.

## Selected commit

`6f4b718037db619539b8b692060e6686f3f0dcc9` (Initial commit), committed June 17, 2024, the arXiv v1 release date. Branch `reproduce-tau-2024`. This is the closest defensible public version; no experiment hash/tag certifies exact identity. Later task fixes and infrastructure rewrites are excluded.

## Environment

macOS; available Python 3.12.11. Full isolated editable installation now succeeds in Framework Python 3.12.0 (`.venv`), with modern resolved packages frozen in evidence. Dependency checks pass. The earlier Miniforge 3.12.11 offline fallback and failed installation logs are preserved. Original setup uses editable installation with unpinned dependency lower bounds.

## Models

Two bounded diagnostic model calls succeeded; no benchmark episodes ran. Proposed agent GPT-4o. Paper user GPT-4-0613; source default GPT-4 alias. Exact snapshot requests require an accounting patch. No substitution has been made. Current documented endpoint shutdown is October 23, 2026; account availability remains untested (see `PAPER_CONFIGURATION.md`).

## Agent configuration

Original function calling, full retail policy, automatic tool/speech choice, one executed tool per action, temperature 0, 30 actions, optional think disabled.

## User simulator configuration

Original `naive` LLM user, temperature 1, 150-token cap, task instruction and full dialogue history. Tools, database and domain policy are hidden. Prompt discourages inventing missing facts, but compliance is probabilistic and unobserved so far.

## Retail pilot results

No tasks run; success rate is unavailable, not zero. Proposed IDs: 0 (exchange), 2 (return and information), 16 (cancellations and return), 22 (address updates and reversal), 24 (cancel intent withdrawn, then product information). All 115 historical evaluation tasks remain unchanged.

## Scoring behavior

Eleven controlled offline scorer checks passed. Gold replays emitted tool errors in 22 task definitions; some are intentional lookup failures, while others include known historical write defects. These are not model performance results. Reward 1 requires final database equality with replayed gold actions and all encoded response substrings. Otherwise reward 0. No LLM judge or explicit unnecessary-question/read-action penalty exists. Additional actions can indirectly cause failure through incorrect state, omitted outputs or consuming the action budget. Authentication and confirmation are policy rules without independent reward checks. pass^1 is mean reward; pass^k measures all k trials succeeding.

## Key architectural observations

Agent and user have separate persistent contexts. The agent can issue consecutive tool calls. The user sees only spoken dialogue and can volunteer facts or change goals per instruction. User profiles contain identity/address/payment/order information; tools retrieve these and full order/product records. There is no structured known/unknown fact model or explicit authenticated flag. Message roles distinguish conversation and backend sources, though call serialization is lossy and fact-level provenance is absent.

## Compatibility changes

No benchmark code/dependency constraints changed. Added secret/artifact ignores, source audit and offline verification helpers, evidence and a team README; the original README is preserved. No compatibility commit or research modifications. Full details: `COMPATIBILITY_PATCHES.md`.

## Differences from the paper

Exact experiment commit and original resolved environment unknown. Source default user alias is less specific than the paper. All behavior claims above are code findings, not measured pilot observations. No numerical reproduction claim exists.

## Reproducibility limitations

Historical model alias drift; impending endpoint retirement; missing exact dependency lock; known later-corrected historical task defects; tool calls saved as object strings; evaluator overwrites agent-final database during gold replay. Full pre-scoring state and request metadata should be preserved externally when execution proceeds.

## What this implies for the Human API extension

Future work may need structured user facts, source/availability annotations, simulator disclosure control, fact-level provenance and separate solicitation/acquisition evaluation. None is implemented. The baseline first needs live trajectories that confirm actual simulator behavior and scoring.

## Recommended next step

Confirm actual Azure deployment names/model versions and inference access; the catalog lists the original GPT-4-0613 user model with a past retirement date. Report availability before any substitute, and complete an isolated dependency installation when package-network access permits. Choose alias versus explicit snapshot transparently before a one-task run, inspect the complete trajectory, and only then run the remaining four pilot tasks. Keep all compatibility patches separate and documented.

Verified deployment: `gpt-4o-2` returns `gpt-4o-2024-11-20`; both bounded chat and tool-calling probes succeeded. Using it in a baseline would be explicitly approximate. Original GPT-4-0613 user availability remains unresolved.
