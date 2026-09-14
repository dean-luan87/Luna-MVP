# -*- coding: utf-8 -*-
"""Phase-DryRun-Lifecycle-Adoption-Scanner-Review-v1-001 — read-only baseline review."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.dryrun_lifecycle_template_v1 import (
    load_json_file,
    write_json_file,
)
from capabilities.midplatform.core.scan_dryrun_lifecycle_adoption_v1 import (
    FINAL_DECISION_READY as SOURCE_FINAL_DECISION_READY,
    PHASE_ID as SOURCE_PHASE_ID,
)

PHASE_ID = "Phase-DryRun-Lifecycle-Adoption-Scanner-Review-v1-001"
SCOPE = "dryrun_lifecycle_adoption_scan_review_read_only"

FINAL_DECISION_BASELINE_GO = "DRYRUN_LIFECYCLE_ADOPTION_SCANNER_BASELINE_GO"
FINAL_DECISION_BASELINE_BLOCKED = "DRYRUN_LIFECYCLE_ADOPTION_SCANNER_BASELINE_BLOCKED"

DEFAULT_INPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "dryrun_lifecycle_adoption_scan_v1_smoke_v0"
)
SCAN_FILENAME = "dryrun_lifecycle_adoption_scan_v1.json"
REVIEW_FILENAME = "dryrun_lifecycle_adoption_scan_review_v1.json"

EXPECTED_ADOPTION_POLICY: Dict[str, str] = {
    "planning_only_candidate_only": "compressed_default",
    "matrix_binding_selection": "matrix_default",
    "high_risk_execution_repair_authorization": "keep_full_or_custom",
    "sealed_go_history": "no_retrofit",
}


def _verify_adoption_policy(policy: Any) -> tuple[bool, List[str]]:
    failed: List[str] = []
    if not isinstance(policy, dict):
        return False, ["adoption_policy.missing_or_not_dict"]

    for key, expected in EXPECTED_ADOPTION_POLICY.items():
        actual = policy.get(key)
        if actual != expected:
            failed.append(f"adoption_policy.{key}: expected={expected!r}, actual={actual!r}")

    return len(failed) == 0, failed


def _category_present(scan: Mapping[str, Any], key: str) -> bool:
    counts = scan.get("category_counts") or {}
    if isinstance(counts, dict) and counts.get(key, 0) >= 1:
        return True
    categories = scan.get("categories") or {}
    if isinstance(categories, dict):
        items = categories.get(key)
        return isinstance(items, list) and len(items) >= 1
    return False


def review_dryrun_lifecycle_adoption_scan_v1(
    *,
    input_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    root = Path(input_root or DEFAULT_INPUT_ROOT).expanduser().resolve()
    scan_path = root / SCAN_FILENAME
    scan = load_json_file(scan_path)

    failed_checks: List[str] = []

    scan_ok = scan.get("scan_ok") is True
    if not scan_ok:
        failed_checks.append("scan_ok=false")

    source_final_decision = scan.get("final_decision")
    if source_final_decision != SOURCE_FINAL_DECISION_READY:
        failed_checks.append(
            f"source_final_decision: expected={SOURCE_FINAL_DECISION_READY!r}, "
            f"actual={source_final_decision!r}"
        )

    template_file_present = scan.get("template_file_present") is True
    if not template_file_present:
        failed_checks.append("template_file_present=false")

    full_split_pairs = scan.get("full_split_pairs_detected", 0)
    if not isinstance(full_split_pairs, int) or full_split_pairs < 1:
        failed_checks.append(f"full_split_pairs_detected: expected>=1, actual={full_split_pairs!r}")

    compressed_files = scan.get("compressed_files_detected", 0)
    if not isinstance(compressed_files, int) or compressed_files < 1:
        failed_checks.append(f"compressed_files_detected: expected>=1, actual={compressed_files!r}")

    matrix_files = scan.get("matrix_files_detected", 0)
    if not isinstance(matrix_files, int) or matrix_files < 1:
        failed_checks.append(f"matrix_files_detected: expected>=1, actual={matrix_files!r}")

    adoption_policy_complete, policy_failed = _verify_adoption_policy(scan.get("adoption_policy"))
    failed_checks.extend(policy_failed)

    unknown_needs_review_allowed = True
    unknown_count = (scan.get("category_counts") or {}).get("unknown_needs_review", 0)
    if not isinstance(unknown_count, int) or unknown_count < 0:
        failed_checks.append(f"unknown_needs_review_count_invalid: {unknown_count!r}")

    classification_review = {
        "frozen_full_no_retrofit_present": _category_present(scan, "frozen_full_no_retrofit"),
        "compressed_template_adopted_present": _category_present(scan, "compressed_template_adopted"),
        "matrix_touch_to_align_present": _category_present(scan, "matrix_touch_to_align"),
        "controlled_skeleton_merge_on_touch_present": _category_present(
            scan, "controlled_skeleton_merge_on_touch"
        ),
        "keep_full_or_custom_present": _category_present(scan, "keep_full_or_custom"),
        "unknown_needs_review_allowed": unknown_needs_review_allowed,
    }

    for key, ok in classification_review.items():
        if key == "unknown_needs_review_allowed":
            continue
        if not ok:
            failed_checks.append(f"classification_review.{key}=false")

    adoption_policy_review = {
        "planning_candidate_only_default_compressed": (
            (scan.get("adoption_policy") or {}).get("planning_only_candidate_only")
            == "compressed_default"
        ),
        "matrix_binding_selection_default_matrix": (
            (scan.get("adoption_policy") or {}).get("matrix_binding_selection") == "matrix_default"
        ),
        "high_risk_execution_repair_authorization_keep_full_or_custom": (
            (scan.get("adoption_policy") or {}).get("high_risk_execution_repair_authorization")
            == "keep_full_or_custom"
        ),
        "go_history_no_retrofit": (
            (scan.get("adoption_policy") or {}).get("sealed_go_history") == "no_retrofit"
        ),
    }

    for key, ok in adoption_policy_review.items():
        if not ok:
            failed_checks.append(f"adoption_policy_review.{key}=false")

    blocker_count = len(failed_checks)
    go_ok = (
        scan_ok
        and source_final_decision == SOURCE_FINAL_DECISION_READY
        and template_file_present
        and isinstance(full_split_pairs, int)
        and full_split_pairs >= 1
        and isinstance(compressed_files, int)
        and compressed_files >= 1
        and isinstance(matrix_files, int)
        and matrix_files >= 1
        and adoption_policy_complete
        and unknown_needs_review_allowed
        and blocker_count == 0
    )

    out_path = root / REVIEW_FILENAME
    review: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "source_phase_id": scan.get("phase_id", SOURCE_PHASE_ID),
        "source_final_decision": source_final_decision,
        "source_scan_file": str(scan_path),
        "review_scope": {
            "scan_review_only": True,
            "no_file_modification": True,
            "no_lifecycle_rewrite": True,
            "no_retrofit": True,
            "no_runtime_touch": True,
        },
        "baseline_review": {
            "scan_ok": scan_ok,
            "template_file_present": template_file_present,
            "full_split_pairs_detected": full_split_pairs,
            "compressed_files_detected": compressed_files,
            "matrix_files_detected": matrix_files,
            "template_consumers_detected": scan.get("template_consumers_detected"),
            "go_artifacts_detected": scan.get("go_artifacts_detected"),
        },
        "classification_review": classification_review,
        "adoption_policy_review": adoption_policy_review,
        "governance_decision": {
            "compressed_is_new_default_for_planning_phase": adoption_policy_review[
                "planning_candidate_only_default_compressed"
            ],
            "matrix_is_default_for_selection_binding_phase": adoption_policy_review[
                "matrix_binding_selection_default_matrix"
            ],
            "full_is_exception_for_high_risk_phase": adoption_policy_review[
                "high_risk_execution_repair_authorization_keep_full_or_custom"
            ],
            "unknown_needs_review_is_backlog_not_blocker": unknown_needs_review_allowed,
            "scanner_can_be_used_as_drift_check": scan_ok,
        },
        "handoff_readiness": {
            "ready_for_new_phase_lifecycle_gate": go_ok,
            "ready_for_template_adoption_in_future_modules": go_ok,
            "ready_for_touch_based_matrix_alignment": go_ok,
            "ready_for_controlled_skeleton_merge_on_touch": go_ok,
        },
        "adoption_policy_complete": adoption_policy_complete,
        "unknown_needs_review_count": unknown_count,
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "final_decision": (
            FINAL_DECISION_BASELINE_GO if go_ok else FINAL_DECISION_BASELINE_BLOCKED
        ),
        "output_file": str(out_path),
    }

    if write_file:
        write_json_file(out_path, review)

    return review


def main() -> int:
    try:
        review = review_dryrun_lifecycle_adoption_scan_v1()
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1

    print(
        json.dumps(
            {
                "output_file": review.get("output_file"),
                "source_final_decision": review.get("source_final_decision"),
                "adoption_policy_complete": review.get("adoption_policy_complete"),
                "blocker_count": review["blocker_count"],
                "final_decision": review["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if review["final_decision"] == FINAL_DECISION_BASELINE_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
