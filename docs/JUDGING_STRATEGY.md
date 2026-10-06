# ForgeXi 20/20 Judging Strategy

Target: maximize evidence for each four 5-point judging dimensions. A target score is not represented as an awarded score.

## Technological Implementation
Judge-visible proof:
- NVIDIA Nemotron inference served through Nebius Token Factory on the actual planning/coding/review decision path.
- Bounded reasoning budget and retries.
- Controlled repository/shell tools with reversible patches.
- Verification gate blocks DONE until required tests/build/security checks pass.
- Machine-readable provider usage, latency, trajectory, diff hash, test evidence, and final revision.

Acceptance gate: a fresh clone can reproduce a demo task from documented setup and emit a valid evidence receipt.

## Design
Judge-visible proof:
- Provider-neutral runtime; orchestration is not coupled to one model SDK.
- Explicit state machine, budget governor, retry/failure policy, checkpoints, secret redaction, and deterministic evidence schema.
- UI exposes plan, actions, diff, verification, and evidence instead of hiding autonomy.

Acceptance gate: injected provider/tool/test failures degrade safely and remain visible.

## Potential Impact
No impact claim without measurement.
Paired experiment: same task, base SHA, seed, model policy and budget.
Report task success, verified completion, wall latency, model tokens, provider cost when available, retry/tool-call count and human interventions.

Acceptance gate: raw paired runs and aggregation code reproduce every displayed number.

## Quality of Idea
Core differentiator: Evidence-Gated Adaptive Forge Loop.
1. Allocate reasoning/review compute according to uncertainty and verification state.
2. Execute changes as reversible transactions.
3. Treat tests/build/security evidence as state transitions, not post-hoc decoration.
4. Emit an evidence receipt whose claims are derived only from observed events.

Novelty is demonstrated through ablations, not asserted:
- fixed reasoning vs adaptive reasoning
- no reviewer vs adaptive reviewer
- post-hoc validation vs evidence-gated state transitions
- no checkpoint rollback vs reversible execution

Acceptance gate: ablation results identify which mechanisms improve quality/cost/latency and which do not.
