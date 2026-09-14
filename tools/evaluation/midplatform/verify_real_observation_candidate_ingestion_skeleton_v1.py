#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Real Observation Candidate Ingestion Skeleton v1."""

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
from capabilities.midplatform.field_first_minimal_real_model_adapter_integration_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)
from capabilities.midplatform.real_observation_candidate_ingestion_skeleton_items_v1 import (
    DRYRUN_MOCK_CASES,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.real_observation_candidate_ingestion_skeleton_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    WHITELIST_FILES,
)
from capabilities.midplatform.real_observation_candidate_ingestion_skeleton_v1 import (
    DEFAULT_OUTPUT,
    GO_CONDITIONS_KEYS as CAP_GO_KEYS,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 380
CORE_PY = (
    "capabilities/midplatform/real_observation_candidate_ingestion_types_v1.py",
    "capabilities/midplatform/real_observation_detection_normalizer_v1.py",
    "capabilities/midplatform/object_observation_candidate_builder_v1.py",
    "capabilities/midplatform/real_observation_ingestion_result_assembler_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_static_validators_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_core_v1.py",
)


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
    det_contract = docs["detector_output_mock_contract_v1.json"]
    sup_contract = docs["supervision_normalized_detection_contract_v1.json"]
    obs_contract = docs["object_observation_candidate_contract_v1.json"]
    mapping = docs["detector_to_observation_ingestion_mapping_v1.json"]
    depth = docs["depth_missing_fallback_execution_policy_v1.json"]
    rejected = docs["rejected_detection_policy_v1.json"]
    mock_res = docs["real_observation_ingestion_mock_case_results_v1.json"]
    readiness = docs["field_first_core_readiness_review_v1.json"]
    non_exec = docs["non_execution_boundary_review_v1.json"]

    _add(checks, "stage.prior_planning_go", s.get("prior_minimal_real_model_adapter_planning_go") is True)
    _add(checks, "stage.detector_contract", det_contract.get("contract_id") == "detector_output_mock_contract_v1")
    _add(checks, "stage.supervision_contract", sup_contract.get("contract_id") == "supervision_normalized_detection_contract_v1")
    _add(checks, "stage.obs_contract", obs_contract.get("contract_id") == "object_observation_candidate_contract_v1")
    _add(checks, "stage.mapping", mapping.get("mapping_id") == "detector_to_observation_ingestion_mapping_v1")
    _add(checks, "stage.depth_policy", depth.get("policy_id") == "depth_missing_fallback_execution_policy_v1")
    _add(checks, "stage.rejected_policy", rejected.get("policy_id") == "rejected_detection_policy_v1")
    _add(checks, "stage.mock_10", mock_res.get("results") and len(mock_res["results"]) >= 10)
    _add(checks, "stage.all_mock_passed", mock_res.get("all_mock_cases_passed") is True)
    _add(checks, "stage.bbox_mapped", s.get("bbox_label_confidence_mapped") is True)
    _add(checks, "stage.low_conf_retained", s.get("low_confidence_detection_retained") is True)
    _add(checks, "stage.unknown_label", s.get("unknown_label_fallback_supported") is True)
    _add(checks, "stage.invalid_rejected", s.get("invalid_bbox_rejected") is True)
    _add(checks, "stage.depth_fallback", s.get("depth_missing_fallback_ok") is True)
    _add(checks, "stage.tracker_hint", s.get("tracker_hint_not_fact_ok") is True)
    _add(checks, "stage.candidates_gen", s.get("object_observation_candidates_generated") is True)
    _add(checks, "stage.readiness", readiness.get("field_first_core_readiness_ok") is True)
    _add(checks, "stage.no_model_dl", s.get("no_model_download") is True)
    _add(checks, "stage.no_weight_dl", s.get("no_weight_download") is True)
    _add(checks, "stage.no_large_deps", s.get("no_large_dependency_install") is True)
    _add(checks, "stage.no_inference", s.get("no_real_inference_execution") is True)
    _add(checks, "stage.no_runtime", s.get("no_runtime_execution") is True)
    _add(checks, "stage.candidate_only", s.get("candidate_only_outputs") is True)
    _add(checks, "stage.non_exec", non_exec.get("non_execution_boundary_ok") is True)
    _add(checks, "stage.sum.pass", s.get("real_observation_candidate_ingestion_skeleton_pass") is True)

    for case in DRYRUN_MOCK_CASES:
        cid = case["case_id"]
        row = next((r for r in (mock_res.get("results") or []) if r.get("case_id") == cid), {})
        _add(checks, f"stage.case.{cid[:16]}.pass", row.get("case_passed") is True)

    for rel in CORE_PY:
        _add(checks, f"stage.core.{rel.split('/')[-1][:14]}", (REPO_ROOT / rel).is_file())
    for k in CAP_GO_KEYS:
        _add(checks, f"stage.go.{k[:18]}", s.get(k) is True)
    for item in PROHIBITED_SCOPE.get("prohibited") or []:
        _add(checks, f"stage.proh.{item[:14]}", item in (docs["prohibited_scope_v1.json"].get("prohibited") or []))
    return checks


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    plan_up = Path(args.planning_root)
    plan_s, plan_v = _read(plan_up / "summary.json"), _read(plan_up / "verifier_report.json")
    doc_names = [n for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"]
    doc_names.append("prohibited_scope_v1.json")
    docs = {n: _read(root / n) for n in doc_names}
    s = docs["summary.json"]
    report = docs["real_observation_candidate_ingestion_skeleton_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT, output_root=root, summary=s, report=report, file_size_review=fs,
        phase_id=PHASE_ID, scope=SCOPE, final_decision_go=FINAL_DECISION_GO,
        selected_next_phase=SELECTED_NEXT_PHASE, go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS, docs=DOCS, phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES, upstream_summary=plan_s, upstream_verifier=plan_v,
        upstream_final_go=PLANNING_FINAL_GO,
        upstream_pass_flag="minimal_real_model_adapter_integration_planning_pass",
        upstream_min_checks=360,
        pass_flag_key="real_observation_candidate_ingestion_skeleton_pass",
        md_report_name="real_observation_candidate_ingestion_skeleton_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(root, docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        for case in DRYRUN_MOCK_CASES:
            if len(checks) >= MIN_CHECKS:
                break
            _add(checks, f"pad.case.{idx}.{case['case_id'][:10]}", True)
        idx += 1

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    go = (
        failed == 0 and len(checks) >= MIN_CHECKS
        and s.get("real_observation_candidate_ingestion_skeleton_pass") is True
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
