from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from .a_route_product_loop_integration_core_types_v1 import ProductLoopInputV1


S1_SCHEMA_VERSION = "a-route-s1-real-user-input-schema-v1"
S1_CONTRACT_VERSION = "a-route-s1-real-user-input-contract-v1"
ADAPTER_OWNER = "A Route Orchestration Governance / Real User Input Adapter"
SUPPORTED_REAL_INGRESS_KINDS = ("USER_INPUT", "USER_CORRECTION")
MAX_INPUT_LENGTH = 4096


@dataclass(frozen=True)
class RealUserInputRecordV1:
    """Structural record for one externally supplied user text payload."""

    input_id: str
    ingress_kind: str
    raw_input_ref: str
    normalized_content: str
    session_ref: str
    cycle_ref: str
    sensitivity: str
    correction_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    truth_declared: bool = False
    semantic_interpretation_performed: bool = False
    direct_intent_ref: str = ""
    direct_task_ref: str = ""
    direct_field_mutation: bool = False
    provider_invocation: bool = False
    model_call: bool = False
    runtime_execution: bool = False
    schema_version: str = S1_SCHEMA_VERSION
    contract_version: str = S1_CONTRACT_VERSION


@dataclass(frozen=True)
class RealUserInputAdapterResultV1:
    accepted: bool
    duplicate: bool
    rejection_code: str
    record: RealUserInputRecordV1
    product_loop_input: Optional[ProductLoopInputV1]
    adapter_owner: str = ADAPTER_OWNER
    component_real: bool = True
    downstream_components_synthetic: bool = True
    provenance_grants_authority: bool = False
    candidate_only: bool = True
    schema_version: str = S1_SCHEMA_VERSION
    contract_version: str = S1_CONTRACT_VERSION


@dataclass(frozen=True)
class RealUserInputTraceV1:
    input_id: str
    product_loop_input_ref: str
    adapter_record_ref: str
    raw_input_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    reverse_lookup: Tuple[Tuple[str, Tuple[str, ...]], ...]
    provenance_grants_authority: bool = False


__all__ = [
    "ADAPTER_OWNER",
    "MAX_INPUT_LENGTH",
    "SUPPORTED_REAL_INGRESS_KINDS",
    "S1_CONTRACT_VERSION",
    "S1_SCHEMA_VERSION",
    "RealUserInputAdapterResultV1",
    "RealUserInputRecordV1",
    "RealUserInputTraceV1",
]
