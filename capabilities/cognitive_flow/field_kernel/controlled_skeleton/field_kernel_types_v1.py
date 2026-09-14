from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping,Tuple
SCHEMA="luna.field_kernel.controlled_skeleton.v1"
@dataclass(frozen=True)
class CurrentFieldViewCandidateV1:
 field_view_id:str; field_state_reference:str; candidate_overlay_refs:Tuple[str,...]; context_refs:Tuple[str,...]; temporal_refs:Tuple[str,...]; spatial_refs:Tuple[str,...]; task_refs:Tuple[str,...]; attention_refs:Tuple[str,...]; uncertainty:Mapping[str,object]; provenance:Mapping[str,object]; trace_ref:str; candidate_only:bool=True; field_state_source:bool=False; state_mutation:bool=False; not_state:bool=True; not_fact:bool=True; schema_version:str=SCHEMA
@dataclass(frozen=True)
class FieldKernelSkeletonFlagsV1:
 runtime_executed:bool=False; reducer_invoked:bool=False; state_mutation:bool=False; snapshot_updated:bool=False; temporal_updated:bool=False; model_invoked:bool=False; external_call:bool=False; memory_updated:bool=False; decision_created:bool=False; action_created:bool=False
