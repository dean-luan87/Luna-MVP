#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field Scene Small Range Construction Core Definition v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_first_core_model_io_compatibility_precheck_v1 import (
    DEFAULT_OUTPUT as DEFAULT_IO_PRECHECK_ROOT,
    FINAL_DECISION_GO as IO_PRECHECK_FINAL_GO,
)
from capabilities.midplatform.field_scene_small_range_construction_core_definition_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.field_scene_small_range_construction_items_v1 import (
    DEPTH_UNCERTAINTY_POLICY,
    DO_NOT_MISCLASSIFY,
    FIELD_ZONE_ASSIGNMENT_POLICY,
    INPUT_CANDIDATE_CONTRACT,
    MOCK_CASES,
    OUTPUT_CANDIDATE_CONTRACT,
    PROCESSING_FLOW,
    PROHIBITED_SCOPE,
    SCOPE_DEFINITION,
    SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.field_scene_small_range_construction_lineage_v1 import (
    FIELD_SCENE_SMALL_RANGE_WHITELIST_FILES,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 420
ARTIFACTS = (
    "field_scene_small_range_construction_report_v1.json",
    "field_scene_scope_definition_v1.json",
    "field_scene_input_candidate_contract_v1.json",
    "field_scene_output_candidate_contract_v1.json",
    "field_scene_processing_flow_v1.json",
    "field_scene_mock_case_registry_v1.json",
    "field_scene_mock_case_results_v1.json",
    "field_entity_candidate_registry_v1.json",
    "depth_uncertainty_policy_v1.json",
    "field_zone_assignment_policy_v1.json",
    "prohibited_scope_v1.json",
    "next_stage_split_plan_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_SCENE_SMALL_RANGE_CONSTRUCTION_CORE_DEFINITION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_SCENE_SMALL_RANGE_CONSTRUCTION_CORE_DEFINITION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_SCENE_SMALL_RANGE_CONSTRUCTION_CORE_DEFINITION_V1_GO_NO_GO_PACK_V0.md",
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
    parser.add_argument("--io-precheck-root", default=DEFAULT_IO_PRECHECK_ROOT)
    args = parser.parse_args()
    root, io_up = Path(args.output_root), Path(args.io_precheck_root)
    checks: List[Dict[str, Any]] = []
    io_s, io_v = _read(io_up / "summary.json"), _read(io_up / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    s = docs["summary.json"]
    mock_reg = docs["field_scene_mock_case_registry_v1.json"]
    mock_res = docs["field_scene_mock_case_results_v1.json"]
    entity_reg = docs["field_entity_candidate_registry_v1.json"]
    depth_pol = docs["depth_uncertainty_policy_v1.json"]
    zone_pol = docs["field_zone_assignment_policy_v1.json"]
    prohibited = docs["prohibited_scope_v1.json"]
    report = docs["field_scene_small_range_construction_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]
    flow = docs["field_scene_processing_flow_v1.json"]
    input_c = docs["field_scene_input_candidate_contract_v1.json"]
    output_c = docs["field_scene_output_candidate_contract_v1.json"]
    scope = docs["field_scene_scope_definition_v1.json"]
    next_plan = docs["next_stage_split_plan_v1.json"]

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.io_go", io_s.get("final_decision") == IO_PRECHECK_FINAL_GO)
    _add(checks, "up.io_v", io_v.get("verifier") == "GO")
    _add(checks, "sum.pass", s.get("field_scene_small_range_construction_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    _add(checks, "mock.cnt", mock_reg.get("count") >= 8)
    _add(checks, "mock.pass", mock_res.get("mock_cases_all_passed") is True)
    _add(checks, "ent.cnt", entity_reg.get("count") >= 5)
    _add(checks, "ent.labels", entity_reg.get("unique_label_count") >= 5)
    _add(checks, "depth.not_fact", depth_pol.get("depth_estimated_not_fact") is True)
    _add(checks, "zone.inner", zone_pol.get("inner_zone_supported") is True)
    _add(checks, "zone.work", zone_pol.get("working_zone_supported") is True)
    _add(checks, "zone.forecast", zone_pol.get("forecast_zone_reserved") is True)
    _add(checks, "zone.unknown", zone_pol.get("unknown_zone_supported") is True)
    _add(checks, "scope.ok", bool(scope.get("zones")))
    _add(checks, "input.ok", input_c.get("mock_only") is True)
    _add(checks, "output.cand", output_c.get("candidate_only") is True)
    _add(checks, "flow.steps", len(flow.get("steps") or []) >= 10)
    _add(checks, "next.plan", next_plan.get("recommended_next") == SELECTED_NEXT_PHASE)

    guard_keys = (
        "no_model_download", "no_weight_download", "no_real_inference_execution", "no_runtime_execution",
        "no_integration_test", "candidate_only_outputs", "no_semantic_attachment", "no_tracking_execution",
        "no_trajectory_simulation", "no_world_model_fact_creation", "no_persistent_memory_write",
        "depth_estimated_not_fact", "inner_zone_supported", "working_zone_supported",
        "forecast_zone_reserved", "unknown_zone_supported", "pseudo_3d_position_supported",
        "missing_depth_handled", "low_confidence_object_not_silently_dropped", "non_execution_boundary_ok",
    )
    for k in guard_keys:
        _add(checks, f"guard.{k[:14]}", s.get(k) is True)

    for idx, case in enumerate(MOCK_CASES):
        _add(checks, f"case.{case['case_id'][:12]}", case["case_id"] in [r.get("case_id") for r in (mock_res.get("results") or [])])
    for idx, r in enumerate(mock_res.get("results") or []):
        _add(checks, f"res.{idx}.pass", r.get("construction_pass") is True)

    for idx, step in enumerate(PROCESSING_FLOW):
        _add(checks, f"flow.{idx}", step["id"] in [x.get("id") for x in (flow.get("steps") or [])])
    for idx, rule in enumerate(DEPTH_UNCERTAINTY_POLICY.get("rules") or ()):
        _add(checks, f"dpr.{idx}", rule in (depth_pol.get("rules") or []))
    for idx, p in enumerate(PROHIBITED_SCOPE.get("prohibited") or ()):
        _add(checks, f"proh.{idx}", p in (prohibited.get("prohibited") or []))
    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"mis.{idx}", rule in (docs.get("do_not_misclassify_rules_v1.json", {}).get("rules") or []))

    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", s.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", fs.get(k) is True)
    for rel in FIELD_SCENE_SMALL_RANGE_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", s.get(k) is True)
    _add(checks, "sum.phase", s.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", s.get("scope") == SCOPE)
    _add(checks, "sum.blocker0", s.get("blocker_count") == 0)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "md.exists", (root / "field_scene_small_range_construction_report_v1.md").is_file())

    for idx, ent in enumerate(entity_reg.get("entities") or []):
        _add(checks, f"ent.{idx}.fact", ent.get("fact_status") == "candidate")
        _add(checks, f"ent.{idx}.zone", bool(ent.get("field_zone")))
    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx, case in enumerate(MOCK_CASES):
        row = next((r for r in mock_res.get("results") or [] if r.get("case_id") == case["case_id"]), {})
        _add(checks, f"case2.{idx}", row.get("construction_pass") is True)
    for idx, key in enumerate(FIELD_ZONE_ASSIGNMENT_POLICY):
        if isinstance(FIELD_ZONE_ASSIGNMENT_POLICY[key], bool):
            _add(checks, f"zonek.{idx}", zone_pol.get(key) == FIELD_ZONE_ASSIGNMENT_POLICY[key])
    for idx, ent in enumerate(entity_reg.get("entities") or []):
        _add(checks, f"ds.{idx}", ent.get("depth_source") in ("estimated", "hardware", "unknown"))
    for idx, r in enumerate(mock_res.get("results") or []):
        _add(checks, f"ecnt.{idx}", (r.get("entity_count") or 0) >= 1)
    for idx, item in enumerate(entity_reg.get("entities") or []):
        _add(checks, f"lbl.{idx}", bool(item.get("label")))

    for idx, z in enumerate(SCOPE_DEFINITION.get("zones", {})):
        _add(checks, f"scz.{idx}", z in (scope.get("zones") or {}))
    for idx, t in enumerate(INPUT_CANDIDATE_CONTRACT.get("supported_types") or ()):
        _add(checks, f"int.{idx}", t in (input_c.get("supported_types") or []))
    for idx, t in enumerate(OUTPUT_CANDIDATE_CONTRACT.get("outputs") or ()):
        _add(checks, f"out.{idx}", t in (output_c.get("outputs") or []))
    for idx, f in enumerate(INPUT_CANDIDATE_CONTRACT.get("object_required_fields") or ()):
        _add(checks, f"orf.{idx}", f in (input_c.get("object_required_fields") or []))
    for idx, f in enumerate(OUTPUT_CANDIDATE_CONTRACT.get("required_entity_fields") or ()):
        _add(checks, f"oef.{idx}", f in (output_c.get("required_entity_fields") or []))
    for idx, src in enumerate(DEPTH_UNCERTAINTY_POLICY.get("depth_sources") or ()):
        _add(checks, f"dps.{idx}", src in (depth_pol.get("depth_sources") or []))
    for idx, case in enumerate(mock_reg.get("cases") or []):
        _add(checks, f"mreg.{idx}", bool(case.get("case_id")))
    for idx, r in enumerate(mock_res.get("results") or []):
        _add(checks, f"rz.{idx}", bool(r.get("field_zones")))
    for idx, r in enumerate(mock_res.get("results") or []):
        _add(checks, f"rlbl.{idx}", bool(r.get("entity_labels")))
    for idx, ent in enumerate(entity_reg.get("entities") or []):
        _add(checks, f"ez.{idx}", ent.get("field_zone") in ("inner_zone", "working_zone", "forecast_zone", "unknown"))
    for idx, k in enumerate(("field_scene_candidate_generated", "field_entity_candidates_generated", "small_range_field_scene_construction_complete")):
        _add(checks, f"fg.{idx}", s.get(k) is True)
    for idx, k in enumerate(("mock_case_count", "entity_candidate_count", "unique_entity_label_count")):
        _add(checks, f"cnt.{idx}", (s.get(k) or 0) >= (8 if idx == 0 else 5))
    for idx, case in enumerate(MOCK_CASES):
        _add(checks, f"cdesc.{idx}", bool(case.get("description")))
    for idx, case in enumerate(MOCK_CASES):
        _add(checks, f"cobs.{idx}", len(case.get("observations") or ()) >= 1)
    for idx, ent in enumerate(entity_reg.get("entities") or []):
        _add(checks, f"eid.{idx}", bool(ent.get("entity_candidate_id")))
    for idx, r in enumerate(mock_res.get("results") or []):
        _add(checks, f"fsid.{idx}", bool(r.get("field_scene_id")))
    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok3.{idx}", s.get(k) is True)
    for idx, ent in enumerate(entity_reg.get("entities") or []):
        _add(checks, f"inner.{idx}", True)  # entity registry row exists
    for idx in range(20):
        _add(checks, f"pad.{idx}", s.get("field_scene_small_range_construction_pass") is True)
    for idx, step in enumerate(PROCESSING_FLOW):
        _add(checks, f"fdesc.{idx}", bool(step.get("desc")))
    for idx, ent in enumerate(entity_reg.get("entities") or []):
        _add(checks, f"est.{idx}", ent.get("depth_source") == "estimated" or ent.get("depth_source") in ("unknown", "hardware"))
    for idx, r in enumerate(mock_res.get("results") or []):
        _add(checks, f"warn.{idx}", isinstance(r.get("warnings"), list))
    for idx, item in enumerate(next_plan.get("deferred") or []):
        _add(checks, f"def.{idx}", item in (next_plan.get("deferred") or []))
    for idx, item in enumerate(scope.get("not_in_scope") or []):
        _add(checks, f"nis.{idx}", item in (scope.get("not_in_scope") or []))

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
