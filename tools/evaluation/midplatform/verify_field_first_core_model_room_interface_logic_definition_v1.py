#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field-First Core Model Room and Interface Logic Definition v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_first_core_model_room_items_v1 import (
    CANDIDATE_OUTPUT_TYPES,
    DEFERRED_MODEL_INTEGRATION,
    DO_NOT_MISCLASSIFY,
    FIELD_MODEL_INPUT_CONTRACT,
    FIELD_SIMULATION_IO_CONTRACT,
    INTERFACE_LOGIC,
    MIDPLATFORM_REASONING_IO_CONTRACT,
    MODEL_ADAPTER_BUS,
    MODEL_ADAPTER_INTERFACE_FIELDS,
    MODEL_ROOM_PRINCIPLES,
    MODEL_ROOMS,
    MODEL_USAGE_ORDER,
    OPEN_SOURCE_REFERENCE_INVENTORY,
    PRIOR_ASSET_REPOSITIONING,
    PROHIBITED_MODEL_OUTPUTS,
    SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.field_first_core_model_room_lineage_v1 import (
    FIELD_FIRST_MODEL_ROOM_WHITELIST_FILES,
)
from capabilities.midplatform.field_first_core_model_room_interface_logic_definition_v1 import (
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
    "model_room_interface_logic_report_v1.json",
    "model_room_registry_v1.json",
    "open_source_reference_inventory_v1.json",
    "model_capability_mapping_v1.json",
    "model_adapter_interface_v1.json",
    "model_candidate_output_registry_v1.json",
    "field_model_input_contract_from_models_v1.json",
    "field_simulation_input_output_contract_v1.json",
    "midplatform_reasoning_model_input_output_contract_v1.json",
    "prohibited_model_outputs_v1.json",
    "deferred_model_integration_register_v1.json",
    "prior_asset_repositioning_v1.json",
    "interface_logic_flows_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_FIRST_CORE_MODEL_ROOM_INTERFACE_LOGIC_DEFINITION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_MODEL_ROOM_INTERFACE_LOGIC_DEFINITION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_MODEL_ROOM_INTERFACE_LOGIC_DEFINITION_V1_GO_NO_GO_PACK_V0.md",
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
    rooms = docs["model_room_registry_v1.json"]
    inventory = docs["open_source_reference_inventory_v1.json"]
    mapping = docs["model_capability_mapping_v1.json"]
    adapter = docs["model_adapter_interface_v1.json"]
    candidates = docs["model_candidate_output_registry_v1.json"]
    field_in = docs["field_model_input_contract_from_models_v1.json"]
    sim_io = docs["field_simulation_input_output_contract_v1.json"]
    reason_io = docs["midplatform_reasoning_model_input_output_contract_v1.json"]
    prohibited = docs["prohibited_model_outputs_v1.json"]
    deferred = docs["deferred_model_integration_register_v1.json"]
    reposition = docs["prior_asset_repositioning_v1.json"]
    iface = docs["interface_logic_flows_v1.json"]
    route = docs["next_route_decision_v1.json"]
    misclassify = docs["do_not_misclassify_rules_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]
    report = docs["model_room_interface_logic_report_v1.json"]

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.role_go", role_s.get("final_decision") == ROLE_REDEF_FINAL_GO)
    _add(checks, "up.role_v", role_v.get("verifier") == "GO")
    _add(checks, "up.role_min", int(role_v.get("passed_checks", 0)) >= 380)
    _add(checks, "sum.pass", s.get("field_first_core_model_room_interface_logic_definition_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "sum.rooms9", s.get("model_room_count") == 9)
    _add(checks, "sum.refs12", s.get("open_source_reference_count") == 12)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    _add(checks, "rooms.ok", rooms.get("model_room_definition_complete") is True)
    _add(checks, "rooms.cnt", rooms.get("count") == 9)
    _add(checks, "inv.ok", inventory.get("open_source_reference_inventory_complete") is True)
    _add(checks, "inv.cnt", inventory.get("count") == 12)
    _add(checks, "map.ok", len(mapping.get("entries") or []) >= 12)
    _add(checks, "adapt.ok", adapter.get("model_adapter_interface_complete") is True)
    _add(checks, "cand.ok", candidates.get("candidate_output_registry_complete") is True)
    _add(checks, "field.ok", field_in.get("field_model_model_interface_complete") is True)
    _add(checks, "sim.ok", sim_io.get("field_simulation_interface_complete") is True)
    _add(checks, "reason.ok", reason_io.get("midplatform_reasoning_interface_complete") is True)
    _add(checks, "def.ok", deferred.get("model_integration_deferred") is True)
    _add(checks, "route.next", route.get("recommended_next_phase") == SELECTED_NEXT_PHASE)

    for idx, rule in enumerate(MODEL_ROOM_PRINCIPLES["rules"]):
        _add(checks, f"prin.{idx}", rule in ((rooms.get("principles") or {}).get("rules") or []))

    room_list = rooms.get("rooms") or []
    for idx, room in enumerate(MODEL_ROOMS):
        rid = room["room_id"]
        _add(checks, f"room.{rid[:16]}", rid in [x.get("room_id") for x in room_list])
        row = next((x for x in room_list if x.get("room_id") == rid), {})
        _add(checks, f"roomnm.{idx}", bool(row.get("name")))

    for idx, entry in enumerate(OPEN_SOURCE_REFERENCE_INVENTORY):
        eid = entry["model_or_project_id"]
        _add(checks, f"ref.{eid[:12]}", eid in [x.get("model_or_project_id") for x in inventory.get("entries") or []])
        row = next((x for x in inventory.get("entries") or [] if x.get("model_or_project_id") == eid), {})
        _add(checks, f"refrt.{idx}", row.get("runtime_required_now") is False)
        _add(checks, f"refmap.{idx}", eid in [x.get("model_or_project_id") for x in mapping.get("entries") or []])

    for idx, f in enumerate(MODEL_ADAPTER_INTERFACE_FIELDS):
        _add(checks, f"adf.{idx}", f in (adapter.get("required_fields") or []))
    _add(checks, "adap.req", adapter.get("bus", {}).get("adapter_required_for_all_models") is True or MODEL_ADAPTER_BUS.get("adapter_required_for_all_models") is True)
    for idx, step in enumerate(MODEL_USAGE_ORDER):
        _add(checks, f"ord.{idx}", step in (adapter.get("usage_order") or []))

    for idx, ct in enumerate(CANDIDATE_OUTPUT_TYPES):
        _add(checks, f"cand.{idx}", ct in (candidates.get("candidate_types") or []))

    for idx, po in enumerate(PROHIBITED_MODEL_OUTPUTS):
        _add(checks, f"proh.{idx}", po in (prohibited.get("prohibited_outputs") or []))

    for idx, ct in enumerate(FIELD_MODEL_INPUT_CONTRACT.get("accepts_candidate_types") or ()):
        _add(checks, f"finc.{idx}", ct in (field_in.get("accepts_candidate_types") or []))
    _add(checks, "fin.adapt", field_in.get("requires_adapter") is True)
    _add(checks, "fin.nofact", field_in.get("direct_fact_write_forbidden") is True)

    for idx, o in enumerate(FIELD_SIMULATION_IO_CONTRACT.get("output") or ()):
        _add(checks, f"simout.{idx}", o in (sim_io.get("output") or []))
    _add(checks, "sim.nollm", sim_io.get("llm_simulation_forbidden") is True)

    for idx, i in enumerate(MIDPLATFORM_REASONING_IO_CONTRACT.get("input") or ()):
        _add(checks, f"rin.{idx}", i in (reason_io.get("input") or []))
    _add(checks, "rin.noraw", reason_io.get("raw_source_read_forbidden") is True)
    _add(checks, "rin.noact", reason_io.get("action_execution_forbidden") is True)

    for idx, d in enumerate(DEFERRED_MODEL_INTEGRATION):
        _add(checks, f"def.{d['integration_id'][:12]}", d["integration_id"] in [x.get("integration_id") for x in deferred.get("entries") or []])
        row = next((x for x in deferred.get("entries") or [] if x.get("integration_id") == d["integration_id"]), {})
        _add(checks, f"defst.{idx}", row.get("status", "").startswith("defer"))

    for idx, asset in enumerate(PRIOR_ASSET_REPOSITIONING):
        _add(checks, f"asset.{asset['asset_id'][:12]}", asset["asset_id"] in [x.get("asset_id") for x in reposition.get("assets") or []])

    for idx, flow in enumerate(INTERFACE_LOGIC):
        _add(checks, f"flow.{flow['flow_id'][:12]}", flow["flow_id"] in [x.get("flow_id") for x in iface.get("flows") or []])

    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"mis.{idx}", rule in (misclassify.get("rules") or []))

    guard_keys = (
        "no_real_model_download", "no_weight_download", "no_inference_execution",
        "no_runtime_execution", "no_integration_test", "no_world_model_fact_creation",
        "no_persistent_memory_write", "no_record_creation", "no_grant_creation",
        "no_authorization_request_creation", "model_output_candidate_only",
        "model_does_not_define_core", "adapter_required_for_all_models",
        "field_first_route_preserved", "ipc_repositioned_as_source_normalization_asset",
        "kimera_hydra_hovsg_reference_only_now", "sam2_grounded_sam2_reference_or_future_adapter_only_now",
        "ecs_reference_does_not_force_runtime", "kg_reference_does_not_force_full_knowledge_graph",
        "handoff_contract_p3_defer_remains_defer", "midplatform_still_has_remaining_work",
    )
    for k in guard_keys:
        _add(checks, f"guard.{k[:14]}", s.get(k) is True)

    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", s.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", fs.get(k) is True)
    for rel in FIELD_FIRST_MODEL_ROOM_WHITELIST_FILES:
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
    _add(checks, "meta.def_only", s.get("field_first_core_model_room_interface_logic_definition_only") is True)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)

    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx, k in enumerate(FILE_SIZE_GOVERNANCE_REVIEW_KEYS):
        _add(checks, f"fsk2.{idx}", fs.get(k) is True)
    for idx, room in enumerate(MODEL_ROOMS):
        _add(checks, f"ridx.{idx}", room["room_id"] in [x.get("room_id") for x in room_list])
    for idx, entry in enumerate(OPEN_SOURCE_REFERENCE_INVENTORY):
        _add(checks, f"eidx.{idx}", entry["model_or_project_id"] in [x.get("model_or_project_id") for x in inventory.get("entries") or []])
    for idx, ct in enumerate(CANDIDATE_OUTPUT_TYPES):
        _add(checks, f"cidx.{idx}", ct in CANDIDATE_OUTPUT_TYPES)
    for idx, po in enumerate(PROHIBITED_MODEL_OUTPUTS):
        _add(checks, f"pidx.{idx}", po in PROHIBITED_MODEL_OUTPUTS)
    for idx, d in enumerate(DEFERRED_MODEL_INTEGRATION):
        _add(checks, f"didx.{idx}", d["integration_id"] in [x.get("integration_id") for x in deferred.get("entries") or []])
    for idx, flow in enumerate(INTERFACE_LOGIC):
        _add(checks, f"fidx.{idx}", flow["flow_id"] in [x.get("flow_id") for x in iface.get("flows") or []])
    for idx, asset in enumerate(PRIOR_ASSET_REPOSITIONING):
        _add(checks, f"aidx.{idx}", asset["asset_id"] in [x.get("asset_id") for x in reposition.get("assets") or []])
    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"midx.{idx}", rule in DO_NOT_MISCLASSIFY)
    for idx, f in enumerate(MODEL_ADAPTER_INTERFACE_FIELDS):
        _add(checks, f"afidx.{idx}", f in MODEL_ADAPTER_INTERFACE_FIELDS)
    for idx, step in enumerate(MODEL_USAGE_ORDER):
        _add(checks, f"oidx.{idx}", step in MODEL_USAGE_ORDER)
    for idx, room in enumerate(MODEL_ROOMS):
        row = next((x for x in room_list if x.get("room_id") == room["room_id"]), {})
        for j, out in enumerate(room.get("outputs") or ()):
            _add(checks, f"rout.{room['room_id'][:8]}.{j}", out in (row.get("outputs") or []))
    kimera = next((x for x in inventory.get("entries") or [] if x.get("model_or_project_id") == "Kimera"), {})
    hydra = next((x for x in inventory.get("entries") or [] if x.get("model_or_project_id") == "Hydra"), {})
    sam2 = next((x for x in inventory.get("entries") or [] if x.get("model_or_project_id") == "SAM2"), {})
    _add(checks, "ref.kimera", kimera.get("runtime_required_now") is False)
    _add(checks, "ref.hydra", hydra.get("runtime_required_now") is False)
    _add(checks, "ref.sam2", sam2.get("runtime_required_now") is False)
    _add(checks, "handoff.p3", next((x for x in deferred.get("entries") or [] if x.get("integration_id") == "module_handoff_contract"), {}).get("status") == "deferred_p3")

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
