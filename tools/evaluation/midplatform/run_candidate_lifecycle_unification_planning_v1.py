#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Candidate Lifecycle Unification Planning v1."""

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

from capabilities.midplatform.candidate_lifecycle_unification_planning_v1 import (
    DEFAULT_BOUNDARY_REGISTRY_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    run_candidate_lifecycle_unification_planning_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("candidate_lifecycle_unification_planning_report", "candidate_lifecycle_unification_planning_report_v1.json"),
    ("candidate_lifecycle_scope", "candidate_lifecycle_scope_v1.json"),
    ("candidate_type_registry", "candidate_type_registry_v1.json"),
    ("unified_lifecycle_state_machine", "unified_lifecycle_state_machine_v1.json"),
    ("state_transition_rules", "state_transition_rules_v1.json"),
    ("forbidden_candidate_promotion_rules", "forbidden_candidate_promotion_rules_v1.json"),
    ("candidate_lifecycle_responsibility_matrix", "candidate_lifecycle_responsibility_matrix_v1.json"),
    ("promotion_preconditions", "promotion_preconditions_v1.json"),
    ("candidate_closure_rejection_deferral_rules", "candidate_closure_rejection_deferral_rules_v1.json"),
    ("lifecycle_integration_gap_register", "lifecycle_integration_gap_register_v1.json"),
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
    parser.add_argument("--module-boundary-registry-planning-root", default=DEFAULT_BOUNDARY_REGISTRY_PLANNING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_candidate_lifecycle_unification_planning_v1(
        module_boundary_registry_planning_root=args.module_boundary_registry_planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "candidate_lifecycle_unification_planning_report_v1.md").write_text(
        result["candidate_lifecycle_unification_planning_report_md"] + "\n", encoding="utf-8",
    )
    summary = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "candidate_lifecycle_unification_planning_pass": summary.get("candidate_lifecycle_unification_planning_pass"),
        "selected_next_route": summary.get("selected_next_route"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
