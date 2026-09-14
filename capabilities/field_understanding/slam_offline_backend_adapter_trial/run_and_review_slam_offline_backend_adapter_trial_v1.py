# -*- coding: utf-8 -*-
"""SLAM Offline Backend Adapter Trial — Step 3 runner + verify/review (merged)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.dryrun_lifecycle_template_v1 import write_json_file
from capabilities.field_understanding.slam_offline_backend_adapter_trial.slam_offline_backend_adapter_trial_cases_v1 import (
    OfflineSLAMBackendAdapterTrialCase,
    build_all_trial_cases_v1,
    bundle_from_slam_offline_backend_adapter_trial_case,
)
from capabilities.field_understanding.slam_offline_backend_adapter_trial.slam_offline_backend_adapter_trial_static_validators_v1 import (
    validate_slam_offline_backend_adapter_trial_case_bundle,
)
from capabilities.field_understanding.slam_offline_backend_adapter_trial.slam_offline_backend_adapter_trial_types_v1 import (
    ADAPTER_PROFILE_REF,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_CASES_READY_FOR_RUNNER,
    FINAL_DECISION_REVIEW_BLOCKED,
    FINAL_DECISION_REVIEW_GO,
    MODEL_ADMISSION_STANDARD_REF,
    OUTPUT_CANDIDATE_CONTRACT_REF,
    PHASE_ID,
    TRIAL_PRINCIPLE_ZH,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "slam_offline_backend_adapter_trial_v1_smoke_v0"
)
OUTPUT_FILENAME = "slam_offline_backend_adapter_trial_run_and_review_v1.json"

EXPECTED_TRACE_COUNT = 11
EXPECTED_POSITIVE_PASS = 7
EXPECTED_INVALID_REJECT = 4

INVALID_CASE_IDS = (
    "invalid_trial_a_missing_source_chain",
    "invalid_trial_b_adapter_profile_bypass",
    "invalid_trial_c_field_synthesis_bypass",
    "invalid_trial_d_gpl_commercial_runtime_candidate",
)

TraceDecision = Literal["PASS", "EXPECTED_REJECT", "UNEXPECTED_PASS", "UNEXPECTED_FAIL"]


def classify_trace_decision(expected_ok: bool, actual_ok: bool) -> TraceDecision:
    if expected_ok and actual_ok:
        return "PASS"
    if not expected_ok and not actual_ok:
        return "EXPECTED_REJECT"
    if not expected_ok and actual_ok:
        return "UNEXPECTED_PASS"
    return "UNEXPECTED_FAIL"


def _trial_trace(case: OfflineSLAMBackendAdapterTrialCase) -> Dict[str, Any]:
    bundle = bundle_from_slam_offline_backend_adapter_trial_case(case)
    actual_ok, errors = validate_slam_offline_backend_adapter_trial_case_bundle(bundle)
    decision = classify_trace_decision(case.expected_validation_ok, actual_ok)

    output_file = bundle.get("offline_backend_output_file") or {}
    parser = bundle.get("offline_backend_output_parser") or {}
    config = bundle.get("adapter_trial_config") or {}
    parsed = bundle.get("parsed_evidence_bundle") or {}

    return {
        "case_id": case.case_id,
        "case_name": case.case_name,
        "case_type": case.case_type,
        "case_goal": case.case_goal,
        "backend_format_stub": case.backend_format_stub,
        "offline_backend_output_file": output_file,
        "offline_backend_output_parser": parser,
        "adapter_trial_config": config,
        "parsed_evidence_bundle": parsed,
        "validation": {
            "expected_validation_ok": case.expected_validation_ok,
            "actual_validation_ok": actual_ok,
            "errors": errors,
        },
        "trial_checkpoints": {
            "offline_only": (
                output_file.get("offline_only") is True and parser.get("offline_only") is True
            ),
            "parser_declared": bool(parser.get("parser_ref") and parser.get("parser_status")),
            "parsed_evidence_bundle_candidate_only": parsed.get("candidate_only") is True,
            "adapter_profile": config.get("adapter_profile_ref"),
            "output_candidate_contract": config.get("output_candidate_contract_ref"),
            "field_synthesis_entrypoint_locked": (
                parsed.get("field_synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
                and config.get("field_synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
            ),
            "model_admission_standard_ref_present": bool(config.get("model_admission_standard_ref")),
            "source_chain_present": bool(
                output_file.get("source_chain") and parsed.get("source_chain")
            ),
            "commercial_runtime_approved": config.get("commercial_runtime_approved") is True,
        },
        "trace_decision": decision,
    }


def run_and_review_slam_offline_backend_adapter_trial_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    cases = build_all_trial_cases_v1()
    traces = [_trial_trace(case) for case in cases]

    positive_pass = sum(
        1 for trace in traces if trace["case_type"] == "positive" and trace["trace_decision"] == "PASS"
    )
    invalid_reject = sum(
        1
        for trace in traces
        if trace["case_type"] == "invalid" and trace["trace_decision"] == "EXPECTED_REJECT"
    )
    unexpected_pass = sum(1 for trace in traces if trace["trace_decision"] == "UNEXPECTED_PASS")
    unexpected_fail = sum(1 for trace in traces if trace["trace_decision"] == "UNEXPECTED_FAIL")

    positive_traces = [trace for trace in traces if trace.get("case_type") == "positive"]
    offline_only = all(
        trace.get("trial_checkpoints", {}).get("offline_only") is True for trace in positive_traces
    )
    model_admission_binding_ok = all(
        trace.get("trial_checkpoints", {}).get("model_admission_standard_ref_present") is True
        and (trace.get("adapter_trial_config") or {}).get("model_admission_standard_ref")
        == MODEL_ADMISSION_STANDARD_REF
        for trace in positive_traces
    )
    adapter_mapping_entrypoint_ok = all(
        trace.get("trial_checkpoints", {}).get("adapter_profile") == ADAPTER_PROFILE_REF
        and trace.get("trial_checkpoints", {}).get("output_candidate_contract")
        == OUTPUT_CANDIDATE_CONTRACT_REF
        for trace in positive_traces
    )
    field_synthesis_locked = all(
        trace.get("trial_checkpoints", {}).get("field_synthesis_entrypoint_locked") is True
        for trace in positive_traces
    )
    commercial_runtime_approved = any(
        trace.get("trial_checkpoints", {}).get("commercial_runtime_approved") is True
        for trace in traces
    )

    invalid_checks_ok = all(
        any(trace["case_id"] == case_id and trace["trace_decision"] == "EXPECTED_REJECT" for trace in traces)
        for case_id in INVALID_CASE_IDS
    )

    failed_checks: List[str] = []
    if len(traces) != EXPECTED_TRACE_COUNT:
        failed_checks.append(f"trace_count:{len(traces)}")
    if positive_pass != EXPECTED_POSITIVE_PASS:
        failed_checks.append(f"positive_pass_count:{positive_pass}")
    if invalid_reject != EXPECTED_INVALID_REJECT:
        failed_checks.append(f"invalid_expected_reject_count:{invalid_reject}")
    if unexpected_pass != 0:
        failed_checks.append(f"unexpected_pass_count:{unexpected_pass}")
    if unexpected_fail != 0:
        failed_checks.append(f"unexpected_fail_count:{unexpected_fail}")
    if not offline_only:
        failed_checks.append("offline_only=false")
    if not model_admission_binding_ok:
        failed_checks.append("model_admission_binding_ok=false")
    if not adapter_mapping_entrypoint_ok:
        failed_checks.append("adapter_mapping_entrypoint_ok=false")
    if not field_synthesis_locked:
        failed_checks.append("field_synthesis_entrypoint_locked=false")
    if commercial_runtime_approved:
        failed_checks.append("commercial_runtime_approved=true")
    if not invalid_checks_ok:
        failed_checks.append("invalid_trial_cases_not_all_rejected")

    blocker_count = len(failed_checks)
    runner_ok = (
        len(traces) == EXPECTED_TRACE_COUNT
        and positive_pass == EXPECTED_POSITIVE_PASS
        and invalid_reject == EXPECTED_INVALID_REJECT
        and unexpected_pass == 0
        and unexpected_fail == 0
    )
    review_ok = (
        runner_ok
        and offline_only
        and model_admission_binding_ok
        and adapter_mapping_entrypoint_ok
        and field_synthesis_locked
        and not commercial_runtime_approved
        and invalid_checks_ok
        and blocker_count == 0
    )

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Step 3 Offline Trial Runner + VerifyReview",
        "lifecycle_variant": "compressed_offline_backend_adapter_trial",
        "trial_principle_zh": TRIAL_PRINCIPLE_ZH,
        "source_cases_final_decision": FINAL_DECISION_CASES_READY_FOR_RUNNER,
        "output_root": str(out_root),
        "output_file": str(out_path),
        "trace_count": len(traces),
        "positive_pass_count": positive_pass,
        "invalid_expected_reject_count": invalid_reject,
        "unexpected_pass_count": unexpected_pass,
        "unexpected_fail_count": unexpected_fail,
        "offline_only": offline_only,
        "model_admission_binding_ok": model_admission_binding_ok,
        "adapter_mapping_entrypoint_ok": adapter_mapping_entrypoint_ok,
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT if field_synthesis_locked else None,
        "commercial_runtime_approved": commercial_runtime_approved,
        "runner_ok": runner_ok,
        "verification_ok": runner_ok,
        "review_ok": review_ok,
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "traces": traces,
        "trace_decisions": {trace["case_id"]: trace["trace_decision"] for trace in traces},
        "next_phase_hint": (
            "Minimal real offline parser trial — prefer generic_tum_trajectory_stub "
            "or generic_json_spatial_trace_stub"
        ),
        "final_decision": (
            FINAL_DECISION_REVIEW_GO if review_ok else FINAL_DECISION_REVIEW_BLOCKED
        ),
    }

    if write_file:
        write_json_file(out_path, result)

    return result


def main() -> int:
    result = run_and_review_slam_offline_backend_adapter_trial_v1()
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "trace_count": result["trace_count"],
                "positive_pass_count": result["positive_pass_count"],
                "invalid_expected_reject_count": result["invalid_expected_reject_count"],
                "unexpected_pass_count": result["unexpected_pass_count"],
                "unexpected_fail_count": result["unexpected_fail_count"],
                "model_admission_binding_ok": result["model_admission_binding_ok"],
                "adapter_mapping_entrypoint_ok": result["adapter_mapping_entrypoint_ok"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_REVIEW_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
