#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Evidence Record Approval Permission Alignment Planning v1."""

from __future__ import annotations

import dataclasses
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.evidence_record_approval_permission_alignment_planning_v1 import (
    DEFAULT_CANDIDATE_LIFECYCLE_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    run_evidence_record_approval_permission_alignment_planning_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("evidence_record_approval_permission_alignment_planning_report", "evidence_record_approval_permission_alignment_planning_report_v1.json"),
    ("alignment_scope", "alignment_scope_v1.json"),
    ("alignment_object_registry", "alignment_object_registry_v1.json"),
    ("candidate_real_object_boundary_matrix", "candidate_real_object_boundary_matrix_v1.json"),
    ("promotion_creation_preconditions", "promotion_creation_preconditions_v1.json"),
    ("alignment_responsibility_matrix", "alignment_responsibility_matrix_v1.json"),
    ("forbidden_alignment_transitions", "forbidden_alignment_transitions_v1.json"),
    ("alignment_traceability_contract", "alignment_traceability_contract_v1.json"),
    ("alignment_gap_register", "alignment_gap_register_v1.json"),
    ("next_route_decision", "next_route_decision_v1.json"),
    ("do_not_misclassify_rules", "do_not_misclassify_rules_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("summary", "summary.json"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--candidate-lifecycle-unification-planning-root", default=DEFAULT_CANDIDATE_LIFECYCLE_PLANNING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_evidence_record_approval_permission_alignment_planning_v1(
        candidate_lifecycle_unification_planning_root=args.candidate_lifecycle_unification_planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "evidence_record_approval_permission_alignment_planning_report_v1.md").write_text(
        result["evidence_record_approval_permission_alignment_planning_report_md"] + "\n", encoding="utf-8",
    )
    summary = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "alignment_planning_pass": summary.get("alignment_planning_pass"),
        "selected_next_route": summary.get("selected_next_route"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
