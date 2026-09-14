# -*- coding: utf-8 -*-
"""SLAM Spatial Evidence Adapter — Step 3 mapping runner + verify/review (merged)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.dryrun_lifecycle_template_v1 import write_json_file
from capabilities.field_understanding.slam_spatial_evidence_adapter.slam_spatial_evidence_adapter_mapping_cases_v1 import (
    SLAMSpatialEvidenceAdapterMappingCase,
    build_all_mapping_cases_v1,
    bundle_from_slam_spatial_evidence_adapter_mapping_case,
)
from capabilities.field_understanding.slam_spatial_evidence_adapter.slam_spatial_evidence_adapter_static_validators_v1 import (
    validate_slam_spatial_evidence_adapter_mapping_case_bundle,
)
from capabilities.field_understanding.slam_spatial_evidence_adapter.slam_spatial_evidence_adapter_types_v1 import (
    ADAPTER_SKELETON_PRINCIPLE_ZH,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_MAPPING_CASES_READY_FOR_RUNNER,
    FINAL_DECISION_MAPPING_REVIEW_BLOCKED,
    FINAL_DECISION_MAPPING_REVIEW_GO,
    PHASE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "slam_spatial_evidence_adapter_mapping_v1_smoke_v0"
)
OUTPUT_FILENAME = "slam_spatial_evidence_adapter_mapping_run_and_review_v1.json"

EXPECTED_TRACE_COUNT = 8
EXPECTED_POSITIVE_PASS = 5
EXPECTED_INVALID_REJECT = 3

INVALID_CASE_IDS = (
    "invalid_mapping_a_unsupported_candidate_type",
    "invalid_mapping_b_missing_source_chain",
    "invalid_mapping_c_synthesis_entrypoint_bypass",
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


def _mapping_trace(case: SLAMSpatialEvidenceAdapterMappingCase) -> Dict[str, Any]:
    bundle = bundle_from_slam_spatial_evidence_adapter_mapping_case(case)
    actual_ok, errors = validate_slam_spatial_evidence_adapter_mapping_case_bundle(bundle)
    decision = classify_trace_decision(case.expected_validation_ok, actual_ok)
    output_bundle = (bundle.get("output_bundles") or [{}])[0]
    mapping_rules = bundle.get("mapping_rules") or []

    return {
        "case_id": case.case_id,
        "case_name": case.case_name,
        "case_type": case.case_type,
        "case_goal": case.case_goal,
        "adapter_ref": case.adapter_ref,
        "backend_kind": case.backend_kind,
        "expected_candidate_types": list(case.expected_candidate_types),
        "mapping_rules": mapping_rules,
        "adapter": (bundle.get("adapters") or [{}])[0],
        "output_bundle": output_bundle,
        "validation": {
            "expected_validation_ok": case.expected_validation_ok,
            "actual_validation_ok": actual_ok,
            "errors": errors,
        },
        "mapping_checkpoints": {
            "field_synthesis_entrypoint_locked": (
                output_bundle.get("field_synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
            ),
            "source_chain_present": bool(output_bundle.get("source_chain")),
            "candidate_types_mapped": list(output_bundle.get("output_candidate_types") or ()),
        },
        "trace_decision": decision,
    }


def run_and_review_slam_spatial_evidence_adapter_mapping_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    cases = build_all_mapping_cases_v1()
    traces = [_mapping_trace(case) for case in cases]

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

    field_synthesis_locked = all(
        trace.get("mapping_checkpoints", {}).get("field_synthesis_entrypoint_locked") is True
        for trace in traces
        if trace.get("case_type") == "positive"
    )
    source_chain_required = all(
        trace.get("mapping_checkpoints", {}).get("source_chain_present") is True
        for trace in traces
        if trace.get("case_type") == "positive"
    )
    candidate_bundle_mapping_ok = positive_pass == EXPECTED_POSITIVE_PASS

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
    if not field_synthesis_locked:
        failed_checks.append("field_synthesis_entrypoint_locked=false")
    if not source_chain_required:
        failed_checks.append("source_chain_required=false")
    if not candidate_bundle_mapping_ok:
        failed_checks.append("candidate_bundle_mapping_ok=false")
    if not invalid_checks_ok:
        failed_checks.append("invalid_mapping_cases_not_all_rejected")

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
        and field_synthesis_locked
        and source_chain_required
        and candidate_bundle_mapping_ok
        and invalid_checks_ok
        and blocker_count == 0
    )

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Step 3 Mapping Runner + VerifyReview",
        "lifecycle_variant": "compressed_mapping_delta",
        "adapter_skeleton_principle_zh": ADAPTER_SKELETON_PRINCIPLE_ZH,
        "source_cases_final_decision": FINAL_DECISION_MAPPING_CASES_READY_FOR_RUNNER,
        "output_root": str(out_root),
        "output_file": str(out_path),
        "trace_count": len(traces),
        "positive_pass_count": positive_pass,
        "invalid_expected_reject_count": invalid_reject,
        "unexpected_pass_count": unexpected_pass,
        "unexpected_fail_count": unexpected_fail,
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT if field_synthesis_locked else None,
        "source_chain_required": source_chain_required,
        "candidate_bundle_mapping_ok": candidate_bundle_mapping_ok,
        "runner_ok": runner_ok,
        "verification_ok": runner_ok,
        "review_ok": review_ok,
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "traces": traces,
        "trace_decisions": {trace["case_id"]: trace["trace_decision"] for trace in traces},
        "next_phase_hint": "Phase-SLAM-Offline-Real-Backend-Adapter-Trial-v1-001",
        "final_decision": (
            FINAL_DECISION_MAPPING_REVIEW_GO if review_ok else FINAL_DECISION_MAPPING_REVIEW_BLOCKED
        ),
    }

    if write_file:
        write_json_file(out_path, result)

    return result


def main() -> int:
    result = run_and_review_slam_spatial_evidence_adapter_mapping_v1()
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "trace_count": result["trace_count"],
                "positive_pass_count": result["positive_pass_count"],
                "invalid_expected_reject_count": result["invalid_expected_reject_count"],
                "unexpected_pass_count": result["unexpected_pass_count"],
                "unexpected_fail_count": result["unexpected_fail_count"],
                "candidate_bundle_mapping_ok": result["candidate_bundle_mapping_ok"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_MAPPING_REVIEW_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
