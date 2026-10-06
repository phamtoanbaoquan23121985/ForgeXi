# Self-hosted verification

ForgeXi has one verification entrypoint:

```bash
python3 -m pip install -e '.[dev]'
python3 tools/verify_hardening.py --source-sha "$(git rev-parse HEAD)" --verifier "local-self-hosted"
```

It runs the full pytest suite, executes the deterministic fault campaign, evaluates the hardening gate, writes `benchmarks/results/hardening_scorecard.json`, and exits non-zero unless the decision is `HARDENED`.

The GitHub workflow `.github/workflows/self-hosted-verify.yml` uses the same entrypoint on a runner carrying the `forgexi-verifier` label. Evidence is uploaded even when verification fails. A scorecard is evidence only for the exact `source_sha` recorded inside it.
