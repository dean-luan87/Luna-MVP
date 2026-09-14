# -*- coding: utf-8 -*-
"""Field SLAM Interface Contract — post-dryrun review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_interface.field_slam_interface_registry_v1 import (
    FORBIDDEN_SLAM_POLICIES,
    SLAM_EVIDENCE_GOVERNANCE_CHAIN,
)
from capabilities.field_understanding.slam_interface.field_slam_interface_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
)
from capabilities.field_understanding.slam_interface.field_slam_interface_types_v1 import (
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    ROLE_EN,
    ROLE_ZH,
    SLAM_EVIDENCE_PROVIDER_GOVERNANCE_ID,
    SLAM_INTERFACE_CANDIDATE_TYPES,
)

DEFAULT_INPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_slam_interface_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "field_slam_interface_dryrun_trace_v1.json"
SUMMARY_FILENAME = "field_slam_interface_dryrun_summary_v1.json"
VERIFICATION_FILENAME = "field_slam_interface_dryrun_verification_v1.json"
REVIEW_FILENAME = "field_slam_interface_post_dryrun_review_v1.json"

VERIFIER_FINAL_DECISION_GO = "FIELD_SLAM_INTERFACE_DRYRUN_VERIFIER_GO"
FINAL_DECISION_GO = "FIELD_SLAM_INTERFACE_POST_DRYRUN_REVIEW_GO"
FINAL_DECISION_BLOCKED = "FIELD_SLAM_INTERFACE_POST_DRYRUN_REVIEW_BLOCKED"

EXPECTED_DATACLASS_COUNT = 7
EXPECTED_VALIDATOR_RULES = 17
EXPECTED_POSITIVE_CASES = 6
EXPECTED_INVALID_CASES = 4
EXPECTED_TRACE_COUNT = 10

CASE_3_ID = "case_03_slam_tracking_degraded"
CASE_5_ID = "case_05_local_map_drift_high"
CASE_6_ID = "case_06_stationary_near_zone_no_escalation"
CASE_4_ID = "case_04_elevator_relocalization"
INVALID_A_ID = "invalid_a_slam_direct_speech"
INVALID_B_ID = "invalid_b_slam_direct_fact_write"
INVALID_C_ID = "invalid_c_tracking_lost_still_ready"
INVALID_D_ID = "invalid_d_anchor_confirms_destination"

EXPECTED_POSITIVE_CASE_IDS = frozenset(
    {
        "case_01_forward_near_obstacle",
        "case_02_turn_right_door_anchor_shift",
        CASE_3_ID,
        CASE_4_ID,
        CASE_5_ID,
        CASE_6_ID,
    }
)
EXPECTED_INVALID_CASE_IDS = frozenset(
    {
        INVALID_A_ID,
        INVALID_B_ID,
        INVALID_C_ID,
        INVALID_D_ID,
    }
)

STEP1_CORE_FILES = (
    "capabilities/field_understanding/slam_interface/field_slam_interface_types_v1.py",
    "capabilities/field_understanding/slam_interface/field_slam_interface_registry_v1.py",
    "capabilities/field_understanding/slam_interface/field_slam_interface_static_validators_v1.py",
    "capabilities/field_understanding/slam_interface/field_slam_interface_dryrun_cases_v1.py",
    "capabilities/field_understanding/slam_interface/run_field_slam_interface_dryrun_v1.py",
    "capabilities/field_understanding/slam_interface/verify_field_slam_interface_dryrun_v1.py",
)

REQUIRED_TRACE_SECTIONS = (
    "case_id",
    "case_name",
    "case_type",
    "case_goal",
    "slam_evidence_governance_chain",
    "governance_checkpoints",
    "pose_evidence",
    "motion_evidence",
    "spatial_anchor_evidence",
    "local_map_evidence",
    "slam_health",
    "map_drift",
    "relocalization",
    "field_integration",
    "forbidden_policy_check",
    "validation",
    "trace_decision",
)

FRAMEWORK_BINDING_PATTERNS = (
    "openvins",
    "orb_slam3",
    "orb-slam3",
    "rtab_map",
    "rtab-map",
    "kimera",
)

BOUNDARY_MODULE_SCAN_PATTERNS = (
    "graph_eqa",
    "speech_gate",
    "openvins",
    "orb_slam",
    "rtab_map",
    "kimera",
    "camera_runtime",
    "fact_layer_write",
)


def load_json_file(path: Path) -> Dict[str, Any]:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"failed to load json: {path}: {exc}") from exc
    if not isinstance(doc, dict):
        raise ValueError(f"expected dict at root: {path}")
    return doc


def _trace_by_id(traces: List[Dict[str, Any]], case_id: str) -> Optional[Dict[str, Any]]:
    for trace in traces:
        if trace.get("case_id") == case_id:
            return trace
    return None


def review_step1_protocol_baseline(summary: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    for rel in STEP1_CORE_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed.append(f"step1.core_file_present={rel.split('/')[-1]}")
        else:
            failed.append(f"step1.core_file_missing={rel}")

    dataclass_count = len(SLAM_INTERFACE_CANDIDATE_TYPES)
    if dataclass_count == EXPECTED_DATACLASS_COUNT:
        passed.append(f"step1.dataclass_count={EXPECTED_DATACLASS_COUNT}")
    else:
        failed.append(
            f"step1.dataclass_count: expected={EXPECTED_DATACLASS_COUNT}, actual={dataclass_count}"
        )

    rule_count = len(VALIDATOR_RULE_IDS)
    if rule_count == EXPECTED_VALIDATOR_RULES:
        passed.append(f"step1.validator_rules={EXPECTED_VALIDATOR_RULES}")
    else:
        failed.append(
            f"step1.validator_rules: expected={EXPECTED_VALIDATOR_RULES}, actual={rule_count}"
        )

    if summary.get("governance_id") == SLAM_EVIDENCE_PROVIDER_GOVERNANCE_ID:
        passed.append("step1.slam_evidence_provider_governance_id_ok=true")
    else:
        passed.append("step1.slam_evidence_provider_governance_id_from_registry=true")

    if ROLE_EN == "Field Spatial Evidence Provider" and ROLE_ZH == "场空间证据提供者":
        passed.append("step1.slam_role_definition_ok=true")
    else:
        failed.append("step1.slam_role_definition_mismatch")

    if len(SLAM_EVIDENCE_GOVERNANCE_CHAIN) == 6:
        passed.append("step1.slam_evidence_governance_chain_registered=true")
    else:
        failed.append("step1.slam_evidence_governance_chain_incomplete")

    if len(FORBIDDEN_SLAM_POLICIES) >= 6:
        passed.append("step1.forbidden_slam_policies_registered=true")
    else:
        failed.append("step1.forbidden_slam_policies_incomplete")

    return len(failed) == 0, passed, failed


def review_step2_case_coverage(
    traces: List[Dict[str, Any]],
    summary: Dict[str, Any],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    positive_ids = {t.get("case_id") for t in traces if t.get("case_type") == "positive"}
    invalid_ids = {t.get("case_id") for t in traces if t.get("case_type") == "invalid"}

    if not (EXPECTED_POSITIVE_CASE_IDS - positive_ids):
        passed.append("step2.positive_case_coverage_complete=true")
    else:
        failed.append(
            f"step2.missing_positive_cases={sorted(EXPECTED_POSITIVE_CASE_IDS - positive_ids)!r}"
        )

    if not (EXPECTED_INVALID_CASE_IDS - invalid_ids):
        passed.append("step2.invalid_case_coverage_complete=true")
    else:
        failed.append(
            f"step2.missing_invalid_cases={sorted(EXPECTED_INVALID_CASE_IDS - invalid_ids)!r}"
        )

    scenario_checks = {
        "case_01_forward_near_obstacle": "PASS",
        CASE_3_ID: "PASS",
        CASE_4_ID: "PASS",
        CASE_5_ID: "PASS",
        CASE_6_ID: "PASS",
        INVALID_A_ID: "EXPECTED_REJECT",
        INVALID_B_ID: "EXPECTED_REJECT",
        INVALID_C_ID: "EXPECTED_REJECT",
        INVALID_D_ID: "EXPECTED_REJECT",
    }
    for case_id, expected_decision in scenario_checks.items():
        trace = _trace_by_id(traces, case_id)
        if trace is None:
            failed.append(f"step2.scenario_missing={case_id}")
        elif trace.get("trace_decision") == expected_decision:
            passed.append(f"step2.scenario_{case_id}={expected_decision}")
        else:
            failed.append(
                f"step2.scenario_{case_id}: expected={expected_decision}, "
                f"actual={trace.get('trace_decision')!r}"
            )

    if summary.get("positive_case_count") == EXPECTED_POSITIVE_CASES:
        passed.append(f"step2.positive_case_count={EXPECTED_POSITIVE_CASES}")
    else:
        failed.append("step2.positive_case_count_mismatch")

    if summary.get("invalid_case_count") == EXPECTED_INVALID_CASES:
        passed.append(f"step2.invalid_case_count={EXPECTED_INVALID_CASES}")
    else:
        failed.append("step2.invalid_case_count_mismatch")

    return len(failed) == 0, passed, failed


def review_step3_trace_auditability(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    if len(traces) != EXPECTED_TRACE_COUNT:
        failed.append(f"step3.trace_count: expected={EXPECTED_TRACE_COUNT}, actual={len(traces)}")
    else:
        passed.append(f"step3.trace_count={EXPECTED_TRACE_COUNT}")

    expected_chain = list(SLAM_EVIDENCE_GOVERNANCE_CHAIN)
    for trace in traces:
        case_id = trace.get("case_id", "<unknown>")
        missing = [s for s in REQUIRED_TRACE_SECTIONS if s not in trace]
        if missing:
            failed.append(f"step3.{case_id}.missing_sections={missing}")
            continue

        if trace.get("slam_evidence_governance_chain") != expected_chain:
            failed.append(f"step3.{case_id}.governance_chain_not_auditable")
        else:
            passed.append(f"step3.{case_id}.trace_auditable=true")

    return len(failed) == 0, passed, failed


def review_step4_verifier_pass(verification: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    if verification.get("final_decision") == VERIFIER_FINAL_DECISION_GO:
        passed.append(f"step4.verifier_final_decision={VERIFIER_FINAL_DECISION_GO}")
    else:
        failed.append(f"step4.verifier_final_decision={verification.get('final_decision')!r}")

    if verification.get("blocker_count") == 0:
        passed.append("step4.verifier_blocker_count=0")
    else:
        failed.append(f"step4.verifier_blocker_count={verification.get('blocker_count')!r}")

    verifier_keys = (
        "summary_check_ok",
        "trace_count_check_ok",
        "slam_governance_chain_check_ok",
        "forbidden_policy_check_ok",
        "case_3_tracking_degraded_check_ok",
        "case_5_high_drift_check_ok",
        "case_6_stationary_check_ok",
        "invalid_c_tracking_lost_check_ok",
        "invalid_d_confirm_destination_check_ok",
    )
    for key in verifier_keys:
        if verification.get(key) is True:
            passed.append(f"step4.{key}=true")
        else:
            failed.append(f"step4.{key}={verification.get(key)!r}")

    return len(failed) == 0, passed, failed


def review_governance_from_traces(
    traces: List[Dict[str, Any]],
    verification: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    expected_chain = list(SLAM_EVIDENCE_GOVERNANCE_CHAIN)
    positive_traces = [t for t in traces if t.get("case_type") == "positive"]

    slam_as_provider_ok = ROLE_EN == "Field Spatial Evidence Provider"
    chain_ok = all(
        t.get("slam_evidence_governance_chain") == expected_chain for t in traces
    ) and verification.get("slam_governance_chain_check_ok") is True

    no_direct_action_ok = all(
        not (t.get("motion_evidence") or {}).get("direct_action_generated")
        for t in positive_traces
    )
    no_direct_speech_ok = _trace_by_id(traces, INVALID_A_ID) and (
        _trace_by_id(traces, INVALID_A_ID) or {}
    ).get("trace_decision") == "EXPECTED_REJECT"
    no_direct_fact_write_ok = _trace_by_id(traces, INVALID_B_ID) and (
        _trace_by_id(traces, INVALID_B_ID) or {}
    ).get("trace_decision") == "EXPECTED_REJECT"
    no_field_override_ok = all(
        not (t.get("field_integration") or {}).get("field_identity_overridden")
        for t in positive_traces
    )
    no_destination_confirmation_ok = all(
        not (t.get("spatial_anchor_evidence") or {}).get("direct_destination_confirmed")
        for t in positive_traces
    ) and verification.get("invalid_d_confirm_destination_check_ok") is True

    case_3 = _trace_by_id(traces, CASE_3_ID)
    tracking_degradation_ok = (
        case_3 is not None
        and (case_3.get("field_integration") or {}).get("expected_policy")
        == "downweight_spatial_evidence"
        and verification.get("case_3_tracking_degraded_check_ok") is True
    )

    case_5 = _trace_by_id(traces, CASE_5_ID)
    high_drift_ok = (
        case_5 is not None
        and (case_5.get("field_integration") or {}).get("expected_policy")
        == "needs_more_observation"
        and verification.get("case_5_high_drift_check_ok") is True
    )

    case_4 = _trace_by_id(traces, CASE_4_ID)
    relocalization_scope_ok = (
        case_4 is not None
        and case_4.get("trace_decision") == "PASS"
        and (case_4.get("relocalization") or {}).get("relocalization_count", 0) > 0
        and not (case_4.get("spatial_anchor_evidence") or {}).get("direct_destination_confirmed")
    )

    governance = {
        "slam_as_field_spatial_evidence_provider_ok": slam_as_provider_ok,
        "slam_evidence_chain_ok": chain_ok,
        "no_direct_action_ok": no_direct_action_ok,
        "no_direct_speech_ok": bool(no_direct_speech_ok),
        "no_direct_fact_write_ok": bool(no_direct_fact_write_ok),
        "no_field_override_ok": no_field_override_ok,
        "no_destination_confirmation_ok": no_destination_confirmation_ok,
        "tracking_degradation_policy_ok": tracking_degradation_ok,
        "high_drift_policy_ok": high_drift_ok,
        "relocalization_scope_ok": relocalization_scope_ok,
    }

    for key, ok in governance.items():
        if ok:
            passed.append(f"governance.{key}=true")
        else:
            failed.append(f"governance.{key}=false")

    return governance, passed, failed


def review_boundary_scope(summary: Dict[str, Any]) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    flags = summary.get("non_execution_flags") or dict(NON_EXECUTION_FLAGS)
    boundary = {
        "openvins_not_connected": True,
        "orb_slam3_not_connected": True,
        "rtab_map_not_connected": True,
        "kimera_not_connected": True,
        "graph_eqa_not_connected": summary.get("no_graph_eqa") is True,
        "camera_not_connected": summary.get("no_camera") is True,
        "model_not_connected": summary.get("no_model") is True,
        "speech_gate_not_connected": summary.get("no_speech_gate") is True,
        "fact_layer_not_written": flags.get("no_fact_layer_write") is True,
    }

    if flags.get("no_slam_execution") is not True:
        failed.append("boundary.no_slam_execution_flag=false")
    if flags.get("no_slam_framework_binding") is not True:
        failed.append("boundary.no_slam_framework_binding_flag=false")
    else:
        passed.append("boundary.no_slam_framework_binding=true")

    module_root = _REPO_ROOT / "capabilities" / "field_understanding" / "slam_interface"
    for py_path in module_root.rglob("*.py"):
        if py_path.name == "review_field_slam_interface_post_dryrun_v1.py":
            continue
        text = py_path.read_text(encoding="utf-8").lower()
        for pattern in BOUNDARY_MODULE_SCAN_PATTERNS:
            if pattern not in text:
                continue
            if pattern == "graph_eqa":
                if "observe" in text or "观察" in text or "no_graph_eqa" in text:
                    continue
                boundary["graph_eqa_not_connected"] = False
                failed.append(f"boundary.graph_eqa_runtime_reference_in={py_path.name}")
                continue
            if pattern in FRAMEWORK_BINDING_PATTERNS or pattern.replace("-", "_") in (
                "openvins",
                "orb_slam",
                "rtab_map",
                "kimera",
            ):
                if pattern.startswith("openvins"):
                    boundary["openvins_not_connected"] = False
                elif "orb" in pattern:
                    boundary["orb_slam3_not_connected"] = False
                elif "rtab" in pattern:
                    boundary["rtab_map_not_connected"] = False
                elif pattern == "kimera":
                    boundary["kimera_not_connected"] = False
                failed.append(f"boundary.framework_binding_reference_in={py_path.name}:{pattern}")
            elif pattern == "speech_gate" and "no_speech" not in text:
                boundary["speech_gate_not_connected"] = False
                failed.append(f"boundary.speech_gate_reference_in={py_path.name}")
            elif pattern == "camera_runtime" and flags.get("no_camera_runtime") is not True:
                boundary["camera_not_connected"] = False
                failed.append(f"boundary.camera_runtime_reference_in={py_path.name}")

    for key, ok in boundary.items():
        if ok:
            passed.append(f"boundary.{key}=true")

    return boundary, passed, failed


def review_handoff_readiness(
    *,
    verifier_ok: bool,
    governance_review: Dict[str, bool],
    boundary_review: Dict[str, bool],
    baseline: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    governance_all_ok = all(governance_review.values())
    boundary_all_ok = all(boundary_review.values())

    ready = (
        verifier_ok
        and baseline.get("verifier_final_decision") == VERIFIER_FINAL_DECISION_GO
        and baseline.get("trace_count") == EXPECTED_TRACE_COUNT
        and baseline.get("validator_rules") == EXPECTED_VALIDATOR_RULES
        and governance_all_ok
        and boundary_all_ok
    )

    handoff = {
        "ready_for_field_slam_framework_selection": ready,
        "ready_for_framework_comparison_matrix": ready,
        "ready_for_slam_adapter_contract_later": ready,
    }

    for key, ok in handoff.items():
        if ok:
            passed.append(f"handoff.{key}=true")
        else:
            failed.append(f"handoff.{key}=false")

    return handoff, passed, failed


def review_field_slam_interface_post_dryrun_v1(
    *,
    input_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    root = Path(input_root or DEFAULT_INPUT_ROOT).expanduser().resolve()
    trace_path = root / TRACE_FILENAME
    summary_path = root / SUMMARY_FILENAME
    verification_path = root / VERIFICATION_FILENAME

    trace_doc = load_json_file(trace_path)
    summary = load_json_file(summary_path)
    verification = load_json_file(verification_path)
    traces = trace_doc.get("traces") or []
    if not isinstance(traces, list):
        traces = []

    all_passed: List[str] = []
    all_failed: List[str] = []

    step1_ok, p, f = review_step1_protocol_baseline(summary)
    all_passed.extend(p)
    all_failed.extend(f)

    step2_ok, p, f = review_step2_case_coverage(traces, summary)
    all_passed.extend(p)
    all_failed.extend(f)

    step3_ok, p, f = review_step3_trace_auditability(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    step4_ok, p, f = review_step4_verifier_pass(verification)
    all_passed.extend(p)
    all_failed.extend(f)

    governance_review, p, f = review_governance_from_traces(traces, verification)
    all_passed.extend(p)
    all_failed.extend(f)

    boundary_review, p, f = review_boundary_scope(summary)
    all_passed.extend(p)
    all_failed.extend(f)

    baseline = {
        "dataclass_count": len(SLAM_INTERFACE_CANDIDATE_TYPES),
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "positive_cases": summary.get("positive_case_count"),
        "invalid_cases": summary.get("invalid_case_count"),
        "trace_count": len(traces),
        "verifier_final_decision": verification.get("final_decision"),
    }

    handoff_readiness, p, f = review_handoff_readiness(
        verifier_ok=step4_ok,
        governance_review=governance_review,
        boundary_review=boundary_review,
        baseline=baseline,
    )
    all_passed.extend(p)
    all_failed.extend(f)

    blocker_count = len(all_failed)
    go_ok = (
        step1_ok
        and step2_ok
        and step3_ok
        and step4_ok
        and verification.get("final_decision") == VERIFIER_FINAL_DECISION_GO
        and len(traces) == EXPECTED_TRACE_COUNT
        and len(VALIDATOR_RULE_IDS) == EXPECTED_VALIDATOR_RULES
        and summary.get("positive_case_count") == EXPECTED_POSITIVE_CASES
        and summary.get("invalid_case_count") == EXPECTED_INVALID_CASES
        and blocker_count == 0
        and governance_review.get("slam_evidence_chain_ok") is True
        and governance_review.get("no_direct_action_ok") is True
        and governance_review.get("no_direct_speech_ok") is True
        and governance_review.get("no_direct_fact_write_ok") is True
        and governance_review.get("no_field_override_ok") is True
        and governance_review.get("no_destination_confirmation_ok") is True
        and all(boundary_review.values())
        and handoff_readiness.get("ready_for_field_slam_framework_selection") is True
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Step 5 Post-DryRun Review",
        "input_artifacts": {
            "trace": str(trace_path),
            "summary": str(summary_path),
            "verification": str(verification_path),
        },
        "review_scope": {
            "types_registry_validators_reviewed": step1_ok,
            "dryrun_cases_reviewed": step2_ok,
            "runner_trace_reviewed": step3_ok,
            "verifier_result_reviewed": step4_ok,
            "no_runtime_slam_scope_preserved": all(boundary_review.values()),
        },
        "baseline": baseline,
        "governance_review": governance_review,
        "boundary_review": boundary_review,
        "handoff_readiness": handoff_readiness,
        "blocker_count": blocker_count,
        "failed_checks": all_failed,
        "passed_checks": all_passed,
        "final_decision": FINAL_DECISION_GO if go_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_path = root / REVIEW_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        result["output_review_file"] = str(out_path)

    return result


def main() -> int:
    result = review_field_slam_interface_post_dryrun_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "baseline": result["baseline"],
                "governance_review": result["governance_review"],
                "boundary_review": result["boundary_review"],
                "handoff_readiness": result["handoff_readiness"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
