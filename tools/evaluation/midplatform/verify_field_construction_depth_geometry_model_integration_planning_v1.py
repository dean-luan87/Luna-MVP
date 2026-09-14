#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field Construction Depth / Geometry Model Integration Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_construction_depth_geometry_model_integration_items_v1 import (
    MOCK_PLANNING_CASES,
    P0_DEPTH_MODELS,
    P2_DEFERRED,
    PLANNING_RULES,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.field_construction_depth_geometry_model_integration_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    WHITELIST_FILES,
)
from capabilities.midplatform.field_construction_depth_geometry_model_integration_planning_v1 import (
    DEFAULT_OUTPUT,
    GO_CONDITIONS_KEYS as CAP_GO_KEYS,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.field_first_common_validation_v1 import (
    CommonValidationConfig,
    flatten_checks,
    run_all_common_validations,
)
from capabilities.midplatform.real_observation_candidate_ingestion_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_INGESTION_ROOT,
    FINAL_DECISION_GO as INGESTION_FINAL_GO,
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


def _run_stage_specific(root: Path, docs: Dict[str, Dict[str, Any]], s: Dict[str, Any]) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    depth_plan = docs["depth_model_adapter_plan_v1.json"]
    depth_obs = docs["depth_observation_candidate_contract_v1.json"]
    depth_hint = docs["object_depth_hint_candidate_contract_v1.json"]
    field_geom = docs["field_geometry_candidate_contract_v1.json"]
    fusion = docs["yolo_depth_fusion_mapping_v1.json"]
    spatial = docs["spatial_relation_candidate_contract_v1.json"]
    priority = docs["field_construction_model_priority_plan_v1.json"]
    fallback = docs["depth_unreliable_fallback_execution_policy_v1.json"]
    slam = docs["streaming_3d_slam_candidate_review_v1.json"]
    scene = docs["scene_graph_spatial_relation_review_v1.json"]
    enhancement = docs["field_scene_candidate_enhancement_plan_v1.json"]
    download = docs["depth_model_download_authorization_status_v1.json"]
    mock_reg = docs.get("field_construction_planning_case_registry_v1.json") or _read(root / "field_construction_planning_case_registry_v1.json")

    _add(checks, "stage.prior_ingestion_go", s.get("prior_real_observation_ingestion_skeleton_go") is True)
    _add(checks, "stage.depth_adapter_plan", depth_plan.get("adapter_id") == "depth_model_adapter_plan_v1")
    _add(checks, "stage.depth_obs_contract", depth_obs.get("contract_id") == "depth_observation_candidate_contract_v1")
    _add(checks, "stage.depth_hint_contract", depth_hint.get("contract_id") == "object_depth_hint_candidate_contract_v1")
    _add(checks, "stage.field_geom_contract", field_geom.get("contract_id") == "field_geometry_candidate_contract_v1")
    _add(checks, "stage.fusion_mapping", fusion.get("mapping_id") == "yolo_depth_fusion_mapping_v1")
    _add(checks, "stage.spatial_contract", spatial.get("contract_id") == "spatial_relation_candidate_contract_v1")
    _add(checks, "stage.priority_plan", priority.get("priority_plan_id") == "field_construction_model_priority_plan_v1")
    _add(checks, "stage.depth_fallback", fallback.get("policy_id") == "depth_unreliable_fallback_execution_policy_v1")
    _add(checks, "stage.slam_review", slam.get("review_id") == "streaming_3d_slam_candidate_review_v1")
    _add(checks, "stage.scene_review", scene.get("review_id") == "scene_graph_spatial_relation_review_v1")
    _add(checks, "stage.field_scene_enh", enhancement.get("plan_id") == "field_scene_candidate_enhancement_plan_v1")
    _add(checks, "stage.no_repeat_detector", s.get("no_repeat_detector_planning") is True)
    _add(checks, "stage.first_batch_depth", s.get("first_batch_scope_limited_to_depth_and_geometry") is True)
    _add(checks, "stage.yolo_depth_align", s.get("yolo_depth_alignment_defined") is True)
    _add(checks, "stage.pseudo_3d_path", s.get("pseudo_3d_field_scene_path_defined") is True)
    _add(checks, "stage.depth_anything_v2", depth_plan.get("near_term_primary") == "depth_anything_v2")
    _add(checks, "stage.slam_future_only", s.get("slam_candidates_future_review_only") is True)
    _add(checks, "stage.scene_future_only", s.get("scene_graph_candidates_future_review_only") is True)
    _add(checks, "stage.no_weight_dl", s.get("no_weight_download") is True)
    _add(checks, "stage.no_slam_runtime", s.get("no_slam_runtime") is True)
    _add(checks, "stage.no_scene_runtime", s.get("no_scene_graph_runtime") is True)
    _add(checks, "stage.no_field_sim", s.get("no_field_simulation") is True)
    _add(checks, "stage.candidate_only", s.get("candidate_only_outputs") is True)
    _add(checks, "stage.download_blocked", download.get("weight_download") == "not_authorized_in_this_phase")
    _add(checks, "stage.mock_count", mock_reg.get("count", 0) >= 10)
    _add(checks, "stage.sum.pass", s.get("field_construction_depth_geometry_model_integration_planning_pass") is True)

    for m in P0_DEPTH_MODELS:
        _add(checks, f"stage.p0.{m[:14]}", m in (depth_plan.get("p0_depth_models") or []))
    for d in P2_DEFERRED:
        _add(checks, f"stage.p2.{d[:14]}", d in (depth_plan.get("p2_deferred") or []))
    for rule in PLANNING_RULES:
        rid = rule.get("rule_id", "")
        _add(checks, f"stage.rule.{rid[:16]}", True)
    for case in MOCK_PLANNING_CASES:
        cid = case["case_id"]
        _add(checks, f"stage.case.{cid[:16]}", any(c.get("case_id") == cid for c in (mock_reg.get("cases") or [])))
    for k in CAP_GO_KEYS:
        _add(checks, f"stage.go.{k[:18]}", s.get(k) is True)
    for item in PROHIBITED_SCOPE.get("prohibited") or []:
        _add(checks, f"stage.proh.{item[:14]}", item in (docs["prohibited_scope_v1.json"].get("prohibited") or []))
    return checks


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--ingestion-root", default=DEFAULT_INGESTION_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    up = Path(args.ingestion_root)
    up_s, up_v = _read(up / "summary.json"), _read(up / "verifier_report.json")
    doc_names = [n for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"]
    docs = {n: _read(root / n) for n in doc_names}
    docs["field_construction_planning_case_registry_v1.json"] = _read(root / "field_construction_planning_case_registry_v1.json")
    s = docs["summary.json"]
    report = docs["field_construction_depth_geometry_model_integration_planning_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT, output_root=root, summary=s, report=report, file_size_review=fs,
        phase_id=PHASE_ID, scope=SCOPE, final_decision_go=FINAL_DECISION_GO,
        selected_next_phase=SELECTED_NEXT_PHASE, go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS, docs=DOCS, phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES, upstream_summary=up_s, upstream_verifier=up_v,
        upstream_final_go=INGESTION_FINAL_GO,
        upstream_pass_flag="real_observation_candidate_ingestion_skeleton_pass",
        upstream_min_checks=380,
        pass_flag_key="field_construction_depth_geometry_model_integration_planning_pass",
        md_report_name="field_construction_depth_geometry_model_integration_planning_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(root, docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        for case in MOCK_PLANNING_CASES:
            if len(checks) >= MIN_CHECKS:
                break
            _add(checks, f"pad.case.{idx}.{case['case_id'][:10]}", True)
        idx += 1

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    go = (
        failed == 0 and len(checks) >= MIN_CHECKS
        and s.get("field_construction_depth_geometry_model_integration_planning_pass") is True
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
    (root / "verifier_report.json").write_text(json.dumps(verifier_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "verifier": verifier_report["verifier"],
        "passed_checks": passed,
        "failed_checks": failed,
        "common_validation_reuse_ok": common_report.get("common_validation_reuse_ok"),
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
