"""User-terminal Runner for the first real provider execution path."""

from __future__ import annotations

import argparse
import json
import uuid
from dataclasses import replace
from pathlib import Path
from typing import Any, Dict, Tuple

from capabilities.evaluation.runtime_grant_pre_execution_authorization_controlled.fixtures_v1 import (
    build_controlled_canonical_runtime_scope_v1,
)
from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    form_runtime_safety_prerequisite_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_active_observation_control_engine_v1 import (
    FieldPerceptionActiveObservationControlEngineV1,
)
from capabilities.midplatform.core.runtime_executor.runtime_allocation_preparation_candidate_v1 import (
    ExecutionInstancePreparationInputV1,
    RuntimeAllocationPreparationInputV1,
    form_execution_instance_preparation_candidates,
    form_runtime_allocation_preparation_candidates,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_resolution_v1 import (
    CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    RuntimeExecutionGrantDecisionV1,
    RuntimeExecutionGrantInputV1,
    build_pregrant_authority_binding_key,
    form_runtime_execution_grants,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_candidate_v1 import (
    ProviderBindingCandidateInputV1,
    form_provider_binding_candidates,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_runtime_preparation_v1 import (
    ProviderBindingRuntimePreparationCandidateV1,
    ProviderBindingRuntimePreparationInputV1,
    form_provider_binding_runtime_preparation_candidates,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_registry_v1 import (
    CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_target_preparation_v1 import (
    ProviderRuntimeTargetPreparationCandidateV1,
)

from .engine_v1 import ProviderRuntimeObservationIngressEngineV1, _jsonable
from .fixtures_v1 import build_provider_observation_cases_v1
from .real_provider_execution_engine_v1 import (
    MODEL_ASSET_ID,
    PROVIDER_REF,
    RealProviderExecutionEngineV1,
)


def _repo_root() -> Path:
    path = Path(__file__).resolve()
    for candidate in (path, *path.parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
OUTPUT_DIR = ROOT / "_eval_out/real_provider_execution_integration_v1"
DEFAULT_SOURCE = ROOT / "_tmp_eval_inputs/roboflow_real_exit_v1/source_image.jpg"
DEFAULT_MODEL = ROOT / "vision/detection/yolo/yolo11n.pt"


def _controlled_runtime_grant(
    case: Any,
    fpo_record: Any,
    requirement: Any,
    resolution: Any,
) -> Tuple[RuntimeExecutionGrantDecisionV1 | None, Tuple[str, ...]]:
    """Issue the Owner grant for this real controlled-evaluation instance.

    This assembles candidate/preparation inputs only.  The Permission /
    Admission Manager remains the sole creator of the Granted decision and
    the sole writer of current authorization state.
    """

    canonical_scope = build_controlled_canonical_runtime_scope_v1(
        f"real-yolo:{case.execution_instance_ref}"
    )
    if canonical_scope is None:
        return None, ("controlled_runtime_scope_unavailable",)
    admitted_action_ref, working_envelope_ref, working_envelope_version_ref = canonical_scope

    demand = fpo_record.demand
    request = fpo_record.request
    trace = fpo_record.trace
    if request is None or requirement is None or resolution is None or not resolution.module_ref:
        return None, ("controlled_runtime_prerequisite_missing",)

    parent_ref = case.concern_ref
    source_state_ref = trace.root_cycle_trace_id
    target_ref = f"provider-target:{case.execution_instance_ref}"
    resolution_ref = resolution.scope_assessment_ref or requirement.requirement_id
    lineage = (
        target_ref,
        request.request_id,
        demand.demand_id,
        requirement.requirement_id,
        resolution_ref,
    )
    context_refs = (case.context_ref,)
    provenance_refs = tuple(
        dict.fromkeys((*demand.provenance_refs, *trace.provenance_refs))
    )
    target = ProviderRuntimeTargetPreparationCandidateV1(
        provider_target_candidate_ref=target_ref,
        source_admission_compatibility_candidate_ref=request.request_id,
        source_perception_routing_candidate_ref=trace.control_trace_ref,
        source_observation_demand_ref=demand.demand_id,
        source_capability_requirement_ref=requirement.requirement_id,
        source_capability_resolution_candidate_ref=resolution_ref,
        capability_candidate_ref=resolution.module_ref,
        capability_class_ref=resolution.module_ref,
        provider_candidate_ref=PROVIDER_REF,
        provider_class_ref="yolo:local",
        source_model_ref=MODEL_ASSET_ID,
        provider_mapping_basis_refs=(PROVIDER_REF, MODEL_ASSET_ID),
        provider_admission_refs=(PROVIDER_REF,),
        provider_availability_refs=(fpo_record.provider_session.session_id if fpo_record.provider_session else request.request_id,),
        observation_class=case.capability_kind,
        observation_target_refs=(request.target_region_candidate,),
        observation_constraint_refs=tuple(demand.stop_conditions),
        expected_information_contribution_refs=tuple(case.expected_evidence_kinds),
        information_need_refs=(demand.information_need,),
        information_gap_refs=tuple(demand.uncertainty_refs),
        source_strategy_ref=trace.control_trace_ref,
        source_branch_ref=case.goal_ref,
        parent_cognitive_problem_ref=parent_ref,
        source_state_ref=source_state_ref,
        context_refs=context_refs,
        lineage_refs=lineage,
        provenance_refs=provenance_refs,
        trace_ref=trace.control_trace_ref,
        admitted_action_ref=admitted_action_ref,
        working_envelope_ref=working_envelope_ref,
        working_envelope_version_ref=working_envelope_version_ref,
    )
    binding_preparation = form_provider_binding_runtime_preparation_candidates(
        ProviderBindingRuntimePreparationInputV1(
            preparation_ref=f"binding-prep:{case.execution_instance_ref}",
            parent_cognitive_problem_ref=parent_ref,
            source_state_ref=source_state_ref,
            provider_target_candidates=(target,),
            context_refs=context_refs,
            trace_ref=f"trace:binding-prep:{case.execution_instance_ref}",
            provenance_refs=provenance_refs,
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=working_envelope_ref,
            working_envelope_version_ref=working_envelope_version_ref,
        )
    )
    if len(binding_preparation.candidates) != 1:
        return None, tuple(binding_preparation.validation_errors) or ("binding_preparation_failed",)

    binding_candidates = form_provider_binding_candidates(
        ProviderBindingCandidateInputV1(
            preparation_ref=f"binding-candidate:{case.execution_instance_ref}",
            parent_cognitive_problem_ref=parent_ref,
            source_state_ref=source_state_ref,
            preparation_candidates=binding_preparation.candidates,
            context_refs=context_refs,
            trace_ref=f"trace:binding-candidate:{case.execution_instance_ref}",
            provenance_refs=provenance_refs,
            runtime_requirement_refs=tuple(requirement.resource_refs),
            resource_class_refs=tuple(requirement.resource_refs),
            execution_class_refs=(requirement.execution_boundary_ref,),
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=working_envelope_ref,
            working_envelope_version_ref=working_envelope_version_ref,
        )
    )
    if len(binding_candidates.candidates) != 1:
        return None, tuple(binding_candidates.validation_errors) or ("binding_candidate_failed",)

    allocation = form_runtime_allocation_preparation_candidates(
        RuntimeAllocationPreparationInputV1(
            preparation_ref=f"allocation-prep:{case.execution_instance_ref}",
            parent_cognitive_problem_ref=parent_ref,
            source_state_ref=source_state_ref,
            provider_binding_candidates=binding_candidates.candidates,
            context_refs=context_refs,
            trace_ref=f"trace:allocation-prep:{case.execution_instance_ref}",
            provenance_refs=provenance_refs,
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=working_envelope_ref,
            working_envelope_version_ref=working_envelope_version_ref,
        )
    )
    if len(allocation.candidates) != 1:
        return None, tuple(allocation.validation_errors) or ("allocation_preparation_failed",)

    execution = form_execution_instance_preparation_candidates(
        ExecutionInstancePreparationInputV1(
            preparation_ref=f"execution-prep:{case.execution_instance_ref}",
            parent_cognitive_problem_ref=parent_ref,
            source_state_ref=source_state_ref,
            runtime_allocation_candidates=allocation.candidates,
            runtime_envelope_shape_refs=("runtime-envelope:observation",),
            context_refs=context_refs,
            trace_ref=f"trace:execution-prep:{case.execution_instance_ref}",
            provenance_refs=provenance_refs,
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=working_envelope_ref,
            working_envelope_version_ref=working_envelope_version_ref,
        )
    )
    if len(execution.candidates) != 1:
        return None, tuple(execution.validation_errors) or ("execution_preparation_failed",)

    binding = binding_candidates.candidates[0]
    allocation_candidate = allocation.candidates[0]
    execution_candidate = execution.candidates[0]
    binding_key = build_pregrant_authority_binding_key(
        execution_instance_preparation_candidate_ref=execution_candidate.execution_instance_preparation_candidate_ref,
        provider_candidate_ref=binding.provider_candidate_ref,
        capability_candidate_ref=binding.capability_candidate_ref,
        admitted_action_ref=admitted_action_ref,
        working_envelope_ref=working_envelope_ref,
        working_envelope_version_ref=working_envelope_version_ref,
    )
    safety = form_runtime_safety_prerequisite_v1(
        binding_key=(*binding_key, "runtime-execution"),
        effect_class="runtime-execution",
    )
    grant_result = form_runtime_execution_grants(
        RuntimeExecutionGrantInputV1(
            grant_request_ref=f"grant-request:{case.execution_instance_ref}",
            parent_cognitive_problem_ref=parent_ref,
            source_state_ref=source_state_ref,
            provider_binding_candidates=binding_candidates.candidates,
            runtime_allocation_candidates=allocation.candidates,
            execution_instance_preparation_candidates=execution.candidates,
            permission_refs=tuple(requirement.permission_refs),
            safety_refs=(safety.result_ref,),
            safety_prerequisite_refs=(safety.result_ref,),
            protocol_refs=("protocol:runtime-execution-grant:v1",),
            governance_refs=provenance_refs,
            constraint_refs=tuple(demand.stop_conditions),
            validity_scope=(request.target_region_candidate,),
            expiry_boundary_ref=f"expiry:{case.execution_instance_ref}",
            effect_class="runtime-execution",
            provider_evaluation_profile_ref=CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF,
            capability_evaluation_profile_ref=CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF,
            context_refs=context_refs,
            lineage_refs=tuple(dict.fromkeys((*binding.lineage_refs, *allocation_candidate.lineage_refs, *execution_candidate.lineage_refs))),
            provenance_refs=provenance_refs,
            trace_ref=f"trace:grant:{case.execution_instance_ref}",
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=working_envelope_ref,
            working_envelope_version_ref=working_envelope_version_ref,
        )
    )
    grants = tuple(
        decision
        for decision in grant_result.decisions
        if decision.decision == "GRANTED"
        and decision.execution_authorized
        and decision.provider_candidate_ref == PROVIDER_REF
        and decision.capability_candidate_ref == resolution.module_ref
        and decision.source_execution_instance_preparation_ref
        == execution_candidate.execution_instance_preparation_candidate_ref
    )
    if len(grants) != 1:
        return None, ("controlled_runtime_grant_missing_or_ambiguous",)
    return grants[0], ()


def _summary(result: Dict[str, Any], source_ref: str, model_path: str) -> Dict[str, Any]:
    provider = result.get("provider")
    provider_result = result.get("provider_result")
    request = result.get("provider_request")
    details = result.get("details") or {}
    return {
        "phase": "Phase-P1-Luna-Real-Provider-Execution-Integration-v1-001",
        "execution_mode": "LIVE_RUNTIME",
        "selected_provider": "YOLO11n local provider",
        "provider_family": "yolo",
        "source_ref": source_ref,
        "model_path": model_path,
        "provider_real_execution_attempted": bool(result.get("provider_real_execution_attempted")),
        "provider_real_execution_verified": bool(result.get("provider_real_execution_verified")),
        "provider_invoked": bool(result.get("provider_invoked")),
        "model_invoked": bool(result.get("model_invoked")),
        "recorded_provider_result_used": False,
        "provider_status": provider_result.status if provider_result else None,
        "provider_result_ref": provider_result.provider_result_ref if provider_result else None,
        "provider_request_ref": request.provider_request_ref if request else None,
        "runtime_observation_ref": result.get("runtime_observation_ref"),
        "gateway_admission_ref": result.get("gateway_admission_ref"),
        "evidence_refs": list(result.get("evidence_refs") or ()),
        "a_route_execution_ref": result.get("a_route_execution_ref"),
        "sufficiency_ref": result.get("sufficiency_ref"),
        "information_gap_ref": result.get("information_gap_ref"),
        "stop_ref": result.get("stop_ref"),
        "observation_demand_ref": request.observation_demand_ref if request else None,
        "capability_requirement_ref": request.capability_requirement_ref if request else None,
        "capability_ref": request.capability_ref if request else None,
        "provider_ref": request.provider_ref if request else None,
        "model_ref": request.model_ref if request else None,
        "trace_refs": list(request.trace_refs) if request else [],
        "provenance_refs": list(request.provenance_refs) if request else [],
        "forbidden_behaviors": {
            "decision_execution": False,
            "task_execution": False,
            "action_execution": False,
            "runtime_executor_invocation": False,
            "device_control": False,
            "external_side_effect": False,
            "field_mutation": bool(getattr(provider, "field_mutation", False)) if provider else False,
            "world_truth_declared": bool(getattr(provider, "truth_declared", False)) if provider else False,
        },
        "provider_native_result": _jsonable(provider) if provider else None,
        "provider_runtime_result": _jsonable(provider_result) if provider_result else None,
        "details": details,
        "validation_errors": list(result.get("errors") or ()),
        "status": "REAL_PROVIDER_EXECUTION_RESULT_CANDIDATE",
    }


def build_runner_summary_v1(*, source_ref: str = str(DEFAULT_SOURCE), model_path: str = str(DEFAULT_MODEL)) -> Dict[str, Any]:
    base_case = build_provider_observation_cases_v1()[0]
    case = replace(
        base_case,
        case_id="REAL_PROVIDER_EXECUTION_VISION",
        title="one bounded local YOLO11n provider result enters cognition",
        execution_instance_ref=f"provider-runtime:real-yolo11n:{uuid.uuid4().hex[:12]}",
    )
    ingress_engine = ProviderRuntimeObservationIngressEngineV1()
    fpo_payload = ingress_engine._fpo_payload(case)
    # The real execution engine owns the complete provider invocation path;
    # this runner only prepares the Owner grant input from the same canonical
    # FPO resolution boundary before carrying the resulting decision.
    fpo_record = FieldPerceptionActiveObservationControlEngineV1().run_case(fpo_payload)
    requirement, _assessment, resolution, resolution_errors = ingress_engine._resolve(case, fpo_record)
    grant, grant_errors = (None, ("capability_resolution_not_ready",))
    if not resolution_errors and requirement is not None and resolution is not None:
        grant, grant_errors = _controlled_runtime_grant(case, fpo_record, requirement, resolution)
    result = RealProviderExecutionEngineV1(ROOT).run(
        case,
        source_ref=source_ref,
        model_path=model_path,
        runtime_authorization_grant=grant,
    )
    summary = _summary(result, source_ref, model_path)
    summary["runtime_authorization_grant_ref"] = grant.grant_ref if grant else None
    summary["grant_issued_by_owner"] = bool(grant)
    summary["grant_issuance_errors"] = list(grant_errors or resolution_errors)
    summary["provider_ref"] = summary.get("provider_ref") or PROVIDER_REF
    summary["model_ref"] = summary.get("model_ref") or MODEL_ASSET_ID
    summary["all_checks_passed"] = bool(
        summary["provider_real_execution_verified"]
        and summary["provider_invoked"]
        and summary["provider_status"] in {"SUCCESS", "EMPTY_SUCCESS"}
        and summary["runtime_observation_ref"]
        and summary["gateway_admission_ref"]
        and summary["a_route_execution_ref"]
        and not summary["validation_errors"]
        and not any(summary["forbidden_behaviors"].values())
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one bounded real YOLO11n provider through Luna observation ingress.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--model-path", default=str(DEFAULT_MODEL))
    args = parser.parse_args()
    summary = build_runner_summary_v1(source_ref=args.source, model_path=args.model_path)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
