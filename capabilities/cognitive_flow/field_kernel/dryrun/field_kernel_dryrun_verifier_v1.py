from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Mapping
def verify(p:Mapping):
 issues=[];n=0
 n+=1
 if p.get("schema_version")!="luna.field_kernel.dryrun.v1" or p.get("phase")!="Phase-A3-Field-Kernel-DryRun-v1-001":issues.append("identity")
 for f in ("runtime_executed","reducer_invoked","state_mutation","snapshot_updated","temporal_updated","model_invoked","external_call","memory_updated","decision_created","action_created"):
  n+=1
  if p.get(f) is not False:issues.append(f)
 for r in p.get("cases",[]):
  n+=1;c=r.get("candidate",{});q=c.get("provenance",{})
  if not r.get("base_reference") or not c.get("candidate_overlay_refs") or c.get("candidate_only") is not True or c.get("not_state") is not True or c.get("not_fact") is not True or c.get("state_mutation") is not False:issues.append("boundary")
  if not q.get("source_refs") or q.get("trace_ref")!=c.get("trace_ref"):issues.append("trace")
 n+=1
 if len(p.get("cases",[]))!=6:issues.append("case_count")
 return {"valid":not issues,"issues":issues,"checks_performed":n,"verifier_independence":"serialized_output_only_no_runner_or_skeleton_import"}
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",required=True,type=Path);p.add_argument("--compare",type=Path);a=p.parse_args();raw=a.input.read_text();o=json.loads(raw);r=verify(o);r["canonical_serialization"]=raw==json.dumps(o,ensure_ascii=False,indent=2,sort_keys=True)+"\n";r["comparison_equal"]=raw==a.compare.read_text() if a.compare else None
 if a.compare and not r["comparison_equal"]:r["valid"]=False;r["issues"].append("determinism")
 print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(0 if r["valid"] else 1)
if __name__=="__main__":main()
