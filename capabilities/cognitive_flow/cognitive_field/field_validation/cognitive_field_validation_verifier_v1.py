"""Independent verifier reads serialized Validation Closure output only."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any,Iterable,Mapping
_CHECKS=("source_dryrun_identity_valid","six_field_cases_covered","schema_valid","primitive_references_valid","concept_references_valid","context_bindings_valid","temporal_boundaries_valid","spatial_boundaries_valid","task_boundaries_valid","attention_boundaries_valid","provenance_closed","candidate_lifecycle_valid","source_flags_valid")
_GUARDS=("representation_not_state","representation_not_fact","representation_not_memory","attention_not_action","concept_not_state","external_output_not_field_input","confidence_not_admission_authority","reducer_only_mutation_authority")
def verify_field_validation_v1(payload:Mapping[str,Any])->dict[str,Any]:
 issues=[];n=0
 n+=1
 if payload.get("schema_version")!="luna.cognitive_field_representation.validation_closure.v1" or payload.get("phase")!="Phase-A3-Cognitive-Field-Representation-Validation-Closure-v1-001":issues.append({"check_id":"identity","message":"closure identity mismatch"})
 for f in ("runtime_executed","field_kernel_runtime","reducer_integrated","state_mutation"):
  n+=1
  if payload.get(f) is not False:issues.append({"check_id":"boundary."+f,"message":f+" must be false"})
 for group,names in ((payload.get("checks",{}),_CHECKS),(payload.get("negative_guard_results",{}),_GUARDS)):
  for name in names:
   n+=1
   if group.get(name) is not True:issues.append({"check_id":"required."+name,"message":"required closure check failed"})
 n+=1
 if not isinstance(payload.get("cases"),list) or len(payload["cases"])!=6:issues.append({"check_id":"cases","message":"six closure case results required"})
 return {"valid":not issues,"issues":issues,"checks_performed":n,"verifier_independence":"serialized_validation_output_only_no_runner_skeleton_or_field_runtime_import"}
def main(argv:Iterable[str]|None=None)->int:
 p=argparse.ArgumentParser();p.add_argument("--input",required=True,type=Path);p.add_argument("--compare",type=Path);a=p.parse_args(argv);raw=a.input.read_text(encoding="utf-8");payload=json.loads(raw);r=verify_field_validation_v1(payload);r["canonical_serialization"]=raw==json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n";r["comparison_equal"]=a.compare is not None and raw==a.compare.read_text(encoding="utf-8") if a.compare else None
 if a.compare and not r["comparison_equal"]:r["valid"]=False;r["issues"].append({"check_id":"determinism","message":"run outputs differ"})
 print(json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True));return 0 if r["valid"] else 1
if __name__=="__main__":raise SystemExit(main())
