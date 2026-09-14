#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field-First Core Recalibration and Next Work Definition v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_first_core_recalibration_and_next_work_definition_items_v1 import (
    ATTRIBUTE_TIERS,
    CORE_ROUTE_ADJUSTMENT,
    DEFERRED_ROUTES,
    DO_NOT_MISCLASSIFY,
    DRIVE_LAYER_FIELD,
    FIELD_BOUNDARY,
    FIELD_CONTINUITY,
    FIELD_FIRST_CONCEPTS,
    FIELD_MODEL_LAYERS,
    FIELD_SIMULATION,
    IPC_REPOSITIONING,
    MIDPLATFORM_REASONING_INPUT,
    NEW_ROUTE,
    NEXT_WORK_ITEMS,
    OLD_ROUTE,
    PERCEPTION_LOOP,
    SELECTED_NEXT_PHASE,
    SOURCE_MOUNTING,
)
from capabilities.midplatform.field_first_core_recalibration_and_next_work_definition_lineage_v1 import (
    FIELD_FIRST_RECAL_WHITELIST_FILES,
)
from capabilities.midplatform.field_first_core_recalibration_and_next_work_definition_v1 import (
    DEFAULT_IPC_DESIGN_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.information_processing_core_self_work_core_design_v1 import (
    FINAL_DECISION_GO as IPC_DESIGN_FINAL_GO,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 340
ARTIFACTS = (
    "field_first_core_recalibration_report_v1.json",
    "core_route_adjustment_v1.json",
    "field_first_core_concept_definition_v1.json",
    "field_model_architecture_sketch_v1.json",
    "source_mounting_model_v1.json",
    "field_boundary_model_v1.json",
    "field_continuity_model_v1.json",
    "field_simulation_model_v1.json",
    "midplatform_reasoning_input_model_v1.json",
    "drive_layer_field_relationship_v1.json",
    "perception_request_loop_model_v1.json",
    "ipc_repositioning_review_v1.json",
    "deferred_route_register_v1.json",
    "next_work_definition_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_FIRST_CORE_RECALIBRATION_AND_NEXT_WORK_DEFINITION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_RECALIBRATION_AND_NEXT_WORK_DEFINITION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_RECALIBRATION_AND_NEXT_WORK_DEFINITION_V1_GO_NO_GO_PACK_V0.md",
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
    parser.add_argument("--ipc-design-root", default=DEFAULT_IPC_DESIGN_ROOT)
    args = parser.parse_args()
    root, upstream = Path(args.output_root), Path(args.ipc_design_root)
    checks: List[Dict[str, Any]] = []
    design_s, design_v = _read(upstream / "summary.json"), _read(upstream / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    s = docs["summary.json"]
    route_adj = docs["core_route_adjustment_v1.json"]
    concepts = docs["field_first_core_concept_definition_v1.json"]
    arch = docs["field_model_architecture_sketch_v1.json"]
    source = docs["source_mounting_model_v1.json"]
    boundary = docs["field_boundary_model_v1.json"]
    continuity = docs["field_continuity_model_v1.json"]
    simulation = docs["field_simulation_model_v1.json"]
    reasoning = docs["midplatform_reasoning_input_model_v1.json"]
    drive = docs["drive_layer_field_relationship_v1.json"]
    perception = docs["perception_request_loop_model_v1.json"]
    ipc_repo = docs["ipc_repositioning_review_v1.json"]
    deferred = docs["deferred_route_register_v1.json"]
    next_work = docs["next_work_definition_v1.json"]
    route = docs["next_route_decision_v1.json"]
    misclassify = docs["do_not_misclassify_rules_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]
    report = docs["field_first_core_recalibration_report_v1.json"]

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.design_go", design_s.get("final_decision") == IPC_DESIGN_FINAL_GO)
    _add(checks, "up.design_v", design_v.get("verifier") == "GO")
    _add(checks, "up.design_min", int(design_v.get("passed_checks", 0)) >= 300)
    _add(checks, "sum.pass", s.get("field_first_core_recalibration_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "sum.field_first", s.get("field_first_midplatform_core") is True)
    _add(checks, "sum.ipc_not_center", s.get("ipc_no_longer_direct_center") is True)
    _add(checks, "sum.handoff_defer", s.get("handoff_contract_p3_defer_remains_defer") is True)
    _add(checks, "sum.remaining", s.get("midplatform_still_has_remaining_work") is True)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    _add(checks, "route.adj_ok", route_adj.get("core_route_adjustment_complete") is True)
    _add(checks, "route.ff", route_adj.get("field_first_midplatform_core") is True)
    _add(checks, "route.ipc_nc", route_adj.get("ipc_no_longer_direct_center") is True)
    _add(checks, "concept.ok", concepts.get("field_first_core_concept_complete") is True)
    _add(checks, "arch.ok", arch.get("field_model_architecture_sketch_complete") is True)
    _add(checks, "arch.layers3", len(arch.get("layers") or []) >= 3)
    _add(checks, "source.ok", source.get("model_id") == "source_mounting_model_v1")
    _add(checks, "boundary.ok", boundary.get("model_id") == "field_boundary_model_v1")
    _add(checks, "continuity.ok", continuity.get("model_id") == "field_continuity_model_v1")
    _add(checks, "simulation.ok", simulation.get("model_id") == "field_simulation_model_v1")
    _add(checks, "reasoning.ok", reasoning.get("model_id") == "midplatform_reasoning_input_model_v1")
    _add(checks, "drive.ok", drive.get("model_id") == "drive_layer_field_relationship_v1")
    _add(checks, "perception.ok", perception.get("model_id") == "perception_request_loop_model_v1")
    _add(checks, "ipc_repo.ok", ipc_repo.get("ipc_not_invalidated") is True)
    _add(checks, "next_work.ok", next_work.get("next_work_definition_complete") is True)
    _add(checks, "next_work.cnt", len(next_work.get("items") or []) >= 14)
    _add(checks, "route.next", route.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "route.rationale", bool(route.get("rationale")))

    for idx, step in enumerate(OLD_ROUTE):
        _add(checks, f"old.{idx}", step in (route_adj.get("old_route") or []))
    for idx, step in enumerate(NEW_ROUTE):
        _add(checks, f"new.{idx}", step in (route_adj.get("new_route") or []))
    _add(checks, "route.key_change", route_adj.get("key_change") == CORE_ROUTE_ADJUSTMENT["key_change"])

    for key in ("world_model", "field_model", "relationship"):
        _add(checks, f"concept.{key[:12]}", bool(concepts.get(key)))
    for idx, task in enumerate(FIELD_FIRST_CONCEPTS["midplatform_core_phase1"]):
        _add(checks, f"core1.{idx}", task in (concepts.get("midplatform_core_phase1") or []))

    for idx, layer in enumerate(FIELD_MODEL_LAYERS):
        _add(checks, f"layer.{layer['layer_id'][:12]}", layer["layer_id"] in [x.get("layer_id") for x in arch.get("layers") or []])
        _add(checks, f"layp.{idx}", bool(layer.get("purpose")))
        _add(checks, f"laye.{idx}", bool(layer.get("examples")))

    for idx, tier in enumerate(ATTRIBUTE_TIERS):
        _add(checks, f"tier.{tier['tier'][:12]}", tier["tier"] in [x.get("tier") for x in arch.get("attribute_tiers") or []])
        _add(checks, f"tierx.{idx}", bool(tier.get("examples")))

    for idx, step in enumerate(SOURCE_MOUNTING["path"]):
        _add(checks, f"srcpath.{idx}", step in (source.get("path") or []))
    for idx, st in enumerate(SOURCE_MOUNTING["source_types"]):
        _add(checks, f"srctype.{idx}", st in (source.get("source_types") or []))
    for idx, f in enumerate(SOURCE_MOUNTING["source_profile_fields"]):
        _add(checks, f"srcpf.{idx}", f in (source.get("source_profile_fields") or []))
    _add(checks, "src.principle", source.get("principle") == SOURCE_MOUNTING["principle"])

    _add(checks, "bound.std", boundary.get("standard") == FIELD_BOUNDARY["standard"])
    _add(checks, "bound.rad", boundary.get("default_radius_m") == 20)
    for idx, zone in enumerate(FIELD_BOUNDARY["zones"]):
        _add(checks, f"zone.{idx}", zone[0] in [z[0] if isinstance(z, (list, tuple)) else z.get("zone_id") for z in boundary.get("zones") or []])
    for idx, ta in enumerate(FIELD_BOUNDARY["task_adaptation"]):
        _add(checks, f"taska.{idx}", ta in (boundary.get("task_adaptation") or []))

    for idx, f in enumerate(FIELD_CONTINUITY["field_session_fields"]):
        _add(checks, f"fsess.{idx}", f in (continuity.get("field_session_fields") or []))
    for idx, r in enumerate(FIELD_CONTINUITY["continuity_rules"]):
        _add(checks, f"cont.{idx}", r in (continuity.get("continuity_rules") or []))
    for idx, v in enumerate(FIELD_CONTINUITY["visibility_states"]):
        _add(checks, f"vis.{idx}", v in (continuity.get("visibility_states") or []))

    for idx, mode in enumerate(FIELD_SIMULATION["modes"]):
        _add(checks, f"simmode.{idx}", mode in (simulation.get("modes") or []))
    _add(checks, "sim.out", simulation.get("output_type") == "FieldSimulationResultCandidate")
    for task, modes in FIELD_SIMULATION["task_modes"].items():
        _add(checks, f"simtask.{task[:12]}", task in (simulation.get("task_modes") or {}))
        for idx, m in enumerate(modes):
            tm = (simulation.get("task_modes") or {}).get(task) or []
            _add(checks, f"simtm.{task[:8]}.{idx}", m in tm)

    for idx, r in enumerate(MIDPLATFORM_REASONING_INPUT["reads"]):
        _add(checks, f"read.{idx}", r in (reasoning.get("reads") or []))
    for idx, nr in enumerate(MIDPLATFORM_REASONING_INPUT["does_not_read"]):
        _add(checks, f"noread.{idx}", nr in (reasoning.get("does_not_read") or []))
    for idx, resp in enumerate(MIDPLATFORM_REASONING_INPUT["responsibilities"]):
        _add(checks, f"resp.{idx}", resp in (reasoning.get("responsibilities") or []))
    for idx, fb in enumerate(MIDPLATFORM_REASONING_INPUT["forbidden"]):
        _add(checks, f"forbid.{idx}", fb in (reasoning.get("forbidden") or []))

    _add(checks, "drive.surv", bool(drive.get("survival_drive")))
    _add(checks, "drive.task", bool(drive.get("task_drive")))
    _add(checks, "drive.refl", bool(drive.get("reflection_drive")))

    for idx, step in enumerate(PERCEPTION_LOOP["chain"]):
        _add(checks, f"ploop.{idx}", step in (perception.get("chain") or []))
    for idx, ex in enumerate(PERCEPTION_LOOP["examples"]):
        _add(checks, f"pex.{idx}", ex in (perception.get("examples") or []))
    _add(checks, "ploop.closed", perception.get("closed_loop") == PERCEPTION_LOOP["closed_loop"])

    _add(checks, "ipc.status", ipc_repo.get("ipc_status") == IPC_REPOSITIONING["ipc_status"])
    _add(checks, "ipc.preserved", ipc_repo.get("ipc_prior_work_preserved") is True)
    _add(checks, "ipc.role", bool(ipc_repo.get("ipc_role_in_new_route")))

    for idx, dr in enumerate(DEFERRED_ROUTES):
        _add(checks, f"def.{dr['route_id'][:12]}", dr["route_id"] in [x.get("route_id") for x in deferred.get("routes") or []])
        _add(checks, f"defs.{idx}", (deferred.get("routes") or [{}])[idx].get("status", "").startswith("defer") if idx < len(deferred.get("routes") or []) else False)

    for idx, item in enumerate(NEXT_WORK_ITEMS):
        _add(checks, f"nwi.{idx}", item in (next_work.get("items") or []))

    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"mis.{idx}", rule in (misclassify.get("rules") or []))

    for k in ("no_runtime_execution", "no_integration_test", "no_record_creation", "no_grant_creation", "no_authorization_request_creation"):
        _add(checks, f"guard.{k[:14]}", s.get(k) is True)
    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", s.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", fs.get(k) is True)
    for rel in FIELD_FIRST_RECAL_WHITELIST_FILES:
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
    _add(checks, "meta.recal_only", s.get("field_first_core_recalibration_only") is True)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "report.ff", report.get("field_first_midplatform_core") is True)

    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx, k in enumerate(FILE_SIZE_GOVERNANCE_REVIEW_KEYS):
        _add(checks, f"fsk2.{idx}", fs.get(k) is True)
    for idx, step in enumerate(NEW_ROUTE):
        _add(checks, f"new2.{idx}", step in NEW_ROUTE)
    for idx, step in enumerate(OLD_ROUTE):
        _add(checks, f"old2.{idx}", step in OLD_ROUTE)
    for idx, layer in enumerate(FIELD_MODEL_LAYERS):
        _add(checks, f"lidx.{idx}", layer["layer_id"] in [x.get("layer_id") for x in arch.get("layers") or []])
    for idx, item in enumerate(NEXT_WORK_ITEMS):
        _add(checks, f"nwidx.{idx}", item in NEXT_WORK_ITEMS)
    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"midx.{idx}", rule in DO_NOT_MISCLASSIFY)
    for idx, dr in enumerate(DEFERRED_ROUTES):
        _add(checks, f"didx.{idx}", dr["route_id"] in [x.get("route_id") for x in deferred.get("routes") or []])
    for idx, st in enumerate(SOURCE_MOUNTING["source_types"]):
        _add(checks, f"stidx.{idx}", st in SOURCE_MOUNTING["source_types"])
    for idx, f in enumerate(SOURCE_MOUNTING["source_profile_fields"]):
        _add(checks, f"spfidx.{idx}", f in SOURCE_MOUNTING["source_profile_fields"])
    for idx, tier in enumerate(ATTRIBUTE_TIERS):
        _add(checks, f"tidx.{idx}", tier["tier"] in [x.get("tier") for x in arch.get("attribute_tiers") or []])
    for idx, task in enumerate(FIELD_FIRST_CONCEPTS["midplatform_core_phase1"]):
        _add(checks, f"cidx.{idx}", task in FIELD_FIRST_CONCEPTS["midplatform_core_phase1"])
    for idx, mode in enumerate(FIELD_SIMULATION["modes"]):
        _add(checks, f"smidx.{idx}", mode in FIELD_SIMULATION["modes"])
    for idx, ex in enumerate(PERCEPTION_LOOP["examples"]):
        _add(checks, f"peidx.{idx}", ex in PERCEPTION_LOOP["examples"])
    for idx, step in enumerate(PERCEPTION_LOOP["chain"]):
        _add(checks, f"pcidx.{idx}", step in PERCEPTION_LOOP["chain"])
    for idx, f in enumerate(FIELD_CONTINUITY["field_session_fields"]):
        _add(checks, f"fcidx.{idx}", f in FIELD_CONTINUITY["field_session_fields"])
    for idx, v in enumerate(FIELD_CONTINUITY["visibility_states"]):
        _add(checks, f"vsidx.{idx}", v in FIELD_CONTINUITY["visibility_states"])
    for idx, r in enumerate(MIDPLATFORM_REASONING_INPUT["reads"]):
        _add(checks, f"mridx.{idx}", r in MIDPLATFORM_REASONING_INPUT["reads"])
    for idx, fb in enumerate(MIDPLATFORM_REASONING_INPUT["forbidden"]):
        _add(checks, f"mfidx.{idx}", fb in MIDPLATFORM_REASONING_INPUT["forbidden"])
    for task, modes in FIELD_SIMULATION["task_modes"].items():
        for idx, m in enumerate(modes):
            _add(checks, f"stask.{task[:6]}{idx}", m in modes)

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
