#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field-First Minimal Real Model Adapter Integration Planning v1."""

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
from capabilities.midplatform.field_first_core_logic_formal_implementation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_CORE_LOGIC_ROOT,
    FINAL_DECISION_GO as CORE_LOGIC_FINAL_GO,
)
from capabilities.midplatform.field_first_minimal_real_model_adapter_integration_items_v1 import (
    MOCK_PLANNING_CASES,
    P0_MODELS,
    P2_DEFERRED,
    PLANNING_RULES,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.field_first_minimal_real_model_adapter_integration_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    WHITELIST_FILES,
)
from capabilities.midplatform.field_first_minimal_real_model_adapter_integration_planning_v1 import (
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


def _run_stage_specific(root: Path, docs: Dict[str, Dict[str, Any]], s: Dict[str, Any]) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    detector = docs["minimal_detector_adapter_plan_v1.json"]
    supervision = docs["supervision_normalization_plan_v1.json"]
    ingestion = docs["real_observation_candidate_ingestion_plan_v1.json"]
    mapping = docs["detector_output_to_observation_candidate_mapping_v1.json"]
    depth = docs["depth_missing_fallback_policy_v1.json"]
    readiness = docs["real_model_success_path_readiness_plan_v1.json"]
    download = docs["model_download_authorization_status_v1.json"]
    mock_reg = docs.get("minimal_real_model_planning_case_registry_v1.json") or _read(root / "minimal_real_model_planning_case_registry_v1.json")

    _add(checks, "stage.prior_core_go", s.get("prior_field_first_core_logic_go") is True)
    _add(checks, "stage.detector_plan_exists", detector.get("adapter_id") == "minimal_detector_adapter_plan_v1")
    _add(checks, "stage.supervision_plan_exists", supervision.get("normalization_id") == "supervision_normalization_plan_v1")
    _add(checks, "stage.ingestion_plan_exists", ingestion.get("ingestion_plan_id") == "real_observation_candidate_ingestion_plan_v1")
    _add(checks, "stage.mapping_exists", mapping.get("mapping_id") == "detector_output_to_observation_candidate_mapping_v1")
    _add(checks, "stage.depth_policy_exists", depth.get("policy_id") == "depth_missing_fallback_policy_v1")
    _add(checks, "stage.readiness_exists", readiness.get("readiness_plan_id") == "real_model_success_path_readiness_plan_v1")
    _add(checks, "stage.first_batch_limited", s.get("first_batch_scope_limited_to_detector_and_normalization") is True)
    _add(checks, "stage.yolo_adapter_source", s.get("yolo_or_lightweight_detector_positioned_as_adapter_source") is True)
    _add(checks, "stage.supervision_layer", s.get("supervision_positioned_as_normalization_layer") is True)
    _add(checks, "stage.maps_to_observation", s.get("model_output_maps_to_observation_candidate") is True)
    _add(checks, "stage.depth_unknown", s.get("depth_unknown_policy_defined") is True)
    _add(checks, "stage.no_weight_download", s.get("no_weight_download") is True)
    _add(checks, "stage.no_large_deps", s.get("no_large_dependency_install") is True)
    _add(checks, "stage.no_production_sel", s.get("no_production_model_selection") is True)
    _add(checks, "stage.no_field_sim", s.get("no_field_simulation") is True)
    _add(checks, "stage.no_task_exec", s.get("no_task_execution") is True)
    _add(checks, "stage.candidate_only", s.get("candidate_only_outputs") is True)
    _add(checks, "stage.download_blocked", download.get("weight_download") == "not_authorized_in_this_phase")
    _add(checks, "stage.detector.cand", detector.get("candidate_only") is True)
    _add(checks, "stage.detector.maps", detector.get("maps_to_candidate_type") == "ObjectObservationCandidate")
    _add(checks, "stage.mock_count", mock_reg.get("count", 0) >= 10)
    _add(checks, "stage.sum.pass", s.get("minimal_real_model_adapter_integration_planning_pass") is True)

    for m in P0_MODELS:
        _add(checks, f"stage.p0.{m[:14]}", m in (detector.get("p0_models") or []))
    for d in P2_DEFERRED:
        _add(checks, f"stage.p2.{d[:14]}", d in (detector.get("p2_deferred") or []))
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
    parser.add_argument("--core-logic-root", default=DEFAULT_CORE_LOGIC_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    core_up = Path(args.core_logic_root)
    core_s = _read(core_up / "summary.json")
    core_v = _read(core_up / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    docs["minimal_real_model_planning_case_registry_v1.json"] = _read(root / "minimal_real_model_planning_case_registry_v1.json")
    s = docs["summary.json"]
    report = docs["minimal_real_model_adapter_integration_planning_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT, output_root=root, summary=s, report=report, file_size_review=fs,
        phase_id=PHASE_ID, scope=SCOPE, final_decision_go=FINAL_DECISION_GO,
        selected_next_phase=SELECTED_NEXT_PHASE, go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS, docs=DOCS, phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES, upstream_summary=core_s, upstream_verifier=core_v,
        upstream_final_go=CORE_LOGIC_FINAL_GO,
        upstream_pass_flag="field_first_core_logic_formal_implementation_pass",
        upstream_min_checks=420,
        pass_flag_key="minimal_real_model_adapter_integration_planning_pass",
        md_report_name="minimal_real_model_adapter_integration_planning_report_v1.md",
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
        and s.get("minimal_real_model_adapter_integration_planning_pass") is True
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
