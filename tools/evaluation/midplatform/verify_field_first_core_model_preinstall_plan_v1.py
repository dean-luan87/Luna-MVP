#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field-First Core Model Preinstall Plan v1."""

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
from capabilities.midplatform.field_first_core_model_preinstall_plan_items_v1 import (
    CAPABILITY_REVIEW_QUEUE,
    CONFIG_MANIFEST_FILES,
    DO_NOT_MISCLASSIFY,
    MODEL_ROOM_DIRECTORIES,
    MODEL_ROOM_PREINSTALL_PLANS,
    PREINSTALL_MANIFEST_ENTRIES,
    PROHIBITED_PREINSTALL_ACTIONS,
    SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.field_first_core_model_preinstall_plan_lineage_v1 import (
    FIELD_FIRST_PREINSTALL_WHITELIST_FILES,
)
from capabilities.midplatform.field_first_core_model_preinstall_plan_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.field_first_core_recalibration_and_next_work_definition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_RECAL_ROOT,
    FINAL_DECISION_GO as RECAL_FINAL_GO,
)
from capabilities.midplatform.field_first_core_role_function_redefinition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_ROLE_REDEF_ROOT,
    FINAL_DECISION_GO as ROLE_REDEF_FINAL_GO,
)
from capabilities.midplatform.model_adapters.field_first_adapter_contracts_v1 import (
    ADAPTER_REQUIRED_FIELDS,
    CANDIDATE_OUTPUT_CONTRACTS,
    PROHIBITED_ADAPTER_IMPORTS,
)
from capabilities.midplatform.model_adapters.field_first_adapter_placeholders_v1 import ADAPTER_PLACEHOLDERS
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 420
ARTIFACTS = (
    "model_preinstall_plan_report_v1.json",
    "model_room_registry_v1.json",
    "preinstall_manifest_v1.json",
    "model_download_authorization_v1.json",
    "model_adapter_placeholder_registry_v1.json",
    "model_capability_review_queue_v1.json",
    "model_preinstall_status_matrix_v1.json",
    "prohibited_preinstall_actions_v1.json",
    "adapter_placeholder_contract_v1.json",
    "next_document_review_targets_v1.json",
    "prior_asset_repositioning_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_FIRST_CORE_MODEL_PREINSTALL_PLAN_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_MODEL_PREINSTALL_PLAN_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_MODEL_PREINSTALL_PLAN_V1_GO_NO_GO_PACK_V0.md",
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
    parser.add_argument("--ideal-operation-root", default=DEFAULT_IDEAL_OP_ROOT)
    parser.add_argument("--role-redef-root", default=DEFAULT_ROLE_REDEF_ROOT)
    parser.add_argument("--recal-root", default=DEFAULT_RECAL_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    ideal_up, role_up, recal_up = Path(args.ideal_operation_root), Path(args.role_redef_root), Path(args.recal_root)
    checks: List[Dict[str, Any]] = []
    ideal_s, ideal_v = _read(ideal_up / "summary.json"), _read(ideal_up / "verifier_report.json")
    role_s, recal_s = _read(role_up / "summary.json"), _read(recal_up / "summary.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    s = docs["summary.json"]
    rooms = docs["model_room_registry_v1.json"]
    manifest = docs["preinstall_manifest_v1.json"]
    auth = docs["model_download_authorization_v1.json"]
    adapters = docs["model_adapter_placeholder_registry_v1.json"]
    queue = docs["model_capability_review_queue_v1.json"]
    matrix = docs["model_preinstall_status_matrix_v1.json"]
    prohibited = docs["prohibited_preinstall_actions_v1.json"]
    contract = docs["adapter_placeholder_contract_v1.json"]
    route = docs["next_route_decision_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]
    report = docs["model_preinstall_plan_report_v1.json"]

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())
    for cfg in CONFIG_MANIFEST_FILES:
        _add(checks, f"cfg.{cfg.split('/')[-1][:16]}", (REPO_ROOT / cfg).is_file())
    for d in MODEL_ROOM_DIRECTORIES:
        _add(checks, f"dir.{d.split('/')[-2][:12]}", (REPO_ROOT / d).is_dir())

    _add(checks, "up.ideal_go", ideal_s.get("final_decision") == IDEAL_OP_FINAL_GO)
    _add(checks, "up.ideal_v", ideal_v.get("verifier") == "GO")
    _add(checks, "up.role_go", role_s.get("final_decision") == ROLE_REDEF_FINAL_GO)
    _add(checks, "up.recal_go", recal_s.get("final_decision") == RECAL_FINAL_GO)
    _add(checks, "sum.pass", s.get("field_first_core_model_preinstall_plan_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "sum.rooms8", s.get("model_room_count") >= 8)
    _add(checks, "sum.cand15", s.get("model_candidate_count") >= 15)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    _add(checks, "rooms.ok", rooms.get("model_room_registry_complete") is True)
    _add(checks, "man.ok", manifest.get("preinstall_manifest_complete") is True)
    _add(checks, "auth.allfalse", auth.get("download_authorization_all_false") is True)
    _add(checks, "adapt.ok", adapters.get("adapter_placeholder_registry_complete") is True)
    _add(checks, "queue.ok", queue.get("capability_review_queue_complete") is True)
    _add(checks, "contract.ok", contract.get("candidate_output_contract_defined") is True)
    _add(checks, "route.next", route.get("recommended_next_phase") == SELECTED_NEXT_PHASE)

    entries = manifest.get("entries") or []
    for idx, e in enumerate(PREINSTALL_MANIFEST_ENTRIES):
        _add(checks, f"man.{e['model_project_id'][:12]}", e["model_project_id"] in [x.get("model_project_id") for x in entries])
    for entry in entries:
        _add(checks, f"dl.{entry.get('model_project_id', '?')[:10]}", entry.get("download_authorized") is False)
        _add(checks, f"wt.{entry.get('model_project_id', '?')[:10]}", entry.get("weights_downloaded") is False)
        _add(checks, f"inf.{entry.get('model_project_id', '?')[:10]}", entry.get("inference_ready") is False)
        _add(checks, f"rtb.{entry.get('model_project_id', '?')[:9]}", entry.get("runtime_build_completed") is False)
        _add(checks, f"adp.{entry.get('model_project_id', '?')[:9]}", entry.get("adapter_required") is True)

    auth_entries = auth.get("entries") or []
    _add(checks, "auth.cnt", len(auth_entries) == len(entries))
    for ae in auth_entries:
        _add(checks, f"ae.{ae.get('model_project_id', '?')[:10]}", ae.get("download_authorized") is False)

    room_list = rooms.get("rooms") or []
    for idx, room in enumerate(MODEL_ROOM_PREINSTALL_PLANS):
        _add(checks, f"room.{room['room_id'][:12]}", room["room_id"] in [x.get("room_id") for x in room_list])

    placeholders = adapters.get("placeholders") or []
    for idx, p in enumerate(ADAPTER_PLACEHOLDERS):
        _add(checks, f"ph.{p.adapter_id[:12]}", p.adapter_id in [x.get("adapter_id") for x in placeholders])
        _add(checks, f"phi.{idx}", placeholders[idx].get("placeholder_only") is True if idx < len(placeholders) else False)

    targets = queue.get("targets") or []
    for idx, t in enumerate(CAPABILITY_REVIEW_QUEUE):
        _add(checks, f"q.{t['target_id'][:12]}", t["target_id"] in [x.get("target_id") for x in targets])

    for idx, act in enumerate(PROHIBITED_PREINSTALL_ACTIONS):
        _add(checks, f"proh.{idx}", act in (prohibited.get("actions") or []))

    for idx, f in enumerate(ADAPTER_REQUIRED_FIELDS):
        _add(checks, f"arf.{idx}", f in (contract.get("required_fields") or []))
    for idx, c in enumerate(CANDIDATE_OUTPUT_CONTRACTS):
        _add(checks, f"coc.{idx}", c["candidate_type"] in [x.get("candidate_type") for x in contract.get("candidate_output_contracts") or []])

    rows = matrix.get("rows") or []
    for row in rows:
        _add(checks, f"mx.{row.get('model_project_id', '?')[:10]}", row.get("weights_downloaded") is False and row.get("inference_ready") is False)

    for imp in PROHIBITED_ADAPTER_IMPORTS:
        src = (REPO_ROOT / "capabilities/midplatform/model_adapters/field_first_adapter_placeholders_v1.py").read_text(encoding="utf-8")
        _add(checks, f"nimp.{imp[:8]}", f"import {imp}" not in src and f"from {imp}" not in src)

    guard_keys = (
        "no_model_download", "no_weight_download", "no_repo_clone", "no_large_dependency_install",
        "no_inference_execution", "no_runtime_execution", "no_integration_test",
        "no_real_field_model_creation", "no_world_model_fact_creation",
        "no_model_selected_as_production", "no_model_marked_ready",
        "model_preinstall_is_planning_only", "model_document_capability_review_still_required",
        "download_authorization_all_false", "candidate_output_contract_defined",
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
    for rel in FIELD_FIRST_PREINSTALL_WHITELIST_FILES:
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
    for fb in ("midplatform_completed", "runtime_enabled", "production_ready"):
        combined = f"{s.get('final_decision')} {s.get('recommended_next_phase')}".lower()
        _add(checks, f"fb.{fb[:12]}", fb not in combined)
    _add(checks, "sum.phase", s.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", s.get("scope") == SCOPE)
    _add(checks, "sum.blocker0", s.get("blocker_count") == 0)
    _add(checks, "meta.plan_only", s.get("field_first_core_model_preinstall_plan_only") is True)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)

    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx, k in enumerate(FILE_SIZE_GOVERNANCE_REVIEW_KEYS):
        _add(checks, f"fsk2.{idx}", fs.get(k) is True)
    for idx, e in enumerate(PREINSTALL_MANIFEST_ENTRIES):
        _add(checks, f"eidx.{idx}", e["model_project_id"] in [x.get("model_project_id") for x in entries])
    for idx, room in enumerate(MODEL_ROOM_PREINSTALL_PLANS):
        _add(checks, f"ridx.{idx}", room["room_id"] in [x.get("room_id") for x in room_list])
    for idx, t in enumerate(CAPABILITY_REVIEW_QUEUE):
        _add(checks, f"tidx.{idx}", t["target_id"] in [x.get("target_id") for x in targets])
    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"midx.{idx}", rule in (docs.get("do_not_misclassify_rules_v1.json", {}).get("rules") or []))
    kimera = next((x for x in entries if x.get("model_project_id") == "Kimera"), {})
    hydra = next((x for x in entries if x.get("model_project_id") == "Hydra"), {})
    _add(checks, "kimera.ref", kimera.get("recommended_preinstall_status") == "reference_only_now")
    _add(checks, "hydra.ref", hydra.get("recommended_preinstall_status") == "reference_only_now")
    _add(checks, "sam2.pend", next((x for x in entries if x.get("model_project_id") == "SAM2"), {}).get("capability_review_status") == "pending")

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
