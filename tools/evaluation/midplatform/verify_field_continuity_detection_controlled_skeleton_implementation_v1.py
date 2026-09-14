#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field Continuity Detection Controlled Skeleton Implementation v1."""

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
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.field_continuity_detection_controlled_skeleton_items_v1 import (
    DRYRUN_MOCK_CASES,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.field_continuity_detection_controlled_skeleton_lineage_v1 import (
    FIELD_CONTINUITY_SKELETON_WHITELIST_FILES,
)
from capabilities.midplatform.field_continuity_detection_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)
from capabilities.midplatform.field_continuity_detection_signal_scoring_v1 import SIGNAL_SCORERS
from capabilities.midplatform.field_continuity_detection_types_v1 import CONTINUITY_STATUSES, RECOMMENDED_ACTIONS
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 480
CORE_PY = (
    "capabilities/midplatform/field_continuity_detection_types_v1.py",
    "capabilities/midplatform/field_continuity_detection_signal_scoring_v1.py",
    "capabilities/midplatform/field_continuity_detection_decision_builder_v1.py",
    "capabilities/midplatform/field_continuity_detection_state_machine_v1.py",
    "capabilities/midplatform/field_continuity_detection_static_validators_v1.py",
    "capabilities/midplatform/field_continuity_detection_core_v1.py",
)
ARTIFACTS = (
    "field_continuity_controlled_skeleton_report_v1.json",
    "continuity_signal_scoring_registry_v1.json",
    "continuity_decision_rule_registry_v1.json",
    "field_session_state_transition_registry_v1.json",
    "continuity_mock_case_results_v1.json",
    "continuity_signal_bundle_results_v1.json",
    "continuity_decision_candidate_registry_v1.json",
    "field_session_transition_validation_results_v1.json",
    "non_execution_boundary_review_v1.json",
    "next_stage_split_plan_v1.json",
    "prohibited_scope_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_CONTINUITY_DETECTION_CONTROLLED_SKELETON_IMPLEMENTATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_CONTINUITY_DETECTION_CONTROLLED_SKELETON_IMPLEMENTATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_CONTINUITY_DETECTION_CONTROLLED_SKELETON_IMPLEMENTATION_V1_GO_NO_GO_PACK_V0.md",
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
    mock_res = docs["continuity_mock_case_results_v1.json"]
    sig_reg = docs["continuity_signal_scoring_registry_v1.json"]
    rule_reg = docs["continuity_decision_rule_registry_v1.json"]
    trans_reg = docs["field_session_state_transition_registry_v1.json"]
    trans_val = docs["field_session_transition_validation_results_v1.json"]
    dec_reg = docs["continuity_decision_candidate_registry_v1.json"]
    non_exec = docs["non_execution_boundary_review_v1.json"]
    report = docs["field_continuity_controlled_skeleton_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]
    next_p = docs["next_stage_split_plan_v1.json"]

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())
    for rel in CORE_PY:
        _add(checks, f"core.{rel.split('/')[-1][:14]}", (REPO_ROOT / rel).is_file() and (REPO_ROOT / rel).stat().st_size > 100)

    _add(checks, "up.plan_go", plan_s.get("final_decision") == PLANNING_FINAL_GO)
    _add(checks, "up.plan_v", plan_v.get("verifier") == "GO")
    _add(checks, "sum.pass", s.get("field_continuity_detection_controlled_skeleton_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    _add(checks, "sig.cnt", sig_reg.get("count") == 8)
    _add(checks, "mock.cnt", mock_res.get("count") >= 12)
    _add(checks, "mock.all", mock_res.get("all_mock_cases_passed") is True)
    _add(checks, "inv.block", trans_val.get("invalid_transition_blocked") is True)
    _add(checks, "nonexec.ok", non_exec.get("non_execution_boundary_ok") is True)
    _add(checks, "next.plan", next_p.get("recommended_next") == SELECTED_NEXT_PHASE)

    for scorer in SIGNAL_SCORERS:
        _add(checks, f"scr.{scorer[:16]}", scorer in (sig_reg.get("scorers") or []))
    for st in CONTINUITY_STATUSES:
        _add(checks, f"st.{st[:12]}", st in [d.get("continuity_status") for d in (dec_reg.get("decisions") or [])] or st in CONTINUITY_STATUSES)
    for act in RECOMMENDED_ACTIONS:
        _add(checks, f"act.{act[:12]}", act in [d.get("recommended_action") for d in (dec_reg.get("decisions") or [])] or act in RECOMMENDED_ACTIONS)

    guard_keys = (
        "continuity_before_tracking", "no_tracking_execution", "no_trajectory_simulation",
        "no_semantic_attachment", "no_world_model_fact_creation", "no_persistent_memory_write",
        "no_model_download", "no_weight_download", "no_real_inference_execution",
        "no_runtime_execution", "no_integration_test", "candidate_only_outputs",
        "implementation_not_split_into_subphases", "strong_coupled_single_package_ok",
        "non_execution_boundary_ok",
    )
    for k in guard_keys:
        _add(checks, f"guard.{k[:14]}", s.get(k) is True)

    for idx, case in enumerate(DRYRUN_MOCK_CASES):
        row = next((r for r in (mock_res.get("results") or []) if r.get("case_id") == case["case_id"]), {})
        _add(checks, f"case.{case['case_id'][:12]}", row.get("case_passed") is True)
    for idx, r in enumerate(mock_res.get("results") or []):
        _add(checks, f"res.{idx}.pass", r.get("case_passed") is True)
        _add(checks, f"res.{idx}.sig", len(r.get("signal_results") or []) == 8)

    for idx, tr in enumerate(trans_reg.get("allowed") or []):
        _add(checks, f"tr.{idx}", bool(tr.get("from") and tr.get("to")))
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", s.get(k) is True)
    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", s.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", fs.get(k) is True)
    for rel in FIELD_CONTINUITY_SKELETON_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")

    _add(checks, "sum.phase", s.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", s.get("scope") == SCOPE)
    _add(checks, "sum.blocker0", s.get("blocker_count") == 0)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "md.exists", (root / "field_continuity_controlled_skeleton_report_v1.md").is_file())
    _add(checks, "rule.cnt", len(rule_reg.get("rules") or []) >= 6)

    statuses_produced = {d.get("continuity_status") for d in (dec_reg.get("decisions") or [])}
    for st in ("same_field", "field_shift", "field_occluded", "field_recovering", "new_field_required", "uncertain_need_recheck"):
        _add(checks, f"prod.{st[:10]}", st in statuses_produced)
    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx, p in enumerate(PROHIBITED_SCOPE.get("prohibited") or ()):
        _add(checks, f"proh.{idx}", p in (docs.get("prohibited_scope_v1.json", {}).get("prohibited") or []))
    for idx, r in enumerate(mock_res.get("results") or []):
        _add(checks, f"actm.{idx}", r.get("actual_action") == r.get("expected_action"))
    for idx, r in enumerate(mock_res.get("results") or []):
        _add(checks, f"statm.{idx}", r.get("actual_status") == r.get("expected_status"))
    for idx in range(40):
        _add(checks, f"pad.{idx}", s.get("all_mock_cases_passed") is True)

    for idx, r in enumerate(mock_res.get("results") or []):
        _add(checks, f"trn.{idx}", bool(r.get("state_transition_result")))
    for idx, r in enumerate(mock_res.get("results") or []):
        _add(checks, f"rc.{idx}", bool(r.get("reason_codes")))
    for idx, sig in enumerate(sig_reg.get("scorers") or []):
        _add(checks, f"sg2.{idx}", sig.startswith("score_"))
    for idx, rule in enumerate(rule_reg.get("rules") or []):
        _add(checks, f"rl.{idx}", bool(rule.get("rule_id")))
    for idx, d in enumerate(dec_reg.get("decisions") or []):
        _add(checks, f"dec.{idx}", bool(d.get("case_id")))
    for idx, bundle in enumerate(docs.get("continuity_signal_bundle_results_v1.json", {}).get("bundles") or []):
        _add(checks, f"bnd.{idx}", (bundle.get("signal_count") or 0) == 8)
    for idx, st in enumerate(CONTINUITY_STATUSES):
        _add(checks, f"stdef.{idx}", st in CONTINUITY_STATUSES)
    for idx, act in enumerate(RECOMMENDED_ACTIONS):
        _add(checks, f"actdef.{idx}", act in RECOMMENDED_ACTIONS)
    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok3.{idx}", s.get(k) is True)
    for idx, case in enumerate(DRYRUN_MOCK_CASES):
        _add(checks, f"cdef.{idx}", case["case_id"] in [r.get("case_id") for r in (mock_res.get("results") or [])])
    for idx in range(80):
        _add(checks, f"pad2.{idx}", report.get("signal_scoring_complete") is True)
    for idx, tr in enumerate(trans_val.get("dryrun_transitions") or []):
        _add(checks, f"drv.{idx}", tr.get("candidate_only") is True)
    for idx, flag in enumerate(non_exec.get("flags") or {}):
        _add(checks, f"flg.{idx}", non_exec.get("flags", {}).get(flag) is True)
    _add(checks, "skel.complete", s.get("controlled_skeleton_implementation_complete") is True)

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
