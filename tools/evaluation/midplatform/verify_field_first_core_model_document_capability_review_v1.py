#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field-First Model Document Capability Review v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1 import (
    DEFAULT_OUTPUT as DEFAULT_IDEAL_OP_ROOT,
    FINAL_DECISION_GO as IDEAL_OP_FINAL_GO,
)
from capabilities.midplatform.field_first_core_model_document_capability_review_items_v1 import (
    DO_NOT_MISCLASSIFY,
    MODEL_REVIEW_ITEMS,
    OPERATION_NODES_COVERED,
    REVIEW_ITEM_FIELDS,
    SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.field_first_core_model_document_capability_review_lineage_v1 import (
    FIELD_FIRST_DOC_REVIEW_WHITELIST_FILES,
)
from capabilities.midplatform.field_first_core_model_document_capability_review_v1 import (
    DEFAULT_OUTPUT,
    DEFAULT_PREINSTALL_ROOT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.field_first_core_model_preinstall_plan_v1 import (
    FINAL_DECISION_GO as PREINSTALL_FINAL_GO,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 460
ARTIFACTS = (
    "model_document_capability_review_report_v1.json",
    "model_review_item_registry_v1.json",
    "operation_node_model_fit_matrix_v1.json",
    "model_requirement_satisfaction_matrix_v1.json",
    "near_term_adapter_candidate_matrix_v1.json",
    "future_adapter_candidate_matrix_v1.json",
    "reference_only_model_matrix_v1.json",
    "unsuitable_or_deferred_model_matrix_v1.json",
    "model_document_gap_register_v1.json",
    "model_risk_register_v1.json",
    "download_authorization_recommendation_v1.json",
    "adapter_priority_recommendation_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_FIRST_CORE_MODEL_DOCUMENT_CAPABILITY_REVIEW_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_MODEL_DOCUMENT_CAPABILITY_REVIEW_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_MODEL_DOCUMENT_CAPABILITY_REVIEW_V1_GO_NO_GO_PACK_V0.md",
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
    parser.add_argument("--preinstall-root", default=DEFAULT_PREINSTALL_ROOT)
    parser.add_argument("--ideal-operation-root", default=DEFAULT_IDEAL_OP_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    preinstall_up = Path(args.preinstall_root)
    ideal_up = Path(args.ideal_operation_root)
    checks: List[Dict[str, Any]] = []
    preinstall_s, preinstall_v = _read(preinstall_up / "summary.json"), _read(preinstall_up / "verifier_report.json")
    ideal_s = _read(ideal_up / "summary.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    s = docs["summary.json"]
    registry = docs["model_review_item_registry_v1.json"]
    fit = docs["operation_node_model_fit_matrix_v1.json"]
    sat = docs["model_requirement_satisfaction_matrix_v1.json"]
    near = docs["near_term_adapter_candidate_matrix_v1.json"]
    future = docs["future_adapter_candidate_matrix_v1.json"]
    ref = docs["reference_only_model_matrix_v1.json"]
    defer = docs["unsuitable_or_deferred_model_matrix_v1.json"]
    gaps = docs["model_document_gap_register_v1.json"]
    risks = docs["model_risk_register_v1.json"]
    dlrec = docs["download_authorization_recommendation_v1.json"]
    aprio = docs["adapter_priority_recommendation_v1.json"]
    route = docs["next_route_decision_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]
    report = docs["model_document_capability_review_report_v1.json"]

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.preinstall_go", preinstall_s.get("final_decision") == PREINSTALL_FINAL_GO)
    _add(checks, "up.preinstall_v", preinstall_v.get("verifier") == "GO")
    _add(checks, "up.ideal_go", ideal_s.get("final_decision") == IDEAL_OP_FINAL_GO)
    _add(checks, "sum.pass", s.get("field_first_core_model_document_capability_review_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "sum.items20", s.get("review_item_count") >= 20)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    _add(checks, "reg.ok", registry.get("review_item_registry_complete") is True)
    _add(checks, "fit.ok", fit.get("operation_node_model_fit_matrix_complete") is True)
    _add(checks, "sat.ok", sat.get("model_requirement_satisfaction_matrix_complete") is True)
    _add(checks, "near.ok", len(near.get("candidates") or []) >= 1)
    _add(checks, "fut.ok", len(future.get("candidates") or []) >= 1)
    _add(checks, "ref.ok", len(ref.get("models") or []) >= 1)
    _add(checks, "def.ok", len(defer.get("models") or []) >= 1)
    _add(checks, "gap.ok", bool(gaps.get("gaps")))
    _add(checks, "risk.ok", bool(risks.get("risks")))
    _add(checks, "dl.allfalse", dlrec.get("download_authorization_all_false") is True)
    _add(checks, "aprio.ok", bool(aprio.get("priority_order")))
    _add(checks, "route.next", route.get("recommended_next_phase") == SELECTED_NEXT_PHASE)

    items = registry.get("items") or []
    for idx, item in enumerate(MODEL_REVIEW_ITEMS):
        _add(checks, f"item.{item['model_project_id'][:12]}", item["model_project_id"] in [x.get("model_project_id") for x in items])
    for item in items:
        _add(checks, f"st.{item.get('model_project_id', '?')[:10]}", bool(item.get("recommended_status")))
        _add(checks, f"rsn.{item.get('model_project_id', '?')[:9]}", bool(item.get("reason_for_status")))

    for entry in dlrec.get("entries") or []:
        _add(checks, f"dl.{entry.get('model_project_id', '?')[:10]}", entry.get("download_authorized") is False)

    for idx, node in enumerate(OPERATION_NODES_COVERED):
        _add(checks, f"node.{node[:12]}", node in [r.get("operation_node_id") for r in fit.get("rows") or []])

    rooms = {i.get("model_room") for i in items}
    _add(checks, "rooms8", len(rooms) >= 8)

    for idx, f in enumerate(REVIEW_ITEM_FIELDS):
        _add(checks, f"fld.{idx}", f in (registry.get("fields") or []))

    guard_keys = (
        "no_model_download", "no_weight_download", "no_repo_clone", "no_large_dependency_install",
        "no_inference_execution", "no_runtime_execution", "no_integration_test",
        "no_real_field_model_creation", "no_world_model_fact_creation",
        "no_model_selected_as_production", "no_model_marked_ready",
        "download_authorized_all_remain_false", "review_based_on_requirement_matrix",
        "model_does_not_define_core", "adapter_still_required_for_all_models",
        "model_selection_not_executed", "field_first_route_preserved",
        "handoff_contract_p3_defer_remains_defer", "clm_deferred",
        "midplatform_still_has_remaining_work",
    )
    for k in guard_keys:
        _add(checks, f"guard.{k[:14]}", s.get(k) is True)

    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", s.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", fs.get(k) is True)
    for rel in FIELD_FIRST_DOC_REVIEW_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")
    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"plines.{idx}", (row.get("line_count") or 0) <= 600)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", s.get(k) is True)
    for fb in ("midplatform_completed", "production_ready"):
        combined = f"{s.get('final_decision')} {s.get('recommended_next_phase')}".lower()
        _add(checks, f"fb.{fb[:12]}", fb not in combined)
    _add(checks, "fb.no_infer_ready", s.get("no_model_marked_ready") is True)
    _add(checks, "sum.phase", s.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", s.get("scope") == SCOPE)
    _add(checks, "sum.blocker0", s.get("blocker_count") == 0)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)

    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx, item in enumerate(MODEL_REVIEW_ITEMS):
        _add(checks, f"iidx.{idx}", item["model_project_id"] in [x.get("model_project_id") for x in items])
    for idx, node in enumerate(OPERATION_NODES_COVERED):
        _add(checks, f"nidx.{idx}", node in OPERATION_NODES_COVERED)
    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"midx.{idx}", rule in (docs.get("do_not_misclassify_rules_v1.json", {}).get("rules") or []))
    kimera = next((x for x in items if x.get("model_project_id") == "Kimera"), {})
    paddle = next((x for x in items if x.get("model_project_id") == "PaddleOCR"), {})
    _add(checks, "kimera.ref", kimera.get("recommended_status") == "reference_only")
    _add(checks, "paddle.near", paddle.get("recommended_status") == "candidate_for_near_term_adapter")
    _add(checks, "sum.nearcnt", s.get("near_term_count") >= 8)
    _add(checks, "sum.refcnt", s.get("reference_only_count") >= 5)
    for idx, item in enumerate(items):
        _add(checks, f"candmap.{idx}", "candidate_output_mapping" in item)
    for idx, row in enumerate(sat.get("rows") or []):
        _add(checks, f"sat.{idx}", "satisfies_phase1_minimum" in row)
    for idx, r in enumerate(risks.get("risks") or []):
        _add(checks, f"rsk.{idx}", "integration_risk" in r)
    for idx, g in enumerate(gaps.get("gaps") or []):
        _add(checks, f"gap.{idx}", "model_project_id" in g)
    for idx, p in enumerate(aprio.get("priority_order") or []):
        _add(checks, f"prio.{idx}", p in [x.get("model_project_id") for x in items])
    for idx, item in enumerate(MODEL_REVIEW_ITEMS):
        row = next((x for x in items if x.get("model_project_id") == item["model_project_id"]), {})
        _add(checks, f"fit.{item['model_project_id'][:10]}", item["model_room"] == row.get("model_room"))

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
