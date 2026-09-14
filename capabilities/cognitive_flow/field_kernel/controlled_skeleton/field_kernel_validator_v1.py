from __future__ import annotations
from dataclasses import dataclass,fields
from typing import Mapping,Tuple
from .field_kernel_types_v1 import CurrentFieldViewCandidateV1,SCHEMA
@dataclass(frozen=True)
class FieldKernelValidationResultV1:
 issues:Tuple[str,...]
 @property
 def valid(self)->bool:return not self.issues
def validate_current_field_view_v1(v:CurrentFieldViewCandidateV1)->FieldKernelValidationResultV1:
 issues=[]
 if v.schema_version!=SCHEMA or not v.field_view_id or not v.field_state_reference:issues.append("schema_or_base_reference_invalid")
 for x in (v.candidate_overlay_refs,v.context_refs,v.temporal_refs,v.spatial_refs,v.task_refs,v.attention_refs):
  if not isinstance(x,tuple) or not x or any(not isinstance(r,str) or not r for r in x):issues.append("reference_integrity_invalid");break
 if not isinstance(v.uncertainty,Mapping) or not isinstance(v.provenance,Mapping) or not v.provenance.get("source_refs") or v.provenance.get("trace_ref")!=v.trace_ref:issues.append("traceability_invalid")
 if v.candidate_only is not True or v.field_state_source is not False or v.state_mutation is not False or v.not_state is not True or v.not_fact is not True:issues.append("base_overlay_or_candidate_boundary_invalid")
 if {f.name for f in fields(v)} & {"state_id","snapshot_write_target","fact_id","decision_id","action_id","memory_target"}:issues.append("forbidden_authority_field")
 return FieldKernelValidationResultV1(tuple(issues))
