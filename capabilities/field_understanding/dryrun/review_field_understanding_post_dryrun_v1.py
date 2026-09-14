# -*- coding: utf-8 -*-
"""Field-Oriented Egocentric Action Understanding — post-dryrun review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.core.field_understanding_registry_v1 import (
    FIELD_SYNTHESIS_CHAIN,
    PROHIBITED_FIELD_REVISION_POLICIES,
    PROHIBITED_FIELD_TYPES_FROM_ISOLATED_FACT,
)
from capabilities.field_understanding.core.field_understanding_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
)
from capabilities.field_understanding.core.field_understanding_types_v1 import (
    FIELD_CONTEXT_GOVERNANCE_ID,
    FIELD_INFORMATION_PRIORITY_GOVERNANCE_ID,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
)

DEFAULT_INPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_understanding_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "field_understanding_dryrun_trace_v1.json"
SUMMARY_FILENAME = "field_understanding_dryrun_summary_v1.json"
VERIFICATION_FILENAME = "field_understanding_dryrun_verification_v1.json"
REVIEW_FILENAME = "field_understanding_post_dryrun_review_v1.json"

VERIFIER_FINAL_DECISION_GO = "FIELD_UNDERSTANDING_DRYRUN_VERIFIER_GO"
FINAL_DECISION_GO = "FIELD_UNDERSTANDING_POST_DRYRUN_REVIEW_GO"
FINAL_DECISION_BLOCKED = "FIELD_UNDERSTANDING_POST_DRYRUN_REVIEW_BLOCKED"

EXPECTED_VALIDATOR_RULES = 22
EXPECTED_POSITIVE_CASES = 10
EXPECTED_INVALID_CASES = 5
EXPECTED_TRACE_COUNT = 15

CASE_9_ID = "case_09_user_exit_fact_influences_field"
CASE_10_ID = "case_10_metro_train_display_influences_field_state"

EXPECTED_POSITIVE_CASE_IDS = frozenset(
    {
        "case_01_corridor_door_anchor",
        "case_02_elevator_lobby_alignment",
        "case_03_temporary_box_obstacle",
        "case_04_metro_crowd_density",
        "case_05_map_exit_not_observed",
        "case_06_night_street_low_visibility",
        "case_07_memory_anchor_door",
        "case_08_crosswalk_vehicle_risk",
        CASE_9_ID,
        CASE_10_ID,
    }
)
EXPECTED_INVALID_CASE_IDS = frozenset(
    {
        "invalid_a_dynamic_box_in_static",
        "invalid_b_aligned_without_anchors",
        "invalid_c_near_zone_without_sources",
        "invalid_d_fact_overrides_field",
        "invalid_e_fact_action_without_field_context",
    }
)

STEP1_CORE_FILES = (
    "capabilities/field_understanding/core/field_understanding_types_v1.py",
    "capabilities/field_understanding/core/field_understanding_registry_v1.py",
    "capabilities/field_understanding/core/field_understanding_static_validators_v1.py",
    "capabilities/field_understanding/dryrun/field_understanding_dryrun_cases_v1.py",
    "capabilities/field_understanding/dryrun/run_field_understanding_dryrun_v1.py",
    "capabilities/field_understanding/dryrun/verify_field_understanding_dryrun_v1.py",
)

REQUIRED_TRACE_SECTIONS = (
    "field_context",
    "governance_chain",
    "governance_checkpoints",
    "static_dynamic_split",
    "semantic_governance",
    "fact_influence_governance",
    "map_alignment",
    "action_distance",
    "fusion",
    "validation",
    "trace_decision",
)

BOUNDARY_MODULE_SCAN_PATTERNS = (
    "graph_eqa",
    "speech_gate",
    "slam_runtime",
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


def review_step1_protocol_baseline(
    summary: Dict[str, Any],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    for rel in STEP1_CORE_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed.append(f"step1.core_file_present={rel.split('/')[-1]}")
        else:
            failed.append(f"step1.core_file_missing={rel}")

    rule_count = len(VALIDATOR_RULE_IDS)
    if rule_count == EXPECTED_VALIDATOR_RULES:
        passed.append(f"step1.validator_rules={EXPECTED_VALIDATOR_RULES}")
    else:
        failed.append(
            f"step1.validator_rules: expected={EXPECTED_VALIDATOR_RULES}, actual={rule_count}"
        )

    gov = summary.get("governance_ids") or {}
    if gov.get("field_information_priority") == FIELD_INFORMATION_PRIORITY_GOVERNANCE_ID:
        passed.append("step1.field_information_priority_governance_id_ok=true")
    else:
        failed.append("step1.field_information_priority_governance_id_mismatch")

    if gov.get("field_context_governance") == FIELD_CONTEXT_GOVERNANCE_ID:
        passed.append("step1.field_context_governance_id_ok=true")
    else:
        failed.append("step1.field_context_governance_id_mismatch")

    expected_chain = list(FIELD_SYNTHESIS_CHAIN)
    if len(expected_chain) == 6:
        passed.append("step1.field_synthesis_chain_registered=true")
    else:
        failed.append("step1.field_synthesis_chain_incomplete")

    return len(failed) == 0, passed, failed


def review_step2_case_coverage(
    traces: List[Dict[str, Any]],
    summary: Dict[str, Any],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    case_ids = {t.get("case_id") for t in traces}
    positive_ids = {t.get("case_id") for t in traces if t.get("case_type") == "positive"}
    invalid_ids = {t.get("case_id") for t in traces if t.get("case_type") == "invalid"}

    missing_positive = EXPECTED_POSITIVE_CASE_IDS - positive_ids
    missing_invalid = EXPECTED_INVALID_CASE_IDS - invalid_ids
    if not missing_positive:
        passed.append("step2.positive_case_coverage_complete=true")
    else:
        failed.append(f"step2.missing_positive_cases={sorted(missing_positive)!r}")

    if not missing_invalid:
        passed.append("step2.invalid_case_coverage_complete=true")
    else:
        failed.append(f"step2.missing_invalid_cases={sorted(missing_invalid)!r}")

    if summary.get("positive_case_count") == EXPECTED_POSITIVE_CASES:
        passed.append(f"step2.positive_case_count={EXPECTED_POSITIVE_CASES}")
    else:
        failed.append("step2.positive_case_count_mismatch")

    if summary.get("invalid_case_count") == EXPECTED_INVALID_CASES:
        passed.append(f"step2.invalid_case_count={EXPECTED_INVALID_CASES}")
    else:
        failed.append("step2.invalid_case_count_mismatch")

    scenario_checks = {
        "case_03_temporary_box_obstacle": "dynamic_ttl",
        "case_05_map_exit_not_observed": "map_not_confirmed_as_fact",
        "invalid_a_dynamic_box_in_static": "static_dynamic_split",
        "invalid_b_aligned_without_anchors": "map_alignment_anchors",
        "invalid_c_near_zone_without_sources": "action_distance_sources",
        "invalid_d_fact_overrides_field": "fact_override_blocked",
        "invalid_e_fact_action_without_field_context": "field_context_before_fact",
    }
    for case_id, label in scenario_checks.items():
        trace = _trace_by_id(traces, case_id)
        if trace is None:
            failed.append(f"step2.scenario_missing={case_id}")
            continue
        decision = trace.get("trace_decision")
        expected = "PASS" if case_id.startswith("case_") else "EXPECTED_REJECT"
        if decision == expected:
            passed.append(f"step2.scenario_{label}={case_id}:{decision}")
        else:
            failed.append(f"step2.scenario_{label}={case_id}:expected={expected},actual={decision}")

    return len(failed) == 0, passed, failed


def review_step3_trace_auditability(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    if len(traces) != EXPECTED_TRACE_COUNT:
        failed.append(
            f"step3.trace_count: expected={EXPECTED_TRACE_COUNT}, actual={len(traces)}"
        )
    else:
        passed.append(f"step3.trace_count={EXPECTED_TRACE_COUNT}")

    for trace in traces:
        case_id = trace.get("case_id", "<unknown>")
        missing = [s for s in REQUIRED_TRACE_SECTIONS if s not in trace]
        if missing:
            failed.append(f"step3.{case_id}.missing_sections={missing}")
            continue

        checkpoints = trace.get("governance_checkpoints") or {}
        if not isinstance(checkpoints, dict) or not checkpoints:
            failed.append(f"step3.{case_id}.governance_checkpoints_empty")
            continue

        if trace.get("governance_chain") == list(FIELD_SYNTHESIS_CHAIN):
            passed.append(f"step3.{case_id}.governance_chain_auditable=true")
        else:
            failed.append(f"step3.{case_id}.governance_chain_not_auditable")

    return len(failed) == 0, passed, failed


def review_step4_verifier_pass(
    verification: Dict[str, Any],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    final_decision = verification.get("final_decision")
    if final_decision == VERIFIER_FINAL_DECISION_GO:
        passed.append(f"step4.verifier_final_decision={VERIFIER_FINAL_DECISION_GO}")
    else:
        failed.append(f"step4.verifier_final_decision={final_decision!r}")

    if verification.get("blocker_count") == 0:
        passed.append("step4.verifier_blocker_count=0")
    else:
        failed.append(f"step4.verifier_blocker_count={verification.get('blocker_count')!r}")

    verifier_checks = (
        "summary_check_ok",
        "trace_count_check_ok",
        "case_id_unique_check_ok",
        "trace_decision_check_ok",
        "governance_checkpoint_check_ok",
        "case_9_governance_check_ok",
        "case_10_governance_check_ok",
    )
    for key in verifier_checks:
        if verification.get(key) is True:
            passed.append(f"step4.{key}=true")
        else:
            failed.append(f"step4.{key}={verification.get(key)!r}")

    return len(failed) == 0, passed, failed


def review_governance_from_traces(
    traces: List[Dict[str, Any]],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    positive_traces = [t for t in traces if t.get("case_type") == "positive"]

    field_info_ok = True
    for trace in positive_traces:
        case_id = trace.get("case_id", "<unknown>")
        chain = trace.get("governance_chain") or []
        if chain != list(FIELD_SYNTHESIS_CHAIN):
            field_info_ok = False
            failed.append(f"governance.{case_id}.synthesis_chain_bypassed")
        policy = (trace.get("fact_influence_governance") or {}).get("field_revision_policy")
        if policy in PROHIBITED_FIELD_REVISION_POLICIES:
            field_info_ok = False
            failed.append(f"governance.{case_id}.prohibited_policy={policy!r}")
    if field_info_ok:
        passed.append("governance.field_information_priority_governance_ok=true")

    field_context_ok = all(
        (t.get("field_context") or {}).get("field_context_resolved") is True
        for t in positive_traces
    )
    if field_context_ok:
        passed.append("governance.field_context_governance_ok=true")
    else:
        failed.append("governance.field_context_not_resolved_on_positive_traces")

    fact_influence_ok = all(
        (t.get("fact_influence_governance") or {}).get("direct_override_blocked") is True
        for t in positive_traces
    )
    if fact_influence_ok:
        passed.append("governance.fact_influence_without_override_ok=true")
    else:
        failed.append("governance.fact_influence_override_not_blocked")

    static_dynamic_ok = all(
        (t.get("governance_checkpoints") or {}).get("static_dynamic_not_mixed") is True
        for t in positive_traces
    )
    invalid_a = _trace_by_id(traces, "invalid_a_dynamic_box_in_static")
    if static_dynamic_ok and invalid_a and invalid_a.get("trace_decision") == "EXPECTED_REJECT":
        passed.append("governance.static_dynamic_split_ok=true")
    else:
        failed.append("governance.static_dynamic_split_not_verified")

    map_ok = all(
        (t.get("governance_checkpoints") or {}).get("map_aligned_requires_anchors") is True
        for t in positive_traces
    )
    invalid_b = _trace_by_id(traces, "invalid_b_aligned_without_anchors")
    case_05 = _trace_by_id(traces, "case_05_map_exit_not_observed")
    if (
        map_ok
        and invalid_b
        and invalid_b.get("trace_decision") == "EXPECTED_REJECT"
        and case_05
        and case_05.get("trace_decision") == "PASS"
    ):
        passed.append("governance.map_candidate_not_fact_ok=true")
    else:
        failed.append("governance.map_candidate_governance_not_verified")

    distance_ok = all(
        (t.get("action_distance") or {}).get("precise_distance_exposed_to_speech") is False
        and (t.get("governance_checkpoints") or {}).get("precise_distance_blocked_for_speech") is True
        for t in positive_traces
    )
    invalid_c = _trace_by_id(traces, "invalid_c_near_zone_without_sources")
    if distance_ok and invalid_c and invalid_c.get("trace_decision") == "EXPECTED_REJECT":
        passed.append("governance.action_distance_not_precise_speech_ok=true")
    else:
        failed.append("governance.action_distance_governance_not_verified")

    governance_review = {
        "field_information_priority_governance_ok": field_info_ok,
        "field_context_governance_ok": field_context_ok,
        "fact_influence_without_override_ok": fact_influence_ok,
        "static_dynamic_split_ok": static_dynamic_ok
        and bool(invalid_a and invalid_a.get("trace_decision") == "EXPECTED_REJECT"),
        "map_candidate_not_fact_ok": map_ok
        and bool(invalid_b and invalid_b.get("trace_decision") == "EXPECTED_REJECT"),
        "action_distance_not_precise_speech_ok": distance_ok
        and bool(invalid_c and invalid_c.get("trace_decision") == "EXPECTED_REJECT"),
    }
    return governance_review, passed, failed


def review_case_9_and_10(
    traces: List[Dict[str, Any]],
    verification: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    case_9 = _trace_by_id(traces, CASE_9_ID)
    case_10 = _trace_by_id(traces, CASE_10_ID)

    case_9_ok = verification.get("case_9_governance_check_ok") is True
    if case_9:
        fig = case_9.get("fact_influence_governance") or {}
        fusion = case_9.get("fusion") or {}
        checks = [
            fig.get("field_revision_policy") == "influence_only",
            fig.get("fact_influence_level") == "strong",
            "field_attention" in (fig.get("affected_field_dimensions") or []),
            fusion.get("action_readiness") == "needs_more_observation",
            fig.get("field_revision_policy") not in PROHIBITED_FIELD_REVISION_POLICIES,
            (case_9.get("field_context") or {}).get("field_type") != "confirmed_exit_field",
        ]
        case_9_ok = case_9_ok and all(checks)
        if case_9_ok:
            passed.append("case_review.case_9_fact_influence_review_ok=true")
        else:
            failed.append("case_review.case_9_governance_trace_mismatch")
    else:
        failed.append("case_review.case_9_missing")
        case_9_ok = False

    case_10_ok = verification.get("case_10_governance_check_ok") is True
    if case_10:
        field_ctx = case_10.get("field_context") or {}
        fig = case_10.get("fact_influence_governance") or {}
        dims = set(fig.get("affected_field_dimensions") or [])
        checks = [
            field_ctx.get("field_type") == "metro_station",
            field_ctx.get("field_type") != "display_screen",
            fig.get("fact_influence_level") == "strong",
            {"field_action_logic", "field_state", "field_task_relevance"}.issubset(dims),
            fig.get("field_type_preserved") is True,
        ]
        case_10_ok = case_10_ok and all(checks)
        if case_10_ok:
            passed.append("case_review.case_10_field_context_review_ok=true")
        else:
            failed.append("case_review.case_10_governance_trace_mismatch")
    else:
        failed.append("case_review.case_10_missing")
        case_10_ok = False

    return {
        "case_9_fact_influence_review_ok": case_9_ok,
        "case_10_field_context_review_ok": case_10_ok,
    }, passed, failed


def review_boundary_scope(
    summary: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    flags = summary.get("non_execution_flags") or {}
    expected_flags = dict(NON_EXECUTION_FLAGS)
    boundary = {
        "model_not_connected": flags.get("no_model_execution") is True,
        "slam_not_connected": flags.get("no_slam_execution") is True,
        "camera_not_connected": flags.get("no_camera_runtime") is True,
        "graph_eqa_not_connected": True,
        "speech_gate_not_connected": flags.get("no_speech_output") is True,
        "fact_layer_not_written": flags.get("no_fact_layer_write") is True,
    }

    for key, expected in expected_flags.items():
        actual = flags.get(key)
        if actual is expected:
            passed.append(f"boundary.non_execution_flag.{key}={actual}")
        else:
            failed.append(f"boundary.non_execution_flag.{key}: expected={expected!r}, actual={actual!r}")
            if key == "no_model_execution":
                boundary["model_not_connected"] = False
            elif key == "no_slam_execution":
                boundary["slam_not_connected"] = False
            elif key == "no_camera_runtime":
                boundary["camera_not_connected"] = False
            elif key == "no_speech_output":
                boundary["speech_gate_not_connected"] = False
            elif key == "no_fact_layer_write":
                boundary["fact_layer_not_written"] = False

    module_root = _REPO_ROOT / "capabilities" / "field_understanding"
    for py_path in module_root.rglob("*.py"):
        if py_path.name == "review_field_understanding_post_dryrun_v1.py":
            continue
        text = py_path.read_text(encoding="utf-8").lower()
        for pattern in BOUNDARY_MODULE_SCAN_PATTERNS:
            if pattern == "graph_eqa" and pattern in text:
                if "observe" in text or "观察" in text:
                    continue
                boundary["graph_eqa_not_connected"] = False
                failed.append(f"boundary.graph_eqa_runtime_reference_in={py_path.name}")

    if boundary["graph_eqa_not_connected"]:
        passed.append("boundary.graph_eqa_not_connected=true")

    return boundary, passed, failed


def review_handoff_readiness(
    *,
    verifier_ok: bool,
    governance_review: Dict[str, bool],
    case_review: Dict[str, bool],
    boundary_review: Dict[str, bool],
    baseline: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    governance_all_ok = all(governance_review.values())
    boundary_all_ok = all(boundary_review.values())
    case_all_ok = all(case_review.values())

    ready_for_slam = (
        verifier_ok
        and baseline.get("verifier_final_decision") == VERIFIER_FINAL_DECISION_GO
        and baseline.get("trace_count") == EXPECTED_TRACE_COUNT
        and baseline.get("validator_rules") == EXPECTED_VALIDATOR_RULES
        and governance_all_ok
        and boundary_all_ok
        and case_all_ok
    )

    handoff = {
        "ready_for_slam_interface_contract": ready_for_slam,
        "ready_for_midplatform_candidate_governance_mapping": ready_for_slam,
        "ready_for_post_review_closure": ready_for_slam,
    }

    for key, ok in handoff.items():
        if ok:
            passed.append(f"handoff.{key}=true")
        else:
            failed.append(f"handoff.{key}=false")

    return handoff, passed, failed


def review_field_understanding_post_dryrun_v1(
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

    governance_review, p, f = review_governance_from_traces(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    case_review, p, f = review_case_9_and_10(traces, verification)
    all_passed.extend(p)
    all_failed.extend(f)

    boundary_review, p, f = review_boundary_scope(summary)
    all_passed.extend(p)
    all_failed.extend(f)

    baseline = {
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "positive_cases": summary.get("positive_case_count"),
        "invalid_cases": summary.get("invalid_case_count"),
        "trace_count": len(traces),
        "verifier_final_decision": verification.get("final_decision"),
    }

    handoff_readiness, p, f = review_handoff_readiness(
        verifier_ok=step4_ok,
        governance_review=governance_review,
        case_review=case_review,
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
        and governance_review.get("field_information_priority_governance_ok") is True
        and governance_review.get("field_context_governance_ok") is True
        and all(boundary_review.values())
        and handoff_readiness.get("ready_for_slam_interface_contract") is True
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
            "no_runtime_model_scope_preserved": all(boundary_review.values()),
        },
        "baseline": baseline,
        "governance_review": governance_review,
        "case_review": case_review,
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
    result = review_field_understanding_post_dryrun_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "baseline": result["baseline"],
                "governance_review": result["governance_review"],
                "case_review": result["case_review"],
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
