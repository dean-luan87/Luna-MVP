from __future__ import annotations
import argparse,json
from dataclasses import asdict
from pathlib import Path
from ..controlled_skeleton.field_kernel_skeleton_v1 import FieldKernelControlledSkeletonV1
CASES={"case_1_multi_concept":"multi_concept_field_assembly","case_2_conflict":"conflicting_candidate_overlay","case_3_temporal":"temporal_field_transition_reference","case_4_task":"task_dependent_field_view","case_5_attention":"attention_selection_overlay","case_6_unknown":"unknown_incomplete_field_view"}
def run():
 rows=[]
 for cid,kind in CASES.items():
  t="trace:fixture:field-kernel:"+cid+":v1"; v={"field_view_id":"field-view:fixture:"+cid+":v1","field_state_reference":"snapshot:fixture:"+cid+":v1","candidate_overlay_refs":("field-representation:fixture:"+cid+":v1","concept:fixture:"+cid+":v1","primitive:fixture:"+cid+":v1"),"context_refs":("context:fixture:"+cid+":v1",),"temporal_refs":("temporal:fixture:"+cid+":v1",),"spatial_refs":("spatial:fixture:"+cid+":v1",),"task_refs":("task:fixture:"+cid+":v1",),"attention_refs":("attention:fixture:"+cid+":v1",),"uncertainty":{"status":"unknown_preserved" if cid=="case_6_unknown" else "fixture_only","conflict":"unresolved" if cid=="case_2_conflict" else "none"},"provenance":{"source_refs":("evidence:fixture:"+cid+":v1",),"field_representation_refs":("field-representation:fixture:"+cid+":v1",),"trace_ref":t},"trace_ref":t}
  c=FieldKernelControlledSkeletonV1.create_current_field_view(v); x=FieldKernelControlledSkeletonV1.validate_current_field_view(c)
  if not x.valid:raise ValueError(cid)
  rows.append({"case_id":cid,"fixture_type":kind,"base_reference":c.field_state_reference,"candidate":asdict(c),"skeleton_validation":{"valid":True,"issues":[]}})
 return {"schema_version":"luna.field_kernel.dryrun.v1","phase":"Phase-A3-Field-Kernel-DryRun-v1-001","runtime_executed":False,"simulation_only":True,"fixture_only":True,"reducer_invoked":False,"state_mutation":False,"snapshot_updated":False,"temporal_updated":False,"model_invoked":False,"external_call":False,"memory_updated":False,"decision_created":False,"action_created":False,"case_count":6,"cases":rows}
def main():
 p=argparse.ArgumentParser();p.add_argument("--output-dir",required=True,type=Path);a=p.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True);z=a.output_dir/"field_kernel_dryrun_result_v1.json";z.write_text(json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(z)
if __name__=="__main__":main()
