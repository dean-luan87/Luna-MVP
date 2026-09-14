"""Independent serialized-output verifier; no runner/skeleton call."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Mapping
from .observation_planning_serializer_v1 import write_canonical_json_v1
_CASES=("navigation_context","home_context","workplace_context","unknown_field_context","risk_context","goal_change_context")
_TYPES={"survival_observation","task_observation","risk_observation","transition_observation","uncertainty_reduction_observation"}
def verify_observation_planning_dryrun_v1(output_dir:Path)->Mapping[str,object]:
    v=json.loads((output_dir/"observation_planning_dryrun_result_v1.json").read_text()); issues=[]; cases=v.get("cases",[])
    if tuple(x.get("case_id") for x in cases)!=_CASES: issues.append("case_inventory_invalid")
    for x in cases:
        c=x.get("candidate",{})
        if c.get("observation_type") not in _TYPES: issues.append("observation_type_invalid")
        if not all(c.get(k) for k in ("context_reference","field_reference","attention_reference","goal_reference","survival_constraint_reference","information_gap_reference","provenance_reference","trace_reference")): issues.append("reference_closure_invalid")
        if not all(c.get(k) is True for k in ("candidate_only","not_fact","not_state","not_decision","not_action","not_memory")): issues.append("candidate_boundary_invalid")
    f=v.get("runtime_flags",{}); false=("runtime_executed","model_invoked","provider_invoked","sensor_invoked","observation_executed","decision_created","action_created","permission_granted","memory_updated","learning_integrated","hive_integrated","reducer_integrated","state_mutation")
    if any(f.get(k) is not False for k in false): issues.append("execution_boundary_invalid")
    if f.get("fixture_only") is not True or f.get("simulation_only") is not True: issues.append("fixture_boundary_invalid")
    if v.get("deterministic_run2_equal") is not True: issues.append("determinism_invalid")
    return {"valid":not issues,"issues":sorted(set(issues)),"case_count":len(cases),"verifier_independent":True,"runner_called":False,"skeleton_called":False}
def main()->None:
    p=argparse.ArgumentParser();p.add_argument("--output-dir",required=True,type=Path);a=p.parse_args();r=verify_observation_planning_dryrun_v1(a.output_dir);write_canonical_json_v1(a.output_dir/"verification_result_v1.json",r);print(json.dumps(r,sort_keys=True));
    if not r["valid"]:raise SystemExit(1)
if __name__=="__main__":main()
