"""Controlled runner engine for the governance verification backbone."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Mapping

from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    CORE_GOVERNANCE_RULE_REGISTRY_V1,
    compute_unified_final_decision,
    resolve_applicable_governance_set,
    run_governance_postflight,
    run_governance_preflight,
    validate_adapter_boundary,
    validate_authority_responsibility_records,
    validate_gateway_authority_boundary,
    validate_requester_executor_boundary,
)

from .fixtures_v1 import (
    build_governance_backbone_cases_v1,
    provider_binding_preparation_reference,
    valid_authority_records,
)


PHASE = "Phase-Luna-Governance-Verification-Backbone-Core-Rules-Controlled-Implementation-v1-001"


def _json_safe(value: Any) -> Any:
    if is_dataclass(value):
        return _json_safe(asdict(value))
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    return value


def _evaluate(case: Mapping[str, Any]) -> Any:
    category = case["category"]
    payload = case["payload"]
    if category == "preflight":
        profile, registry, records, protocol_refs = payload
        return run_governance_preflight(profile, registry, records, protocol_refs)
    if category == "authority":
        return {"errors": validate_authority_responsibility_records(payload)}
    if category == "postflight":
        profile, artifact = payload
        return run_governance_postflight(profile, artifact)
    if category == "boundary":
        return {"errors": validate_requester_executor_boundary(payload)}
    if category == "adapter":
        return {"errors": validate_adapter_boundary(payload)}
    if category == "gateway":
        return {"errors": validate_gateway_authority_boundary(payload)}
    if category == "decision":
        decision_inputs = {
            key: value for key, value in payload.items() if key != "runner_status"
        }
        return {
            "final_decision": compute_unified_final_decision(**decision_inputs),
            "runner_status": payload.get("runner_status", "READY_FOR_USER_VERIFICATION"),
        }
    if category == "determinism":
        if isinstance(payload, tuple) and len(payload) == 2:
            profile, registry = payload
            first = resolve_applicable_governance_set(profile, registry)
            second = resolve_applicable_governance_set(profile, registry)
            return {
                "first": first,
                "second": second,
                "deterministic": _json_safe(first) == _json_safe(second),
            }
        decision_inputs = {
            key: value for key, value in payload.items() if key != "runner_status"
        }
        first = compute_unified_final_decision(**decision_inputs)
        second = compute_unified_final_decision(**decision_inputs)
        return {"first": first, "second": second, "deterministic": first == second}
    return {"errors": (f"unknown_case_category:{category}",)}


class GovernanceVerificationBackboneEvaluationEngineV1:
    def run(self) -> dict[str, Any]:
        case_results = []
        for case in build_governance_backbone_cases_v1():
            result = _evaluate(case)
            case_results.append(
                {
                    "case_id": case["case_id"],
                    "category": case["category"],
                    "expected": _json_safe(case["expected"]),
                    "result": _json_safe(result),
                }
            )
        return {
            "phase": PHASE,
            "source_mode": "CONTROLLED_GOVERNANCE_VERIFICATION_BACKBONE",
            "canonical_owner": "Protocol Manager",
            "constitution_source_ref": "docs/architecture/luna_system_constitution_governance_v1/luna_system_constitution_v1.md",
            "protocol_source_ref": "docs/architecture/cognitive_governance_plane_v1/protocol_manager_governance_manual_v1.md",
            "architecture_source_ref": "docs/architecture/LUNA_ENGINEERING_ARCHITECTURE_CONSTITUTION_V1.md",
            "protocol_manager_reused": True,
            "permission_admission_assets_reused": True,
            "new_constitution_owner_created": False,
            "new_protocol_owner_created": False,
            "new_governance_super_owner_created": False,
            "requester_owns_requirement_complexity": True,
            "executor_owns_execution_complexity": True,
            "verifier_owns_proof_complexity": True,
            "runtime_execution": False,
            "provider_invocation": False,
            "model_invocation": False,
            "gateway_invocation": False,
            "world_mutation": False,
            "truth_mutation": False,
            "resource_allocation": False,
            "slot_reservation": False,
            "capability_activation": False,
            "decision_formed": False,
            "task_formed": False,
            "action_formed": False,
            "database_used": False,
            "ui_used": False,
            "dynamic_rule_loading": False,
            "llm_rule_inference": False,
            "fuzzy_rule_matching": False,
            "governance_rule_registry": _json_safe(CORE_GOVERNANCE_RULE_REGISTRY_V1),
            "common_profiles": [
                "CANDIDATE_ONLY",
                "READ_ONLY",
                "NO_TRUTH",
                "NO_WORLD_MUTATION",
                "NO_RUNTIME",
                "NO_PROVIDER_INVOCATION",
                "NO_MODEL_INVOCATION",
                "NO_DECISION_ACTION_TASK",
            ],
            "provider_binding_preparation_reference": provider_binding_preparation_reference(),
            "reference_authority_records": _json_safe(valid_authority_records()),
            "cases": case_results,
            "status": "READY_FOR_USER_VERIFICATION",
            "runner_generation_status": "READY_FOR_USER_VERIFICATION",
        }


__all__ = ["PHASE", "GovernanceVerificationBackboneEvaluationEngineV1"]
