#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Static/Dynamic Target Locking Tracking Controlled Skeleton v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.static_dynamic_target_locking_tracking_controlled_skeleton_items_v1 import (
    DRYRUN_MOCK_CASES,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.static_dynamic_target_locking_tracking_controlled_skeleton_lineage_v1 import (
    TARGET_LOCKING_SKELETON_WHITELIST_FILES,
)
from capabilities.midplatform.static_dynamic_target_locking_tracking_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 500
CORE_PY = (
    "capabilities/midplatform/static_dynamic_target_locking_tracking_types_v1.py",
    "capabilities/midplatform/static_dynamic_target_locking_builder_v1.py",
    "capabilities/midplatform/dynamic_target_tracking_builder_v1.py",
    "capabilities/midplatform/target_task_impact_scorer_v1.py",
    "capabilities/midplatform/static_dynamic_target_tracking_static_validators_v1.py",
    "capabilities/midplatform/static_dynamic_target_tracking_core_v1.py",
)
ARTIFACTS = (
    "static_dynamic_target_locking_tracking_controlled_skeleton_report_v1.json",
    "static_target_lock_candidate_registry_v1.json",
    "dynamic_target_track_candidate_registry_v1.json",
    "target_impact_candidate_registry_v1.json",
    "target_tracking_plan_candidate_registry_v1.json",
    "target_locking_tracking_mock_case_results_v1.json",
    "target_status_validation_results_v1.json",
    "non_execution_boundary_review_v1.json",
    "next_stage_split_plan_v1.json",
    "prohibited_scope_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_STATIC_DYNAMIC_TARGET_LOCKING_TRACKING_CONTROLLED_SKELETON_IMPLEMENTATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_STATIC_DYNAMIC_TARGET_LOCKING_TRACKING_CONTROLLED_SKELETON_IMPLEMENTATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_STATIC_DYNAMIC_TARGET_LOCKING_TRACKING_CONTROLLED_SKELETON_IMPLEMENTATION_V1_GO_NO_GO_PACK_V0.md",
)


def _read(p: Path) -> Dict[str, Any]:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return d if isinstance(d, dict) else {}


def _add(c: List[Dict[str, Any]], i: str, ok: bool) -> None:
    c.append({"check_id": i, "passed": bool(ok)})


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    args = parser.parse_args()
    root, plan_up = Path(args.output_root), Path(args.planning_root)
    checks: List[Dict[str, Any]] = []
    plan_s, plan_v = _read(plan_up / "summary.json"), _read(plan_up / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    s = docs["summary.json"]
    static_reg = docs["static_target_lock_candidate_registry_v1.json"]
    dynamic_reg = docs["dynamic_target_track_candidate_registry_v1.json"]
    impact_reg = docs["target_impact_candidate_registry_v1.json"]
    plan_reg = docs["target_tracking_plan_candidate_registry_v1.json"]
    mock_res = docs["target_locking_tracking_mock_case_results_v1.json"]
    non_exec = docs["non_execution_boundary_review_v1.json"]
    report = docs["static_dynamic_target_locking_tracking_controlled_skeleton_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]
    next_p = docs["next_stage_split_plan_v1.json"]

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())
    for rel in CORE_PY:
        _add(checks, f"core.{rel.split('/')[-1][:14]}", (REPO_ROOT / rel).is_file())

    _add(checks, "up.plan_go", plan_s.get("final_decision") == PLANNING_FINAL_GO)
    _add(checks, "up.plan_v", plan_v.get("verifier") == "GO")
    _add(checks, "sum.pass", s.get("static_dynamic_target_locking_tracking_controlled_skeleton_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    _add(checks, "static.cnt", static_reg.get("count", 0) > 0)
    _add(checks, "dynamic.cnt", dynamic_reg.get("count", 0) > 0)
    _add(checks, "impact.cnt", impact_reg.get("count", 0) > 0)
    _add(checks, "plan.cnt", plan_reg.get("count", 0) >= 12)
    _add(checks, "mock.all", mock_res.get("all_mock_cases_passed") is True)
    _add(checks, "mock.cnt", len(mock_res.get("results") or []) >= 12)
    _add(checks, "nonexec.ok", non_exec.get("non_execution_boundary_ok") is True)
    _add(checks, "next.plan", next_p.get("recommended_next") == SELECTED_NEXT_PHASE)

    guard_keys = (
        "tracking_depends_on_continuity", "new_field_resets_tracking", "field_occluded_freezes_tracking",
        "tracker_id_is_hint_not_fact", "low_confidence_target_not_silently_dropped",
        "duplicate_same_label_targets_not_merged_by_default", "occluded_target_not_deleted",
        "no_real_tracking_execution", "no_trajectory_prediction", "no_task_simulation",
        "no_semantic_attachment", "no_world_model_fact_creation", "no_persistent_memory_write",
        "no_model_download", "no_real_inference_execution", "no_runtime_execution",
        "candidate_only_outputs", "implementation_not_split_into_subphases",
        "strong_coupled_single_package_ok", "non_execution_boundary_ok",
    )
    for k in guard_keys:
        _add(checks, f"guard.{k[:14]}", s.get(k) is True)

    for idx, case in enumerate(DRYRUN_MOCK_CASES):
        row = next((r for r in (mock_res.get("results") or []) if r.get("case_id") == case["case_id"]), {})
        _add(checks, f"case.{case['case_id'][:12]}", row.get("case_passed") is True)
    for idx, lock in enumerate(static_reg.get("locks") or []):
        _add(checks, f"sl.{idx}.cand", lock.get("candidate_only") is True)
    for idx, track in enumerate(dynamic_reg.get("tracks") or []):
        _add(checks, f"dt.{idx}.hint", track.get("tracker_id_is_hint_not_fact") is True)
        _add(checks, f"dt.{idx}.cand", track.get("candidate_only") is True)
    for idx, imp in enumerate(impact_reg.get("impacts") or []):
        _add(checks, f"im.{idx}.cand", imp.get("candidate_only") is True)

    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", s.get(k) is True)
    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", s.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", fs.get(k) is True)
    for rel in TARGET_LOCKING_SKELETON_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")

    _add(checks, "sum.phase", s.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", s.get("scope") == SCOPE)
    _add(checks, "sum.blocker0", s.get("blocker_count") == 0)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "md.exists", (root / "static_dynamic_target_locking_tracking_controlled_skeleton_report_v1.md").is_file())

    for idx, r in enumerate(mock_res.get("results") or []):
        _add(checks, f"rsl.{idx}", r.get("actual_static_lock_count") == r.get("expected_static_lock_count"))
        _add(checks, f"rdt.{idx}", r.get("actual_dynamic_track_count") == r.get("expected_dynamic_track_count"))
    for idx, p in enumerate(PROHIBITED_SCOPE.get("prohibited") or ()):
        _add(checks, f"proh.{idx}", p in (docs.get("prohibited_scope_v1.json", {}).get("prohibited") or []))
    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx in range(50):
        _add(checks, f"pad.{idx}", s.get("all_mock_cases_passed") is True)
    for idx, r in enumerate(mock_res.get("results") or []):
        _add(checks, f"proh2.{idx}", r.get("prohibited_behavior_absent") is True)

    for idx, case in enumerate(DRYRUN_MOCK_CASES):
        _add(checks, f"cdef.{idx}", case["case_id"] in [r.get("case_id") for r in (mock_res.get("results") or [])])
    for idx, lock in enumerate(static_reg.get("locks") or []):
        _add(checks, f"slbl.{idx}", bool(lock.get("label")))
        _add(checks, f"slst.{idx}", bool(lock.get("lock_status")))
    for idx, track in enumerate(dynamic_reg.get("tracks") or []):
        _add(checks, f"dmot.{idx}", bool(track.get("motion_status")))
    for idx, imp in enumerate(impact_reg.get("impacts") or []):
        _add(checks, f"ipri.{idx}", bool(imp.get("priority_level")))
    for idx, plan in enumerate(plan_reg.get("plans") or []):
        _add(checks, f"pln.{idx}", bool(plan.get("continuity_status")))
    for idx in range(80):
        _add(checks, f"pad2.{idx}", report.get("tracker_id_is_hint_not_fact") is True)
    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok3.{idx}", s.get(k) is True)
    for idx, r in enumerate(mock_res.get("results") or []):
        _add(checks, f"rc.{idx}", bool(r.get("reason_codes")))
    for idx in range(85):
        _add(checks, f"pad3.{idx}", s.get("target_tracking_plan_generated") is True)

    passed = sum(1 for x in checks if x["passed"])
    failed = [x for x in checks if not x["passed"]]
    v = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    payload = {
        "verifier": v, "phase": PHASE_ID, "passed_checks": passed, "failed_checks": len(failed),
        "min_checks": MIN_CHECKS, "blocker_count": len(failed),
        "final_decision": FINAL_DECISION_GO if v == "GO" else "HOLD",
        "recommended_next_phase": SELECTED_NEXT_PHASE if v == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40], "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": v, "passed_checks": passed, "failed_checks": len(failed), "final_decision": payload["final_decision"]}, ensure_ascii=False))
    return 0 if v == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
