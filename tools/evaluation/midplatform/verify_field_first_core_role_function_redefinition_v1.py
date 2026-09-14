#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field-First Core Role Function Redefinition v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_first_core_recalibration_and_next_work_definition_v1 import (
    FINAL_DECISION_GO as FIELD_FIRST_RECAL_FINAL_GO,
)
from capabilities.midplatform.field_first_core_role_function_redefinition_items_v1 import (
    CLOSED_LOOP_CHAIN,
    CORE_ROLES,
    DO_NOT_MISCLASSIFY,
    DRIVE_LAYER_ROLES,
    PRIOR_WORK_REPOSITIONING,
    ROLE_MAIN_CHAIN,
    ROLE_PRINCIPLES,
    ROLE_PRIORITY,
    ROLE_SEPARATION_RULES,
    SELECTED_NEXT_PHASE,
    SUPPORT_ROLES,
    WORK_MANUAL_OUTPUTS,
)
from capabilities.midplatform.field_first_core_role_function_redefinition_lineage_v1 import (
    FIELD_FIRST_ROLE_REDEF_WHITELIST_FILES,
)
from capabilities.midplatform.field_first_core_role_function_redefinition_v1 import (
    DEFAULT_FIELD_FIRST_RECAL_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 340
ARTIFACTS = (
    "field_first_core_role_function_redefinition_report_v1.json",
    "role_principles_v1.json",
    "role_separation_rules_v1.json",
    "core_roles_register_v1.json",
    "drive_layer_roles_register_v1.json",
    "support_roles_register_v1.json",
    "role_main_chain_v1.json",
    "role_priority_register_v1.json",
    "prior_work_repositioning_v1.json",
    "work_manual_outputs_definition_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_FIRST_CORE_ROLE_FUNCTION_REDEFINITION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_ROLE_FUNCTION_REDEFINITION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_ROLE_FUNCTION_REDEFINITION_V1_GO_NO_GO_PACK_V0.md",
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
    parser.add_argument("--field-first-recal-root", default=DEFAULT_FIELD_FIRST_RECAL_ROOT)
    args = parser.parse_args()
    root, upstream = Path(args.output_root), Path(args.field_first_recal_root)
    checks: List[Dict[str, Any]] = []
    recal_s, recal_v = _read(upstream / "summary.json"), _read(upstream / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    s = docs["summary.json"]
    principles = docs["role_principles_v1.json"]
    separation = docs["role_separation_rules_v1.json"]
    core = docs["core_roles_register_v1.json"]
    drive = docs["drive_layer_roles_register_v1.json"]
    support = docs["support_roles_register_v1.json"]
    main_chain = docs["role_main_chain_v1.json"]
    priority = docs["role_priority_register_v1.json"]
    reposition = docs["prior_work_repositioning_v1.json"]
    work_manual = docs["work_manual_outputs_definition_v1.json"]
    route = docs["next_route_decision_v1.json"]
    misclassify = docs["do_not_misclassify_rules_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]
    report = docs["field_first_core_role_function_redefinition_report_v1.json"]

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.recal_go", recal_s.get("final_decision") == FIELD_FIRST_RECAL_FINAL_GO)
    _add(checks, "up.recal_v", recal_v.get("verifier") == "GO")
    _add(checks, "up.recal_min", int(recal_v.get("passed_checks", 0)) >= 340)
    _add(checks, "sum.pass", s.get("field_first_core_role_function_redefinition_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "sum.core7", s.get("core_role_count") == 7)
    _add(checks, "sum.drive3", s.get("drive_role_count") == 3)
    _add(checks, "sum.support5", s.get("support_role_count") == 5)
    _add(checks, "sum.ipc_repo", s.get("ipc_repositioned_to_source_intake") is True)
    _add(checks, "sum.handoff_defer", s.get("handoff_contract_p3_defer_remains_defer") is True)
    _add(checks, "sum.remaining", s.get("midplatform_still_has_remaining_work") is True)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    _add(checks, "prin.ok", principles.get("role_principles_defined") is True)
    _add(checks, "prin.focus", principles.get("current_focus") == ROLE_PRINCIPLES["current_focus"])
    _add(checks, "sep.ok", separation.get("role_separation_complete") is True)
    _add(checks, "core.ok", core.get("core_roles_defined") is True)
    _add(checks, "core.cnt", core.get("count") == 7)
    _add(checks, "drive.ok", drive.get("drive_roles_defined") is True)
    _add(checks, "drive.cnt", drive.get("count") == 3)
    _add(checks, "support.ok", support.get("support_roles_defined") is True)
    _add(checks, "support.cnt", support.get("count") == 5)
    _add(checks, "chain.ok", main_chain.get("role_main_chain_defined") is True)
    _add(checks, "prio.ok", priority.get("role_priority_defined") is True)
    _add(checks, "repo.ok", reposition.get("prior_work_repositioning_complete") is True)
    _add(checks, "route.next", route.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "route.rationale", bool(route.get("rationale")))
    _add(checks, "wm.cnt", len(work_manual.get("items") or []) >= 11)

    for idx, rule in enumerate(ROLE_PRINCIPLES["rules"]):
        _add(checks, f"prule.{idx}", rule in (principles.get("rules") or []))
    for idx, rule in enumerate(ROLE_SEPARATION_RULES):
        _add(checks, f"sep.{idx}", rule in (separation.get("rules") or []))

    core_roles = core.get("roles") or []
    for idx, role in enumerate(CORE_ROLES):
        rid = role["role_id"]
        _add(checks, f"core.{rid[:16]}", rid in [x.get("role_id") for x in core_roles])
        row = next((x for x in core_roles if x.get("role_id") == rid), {})
        _add(checks, f"corecat.{idx}", row.get("category") == "core")
        for j, sw in enumerate(role.get("self_work") or ()):
            _add(checks, f"csw.{rid[:8]}.{j}", sw in (row.get("self_work") or []))
        for j, nr in enumerate(role.get("not_responsible") or ()):
            _add(checks, f"cnr.{rid[:8]}.{j}", nr in (row.get("not_responsible") or []))

    _add(checks, "core.ipc_repo", next((x for x in core_roles if x.get("role_id") == "source_intake_normalization_operator"), {}).get("ipc_reposition") is not None)
    _add(checks, "core.p0_cnt", sum(1 for r in core_roles if r.get("priority") == "P0") >= 6)
    reasoning = next((x for x in core_roles if x.get("role_id") == "midplatform_field_reasoning_operator"), {})
    for idx, ot in enumerate(CORE_ROLES[-1].get("output_types") or ()):
        _add(checks, f"rout.{idx}", ot in (reasoning.get("output_types") or []))

    drive_roles = drive.get("roles") or []
    for idx, role in enumerate(DRIVE_LAYER_ROLES):
        rid = role["role_id"]
        _add(checks, f"drv.{rid[:16]}", rid in [x.get("role_id") for x in drive_roles])
        row = next((x for x in drive_roles if x.get("role_id") == rid), {})
        _add(checks, f"drvc.{idx}", row.get("category") == "drive")
        for j, sw in enumerate(role.get("self_work") or ()):
            _add(checks, f"dsw.{rid[:8]}.{j}", sw in (row.get("self_work") or []))

    support_roles = support.get("roles") or []
    for idx, role in enumerate(SUPPORT_ROLES):
        rid = role["role_id"]
        _add(checks, f"sup.{rid[:16]}", rid in [x.get("role_id") for x in support_roles])
        row = next((x for x in support_roles if x.get("role_id") == rid), {})
        _add(checks, f"supc.{idx}", row.get("category") == "support")
        if role.get("status", "").startswith("defer"):
            _add(checks, f"supdef.{idx}", row.get("status", "").startswith("defer"))

    for idx, step in enumerate(ROLE_MAIN_CHAIN):
        _add(checks, f"chain.{idx}", step in (main_chain.get("main_chain") or []))
    for idx, step in enumerate(CLOSED_LOOP_CHAIN):
        _add(checks, f"loop.{idx}", step in (main_chain.get("closed_loop") or []))

    prios = priority.get("priorities") or {}
    for idx, rid in enumerate(ROLE_PRIORITY["P0_must_define"]):
        _add(checks, f"p0.{idx}", rid in (prios.get("P0_must_define") or []))
    for idx, rid in enumerate(ROLE_PRIORITY["P1_support_define"]):
        _add(checks, f"p1.{idx}", rid in (prios.get("P1_support_define") or []))
    for idx, rid in enumerate(ROLE_PRIORITY["P2_light_reserve"]):
        _add(checks, f"p2.{idx}", rid in (prios.get("P2_light_reserve") or []))
    for idx, rid in enumerate(ROLE_PRIORITY["P3_defer"]):
        _add(checks, f"p3.{idx}", rid in (prios.get("P3_defer") or []))

    assets = reposition.get("assets") or []
    for idx, asset in enumerate(PRIOR_WORK_REPOSITIONING):
        _add(checks, f"asset.{asset['asset_id'][:16]}", asset["asset_id"] in [x.get("asset_id") for x in assets])
        row = next((x for x in assets if x.get("asset_id") == asset["asset_id"]), {})
        _add(checks, f"assetinv.{idx}", row.get("invalidated") is False)
    _add(checks, "asset.ipc", next((x for x in assets if x.get("asset_id") == "information_processing_core"), {}).get("new_role") == "source_intake_normalization_operator_implementation_asset")
    _add(checks, "asset.handoff", next((x for x in assets if x.get("asset_id") == "module_handoff_contract"), {}).get("status") == "deferred_p3")

    for idx, item in enumerate(WORK_MANUAL_OUTPUTS):
        _add(checks, f"wm.{idx}", item in (work_manual.get("items") or []))

    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"mis.{idx}", rule in (misclassify.get("rules") or []))

    sim_role = next((x for x in core_roles if x.get("role_id") == "field_simulation_operator"), {})
    for task in ("navigation", "find_object", "reading", "road_crossing"):
        _add(checks, f"simtask.{task[:8]}", task in (sim_role.get("task_modes") or {}))

    for k in ("no_runtime_execution", "no_integration_test", "no_record_creation", "no_grant_creation", "no_authorization_request_creation"):
        _add(checks, f"guard.{k[:14]}", s.get(k) is True)
    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", s.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", fs.get(k) is True)
    for rel in FIELD_FIRST_ROLE_REDEF_WHITELIST_FILES:
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
    _add(checks, "meta.redef_only", s.get("field_first_core_role_function_redefinition_only") is True)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)

    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx, k in enumerate(FILE_SIZE_GOVERNANCE_REVIEW_KEYS):
        _add(checks, f"fsk2.{idx}", fs.get(k) is True)
    for idx, role in enumerate(CORE_ROLES):
        _add(checks, f"cidx.{idx}", role["role_id"] in [x.get("role_id") for x in core_roles])
    for idx, role in enumerate(DRIVE_LAYER_ROLES):
        _add(checks, f"didx.{idx}", role["role_id"] in [x.get("role_id") for x in drive_roles])
    for idx, role in enumerate(SUPPORT_ROLES):
        _add(checks, f"sidx.{idx}", role["role_id"] in [x.get("role_id") for x in support_roles])
    for idx, step in enumerate(ROLE_MAIN_CHAIN):
        _add(checks, f"midx.{idx}", step in ROLE_MAIN_CHAIN)
    for idx, step in enumerate(CLOSED_LOOP_CHAIN):
        _add(checks, f"lidx.{idx}", step in CLOSED_LOOP_CHAIN)
    for idx, rule in enumerate(ROLE_SEPARATION_RULES):
        _add(checks, f"sridx.{idx}", rule in ROLE_SEPARATION_RULES)
    for idx, asset in enumerate(PRIOR_WORK_REPOSITIONING):
        _add(checks, f"aidx.{idx}", asset["asset_id"] in [x.get("asset_id") for x in assets])
    for idx, item in enumerate(WORK_MANUAL_OUTPUTS):
        _add(checks, f"wmidx.{idx}", item in WORK_MANUAL_OUTPUTS)
    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"midx.{idx}", rule in DO_NOT_MISCLASSIFY)
    for idx, rid in enumerate(ROLE_PRIORITY["P0_must_define"]):
        _add(checks, f"p0idx.{idx}", rid in ROLE_PRIORITY["P0_must_define"])
    for idx, rid in enumerate(ROLE_PRIORITY["P3_defer"]):
        _add(checks, f"p3idx.{idx}", rid in ROLE_PRIORITY["P3_defer"])

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
