# -*- coding: utf-8 -*-
"""Field SLAM Interface Contract — dry-run runner v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_interface.field_slam_interface_dryrun_cases_v1 import (
    FieldSLAMInterfaceDryRunCase,
    build_all_slam_interface_cases_v1,
    bundle_from_slam_interface_case,
)
from capabilities.field_understanding.slam_interface.field_slam_interface_registry_v1 import (
    FORBIDDEN_SLAM_POLICIES,
    HIGH_DRIFT_RISK_LEVELS,
    SLAM_BYPASS_FIELD_SYNTHESIS_KEYS,
    SLAM_DESTINATION_CONFIRMATION_KEYS,
    SLAM_EVIDENCE_GOVERNANCE_CHAIN,
    SLAM_FIELD_IDENTITY_OVERRIDE_KEYS,
    TRACKING_DEGRADED_STATUSES,
)
from capabilities.field_understanding.slam_interface.field_slam_interface_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
    validate_slam_interface_bundle,
)
from capabilities.field_understanding.slam_interface.field_slam_interface_types_v1 import (
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    SLAM_EVIDENCE_PROVIDER_GOVERNANCE_ID,
)

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_slam_interface_dryrun_v1_smoke_v0"
)
FINAL_DECISION_TRACE_READY = "FIELD_SLAM_INTERFACE_DRYRUN_TRACE_READY_FOR_VERIFIER"
FINAL_DECISION_RUNNER_FAIL = "FIELD_SLAM_INTERFACE_DRYRUN_RUNNER_UNEXPECTED_OUTCOME"

TraceDecision = Literal["PASS", "EXPECTED_REJECT", "UNEXPECTED_PASS", "UNEXPECTED_FAIL"]


def classify_trace_decision(expected_ok: bool, actual_ok: bool) -> TraceDecision:
    if expected_ok and actual_ok:
        return "PASS"
    if not expected_ok and not actual_ok:
        return "EXPECTED_REJECT"
    if not expected_ok and actual_ok:
        return "UNEXPECTED_PASS"
    return "UNEXPECTED_FAIL"


def _collect_forbidden_policies(bundle: Dict[str, Any]) -> List[str]:
    detected: List[str] = []
    for drift in bundle.get("drift_states") or ():
        policy = drift.get("recommended_policy")
        if policy in FORBIDDEN_SLAM_POLICIES:
            detected.append(policy)
    for anchor in bundle.get("anchors") or ():
        for key in SLAM_DESTINATION_CONFIRMATION_KEYS:
            if anchor.get(key) is True:
                detected.append("slam_confirm_destination")
                break
    for item in (
        list(bundle.get("poses") or ())
        + list(bundle.get("motions") or ())
        + list(bundle.get("anchors") or ())
        + list(bundle.get("local_maps") or ())
        + list(bundle.get("health_states") or ())
        + list(bundle.get("drift_states") or ())
        + list(bundle.get("relocalizations") or ())
    ):
        for key in SLAM_BYPASS_FIELD_SYNTHESIS_KEYS:
            if item.get(key) is True:
                policy = key if key in FORBIDDEN_SLAM_POLICIES else f"bypass:{key}"
                if policy not in detected:
                    detected.append(policy)
    return sorted(set(detected))


def _governance_checkpoints(
    case: FieldSLAMInterfaceDryRunCase,
    bundle: Dict[str, Any],
) -> Dict[str, Any]:
    motions = bundle.get("motions") or ()
    anchors = bundle.get("anchors") or ()
    local_maps = bundle.get("local_maps") or ()
    health_states = bundle.get("health_states") or ()
    drift_states = bundle.get("drift_states") or ()
    relocalizations = bundle.get("relocalizations") or ()
    action_readiness = bundle.get("action_readiness")

    motion_direct_action = any(
        m.get("action_readiness") or m.get("ready_for_action_decision") is True
        for m in motions
    )
    anchor_confirms_destination = any(
        anchor.get(key) is True
        for anchor in anchors
        for key in SLAM_DESTINATION_CONFIRMATION_KEYS
    )
    long_term_map = any(
        lm.get("long_term_map") is True
        or lm.get("is_persistent_map") is True
        or lm.get("confirmed_map") is True
        for lm in local_maps
    )
    high_drift = any(lm.get("drift_risk") in HIGH_DRIFT_RISK_LEVELS for lm in local_maps)
    drift_policies = {d.get("recommended_policy") for d in drift_states}
    high_drift_handled = not high_drift or (
        action_readiness != "ready_for_action_decision"
        and (
            "needs_more_observation" in drift_policies
            or "downweight_spatial_evidence" in drift_policies
            or case.expected_policy in ("needs_more_observation", "downweight_spatial_evidence")
        )
    )
    tracking_lost = any(h.get("tracking_status") == "tracking_lost" for h in health_states)
    tracking_lost_not_ready = not tracking_lost or action_readiness != "ready_for_action_decision"
    forbidden = _collect_forbidden_policies(bundle)
    identity_override = any(
        item.get(key)
        for item in (
            list(bundle.get("poses") or ())
            + list(bundle.get("anchors") or ())
            + list(bundle.get("local_maps") or ())
        )
        for key in SLAM_FIELD_IDENTITY_OVERRIDE_KEYS
    )
    bypass = bool(forbidden) or any(
        item.get(key) is True
        for item in (
            list(bundle.get("poses") or ())
            + list(bundle.get("motions") or ())
            + list(bundle.get("anchors") or ())
            + list(bundle.get("local_maps") or ())
            + list(bundle.get("health_states") or ())
            + list(bundle.get("drift_states") or ())
        )
        for key in SLAM_BYPASS_FIELD_SYNTHESIS_KEYS
    )
    relocalization_memory_only = all(
        r.get("relocalization_status") in ("matched", "partially_matched", "unknown", "not_matched", "ambiguous")
        for r in relocalizations
    ) if relocalizations else True

    stationary_near_no_escalation = True
    if case.case_id == "case_06_stationary_near_zone_no_escalation":
        stationary_near_no_escalation = (
            any(m.get("motion_state") == "stationary" for m in motions)
            and action_readiness != "ready_for_action_decision"
            and case.expected_policy == "influence_only"
        )

    return {
        "slam_evidence_chain_traversed": list(SLAM_EVIDENCE_GOVERNANCE_CHAIN),
        "motion_no_direct_action": not motion_direct_action,
        "anchor_no_direct_destination": not anchor_confirms_destination,
        "local_map_short_term_only": not long_term_map,
        "high_drift_triggers_downweight_or_needs_observation": high_drift_handled,
        "tracking_lost_not_ready_for_action": tracking_lost_not_ready,
        "relocalization_supports_memory_not_action": relocalization_memory_only,
        "forbidden_policies_identified": forbidden,
        "no_field_identity_override": not identity_override,
        "no_bypass_field_synthesis": not bypass,
        "stationary_near_no_immediate_risk_escalation": stationary_near_no_escalation,
    }


def build_trace_for_case(
    case: FieldSLAMInterfaceDryRunCase,
    *,
    actual_ok: bool,
    errors: List[str],
    bundle: Dict[str, Any],
) -> Dict[str, Any]:
    poses = bundle.get("poses") or ()
    motions = bundle.get("motions") or ()
    anchors = bundle.get("anchors") or ()
    local_maps = bundle.get("local_maps") or ()
    health_states = bundle.get("health_states") or ()
    drift_states = bundle.get("drift_states") or ()
    relocalizations = bundle.get("relocalizations") or ()

    forbidden_policies = _collect_forbidden_policies(bundle)
    trace_decision = classify_trace_decision(case.expected_validation_ok, actual_ok)
    matched = trace_decision in ("PASS", "EXPECTED_REJECT")
    checkpoints = _governance_checkpoints(case, bundle)

    tracking_statuses = [h.get("tracking_status") for h in health_states]
    degraded = any(s in TRACKING_DEGRADED_STATUSES for s in tracking_statuses)
    tracking_lost = any(s == "tracking_lost" for s in tracking_statuses)

    return {
        "case_id": case.case_id,
        "case_name": case.case_name,
        "case_type": case.case_type,
        "case_goal": case.case_goal,
        "expected_notes": list(case.expected_notes),
        "slam_evidence_governance_chain": list(SLAM_EVIDENCE_GOVERNANCE_CHAIN),
        "governance_checkpoints": checkpoints,
        "pose_evidence": {
            "pose_count": len(poses),
            "source_methods": sorted({p.get("source_method") for p in poses if p.get("source_method")}),
            "has_source_refs": all(bool(p.get("source_refs")) for p in poses) if poses else True,
        },
        "motion_evidence": {
            "motion_count": len(motions),
            "motion_states": [m.get("motion_state") for m in motions],
            "speed_bands": [m.get("speed_band") for m in motions],
            "direct_action_generated": any(
                m.get("action_readiness") or m.get("ready_for_action_decision") is True for m in motions
            ),
        },
        "spatial_anchor_evidence": {
            "anchor_count": len(anchors),
            "anchor_types": [a.get("anchor_type") for a in anchors],
            "relative_position_bands": [a.get("relative_position_band") for a in anchors],
            "direct_destination_confirmed": any(
                a.get(key) is True for a in anchors for key in SLAM_DESTINATION_CONFIRMATION_KEYS
            ),
        },
        "local_map_evidence": {
            "local_map_count": len(local_maps),
            "time_windows_ms": [lm.get("time_window_ms") for lm in local_maps],
            "drift_risks": [lm.get("drift_risk") for lm in local_maps],
            "long_term_map_declared": any(
                lm.get("long_term_map") is True
                or lm.get("is_persistent_map") is True
                or lm.get("confirmed_map") is True
                for lm in local_maps
            ),
        },
        "slam_health": {
            "health_count": len(health_states),
            "tracking_statuses": tracking_statuses,
            "degraded": degraded,
            "tracking_lost": tracking_lost,
        },
        "map_drift": {
            "drift_count": len(drift_states),
            "drift_risks": [d.get("drift_risk") for d in drift_states],
            "recommended_policies": [d.get("recommended_policy") for d in drift_states],
        },
        "relocalization": {
            "relocalization_count": len(relocalizations),
            "statuses": [r.get("relocalization_status") for r in relocalizations],
            "match_scores": [r.get("match_score") for r in relocalizations],
        },
        "field_integration": {
            "expected_field_influence": list(case.expected_field_influence),
            "expected_policy": case.expected_policy,
            "action_readiness_in_bundle": bundle.get("action_readiness"),
            "bypasses_field_synthesis": not checkpoints["no_bypass_field_synthesis"],
            "field_identity_overridden": not checkpoints["no_field_identity_override"],
        },
        "forbidden_policy_check": {
            "forbidden_policies_detected": forbidden_policies,
            "forbidden_policy_count": len(forbidden_policies),
        },
        "validation": {
            "expected_validation_ok": case.expected_validation_ok,
            "actual_validation_ok": actual_ok,
            "errors": errors,
            "matched_expectation": matched,
        },
        "trace_decision": trace_decision,
    }


def run_single_dryrun_case(case: FieldSLAMInterfaceDryRunCase) -> Dict[str, Any]:
    bundle = bundle_from_slam_interface_case(case)
    actual_ok, errors = validate_slam_interface_bundle(**bundle)
    return build_trace_for_case(case, actual_ok=actual_ok, errors=errors, bundle=bundle)


def summarize_dryrun_traces(traces: List[Dict[str, Any]]) -> Dict[str, Any]:
    positive_pass = sum(1 for t in traces if t["trace_decision"] == "PASS")
    expected_reject = sum(1 for t in traces if t["trace_decision"] == "EXPECTED_REJECT")
    unexpected_pass = sum(1 for t in traces if t["trace_decision"] == "UNEXPECTED_PASS")
    unexpected_fail = sum(1 for t in traces if t["trace_decision"] == "UNEXPECTED_FAIL")
    positive_cases = [t for t in traces if t["case_type"] == "positive"]
    invalid_cases = [t for t in traces if t["case_type"] == "invalid"]

    runner_ok = (
        positive_pass == len(positive_cases)
        and expected_reject == len(invalid_cases)
        and unexpected_pass == 0
        and unexpected_fail == 0
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 3 Dry-run Runner",
        "governance_id": SLAM_EVIDENCE_PROVIDER_GOVERNANCE_ID,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "case_count": len(traces),
        "positive_case_count": len(positive_cases),
        "invalid_case_count": len(invalid_cases),
        "positive_pass_count": positive_pass,
        "invalid_expected_reject_count": expected_reject,
        "unexpected_pass_count": unexpected_pass,
        "unexpected_fail_count": unexpected_fail,
        "trace_count": len(traces),
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "no_runtime_slam": NON_EXECUTION_FLAGS.get("no_slam_execution") is True,
        "no_camera": NON_EXECUTION_FLAGS.get("no_camera_runtime") is True,
        "no_model": NON_EXECUTION_FLAGS.get("no_model_execution") is True,
        "no_graph_eqa": True,
        "no_speech_gate": NON_EXECUTION_FLAGS.get("no_speech_output") is True,
        "trace_decisions": {t["case_id"]: t["trace_decision"] for t in traces},
        "final_decision": FINAL_DECISION_TRACE_READY if runner_ok else FINAL_DECISION_RUNNER_FAIL,
    }


def run_field_slam_interface_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_files: bool = True,
) -> Dict[str, Any]:
    all_cases = build_all_slam_interface_cases_v1()
    traces = [run_single_dryrun_case(case) for case in all_cases]
    summary = summarize_dryrun_traces(traces)

    result = {
        "summary": summary,
        "traces": traces,
        "output_root": str(Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()),
    }

    if write_files:
        out = Path(result["output_root"])
        out.mkdir(parents=True, exist_ok=True)
        trace_doc = {
            "phase_id": PHASE_ID,
            "step": "Step 3 Dry-run Runner",
            "trace_count": len(traces),
            "traces": traces,
        }
        (out / "field_slam_interface_dryrun_trace_v1.json").write_text(
            json.dumps(trace_doc, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (out / "field_slam_interface_dryrun_summary_v1.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return result


def main() -> int:
    result = run_field_slam_interface_dryrun_v1()
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": result["output_root"],
                "positive_pass_count": summary["positive_pass_count"],
                "invalid_expected_reject_count": summary["invalid_expected_reject_count"],
                "unexpected_pass_count": summary["unexpected_pass_count"],
                "unexpected_fail_count": summary["unexpected_fail_count"],
                "trace_count": summary["trace_count"],
                "final_decision": summary["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary["final_decision"] == FINAL_DECISION_TRACE_READY else 1


if __name__ == "__main__":
    raise SystemExit(main())
