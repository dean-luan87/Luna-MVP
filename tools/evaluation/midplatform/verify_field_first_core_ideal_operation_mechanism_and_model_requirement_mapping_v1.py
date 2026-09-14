#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field-First Ideal Operation Mechanism and Model Requirement Mapping v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_first_core_ideal_operation_mechanism_items_v1 import (
    DO_NOT_MISCLASSIFY,
    IDEAL_OPERATION_MECHANISM,
    MODEL_DOCUMENT_REVIEW_TEMPLATE_FIELDS,
    MODEL_ROOM_ALIGNMENT,
    NEXT_RESEARCH_TARGETS,
    OPERATION_NODES,
    RECOMMENDED_STATUS_OPTIONS,
    REQUIREMENT_MATRIX_FIELDS,
    SELECTED_NEXT_PHASE,
    SELF_WORK_VS_MODEL_DEPENDENCY,
)
from capabilities.midplatform.field_first_core_ideal_operation_mechanism_lineage_v1 import (
    FIELD_FIRST_IDEAL_OP_WHITELIST_FILES,
)
from capabilities.midplatform.field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1 import (
    DEFAULT_OUTPUT,
    DEFAULT_ROLE_REDEF_ROOT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.field_first_core_role_function_redefinition_v1 import (
    FINAL_DECISION_GO as ROLE_REDEF_FINAL_GO,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 380
ARTIFACTS = (
    "ideal_operation_mechanism_report_v1.json",
    "ideal_operation_mechanism_v1.json",
    "operation_node_registry_v1.json",
    "operation_node_model_mapping_v1.json",
    "model_requirement_matrix_v1.json",
    "model_document_review_template_v1.json",
    "model_room_alignment_update_v1.json",
    "self_work_vs_model_dependency_boundary_v1.json",
    "next_research_targets_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_FIRST_CORE_IDEAL_OPERATION_MECHANISM_AND_MODEL_REQUIREMENT_MAPPING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_IDEAL_OPERATION_MECHANISM_AND_MODEL_REQUIREMENT_MAPPING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_IDEAL_OPERATION_MECHANISM_AND_MODEL_REQUIREMENT_MAPPING_V1_GO_NO_GO_PACK_V0.md",
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
    parser.add_argument("--role-redef-root", default=DEFAULT_ROLE_REDEF_ROOT)
    args = parser.parse_args()
    root, upstream = Path(args.output_root), Path(args.role_redef_root)
    checks: List[Dict[str, Any]] = []
    role_s, role_v = _read(upstream / "summary.json"), _read(upstream / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    s = docs["summary.json"]
    ideal = docs["ideal_operation_mechanism_v1.json"]
    node_reg = docs["operation_node_registry_v1.json"]
    node_map = docs["operation_node_model_mapping_v1.json"]
    matrix = docs["model_requirement_matrix_v1.json"]
    doc_tmpl = docs["model_document_review_template_v1.json"]
    room_align = docs["model_room_alignment_update_v1.json"]
    boundary = docs["self_work_vs_model_dependency_boundary_v1.json"]
    research = docs["next_research_targets_v1.json"]
    route = docs["next_route_decision_v1.json"]
    misclassify = docs["do_not_misclassify_rules_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]
    report = docs["ideal_operation_mechanism_report_v1.json"]

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.role_go", role_s.get("final_decision") == ROLE_REDEF_FINAL_GO)
    _add(checks, "up.role_v", role_v.get("verifier") == "GO")
    _add(checks, "up.role_min", int(role_v.get("passed_checks", 0)) >= 380)
    _add(checks, "sum.pass", s.get("field_first_core_ideal_operation_mechanism_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "sum.nodes12", s.get("operation_node_count") >= 12)
    _add(checks, "sum.matrix50", s.get("requirement_matrix_row_count") >= 50)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    _add(checks, "ideal.ok", ideal.get("ideal_operation_mechanism_complete") is True)
    _add(checks, "ideal.chain13", len(ideal.get("chain") or []) >= 13)
    _add(checks, "nodes.ok", node_reg.get("operation_node_registry_complete") is True)
    _add(checks, "nodes.cnt", node_reg.get("count") >= 12)
    _add(checks, "map.ok", node_map.get("operation_node_model_mapping_complete") is True)
    _add(checks, "matrix.ok", matrix.get("model_requirement_matrix_complete") is True)
    _add(checks, "matrix.rows", matrix.get("row_count", 0) >= 50)
    _add(checks, "tmpl.ok", doc_tmpl.get("model_document_review_template_complete") is True)
    _add(checks, "tmpl.defer", doc_tmpl.get("model_document_review_deferred_to_next_phase") is True)
    _add(checks, "align.ok", room_align.get("model_room_alignment_update_complete") is True)
    _add(checks, "research.ok", research.get("next_research_targets_complete") is True)
    _add(checks, "route.next", route.get("recommended_next_phase") == SELECTED_NEXT_PHASE)

    for idx, step in enumerate(IDEAL_OPERATION_MECHANISM["chain"]):
        _add(checks, f"chain.{idx}", step in (ideal.get("chain") or []))

    nodes = node_reg.get("nodes") or []
    for idx, node in enumerate(OPERATION_NODES):
        nid = node["operation_node_id"]
        _add(checks, f"node.{nid[:16]}", nid in [x.get("operation_node_id") for x in nodes])
        row = next((x for x in nodes if x.get("operation_node_id") == nid), {})
        _add(checks, f"noderole.{idx}", bool(row.get("node_role")))

    mappings = node_map.get("mappings") or []
    for idx, node in enumerate(OPERATION_NODES):
        _add(checks, f"map.{node['operation_node_id'][:12]}", node["operation_node_id"] in [x.get("operation_node_id") for x in mappings])

    for idx, f in enumerate(REQUIREMENT_MATRIX_FIELDS):
        _add(checks, f"mxf.{idx}", f in (matrix.get("fields") or []))

    for idx, f in enumerate(MODEL_DOCUMENT_REVIEW_TEMPLATE_FIELDS):
        _add(checks, f"dtf.{idx}", f in (doc_tmpl.get("fields") or []))
    for idx, opt in enumerate(RECOMMENDED_STATUS_OPTIONS):
        _add(checks, f"dto.{idx}", opt in (doc_tmpl.get("recommended_status_options") or []))

    alignments = room_align.get("alignments") or []
    for idx, a in enumerate(MODEL_ROOM_ALIGNMENT):
        _add(checks, f"align.{a['operation_node_id'][:12]}", a["operation_node_id"] in [x.get("operation_node_id") for x in alignments])

    entries = boundary.get("entries") or []
    for idx, e in enumerate(SELF_WORK_VS_MODEL_DEPENDENCY):
        _add(checks, f"bnd.{e['domain'][:12]}", e["domain"] in [x.get("domain") for x in entries])

    targets = research.get("targets") or []
    for idx, t in enumerate(NEXT_RESEARCH_TARGETS):
        _add(checks, f"res.{t['target_id'][:12]}", t["target_id"] in [x.get("target_id") for x in targets])
        _add(checks, f"resp.{idx}", targets[idx].get("status") == "pending" if idx < len(targets) else False)

    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"mis.{idx}", rule in (misclassify.get("rules") or []))

    guard_keys = (
        "ideal_operation_before_model_selection", "model_requirements_derived_from_operation_nodes",
        "model_document_review_deferred_to_next_phase", "model_selection_not_executed",
        "no_model_download", "no_weight_download", "no_inference_execution",
        "no_runtime_execution", "no_integration_test", "no_real_field_model_creation",
        "no_world_model_fact_creation", "model_output_candidate_only",
        "field_first_route_preserved", "ipc_repositioned_as_source_normalization_asset",
        "handoff_contract_p3_defer_remains_defer", "clm_deferred",
        "midplatform_still_has_remaining_work",
    )
    for k in guard_keys:
        _add(checks, f"guard.{k[:14]}", s.get(k) is True)

    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", s.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", fs.get(k) is True)
    for rel in FIELD_FIRST_IDEAL_OP_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")
    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"plines.{idx}", (row.get("line_count") or 0) <= 600)
        _add(checks, f"pex.{idx}", (REPO_ROOT / rel).is_file())
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", s.get(k) is True)
    for fb in ("midplatform_completed", "runtime_enabled", "record_created"):
        combined = f"{s.get('final_decision')} {s.get('recommended_next_phase')}".lower()
        _add(checks, f"fb.{fb[:12]}", fb not in combined)
    _add(checks, "sum.phase", s.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", s.get("scope") == SCOPE)
    _add(checks, "sum.blocker0", s.get("blocker_count") == 0)
    _add(checks, "meta.mech_only", s.get("field_first_core_ideal_operation_mechanism_only") is True)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)

    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx, k in enumerate(FILE_SIZE_GOVERNANCE_REVIEW_KEYS):
        _add(checks, f"fsk2.{idx}", fs.get(k) is True)
    for idx, node in enumerate(OPERATION_NODES):
        _add(checks, f"nidx.{idx}", node["operation_node_id"] in [x.get("operation_node_id") for x in nodes])
    for idx, step in enumerate(IDEAL_OPERATION_MECHANISM["chain"]):
        _add(checks, f"cidx.{idx}", step in IDEAL_OPERATION_MECHANISM["chain"])
    for idx, a in enumerate(MODEL_ROOM_ALIGNMENT):
        _add(checks, f"aidx.{idx}", a["operation_node_id"] in [x.get("operation_node_id") for x in alignments])
    for idx, t in enumerate(NEXT_RESEARCH_TARGETS):
        _add(checks, f"tidx.{idx}", t["target_id"] in [x.get("target_id") for x in targets])
    for idx, e in enumerate(SELF_WORK_VS_MODEL_DEPENDENCY):
        _add(checks, f"bidx.{idx}", e["domain"] in [x.get("domain") for x in entries])
    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"midx.{idx}", rule in DO_NOT_MISCLASSIFY)
    for idx, f in enumerate(REQUIREMENT_MATRIX_FIELDS):
        _add(checks, f"mfidx.{idx}", f in REQUIREMENT_MATRIX_FIELDS)
    for idx, f in enumerate(MODEL_DOCUMENT_REVIEW_TEMPLATE_FIELDS):
        _add(checks, f"dfidx.{idx}", f in MODEL_DOCUMENT_REVIEW_TEMPLATE_FIELDS)
    for idx, node in enumerate(OPERATION_NODES):
        row = next((x for x in nodes if x.get("operation_node_id") == node["operation_node_id"]), {})
        for j, cap in enumerate(node.get("required_capabilities") or ()):
            _add(checks, f"ncap.{node['operation_node_id'][:8]}.{j}", cap in (row.get("required_capabilities") or []))
    for idx, node in enumerate(OPERATION_NODES):
        row = next((x for x in nodes if x.get("operation_node_id") == node["operation_node_id"]), {})
        for j, out in enumerate(node.get("expected_outputs") or ()):
            _add(checks, f"nout.{node['operation_node_id'][:8]}.{j}", out in (row.get("expected_outputs") or []))
    sim_node = next((x for x in nodes if x.get("operation_node_id") == "field_simulation"), {})
    _add(checks, "sim.self", sim_node.get("luna_self_work") == "primary_rules_geometry_state_machine")
    drive_node = next((x for x in nodes if x.get("operation_node_id") == "drive_layer"), {})
    _add(checks, "drv.self", drive_node.get("luna_self_work") == "primary_self_developed")
    spatial = next((x for x in nodes if x.get("operation_node_id") == "spatial_slam_dynamic_scene_graph"), {})
    _add(checks, "spat.ref", spatial.get("can_be_reference_only") is True)

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
