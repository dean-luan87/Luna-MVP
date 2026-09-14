# -*- coding: utf-8 -*-
"""Model Admission Governance Standard — Step 3 run + review (merged)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.dryrun_lifecycle_template_v1 import write_json_file
from capabilities.midplatform.model_admission_governance.model_admission_governance_cases_v1 import (
    ModelAdmissionGovernanceCase,
    build_all_model_admission_governance_cases_v1,
    bundle_from_model_admission_governance_case,
)
from capabilities.midplatform.model_admission_governance.model_admission_governance_static_validators_v1 import (
    validate_model_admission_governance_case_bundle,
)
from capabilities.midplatform.model_admission_governance.model_admission_governance_types_v1 import (
    ADMISSION_GOVERNANCE_PRINCIPLE_ZH,
    DRYRUN_LIFECYCLE_TEMPLATE_REF,
    FINAL_DECISION_CASES_READY_FOR_RUNNER,
    FINAL_DECISION_STANDARD_REVIEW_BLOCKED,
    FINAL_DECISION_STANDARD_REVIEW_GO,
    PHASE_ID,
    SHARED_ADMISSION_LIFECYCLE_CHAIN,
)

DEFAULT_OUTPUT_ROOT = _REPO_ROOT / "_tmp_eval_out" / "model_admission_governance_v1_smoke_v0"
OUTPUT_FILENAME = "model_admission_governance_run_and_review_v1.json"

EXPECTED_TRACE_COUNT = 10
EXPECTED_POSITIVE_PASS = 6
EXPECTED_INVALID_REJECT = 4

INVALID_CASE_IDS = (
    "invalid_a_model_bypasses_registry",
    "invalid_b_model_bypasses_license_gate",
    "invalid_c_domain_specific_lifecycle_override",
    "invalid_d_update_replace_remove_missing_lineage",
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


def _admission_trace(case: ModelAdmissionGovernanceCase) -> Dict[str, Any]:
    bundle = bundle_from_model_admission_governance_case(case)
    actual_ok, errors = validate_model_admission_governance_case_bundle(bundle)
    decision = classify_trace_decision(case.expected_validation_ok, actual_ok)

    return {
        "case_id": case.case_id,
        "case_name": case.case_name,
        "case_type": case.case_type,
        "case_goal": case.case_goal,
        "model_id": case.model_id,
        "model_family": case.model_family,
        "domain_id": case.domain_id,
        "adapter_profile_ref": case.adapter_profile_ref,
        "model_operation": case.model_operation,
        "registry_entry": bundle.get("registry_entry"),
        "capability_profile": bundle.get("capability_profile"),
        "license_gate": bundle.get("license_gate"),
        "adapter_contract_ref": bundle.get("adapter_contract_ref"),
        "provider_admission_ref": bundle.get("provider_admission_ref"),
        "runtime_governance_ref": bundle.get("runtime_governance_ref"),
        "admission_checkpoints": {
            "shared_lifecycle_required": (
                bundle.get("model_admission_standard", {}).get("domain_specific_lifecycle_forbidden")
                is True
            ),
            "domain_specific_lifecycle_forbidden": not bundle.get(
                "domain_specific_lifecycle_override", False
            ),
            "lineage_present_or_not_required": (
                case.model_operation == "add_model"
                or bool((bundle.get("registry_entry") or {}).get("lineage_ref"))
            ),
            "runtime_enabled_default_false": (
                (bundle.get("registry_entry") or {}).get("runtime_enabled_default") is False
            ),
            "commercial_runtime_approved_default_false": (
                (bundle.get("registry_entry") or {}).get("commercial_runtime_approved") is False
            ),
        },
        "validation": {
            "expected_validation_ok": case.expected_validation_ok,
            "actual_validation_ok": actual_ok,
            "errors": errors,
        },
        "trace_decision": decision,
    }


def run_and_review_model_admission_governance_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    cases = build_all_model_admission_governance_cases_v1()
    traces = [_admission_trace(case) for case in cases]

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
    if not invalid_checks_ok:
        failed_checks.append("invalid_cases_not_all_rejected")

    blocker_count = len(failed_checks)
    runner_ok = (
        len(traces) == EXPECTED_TRACE_COUNT
        and positive_pass == EXPECTED_POSITIVE_PASS
        and invalid_reject == EXPECTED_INVALID_REJECT
        and unexpected_pass == 0
        and unexpected_fail == 0
    )
    review_ok = runner_ok and invalid_checks_ok and blocker_count == 0

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Step 3 Model Admission Governance Run + Review",
        "lifecycle_variant": "compressed",
        "admission_governance_principle_zh": ADMISSION_GOVERNANCE_PRINCIPLE_ZH,
        "source_cases_final_decision": FINAL_DECISION_CASES_READY_FOR_RUNNER,
        "model_admission_standard_ref": PHASE_ID,
        "dryrun_lifecycle_template_ref": DRYRUN_LIFECYCLE_TEMPLATE_REF,
        "shared_lifecycle_chain": list(SHARED_ADMISSION_LIFECYCLE_CHAIN),
        "output_root": str(out_root),
        "output_file": str(out_path),
        "trace_count": len(traces),
        "positive_pass_count": positive_pass,
        "invalid_expected_reject_count": invalid_reject,
        "unexpected_pass_count": unexpected_pass,
        "unexpected_fail_count": unexpected_fail,
        "runner_ok": runner_ok,
        "verification_ok": runner_ok,
        "review_ok": review_ok,
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "traces": traces,
        "trace_decisions": {trace["case_id"]: trace["trace_decision"] for trace in traces},
        "next_phase_hint": "Phase-SLAM-Offline-Real-Backend-Adapter-Trial-v1-001",
        "slam_offline_trial_binding": {
            "model_id": "sample_slam_spatial_evidence_model",
            "model_family": "slam",
            "domain_id": "spatial_evidence",
            "adapter_profile": "slam_spatial_evidence_adapter",
            "model_admission_standard_ref": PHASE_ID,
        },
        "final_decision": (
            FINAL_DECISION_STANDARD_REVIEW_GO if review_ok else FINAL_DECISION_STANDARD_REVIEW_BLOCKED
        ),
    }

    if write_file:
        write_json_file(out_path, result)

    return result


def main() -> int:
    result = run_and_review_model_admission_governance_v1()
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "trace_count": result["trace_count"],
                "positive_pass_count": result["positive_pass_count"],
                "invalid_expected_reject_count": result["invalid_expected_reject_count"],
                "unexpected_pass_count": result["unexpected_pass_count"],
                "unexpected_fail_count": result["unexpected_fail_count"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_STANDARD_REVIEW_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
