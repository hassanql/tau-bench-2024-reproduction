# Compatibility patch list

Audit date: 2026-10-05. No historical benchmark code or dependency settings have been changed. Historical isolated installation failed on package-network access. A partial offline editable installation succeeded with modern inherited packages.

| File | Change | Reason | Semantics changed? | Possible result impact |
|---|---|---|---|---|
| `.gitignore` (new) | Ignore env files, venvs, caches and build artifacts | Initial release had no ignore file; protect secrets and separate generated dependencies | No | None |
| `scripts/audit_sources.py` (new) | AST-based static extraction, source hashes, Git evidence and task snapshots | Preserve source evidence without imports or API calls | No | None; script does not run the benchmark |
| `scripts/verify_offline.py` (new) | Gold-action replay and controlled reward checks, no API calls | Verify backend/scoring | No | None on benchmark; synthetic checks are not agent results |
| `README.md` | Team landing page; original preserved in `evidence/README.paper-era.md` | GitHub sharing | No benchmark semantics | None |
| Documentation and `evidence/` (new) | Audit record and static source extracts | Required reproducibility record | No | None |

Potential changes identified, **not applied**:

- Add `gpt-4-0613` to historical simulator cost tables to permit the paper's explicit user snapshot. This is accounting-only, but without it successful calls are retried and discarded.
- If selecting the inferred May 2024 GPT-4o snapshot, permit its model identifier in CLI choices and agent cost tables. This pins an endpoint, so the configuration decision must be recorded independently of the mechanical patch.
- External capture of the pre-evaluation database and structured request metadata would strengthen the raw record. Keep the historical evaluator and prompts intact. No future Human API instrumentation has been implemented.

No compatibility commit exists because no compatibility patch has been applied.

## Environment fallback

`.venv-offline` exposes existing Miniforge system packages and installs the package using `--use-pep517 --no-build-isolation --no-deps -e .`. This is an explicit environment deviation, with no `setup.py` edits. It does not satisfy the unused Anthropic/Mistral provider requirements and does not claim historical dependency identity. See installation logs and `installed-packages-system-fallback.txt`.
