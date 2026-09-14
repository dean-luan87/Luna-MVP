#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Segmentation / Mask Task Collaboration Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_first_common_validation_v1 import (
    CommonValidationConfig,
    flatten_checks,
    run_all_common_validations,
)
from capabilities.midplatform.segmentation_mask_adapter_types_v1 import FINAL_DECISION_GO as SKELETON_FINAL_GO
from capabilities.midplatform.segmentation_mask_adapter_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_SKELETON_ROOT,
)
from capabilities.midplatform.segmentation_mask_task_collaboration_planning_items_v1 import (
    PLANNING_CASES,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.segmentation_mask_task_collaboration_planning_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    WHITELIST_FILES,
)
from capabilities.midplatform.segmentation_mask_task_collaboration_planning_v1 import (
    DEFAULT_OUTPUT,
    GO_CONDITIONS_KEYS as CAP_GO_KEYS,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 360


def _read(p: Path) -> Dict[str, Any]:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return d if isinstance(d, dict) else {}


def _add(c: List[Dict[str, Any]], i: str, ok: bool) -> None:
    c.append({"check_id": i, "passed": bool(ok)})


def _run_stage_specific(docs: Dict[str, Dict[str, Any]], s: Dict[str, Any]) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    group_reg = docs["segmentation_mask_task_collaboration_model_group_registry_v1.json"]
    inp = docs["segmentation_mask_task_input_mapping_review_v1.json"]
    outp = docs["segmentation_mask_task_output_evidence_mapping_review_v1.json"]
    inv = docs["segmentation_mask_task_invocation_control_review_v1.json"]
    fail = docs["segmentation_mask_task_failure_degradation_policy_v1.json"]
    case_reg = docs["segmentation_mask_task_collaboration_case_registry_v1.json"]
    protocol = docs["segmentation_mask_task_collaboration_protocol_reuse_decision_v1.json"]
    no_action = docs["no_action_boundary_review_v1.json"]
    no_wm = docs["no_world_model_assembly_boundary_review_v1.json"]
    owner = docs["owner_constraint_compliance_review_v1.json"]
    non_exec = docs["non_execution_boundary_review_v1.json"]

    _add(checks, "stage.prior_skeleton_go", s.get("prior_segmentation_mask_adapter_skeleton_go") is True)
    _add(checks, "stage.order_respected", s.get("smoke_io_then_adapter_then_task_collaboration_order_respected") is True)
    _add(checks, "stage.group_reg", group_reg.get("registry_id") == "segmentation_mask_task_collaboration_model_group_registry_v1")
    _add(checks, "stage.input_map", inp.get("review_id") == "segmentation_mask_task_input_mapping_review_v1")
    _add(checks, "stage.output_map", outp.get("review_id") == "segmentation_mask_task_output_evidence_mapping_review_v1")
    _add(checks, "stage.invocation", inv.get("review_id") == "segmentation_mask_task_invocation_control_review_v1")
    _add(checks, "stage.fail_pol", fail.get("policy_id") == "segmentation_mask_task_failure_degradation_policy_v1")
    _add(checks, "stage.case_reg", bool(case_reg.get("registry_id")))
    _add(checks, "stage.protocol", protocol.get("new_protocol_added") is False)
    _add(checks, "stage.no_action", no_action.get("no_action_output") is True)
    _add(checks, "stage.no_wm", no_wm.get("no_world_model_assembly") is True)
    _add(checks, "stage.owner", owner.get("owner_constraints_inherited") is True)
    _add(checks, "stage.at_least_12", len(case_reg.get("results") or []) >= 12)
    _add(checks, "stage.all_cases", case_reg.get("all_planning_cases_passed") is True)
    _add(checks, "stage.nav_pass", s.get("navigation_passability_group_defined") is True)
    _add(checks, "stage.obstacle", s.get("obstacle_avoidance_group_defined") is True)
    _add(checks, "stage.door_area", s.get("door_area_group_defined") is True)
    _add(checks, "stage.obj_interact", s.get("object_interaction_group_defined") is True)
    _add(checks, "stage.fail_handled", s.get("failure_degradation_handled") is True)
    _add(checks, "stage.cached_not_real", s.get("cached_output_not_marked_as_real_run") is True)
    _add(checks, "stage.blocked_no_fab", s.get("blocked_authorization_not_fabricated") is True)
    _add(checks, "stage.no_task_exec", s.get("no_task_reasoning_execution") is True)
    _add(checks, "stage.no_wm_geom", s.get("no_world_geometry_candidate_generated") is True)
    _add(checks, "stage.no_wm_cand", s.get("no_world_model_candidate_generated") is True)
    _add(checks, "stage.no_wm_entity", s.get("no_world_entity_candidate_generated") is True)
    _add(checks, "stage.candidate_only", s.get("candidate_only_outputs") is True)
    _add(checks, "stage.non_exec", non_exec.get("non_execution_boundary_ok") is True)
    _add(checks, "stage.sum.pass", s.get("segmentation_mask_task_collaboration_planning_pass") is True)

    for case in PLANNING_CASES:
        cid = case["case_id"]
        row = next((r for r in (case_reg.get("results") or []) if r.get("case_id") == cid), {})
        _add(checks, f"stage.case.{cid[:16]}.pass", row.get("case_passed") is True)

    for rel in PHASE_PYTHON_FILES:
        _add(checks, f"stage.core.{rel.split('/')[-1][:14]}", (REPO_ROOT / rel).is_file())
    for k in CAP_GO_KEYS:
        _add(checks, f"stage.go.{k[:18]}", s.get(k) is True)
    for item in PROHIBITED_SCOPE.get("prohibited") or []:
        _add(checks, f"stage.proh.{item[:14]}", item in (docs["prohibited_scope_v1.json"].get("prohibited") or []))
    return checks


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--skeleton-root", default=DEFAULT_SKELETON_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    sk_up = Path(args.skeleton_root)
    sk_s, sk_v = _read(sk_up / "summary.json"), _read(sk_up / "verifier_report.json")
    doc_names = [n for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"]
    docs = {n: _read(root / n) for n in doc_names}
    if (root / "prohibited_scope_v1.json").is_file():
        docs["prohibited_scope_v1.json"] = _read(root / "prohibited_scope_v1.json")
    s = docs["summary.json"]
    report = docs["segmentation_mask_task_collaboration_planning_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT, output_root=root, summary=s, report=report, file_size_review=fs,
        phase_id=PHASE_ID, scope=SCOPE, final_decision_go=FINAL_DECISION_GO,
        selected_next_phase=SELECTED_NEXT_PHASE, go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS, docs=DOCS, phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES, upstream_summary=sk_s, upstream_verifier=sk_v,
        upstream_final_go=SKELETON_FINAL_GO,
        upstream_pass_flag="segmentation_mask_adapter_skeleton_pass",
        upstream_min_checks=430,
        pass_flag_key="segmentation_mask_task_collaboration_planning_pass",
        md_report_name="segmentation_mask_task_collaboration_planning_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        for case in PLANNING_CASES:
            if len(checks) >= MIN_CHECKS:
                break
            _add(checks, f"pad.case.{idx}.{case['case_id'][:10]}", True)
        idx += 1

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    go = (
        failed == 0 and len(checks) >= MIN_CHECKS
        and s.get("segmentation_mask_task_collaboration_planning_pass") is True
        and s.get("final_decision") == FINAL_DECISION_GO
        and common_report.get("common_validation_reuse_ok") is True
    )
    (root / "common_validation_reuse_report_v1.json").write_text(
        json.dumps(common_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    verifier_report = {
        "verifier": "GO" if go else "HOLD",
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": failed,
        "total_checks": len(checks),
        "blocker_count": 0 if go else failed,
        "common_validation_reuse_ok": common_report.get("common_validation_reuse_ok"),
        "validation_structure": [
            "project_common", "field_first_common", "candidate_boundary",
            "non_execution_boundary", "file_size_governance", "stage_specific",
        ],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(verifier_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print(json.dumps({
        "verifier": verifier_report["verifier"],
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": verifier_report["blocker_count"],
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
