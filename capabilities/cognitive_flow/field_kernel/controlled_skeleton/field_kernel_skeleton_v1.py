from __future__ import annotations
import json
from dataclasses import asdict
from typing import Any,Mapping
from .field_kernel_types_v1 import CurrentFieldViewCandidateV1,FieldKernelSkeletonFlagsV1
from .field_kernel_validator_v1 import validate_current_field_view_v1
class FieldKernelControlledSkeletonV1:
 @staticmethod
 def create_current_field_view(v:Mapping[str,Any])->CurrentFieldViewCandidateV1:
  forbidden={"raw_model_output","provider_payload","memory","fact","decision","action","reducer_command","state_id","snapshot_write_target"}&set(v)
  if forbidden:raise ValueError("forbidden input: "+", ".join(sorted(forbidden)))
  req=("field_view_id","field_state_reference","candidate_overlay_refs","context_refs","temporal_refs","spatial_refs","task_refs","attention_refs","uncertainty","provenance","trace_ref")
  missing=[x for x in req if x not in v]
  if missing:raise ValueError("missing: "+", ".join(missing))
  if v.get("candidate_only",True) is not True or v.get("field_state_source",False) is not False or v.get("state_mutation",False) is not False:raise ValueError("view must remain candidate-only/read-only")
  return CurrentFieldViewCandidateV1(v["field_view_id"],v["field_state_reference"],tuple(v["candidate_overlay_refs"]),tuple(v["context_refs"]),tuple(v["temporal_refs"]),tuple(v["spatial_refs"]),tuple(v["task_refs"]),tuple(v["attention_refs"]),dict(v["uncertainty"]),dict(v["provenance"]),v["trace_ref"])
 @staticmethod
 def validate_current_field_view(v):return validate_current_field_view_v1(v)
 @staticmethod
 def serialize_current_field_view(v):return json.dumps(asdict(v),ensure_ascii=False,sort_keys=True,separators=(",",":"))
 @staticmethod
 def flags():return FieldKernelSkeletonFlagsV1()
