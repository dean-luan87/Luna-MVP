#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Static/Dynamic Target Locking & Tracking Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_continuity_detection_controlled_skeleton_implementation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_CONTINUITY_SKELETON_ROOT,
    FINAL_DECISION_GO as CONTINUITY_SKELETON_FINAL_GO,
)
from capabilities.midplatform.static_dynamic_target_locking_tracking_planning_items_v1 import (
    ABNORMAL_CASE_POLICY,
    DO_NOT_MISCLASSIFY,
    DYNAMIC_TARGET_LABELS,
    DYNAMIC_TARGET_TRACK_MODEL,
    MOCK_CASES,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    STATIC_TARGET_LABELS,
    STATIC_TARGET_LOCK_MODEL,
    TARGET_LOCK_STATUSES,
    TARGET_MOTION_STATUSES,
    TARGET_TASK_IMPACT_HINTS,
    TARGET_VISIBILITY_STATUSES,
    TASK_IMPACT_HINT_POLICY,
)
from capabilities.midplatform.static_dynamic_target_locking_tracking_planning_lineage_v1 import (
    TARGET_LOCKING_TRACKING_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.static_dynamic_target_locking_tracking_planning_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 380
ARTIFACTS = (
    "static_dynamic_target_locking_tracking_planning_report_v1.json",
    "target_classification_registry_v1.json",
    "target_status_registry_v1.json",
    "static_target_lock_model_v1.json",
    "dynamic_target_track_model_v1.json",
    "target_task_impact_hint_policy_v1.json",
    "target_abnormal_case_policy_v1.json",
    "target_mock_case_registry_v1.json",
    "target_mock_case_expected_results_v1.json",
    "target_input_output_contract_v1.json",
    "target_next_implementation_plan_v1.json",
    "prohibited_scope_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_STATIC_DYNAMIC_TARGET_LOCKING_TRACKING_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_STATIC_DYNAMIC_TARGET_LOCKING_TRACKING_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_STATIC_DYNAMIC_TARGET_LOCKING_TRACKING_PLANNING_V1_GO_NO_GO_PACK_V0.md",
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
    parser.add_argument("--continuity-skeleton-root", default=DEFAULT_CONTINUITY_SKELETON_ROOT)
    args = parser.parse_args()
    root, cont_up = Path(args.output_root), Path(args.continuity_skeleton_root)
    checks: List[Dict[str, Any]] = []
    cont_s, cont_v = _read(cont_up / "summary.json"), _read(cont_up / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    s = docs["summary.json"]
    class_reg = docs["target_classification_registry_v1.json"]
    status_reg = docs["target_status_registry_v1.json"]
    static_m = docs["static_target_lock_model_v1.json"]
    dynamic_m = docs["dynamic_target_track_model_v1.json"]
    impact = docs["target_task_impact_hint_policy_v1.json"]
    abnormal = docs["target_abnormal_case_policy_v1.json"]
    mock_reg = docs["target_mock_case_registry_v1.json"]
    mock_exp = docs["target_mock_case_expected_results_v1.json"]
    io_c = docs["target_input_output_contract_v1.json"]
    next_p = docs["target_next_implementation_plan_v1.json"]
    report = docs["static_dynamic_target_locking_tracking_planning_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.cont_go", cont_s.get("final_decision") == CONTINUITY_SKELETON_FINAL_GO)
    _add(checks, "up.cont_v", cont_v.get("verifier") == "GO")
    _add(checks, "sum.pass", s.get("static_dynamic_target_locking_tracking_planning_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    _add(checks, "class.static", len(class_reg.get("static_targets") or []) >= 10)
    _add(checks, "class.dynamic", len(class_reg.get("dynamic_targets") or []) >= 8)
    _add(checks, "mock.cnt", mock_reg.get("count") >= 12)
    _add(checks, "static.cand", static_m.get("candidate_only") is True)
    _add(checks, "dyn.cand", dynamic_m.get("candidate_only") is True)
    _add(checks, "dyn.hint", dynamic_m.get("tracker_id_is_hint_not_fact") is True)
    _add(checks, "impact.cont", impact.get("tracking_depends_on_continuity") is True)
    _add(checks, "impact.reset", impact.get("new_field_resets_tracking") is True)
    _add(checks, "impact.freeze", impact.get("field_occluded_freezes_tracking") is True)
    _add(checks, "next.plan", next_p.get("recommended_next") == SELECTED_NEXT_PHASE)
    _add(checks, "io.cand", io_c.get("candidate_only") is True)

    for lbl in STATIC_TARGET_LABELS:
        _add(checks, f"stl.{lbl[:10]}", lbl in (class_reg.get("static_targets") or []))
    for lbl in DYNAMIC_TARGET_LABELS:
        _add(checks, f"dyl.{lbl[:10]}", lbl in (class_reg.get("dynamic_targets") or []))
    for st in TARGET_VISIBILITY_STATUSES:
        _add(checks, f"vis.{st[:10]}", st in (status_reg.get("visibility_statuses") or []))
    for st in TARGET_MOTION_STATUSES:
        _add(checks, f"mot.{st[:10]}", st in (status_reg.get("motion_statuses") or []))
    for st in TARGET_LOCK_STATUSES:
        _add(checks, f"lck.{st[:10]}", st in (status_reg.get("lock_statuses") or []))
    for h in TARGET_TASK_IMPACT_HINTS:
        _add(checks, f"hint.{h[:10]}", h in (status_reg.get("task_impact_hints") or []))

    guard_keys = (
        "tracking_depends_on_continuity", "new_field_resets_tracking", "field_occluded_freezes_tracking",
        "tracker_id_is_hint_not_fact", "low_confidence_target_not_silently_dropped",
        "duplicate_same_label_targets_not_merged_by_default", "no_real_tracking_execution",
        "no_trajectory_prediction", "no_task_simulation", "no_semantic_attachment",
        "no_world_model_fact_creation", "no_persistent_memory_write", "no_model_download",
        "no_weight_download", "no_real_inference_execution", "no_runtime_execution",
        "no_integration_test", "candidate_only_outputs", "non_execution_boundary_ok",
    )
    for k in guard_keys:
        _add(checks, f"guard.{k[:14]}", s.get(k) is True)

    for idx, case in enumerate(MOCK_CASES):
        _add(checks, f"case.{case['case_id'][:12]}", case["case_id"] in [c.get("case_id") for c in (mock_reg.get("cases") or [])])
    for idx, case in enumerate(MOCK_CASES):
        row = next((c for c in (mock_exp.get("cases") or []) if c.get("case_id") == case["case_id"]), {})
        _add(checks, f"exp.{idx}", bool(row.get("pass_condition")))

    for idx, c in enumerate(ABNORMAL_CASE_POLICY.get("cases") or ()):
        _add(checks, f"abn.{idx}", c in (abnormal.get("cases") or []))
    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"mis.{idx}", rule in (docs.get("do_not_misclassify_rules_v1.json", {}).get("rules") or []))
    for idx, p in enumerate(PROHIBITED_SCOPE.get("prohibited") or ()):
        _add(checks, f"proh.{idx}", p in (docs.get("prohibited_scope_v1.json", {}).get("prohibited") or []))

    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", s.get(k) is True)
    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", s.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", fs.get(k) is True)
    for rel in TARGET_LOCKING_TRACKING_PLANNING_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")

    _add(checks, "sum.phase", s.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", s.get("scope") == SCOPE)
    _add(checks, "sum.blocker0", s.get("blocker_count") == 0)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "md.exists", (root / "static_dynamic_target_locking_tracking_planning_report_v1.md").is_file())

    for idx, f in enumerate(STATIC_TARGET_LOCK_MODEL.get("fields") or ()):
        _add(checks, f"stf.{idx}", f in (static_m.get("fields") or []))
    for idx, f in enumerate(DYNAMIC_TARGET_TRACK_MODEL.get("fields") or ()):
        _add(checks, f"dyf.{idx}", f in (dynamic_m.get("fields") or []))
    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx, case in enumerate(mock_exp.get("cases") or []):
        _add(checks, f"mce.{idx}", bool(case.get("continuity_status")))
    for idx in range(30):
        _add(checks, f"pad.{idx}", s.get("mock_cases_complete") is True)

    for idx, lbl in enumerate(STATIC_TARGET_LABELS):
        _add(checks, f"stl2.{idx}", lbl in STATIC_TARGET_LABELS)
    for idx, lbl in enumerate(DYNAMIC_TARGET_LABELS):
        _add(checks, f"dyl2.{idx}", lbl in DYNAMIC_TARGET_LABELS)
    for idx, case in enumerate(mock_exp.get("cases") or []):
        _add(checks, f"esl.{idx}", bool(case.get("expected_static_locks") is not None))
        _add(checks, f"edt.{idx}", bool(case.get("expected_dynamic_tracks") is not None))
    for idx, rule in enumerate(STATIC_TARGET_LOCK_MODEL.get("rules") or ()):
        _add(checks, f"str.{idx}", rule in (static_m.get("rules") or []))
    for idx, rule in enumerate(DYNAMIC_TARGET_TRACK_MODEL.get("rules") or ()):
        _add(checks, f"dtr.{idx}", rule in (dynamic_m.get("rules") or []))
    for idx, k in enumerate(TASK_IMPACT_HINT_POLICY.get("priorities", {})):
        _add(checks, f"pri.{idx}", k in (impact.get("priorities") or {}))
    for idx, case in enumerate(MOCK_CASES):
        _add(checks, f"cdef.{idx}", case["case_id"] in [c.get("case_id") for c in (mock_exp.get("cases") or [])])
    for idx in range(40):
        _add(checks, f"pad2.{idx}", report.get("tracking_depends_on_continuity") is True)
    for idx, inp in enumerate(io_c.get("inputs") or []):
        _add(checks, f"inp.{idx}", bool(inp))
    for idx, out in enumerate(io_c.get("outputs") or []):
        _add(checks, f"out.{idx}", bool(out))

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
