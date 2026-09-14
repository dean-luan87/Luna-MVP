# -*- coding: utf-8 -*-
"""Provider Manager Runtime Skeleton — dry-run runner v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.provider_manager_runtime_skeleton.provider_manager_runtime_skeleton_dryrun_cases_v1 import (
    ProviderManagerRuntimeSkeletonDryRunCase,
    build_all_provider_manager_runtime_skeleton_cases_v1,
    bundle_from_provider_manager_runtime_skeleton_case,
)
from capabilities.midplatform.provider_manager_runtime_skeleton.provider_manager_runtime_skeleton_registry_v1 import (
    FORBIDDEN_RUNTIME_SKELETON_POLICIES,
)
from capabilities.midplatform.provider_manager_runtime_skeleton.provider_manager_runtime_skeleton_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
    _no_domain_specific_manager_duplication,
    validate_provider_manager_runtime_skeleton_case_bundle,
)
from capabilities.midplatform.provider_manager_runtime_skeleton.provider_manager_runtime_skeleton_types_v1 import (
    ACTIVATION_GATE_REQUIRED_CHECKS,
    DOMAIN_SPATIAL_EVIDENCE,
    DOMAIN_VISION_OCR,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_DRYRUN_RUNNER_UNEXPECTED_OUTCOME,
    FINAL_DECISION_DRYRUN_TRACE_READY_FOR_VERIFIER,
    MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    RUNTIME_SKELETON_PRINCIPLE_ZH,
    RUNTIME_SKELETON_REF,
    SHARED_GOVERNANCE_SOURCE_REF,
)

DEFAULT_OUTPUT = (
    _REPO_ROOT / "_tmp_eval_out" / "provider_manager_runtime_skeleton_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "provider_manager_runtime_skeleton_dryrun_trace_v1.json"
SUMMARY_FILENAME = "provider_manager_runtime_skeleton_dryrun_summary_v1.json"

TraceDecision = Literal["PASS", "EXPECTED_REJECT", "UNEXPECTED_PASS", "UNEXPECTED_FAIL"]

_SPATIAL_POLLUTION_CANDIDATES = frozenset({"PoseCandidate", "SLAMHealthCandidate"})

_GATE_FLAG_MAP = {
    "license_gate_required": "license_gate",
    "adapter_gate_required": "adapter_contract_gate",
    "admission_gate_required": "provider_admission_gate",
    "health_gate_required": "health_gate",
    "fallback_gate_required": "fallback_gate",
    "owner_approval_gate_required": "owner_approval_gate",
}


def classify_trace_decision(expected_ok: bool, actual_ok: bool) -> TraceDecision:
    if expected_ok and actual_ok:
        return "PASS"
    if not expected_ok and not actual_ok:
        return "EXPECTED_REJECT"
    if not expected_ok and actual_ok:
        return "UNEXPECTED_PASS"
    return "UNEXPECTED_FAIL"


def _first_item(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return items[0] if items else {}


def _pick_by_domain(
    items: List[Dict[str, Any]],
    domain_id: str,
) -> Dict[str, Any]:
    for item in items:
        if item.get("domain_id") == domain_id:
            return item
    return _first_item(items)


def _domain_boundary(bundle: Dict[str, Any], expected_domain_id: str) -> Dict[str, bool]:
    domain_profiles = bundle.get("domain_profiles") or {}
    spatial_profile = domain_profiles.get(DOMAIN_SPATIAL_EVIDENCE) or {}
    vision_profile = domain_profiles.get(DOMAIN_VISION_OCR) or {}
    dispatches = list(bundle.get("output_dispatch_candidates") or ())
    registries = list(bundle.get("runtime_registries") or ())

    spatial_dispatch = _pick_by_domain(dispatches, DOMAIN_SPATIAL_EVIDENCE)
    vision_dispatch = _pick_by_domain(dispatches, DOMAIN_VISION_OCR)
    vision_registry = _pick_by_domain(registries, DOMAIN_VISION_OCR)

    vision_declared = set(vision_profile.get("supported_output_candidate_types") or ())
    vision_registry_types = set(vision_registry.get("supported_output_candidate_types") or ())
    vision_dispatch_types = set(vision_dispatch.get("output_candidate_types") or ())

    vision_not_polluted = not (
        vision_registry_types.intersection(_SPATIAL_POLLUTION_CANDIDATES - vision_declared)
        or vision_dispatch_types.intersection(_SPATIAL_POLLUTION_CANDIDATES - vision_declared)
    )

    spatial_ok = (
        spatial_profile.get("synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
        and (
            not spatial_dispatch
            or spatial_dispatch.get("synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
        )
    )
    vision_ok = (
        vision_profile.get("synthesis_entrypoint") == MIDPLATFORM_SYNTHESIS_ENTRYPOINT
        and (
            not vision_dispatch
            or vision_dispatch.get("synthesis_entrypoint") == MIDPLATFORM_SYNTHESIS_ENTRYPOINT
        )
        and vision_not_polluted
    )

    if expected_domain_id == DOMAIN_SPATIAL_EVIDENCE:
        return {
            "spatial_evidence_boundary_preserved": spatial_ok,
            "vision_ocr_boundary_preserved": True,
            "vision_ocr_not_polluted_by_spatial_candidates": vision_not_polluted,
        }
    if expected_domain_id == DOMAIN_VISION_OCR:
        return {
            "spatial_evidence_boundary_preserved": True,
            "vision_ocr_boundary_preserved": vision_ok,
            "vision_ocr_not_polluted_by_spatial_candidates": vision_not_polluted,
        }
    return {
        "spatial_evidence_boundary_preserved": spatial_ok,
        "vision_ocr_boundary_preserved": vision_ok,
        "vision_ocr_not_polluted_by_spatial_candidates": vision_not_polluted,
    }


def _governance_checkpoints(bundle: Dict[str, Any]) -> Dict[str, bool]:
    skeletons = list(bundle.get("runtime_skeletons") or ())
    registries = list(bundle.get("runtime_registries") or ())
    gates = list(bundle.get("activation_gates") or ())
    health_loops = list(bundle.get("health_loops") or ())
    fallbacks = list(bundle.get("fallback_executor_candidates") or ())
    dispatches = list(bundle.get("output_dispatch_candidates") or ())
    decisions = list(bundle.get("runtime_decisions") or ())
    planning = list(bundle.get("planning_decisions") or ())

    candidate_only_items = (
        skeletons
        + registries
        + gates
        + health_loops
        + fallbacks
        + dispatches
        + decisions
        + planning
    )

    domain_profiles = bundle.get("domain_profiles") or {}
    registry_domains = {r.get("domain_id") for r in registries}

    return {
        "runtime_execution_still_disabled": all(
            item.get("runtime_execution_allowed") is not True
            for item in skeletons + gates + health_loops + fallbacks + dispatches + decisions
        ),
        "provider_activation_still_disabled": all(
            item.get("provider_activation_allowed") is not True
            for item in skeletons + registries + gates + decisions
        ),
        "fallback_execution_still_disabled": all(
            item.get("fallback_execution_allowed") is not True for item in fallbacks + decisions
        )
        and all(p.get("fallback_execution_allowed") is not True for p in planning),
        "output_dispatch_still_disabled": all(
            item.get("output_dispatch_allowed") is not True for item in dispatches + decisions
        )
        and all(p.get("output_dispatch_allowed") is not True for p in planning),
        "real_provider_not_connected": all(
            item.get("real_provider_connected") is not True
            for item in skeletons + registries + planning
        ),
        "candidate_only_enforced": all(
            item.get("candidate_only") is True for item in candidate_only_items if item
        ),
        "shared_governance_source_required": all(
            item.get("shared_governance_source_ref") == SHARED_GOVERNANCE_SOURCE_REF
            for item in skeletons + registries + gates
            if item.get("shared_governance_source_ref") is not None
        )
        if skeletons or registries or gates
        else True,
        "domain_profile_source_required": (
            all(bool(r.get("domain_profile_ref")) for r in registries)
            if registries
            else bool(domain_profiles)
        ),
        "no_direct_action": all(d.get("direct_action_allowed") is not True for d in dispatches),
        "no_direct_speech": all(d.get("direct_speech_allowed") is not True for d in dispatches),
        "no_direct_fact_write": all(
            d.get("direct_fact_write_allowed") is not True for d in dispatches
        ),
        "no_domain_specific_manager_duplication": _no_domain_specific_manager_duplication(),
        "registry_domains_in_profiles": (
            all(d in domain_profiles for d in registry_domains) if registry_domains else True
        ),
    }


def build_trace_for_case(
    case: ProviderManagerRuntimeSkeletonDryRunCase,
    *,
    actual_ok: bool,
    errors: List[str],
    bundle: Dict[str, Any],
) -> Dict[str, Any]:
    skeletons = list(bundle.get("runtime_skeletons") or ())
    registries = list(bundle.get("runtime_registries") or ())
    gates = list(bundle.get("activation_gates") or ())
    health_loops = list(bundle.get("health_loops") or ())
    fallbacks = list(bundle.get("fallback_executor_candidates") or ())
    dispatches = list(bundle.get("output_dispatch_candidates") or ())
    decisions = list(bundle.get("runtime_decisions") or ())
    planning = list(bundle.get("planning_decisions") or ())

    skeleton = _pick_by_domain(skeletons, case.expected_domain_id)
    if not skeleton and skeletons:
        skeleton = skeletons[0]
    registry = _pick_by_domain(registries, case.expected_domain_id)
    gate = _pick_by_domain(gates, case.expected_domain_id)
    health = _pick_by_domain(health_loops, case.expected_domain_id)
    fallback = _pick_by_domain(fallbacks, case.expected_domain_id)
    dispatch = _pick_by_domain(dispatches, case.expected_domain_id)
    decision = _pick_by_domain(decisions, case.expected_domain_id)
    plan = _first_item(planning)

    trace_decision = classify_trace_decision(case.expected_validation_ok, actual_ok)
    matched = trace_decision in ("PASS", "EXPECTED_REJECT")

    required_gates = set(gate.get("required_gates") or ACTIVATION_GATE_REQUIRED_CHECKS)
    gate_flags = {
        flag: check in required_gates for flag, check in _GATE_FLAG_MAP.items()
    }

    synthesis_entrypoints = [
        d.get("synthesis_entrypoint")
        for d in dispatches
        if d.get("synthesis_entrypoint")
    ]
    if not synthesis_entrypoints:
        domain_profiles = bundle.get("domain_profiles") or {}
        profile = domain_profiles.get(case.expected_domain_id) or {}
        if profile.get("synthesis_entrypoint"):
            synthesis_entrypoints = [profile["synthesis_entrypoint"]]

    return {
        "case_id": case.case_id,
        "case_name": case.case_name,
        "case_type": case.case_type,
        "case_goal": case.case_goal,
        "runtime_skeleton": {
            "skeleton_ref": skeleton.get("skeleton_ref") or RUNTIME_SKELETON_REF,
            "runtime_execution_allowed": skeleton.get("runtime_execution_allowed"),
            "provider_activation_allowed": skeleton.get("provider_activation_allowed"),
            "fallback_execution_allowed": plan.get("fallback_execution_allowed"),
            "output_dispatch_allowed": plan.get("output_dispatch_allowed"),
            "real_provider_connected": skeleton.get("real_provider_connected")
            or registry.get("real_provider_connected"),
        },
        "runtime_registry": {
            "registry_count": len(registries),
            "domain_profiles_attached": list((bundle.get("domain_profiles") or {}).keys()),
            "shared_governance_source_ref": registry.get("shared_governance_source_ref")
            or SHARED_GOVERNANCE_SOURCE_REF,
            "domain_profile_source_required": bool(registry.get("domain_profile_ref"))
            or bool(bundle.get("domain_profiles")),
            "registration_status": registry.get("registration_status"),
            "provider_activation_allowed": registry.get("provider_activation_allowed"),
            "no_domain_specific_manager_duplication": _no_domain_specific_manager_duplication(),
        },
        "activation_gate": {
            "activation_gate_count": len(gates),
            **gate_flags,
            "provider_activation_allowed": gate.get("provider_activation_allowed"),
            "all_gates_passed": gate.get("all_gates_passed"),
            "activation_decision_candidate": gate.get("activation_decision_candidate"),
        },
        "health_loop": {
            "health_loop_count": len(health_loops),
            "health_decision_candidate": health.get("health_decision_candidate"),
            "health_decision_candidate_only": health.get("runtime_disable_executed") is not True
            and health.get("direct_runtime_disable_allowed") is not True,
            "direct_runtime_disable": health.get("runtime_disable_executed") is True
            or health.get("direct_runtime_disable_allowed") is True,
        },
        "fallback_executor": {
            "fallback_candidate_count": len(fallbacks),
            "fallback_execution_allowed": fallback.get("fallback_execution_allowed"),
            "fallback_executed": fallback.get("fallback_executed"),
            "preserve_source_chain": (
                fallback.get("preserve_source_chain") if fallback else True
            ),
            "preserve_conflict_refs": (
                fallback.get("preserve_conflict_refs") if fallback else True
            ),
        },
        "output_dispatch": {
            "dispatch_candidate_count": len(dispatches),
            "output_dispatch_allowed": dispatch.get("output_dispatch_allowed"),
            "candidate_output_only": dispatch.get("output_dispatch_allowed") is not True
            and dispatch.get("direct_action_allowed") is not True,
            "direct_action": dispatch.get("direct_action_allowed") is True,
            "direct_speech": dispatch.get("direct_speech_allowed") is True,
            "direct_fact_write": dispatch.get("direct_fact_write_allowed") is True,
            "synthesis_entrypoint": dispatch.get("synthesis_entrypoint")
            or (synthesis_entrypoints[0] if synthesis_entrypoints else None),
            "output_candidate_types": list(dispatch.get("output_candidate_types") or ()),
        },
        "runtime_decision": {
            "runtime_decision_count": len(decisions),
            "execution_allowed": decision.get("runtime_execution_allowed"),
            "provider_activation_allowed": decision.get("provider_activation_allowed"),
            "fallback_execution_allowed": decision.get("fallback_execution_allowed"),
            "output_dispatch_allowed": decision.get("output_dispatch_allowed"),
            "composite_decision_candidate_only": (
                decision.get("decision_status") == "candidate_only"
                if decision
                else len(decisions) == 0
            ),
            "decision_type": decision.get("decision_type"),
        },
        "domain_boundary": _domain_boundary(bundle, case.expected_domain_id),
        "governance_checkpoints": _governance_checkpoints(bundle),
        "validation": {
            "expected_validation_ok": case.expected_validation_ok,
            "actual_validation_ok": actual_ok,
            "errors": errors,
            "matched_expectation": matched,
        },
        "trace_decision": trace_decision,
        "expected_notes": list(case.expected_notes),
    }


def run_single_dryrun_case(
    case: ProviderManagerRuntimeSkeletonDryRunCase,
) -> Dict[str, Any]:
    bundle = bundle_from_provider_manager_runtime_skeleton_case(case)
    actual_ok, errors = validate_provider_manager_runtime_skeleton_case_bundle(bundle)
    return build_trace_for_case(case, actual_ok=actual_ok, errors=errors, bundle=bundle)


def _trace_review(
    traces: List[Dict[str, Any]],
    case_id: str,
    expected_decision: str,
) -> Dict[str, Any]:
    trace = next((t for t in traces if t["case_id"] == case_id), None)
    if trace is None:
        return {"found": False, "expected_decision": expected_decision}
    return {
        "found": True,
        "trace_decision": trace["trace_decision"],
        "matches_expected": trace["trace_decision"] == expected_decision,
        "validation_errors": trace["validation"]["errors"],
        "governance_checkpoints": trace["governance_checkpoints"],
    }


def summarize_dryrun_traces(traces: List[Dict[str, Any]]) -> Dict[str, Any]:
    positive_pass = sum(1 for t in traces if t["trace_decision"] == "PASS")
    expected_reject = sum(1 for t in traces if t["trace_decision"] == "EXPECTED_REJECT")
    unexpected_pass = sum(1 for t in traces if t["trace_decision"] == "UNEXPECTED_PASS")
    unexpected_fail = sum(1 for t in traces if t["trace_decision"] == "UNEXPECTED_FAIL")
    positive_cases = [t for t in traces if t["case_type"] == "positive"]
    invalid_cases = [t for t in traces if t["case_type"] == "invalid"]

    runner_ok = (
        positive_pass == 9
        and expected_reject == 8
        and unexpected_pass == 0
        and unexpected_fail == 0
        and len(traces) == 17
    )

    no_dup = _no_domain_specific_manager_duplication()
    spatial_boundary = any(
        t["domain_boundary"].get("spatial_evidence_boundary_preserved") is True
        for t in positive_cases
        if t["case_id"] == "case_pos_07_spatial_field_synthesis_dispatch"
    )
    vision_boundary = any(
        t["domain_boundary"].get("vision_ocr_boundary_preserved") is True
        for t in positive_cases
        if t["case_id"] == "case_pos_08_vision_ocr_abstraction_dispatch"
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 3 Provider Manager Runtime Skeleton Runner",
        "runtime_skeleton_principle_zh": RUNTIME_SKELETON_PRINCIPLE_ZH,
        "case_count": len(traces),
        "positive_case_count": len(positive_cases),
        "invalid_case_count": len(invalid_cases),
        "positive_pass_count": positive_pass,
        "invalid_expected_reject_count": expected_reject,
        "unexpected_pass_count": unexpected_pass,
        "unexpected_fail_count": unexpected_fail,
        "trace_count": len(traces),
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "runtime_execution_allowed": False,
        "provider_activation_allowed": False,
        "fallback_execution_allowed": False,
        "output_dispatch_allowed": False,
        "real_provider_connected": False,
        "candidate_only_enforced": True,
        "shared_governance_source_required": True,
        "domain_profile_source_required": True,
        "spatial_evidence_boundary_preserved": spatial_boundary,
        "vision_ocr_boundary_preserved": vision_boundary,
        "no_domain_specific_manager_duplication": no_dup,
        "no_real_provider_connected": NON_EXECUTION_FLAGS.get("no_real_provider_connected")
        is True,
        "no_backend_connected": True,
        "no_camera": NON_EXECUTION_FLAGS.get("no_camera_runtime") is True,
        "no_ros": NON_EXECUTION_FLAGS.get("no_ros_runtime") is True,
        "no_runtime_execution": NON_EXECUTION_FLAGS.get("no_runtime_execution") is True,
        "forbidden_policy_catalog": list(FORBIDDEN_RUNTIME_SKELETON_POLICIES),
        "trace_decisions": {t["case_id"]: t["trace_decision"] for t in traces},
        "invalid_case_reviews": {
            "invalid_a_runtime_execution_allowed": _trace_review(
                traces, "invalid_a_runtime_execution_allowed", "EXPECTED_REJECT"
            ),
            "invalid_b_provider_activation_allowed": _trace_review(
                traces, "invalid_b_provider_activation_allowed", "EXPECTED_REJECT"
            ),
            "invalid_c_fallback_execution_allowed": _trace_review(
                traces, "invalid_c_fallback_execution_allowed", "EXPECTED_REJECT"
            ),
            "invalid_d_output_dispatch_allowed": _trace_review(
                traces, "invalid_d_output_dispatch_allowed", "EXPECTED_REJECT"
            ),
            "invalid_e_real_provider_connected": _trace_review(
                traces, "invalid_e_real_provider_connected", "EXPECTED_REJECT"
            ),
            "invalid_f_health_loop_direct_disable": _trace_review(
                traces, "invalid_f_health_loop_direct_disable", "EXPECTED_REJECT"
            ),
            "invalid_g_direct_output_paths": _trace_review(
                traces, "invalid_g_direct_output_paths", "EXPECTED_REJECT"
            ),
            "invalid_h_vision_ocr_spatial_pollution": _trace_review(
                traces, "invalid_h_vision_ocr_spatial_pollution", "EXPECTED_REJECT"
            ),
        },
        "final_decision": (
            FINAL_DECISION_DRYRUN_TRACE_READY_FOR_VERIFIER
            if runner_ok
            else FINAL_DECISION_DRYRUN_RUNNER_UNEXPECTED_OUTCOME
        ),
    }


def run_provider_manager_runtime_skeleton_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_files: bool = True,
) -> Dict[str, Any]:
    all_cases = build_all_provider_manager_runtime_skeleton_cases_v1()
    traces = [run_single_dryrun_case(case) for case in all_cases]
    summary = summarize_dryrun_traces(traces)

    resolved_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    result: Dict[str, Any] = {
        "summary": summary,
        "traces": traces,
        "output_root": str(resolved_root),
    }

    if write_files:
        resolved_root.mkdir(parents=True, exist_ok=True)
        trace_path = resolved_root / TRACE_FILENAME
        summary_path = resolved_root / SUMMARY_FILENAME

        trace_doc = {
            "phase_id": PHASE_ID,
            "step": "Step 3 Provider Manager Runtime Skeleton Runner",
            "runtime_skeleton_principle_zh": RUNTIME_SKELETON_PRINCIPLE_ZH,
            "trace_count": len(traces),
            "validator_rules": len(VALIDATOR_RULE_IDS),
            "traces": traces,
        }
        trace_path.write_text(
            json.dumps(trace_doc, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        summary_path.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        result["output_trace_file"] = str(trace_path)
        result["output_summary_file"] = str(summary_path)

    return result


def main() -> int:
    result = run_provider_manager_runtime_skeleton_dryrun_v1()
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": result["output_root"],
                "output_trace_file": result.get("output_trace_file"),
                "output_summary_file": result.get("output_summary_file"),
                "positive_pass_count": summary["positive_pass_count"],
                "invalid_expected_reject_count": summary["invalid_expected_reject_count"],
                "unexpected_pass_count": summary["unexpected_pass_count"],
                "unexpected_fail_count": summary["unexpected_fail_count"],
                "trace_count": summary["trace_count"],
                "spatial_evidence_boundary_preserved": summary[
                    "spatial_evidence_boundary_preserved"
                ],
                "vision_ocr_boundary_preserved": summary["vision_ocr_boundary_preserved"],
                "no_domain_specific_manager_duplication": summary[
                    "no_domain_specific_manager_duplication"
                ],
                "final_decision": summary["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary["final_decision"] == FINAL_DECISION_DRYRUN_TRACE_READY_FOR_VERIFIER else 1


if __name__ == "__main__":
    raise SystemExit(main())
