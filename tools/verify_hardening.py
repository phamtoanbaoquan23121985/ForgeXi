#!/usr/bin/env python3
"""Run ForgeXi verification and emit machine-readable evidence."""
from __future__ import annotations
import argparse,json,platform,subprocess,sys
from pathlib import Path

from services.resilience.fault_campaign import FaultCase,FaultCampaign,aggregate_metrics
from tools.hardening_verifier import build_scorecard,exit_code

FAULTS=[
 FaultCase("dns_failure",True),FaultCase("connection_reset",True),FaultCase("timeout",True),
 FaultCase("http_429",True,2),FaultCase("http_5xx",True),FaultCase("malformed_json",True),
 FaultCase("truncated_nemotron_output",True),FaultCase("subprocess_hang",True),
 FaultCase("subprocess_crash",True),FaultCase("test_failure",True),
 FaultCase("corrupted_evidence",False),FaultCase("expired_credential",True),
]

def main():
 p=argparse.ArgumentParser();p.add_argument("--source-sha",required=True);p.add_argument("--verifier",default="self-hosted")
 p.add_argument("--output",default="benchmarks/results/hardening_scorecard.json");a=p.parse_args()
 proc=subprocess.run([sys.executable,"-m","pytest","-q"],text=True,capture_output=True)
 # Counts are intentionally conservative; pytest exit status is the authoritative suite gate.
 tests={"passed":0,"failed":0 if proc.returncode==0 else 1,"skipped":0,"summary_tail":(proc.stdout+proc.stderr)[-2000:]}
 metrics=aggregate_metrics(FaultCampaign().run(FAULTS))
 card=build_scorecard(source_sha=a.source_sha,verifier=a.verifier,pytest_exit_code=proc.returncode,tests=tests,fault_metrics=metrics)
 card["environment"]={"python":platform.python_version(),"platform":platform.platform()}
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(card,indent=2,sort_keys=True)+"\n")
 print(json.dumps(card,indent=2,sort_keys=True));return exit_code(card)
if __name__=="__main__": raise SystemExit(main())
