# -*- coding: utf-8 -*-
"""Shared Provider Runtime Governance Skeleton — dry-run runner v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.provider_runtime_governance.domain_profiles.vision_ocr_governance_compatibility_v1 import (
    verify_vision_ocr_compatibility_v1,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_dryrun_cases_v1 import (
    SharedProviderRuntimeGovernanceDryRunCase,
    build_all_shared_provider_runtime_governance_cases_v1,
    bundle_from_shared_provider_runtime_governance_case,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_registry_v1 import (
    FORBIDDEN_PROVIDER_MANAGER_POLICIES,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
    _no_domain_specific_manager_duplication,
    validate_provider_runtime_governance_case_bundle,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_types_v1 import (
    DOMAIN_SPATIAL_EVIDENCE,
    DOMAIN_VISION_OCR,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_DRYRUN_RUNNER_UNEXPECTED_OUTCOME,
    FINAL_DECISION_DRYRUN_TRACE_READY_FOR_VERIFIER,
    GOVERNANCE_PRINCIPLE_ZH,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    SHARED_MANAGER_REF,
)

DEFAULT_OUTPUT = (
    _REPO_ROOT / "_tmp_eval_out" / "shared_provider_runtime_governance_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "provider_runtime_governance_dryrun_trace_v1.json"
SUMMARY_FILENAME = "provider_runtime_governance_dryrun_summary_v1.json"

TraceDecision = Literal["PASS", "EXPECTED_REJECT", "UNEXPECTED_PASS", "UNEXPECTED_FAIL"]

_SPATIAL_POLLUTION_CANDIDATES = frozenset({"PoseCandidate", "SLAMHealthCandidate"})


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


def _bundle_text_fields(bundle: Dict[str, Any]) -> List[str]:
    texts: List[str] = []
    for section in (
        "managers",
        "domain_profiles",
        "registry_entries",
        "enable_requests",
        "disable_requests",
        "runtime_states",
        "health_snapshots",
        "fallback_routes",
        "runtime_admission_checks",
        "manager_decisions",
    ):
        for item in bundle.get(section) or ():
            for key in ("reason", "disable_reason", "trigger_conditions", "required_checks", "blocked_reasons"):
                val = item.get(key)
                if isinstance(val, str):
                    texts.append(val)
                elif isinstance(val, (list, tuple)):
                    texts.extend(str(v) for v in val)
    return texts


def _forbidden_policy_present(bundle: Dict[str, Any], policy: str) -> bool:
    return any(policy == text or policy in text for text in _bundle_text_fields(bundle))


def _vision_ocr_case_compatible(bundle: Dict[str, Any]) -> bool:
    profiles = list(bundle.get("domain_profiles") or ())
    vision_profile = next(
        (p for p in profiles if p.get("domain_id") == DOMAIN_VISION_OCR),
        None,
    )
    if not vision_profile:
        return True
    declared = set(vision_profile.get("supported_output_candidate_types") or ())
    for entry in bundle.get("registry_entries") or ():
        entry_types = entry.get("supported_output_candidate_types") or ()
        for ctype in entry_types:
            if ctype in _SPATIAL_POLLUTION_CANDIDATES and ctype not in declared:
                return False
    return True


def _spatial_profile_supported(bundle: Dict[str, Any]) -> bool:
    for profile in bundle.get("domain_profiles") or ():
        if profile.get("domain_id") != DOMAIN_SPATIAL_EVIDENCE:
            continue
        return (
            profile.get("synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
            and profile.get("uses_shared_manager_skeleton") is True
        )
    return True


def _governance_checkpoints(bundle: Dict[str, Any]) -> Dict[str, bool]:
    managers = list(bundle.get("managers") or ())
    profiles = list(bundle.get("domain_profiles") or ())
    registry = list(bundle.get("registry_entries") or ())
    fallbacks = list(bundle.get("fallback_routes") or ())
    runtime_states = list(bundle.get("runtime_states") or ())
    candidate_only_items = (
        managers
        + profiles
        + registry
        + list(bundle.get("enable_requests") or ())
        + list(bundle.get("disable_requests") or ())
        + runtime_states
        + list(bundle.get("health_snapshots") or ())
        + fallbacks
        + list(bundle.get("runtime_admission_checks") or ())
    )

    profile_domains = {p.get("domain_id") for p in profiles}
    vision_ok, _, _ = verify_vision_ocr_compatibility_v1()

    return {
        "runtime_activation_still_disabled": all(
            m.get("runtime_activation_allowed") is not True for m in managers
        ),
        "provider_runtime_still_disabled": all(
            m.get("provider_runtime_enabled") is not True for m in managers
        )
        and all(s.get("provider_runtime_enabled") is not True for s in runtime_states),
        "domain_profile_required": (
            all(e.get("domain_id") in profile_domains for e in registry) if registry else bool(profiles)
        ),
        "candidate_only_enforced": all(
            item.get("candidate_only") is True for item in candidate_only_items if item
        ),
        "vision_ocr_compatibility_preserved": vision_ok and _vision_ocr_case_compatible(bundle),
        "spatial_evidence_profile_supported": _spatial_profile_supported(bundle),
        "no_domain_specific_manager_duplication": all(
            SHARED_MANAGER_REF in str(m.get("manager_ref") or "") for m in managers
        ),
        "fallback_preserves_source_chain": (
            all(r.get("preserve_source_chain") is True for r in fallbacks) if fallbacks else True
        ),
        "no_direct_action": not _forbidden_policy_present(bundle, "manager_direct_action"),
        "no_direct_speech": not _forbidden_policy_present(bundle, "manager_direct_speech"),
        "no_direct_fact_write": not _forbidden_policy_present(bundle, "manager_direct_fact_write"),
    }


def build_trace_for_case(
    case: SharedProviderRuntimeGovernanceDryRunCase,
    *,
    actual_ok: bool,
    errors: List[str],
    bundle: Dict[str, Any],
) -> Dict[str, Any]:
    managers = list(bundle.get("managers") or ())
    profiles = list(bundle.get("domain_profiles") or ())
    registry = list(bundle.get("registry_entries") or ())
    enable_requests = list(bundle.get("enable_requests") or ())
    disable_requests = list(bundle.get("disable_requests") or ())
    runtime_states = list(bundle.get("runtime_states") or ())
    health_snapshots = list(bundle.get("health_snapshots") or ())
    fallback_routes = list(bundle.get("fallback_routes") or ())
    admission_checks = list(bundle.get("runtime_admission_checks") or ())

    manager = _pick_by_domain(managers, case.expected_domain_id)
    profile = _pick_by_domain(profiles, case.expected_domain_id)
    admission = _first_item(admission_checks)

    trace_decision = classify_trace_decision(case.expected_validation_ok, actual_ok)
    matched = trace_decision in ("PASS", "EXPECTED_REJECT")

    runtime_enabled_refs: List[str] = []
    for state in runtime_states:
        runtime_enabled_refs.extend(list(state.get("runtime_enabled_provider_refs") or ()))

    return {
        "case_id": case.case_id,
        "case_name": case.case_name,
        "case_type": case.case_type,
        "case_goal": case.case_goal,
        "manager": {
            "manager_ref": manager.get("manager_ref"),
            "domain_id": manager.get("domain_id") or case.expected_domain_id,
            "manager_status": manager.get("manager_status"),
            "runtime_activation_allowed": manager.get("runtime_activation_allowed"),
            "provider_runtime_enabled": manager.get("provider_runtime_enabled"),
        },
        "domain_profile": {
            "domain_id": profile.get("domain_id") or case.expected_domain_id,
            "domain_profile_ref": profile.get("profile_ref"),
            "synthesis_entrypoint": profile.get("synthesis_entrypoint"),
            "candidate_types": list(profile.get("supported_output_candidate_types") or ()),
            "domain_profile_present": bool(profiles),
        },
        "registry": {
            "registry_entry_count": len(registry),
            "enabled_by_default_count": sum(
                1 for e in registry if e.get("enabled_by_default") is True
            ),
            "runtime_enable_allowed_count": sum(
                1 for e in registry if e.get("runtime_enable_allowed") is True
            ),
        },
        "enable_disable": {
            "enable_request_count": len(enable_requests),
            "disable_request_count": len(disable_requests),
            "execution_allowed_count": sum(
                1
                for r in enable_requests + disable_requests
                if r.get("execution_allowed") is True
            ),
        },
        "runtime_state": {
            "runtime_state_count": len(runtime_states),
            "runtime_enabled_provider_refs": runtime_enabled_refs,
            "provider_runtime_enabled": any(
                s.get("provider_runtime_enabled") is True for s in runtime_states
            )
            or any(m.get("provider_runtime_enabled") is True for m in managers),
        },
        "health_and_fallback": {
            "health_snapshot_count": len(health_snapshots),
            "fallback_route_count": len(fallback_routes),
            "source_chain_preserved": all(
                r.get("preserve_source_chain") is True for r in fallback_routes
            )
            if fallback_routes
            else True,
            "conflict_refs_preserved": all(
                r.get("preserve_conflict_refs") is True for r in fallback_routes
            )
            if fallback_routes
            else True,
        },
        "runtime_admission": {
            "runtime_admission_check_count": len(admission_checks),
            "runtime_admission_allowed": admission.get("runtime_admission_allowed"),
            "commercial_runtime_allowed": admission.get("commercial_runtime_allowed"),
        },
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
    case: SharedProviderRuntimeGovernanceDryRunCase,
) -> Dict[str, Any]:
    bundle = bundle_from_shared_provider_runtime_governance_case(case)
    actual_ok, errors = validate_provider_runtime_governance_case_bundle(bundle)
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
        positive_pass == 10
        and expected_reject == 7
        and unexpected_pass == 0
        and unexpected_fail == 0
        and len(traces) == 17
    )

    vision_ok, _, _ = verify_vision_ocr_compatibility_v1()
    no_dup = _no_domain_specific_manager_duplication()
    spatial_supported = any(
        t["domain_profile"].get("domain_id") == DOMAIN_SPATIAL_EVIDENCE for t in positive_cases
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 3 Shared Provider Runtime Governance Runner",
        "governance_principle_zh": GOVERNANCE_PRINCIPLE_ZH,
        "case_count": len(traces),
        "positive_case_count": len(positive_cases),
        "invalid_case_count": len(invalid_cases),
        "positive_pass_count": positive_pass,
        "invalid_expected_reject_count": expected_reject,
        "unexpected_pass_count": unexpected_pass,
        "unexpected_fail_count": unexpected_fail,
        "trace_count": len(traces),
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "shared_provider_runtime_governance_ready": runner_ok,
        "vision_ocr_compatibility_preserved": vision_ok,
        "spatial_evidence_profile_supported": spatial_supported,
        "no_domain_specific_manager_duplication": no_dup,
        "runtime_activation_allowed": False,
        "provider_runtime_enabled": False,
        "candidate_only_enforced": True,
        "domain_profile_required": True,
        "no_real_provider_connected": NON_EXECUTION_FLAGS.get("no_real_provider_runtime") is True,
        "no_real_backend_connected": True,
        "no_camera": True,
        "no_ros": True,
        "no_runtime_activation": NON_EXECUTION_FLAGS.get("no_runtime_activation") is True,
        "forbidden_policy_catalog": list(FORBIDDEN_PROVIDER_MANAGER_POLICIES),
        "trace_decisions": {t["case_id"]: t["trace_decision"] for t in traces},
        "invalid_case_reviews": {
            "invalid_a_default_enabled_provider": _trace_review(
                traces, "invalid_a_default_enabled_provider", "EXPECTED_REJECT"
            ),
            "invalid_b_runtime_activation_allowed": _trace_review(
                traces, "invalid_b_runtime_activation_allowed", "EXPECTED_REJECT"
            ),
            "invalid_c_missing_domain_profile": _trace_review(
                traces, "invalid_c_missing_domain_profile", "EXPECTED_REJECT"
            ),
            "invalid_d_direct_action_forbidden": _trace_review(
                traces, "invalid_d_direct_action_forbidden", "EXPECTED_REJECT"
            ),
            "invalid_e_fallback_no_source_chain": _trace_review(
                traces, "invalid_e_fallback_no_source_chain", "EXPECTED_REJECT"
            ),
            "invalid_f_spatial_bypass_field_synthesis": _trace_review(
                traces, "invalid_f_spatial_bypass_field_synthesis", "EXPECTED_REJECT"
            ),
            "invalid_g_vision_ocr_spatial_candidate_pollution": _trace_review(
                traces, "invalid_g_vision_ocr_spatial_candidate_pollution", "EXPECTED_REJECT"
            ),
        },
        "final_decision": (
            FINAL_DECISION_DRYRUN_TRACE_READY_FOR_VERIFIER
            if runner_ok
            else FINAL_DECISION_DRYRUN_RUNNER_UNEXPECTED_OUTCOME
        ),
    }


def run_provider_runtime_governance_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_files: bool = True,
) -> Dict[str, Any]:
    all_cases = build_all_shared_provider_runtime_governance_cases_v1()
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
            "step": "Step 3 Shared Provider Runtime Governance Runner",
            "governance_principle_zh": GOVERNANCE_PRINCIPLE_ZH,
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
    result = run_provider_runtime_governance_dryrun_v1()
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
                "vision_ocr_compatibility_preserved": summary["vision_ocr_compatibility_preserved"],
                "spatial_evidence_profile_supported": summary["spatial_evidence_profile_supported"],
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
