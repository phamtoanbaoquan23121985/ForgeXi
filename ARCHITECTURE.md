# ForgeXi Architecture

ForgeXi is an evidence-driven coding-agent system. Completion is a verified state, not a model claim.

## Layers
1. Dashboard — task input, live trajectory, diff, verification receipt.
2. Orchestrator — bounded state machine, budgets, retry policy, checkpoints.
3. Agents — planner, coder, reviewer, executor behind a provider-neutral decision contract.
4. Runtime — Nebius/NVIDIA Nemotron adapter, usage accounting, caching, failure handling.
5. Validator & Evidence — tests, builds, security checks, metrics, immutable run artifacts.

## Invariants
- No task is DONE until required verification gates pass.
- Provider failures never silently become successful agent actions.
- Secrets are never written to prompts, logs, trajectories, or scorecards.
- Retries are bounded by attempt, time, token, and cost budgets.
- Benchmark comparisons require matching task, repository/base SHA, seed, model policy, and budget.
- Missing measurements are null/unmeasured, never inferred.
- Generated patches are reversible until verification commits them.

## Repository direction
Production modules live under services/ and tools/. Benchmark outputs are generated under benchmarks/results/ and are not hand-authored as performance claims.
