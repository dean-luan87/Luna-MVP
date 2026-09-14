from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


ERROR_NAMESPACE_V1 = "LUNA-PROTO-L2-FIELD-STATE-REDUCER-BEHAVIOR-POLICY-SKELETON-V1::*"


class BehaviorPolicyErrorCodeV1(str, Enum):
    INVALID_POLICY_INPUT = "invalid_policy_input"
    UNKNOWN_POLICY_ID = "unknown_policy_id"
    UNKNOWN_STATE_TYPE = "unknown_state_type"
    MISSING_POLICY_REGISTRY_SNAPSHOT = "missing_policy_registry_snapshot"
    MISSING_ELIGIBILITY_MATRIX_SNAPSHOT = "missing_eligibility_matrix_snapshot"
    MISSING_PRECEDENCE_SNAPSHOT = "missing_precedence_snapshot"
    MISSING_COMPOSITION_SNAPSHOT = "missing_composition_snapshot"
    POLICY_EXECUTION_FORBIDDEN = "policy_execution_forbidden"
    DIRECT_STATE_WRITE_FORBIDDEN = "direct_state_write_forbidden"
    FACT_PROMOTION_FORBIDDEN = "fact_promotion_forbidden"
    ACTION_TRIGGER_FORBIDDEN = "action_trigger_forbidden"
    PROVIDER_RECALL_FORBIDDEN = "provider_recall_forbidden"
    EXTERNAL_LOOKUP_FORBIDDEN = "external_lookup_forbidden"
    MODEL_CALL_FORBIDDEN = "model_call_forbidden"
    RUNTIME_EXECUTION_FORBIDDEN = "runtime_execution_forbidden"
    UNRESOLVED_POLICY_CONFLICT_PRESERVED = "unresolved_policy_conflict_preserved"


@dataclass(frozen=True)
class BehaviorPolicyErrorV1:
    code: BehaviorPolicyErrorCodeV1
    message: str
    namespace: str = ERROR_NAMESPACE_V1
    detail: Optional[str] = None
