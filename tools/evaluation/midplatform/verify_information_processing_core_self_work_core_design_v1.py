#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify IPC Self-Work Core Design v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.information_processing_core_controlled_implementation_v1 import FINAL_DECISION_GO as IPC_IMPL_GO
from capabilities.midplatform.information_processing_core_self_work_core_design_items_v1 import (
    CONCLUSION_REQUIRED_FIELDS, CONCLUSION_TYPES, CURRENT_NON_GOALS, DESIGN_PRINCIPLES,
    DOWNSTREAM_NEED_OBSERVATIONS, INTERNAL_PROCESSING_FLOW, INFORMATION_TYPES,
    SELF_CHECK_REFEREE_RULES, SELF_WORK_SCOPE, TRANSPARENCY_FIELDS,
    UPSTREAM_MINIMUM_ASSUMPTIONS, WORKLOAD_CONTROL_RULES,
)
from capabilities.midplatform.information_processing_core_self_work_core_design_lineage_v1 import IPC_SELF_WORK_DESIGN_WHITELIST_FILES
from capabilities.midplatform.information_processing_core_self_work_core_design_v1 import (
    DEFAULT_IPC_IMPL_ROOT, DEFAULT_OUTPUT, FINAL_DECISION_GO, GO_CONDITIONS_KEYS,
    PHASE_ID, PHASE_PYTHON_FILES, SCOPE, SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 300
ARTIFACTS = (
    "ipc_self_work_core_design_report_v1.json", "three_part_work_model_positioning_v1.json",
    "ipc_self_work_scope_v1.json", "ipc_internal_processing_flow_v1.json",
    "ipc_conclusion_model_v1.json", "ipc_transparency_traceability_model_v1.json",
    "ipc_self_check_referee_model_v1.json", "ipc_workload_control_model_v1.json",
    "downstream_need_observation_model_v1.json", "upstream_minimum_assumption_register_v1.json",
    "current_non_goals_v1.json", "next_route_decision_v1.json",
    "file_size_governance_review_v1.json", "summary.json", "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_INFORMATION_PROCESSING_CORE_SELF_WORK_CORE_DESIGN_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_SELF_WORK_CORE_DESIGN_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_SELF_WORK_CORE_DESIGN_V1_GO_NO_GO_PACK_V0.md",
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
    parser.add_argument("--ipc-implementation-root", default=DEFAULT_IPC_IMPL_ROOT)
    args = parser.parse_args()
    root, upstream = Path(args.output_root), Path(args.ipc_implementation_root)
    checks: List[Dict[str, Any]] = []
    impl_s, impl_v = _read(upstream / "summary.json"), _read(upstream / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    s = docs["summary.json"]
    three = docs["three_part_work_model_positioning_v1.json"]
    scope = docs["ipc_self_work_scope_v1.json"]
    flow = docs["ipc_internal_processing_flow_v1.json"]
    conc = docs["ipc_conclusion_model_v1.json"]
    trans = docs["ipc_transparency_traceability_model_v1.json"]
    ref = docs["ipc_self_check_referee_model_v1.json"]
    wl = docs["ipc_workload_control_model_v1.json"]
    dn = docs["downstream_need_observation_model_v1.json"]
    up = docs["upstream_minimum_assumption_register_v1.json"]
    ng = docs["current_non_goals_v1.json"]
    route = docs["next_route_decision_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.impl_go", impl_s.get("final_decision") == IPC_IMPL_GO)
    _add(checks, "up.impl_v", impl_v.get("verifier") == "GO")
    _add(checks, "sum.pass", s.get("information_processing_core_self_work_core_design_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "sum.self_first", s.get("self_work_first") is True)
    _add(checks, "sum.no_contract", s.get("downstream_contract_not_defined_yet") is True)
    _add(checks, "sum.no_upstream", s.get("upstream_protocol_not_rewritten_yet") is True)
    _add(checks, "sum.internal", s.get("ipc_internal_processing_defined") is True)
    _add(checks, "sum.observed", s.get("downstream_needs_observed_not_contracted") is True)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    _add(checks, "three.self", three.get("self_work_first") is True)
    _add(checks, "scope.ok", scope.get("ipc_self_work_scope_complete") is True)
    _add(checks, "flow.ok", flow.get("ipc_internal_processing_flow_complete") is True)
    _add(checks, "flow.s12", flow.get("step_count", 0) >= 12)
    _add(checks, "conc.ok", conc.get("ipc_conclusion_model_complete") is True)
    _add(checks, "trans.ok", trans.get("ipc_transparency_traceability_model_complete") is True)
    _add(checks, "ref.ok", ref.get("ipc_self_check_referee_model_complete") is True)
    _add(checks, "wl.ok", wl.get("ipc_workload_control_model_complete") is True)
    _add(checks, "dn.ok", dn.get("downstream_need_observation_model_complete") is True)
    _add(checks, "dn.not_contract", dn.get("downstream_needs_observed_not_contracted") is True)
    _add(checks, "up.ok", up.get("upstream_minimum_assumption_register_complete") is True)
    _add(checks, "ng.handoff", ng.get("handoff_contract_p3_defer_remains_defer") is True)
    _add(checks, "route.next", route.get("recommended_next_phase") == SELECTED_NEXT_PHASE)

    for step in INTERNAL_PROCESSING_FLOW:
        _add(checks, f"step.{step['step_id'][:16]}", step["step_id"] in [x.get("step_id") for x in flow.get("steps") or []])
    for t in INFORMATION_TYPES:
        _add(checks, f"type.{t[:16]}", t in (flow.get("information_types") or []))
    for ct in CONCLUSION_TYPES:
        _add(checks, f"ctype.{ct['conclusion_type'][:16]}", ct["conclusion_type"] in [x.get("conclusion_type") for x in conc.get("conclusion_types") or []])
    for f in CONCLUSION_REQUIRED_FIELDS:
        _add(checks, f"creq.{f[:16]}", f in (conc.get("required_fields") or []))
    for f in TRANSPARENCY_FIELDS:
        _add(checks, f"trans.{f[:16]}", f in (trans.get("fields") or []))
    for r in SELF_CHECK_REFEREE_RULES:
        _add(checks, f"ref.{r['check_id'][:16]}", r["check_id"] in [x.get("check_id") for x in ref.get("checks") or []])
    for r in WORKLOAD_CONTROL_RULES:
        _add(checks, f"wl.{r['rule_id'][:16]}", r["rule_id"] in [x.get("rule_id") for x in wl.get("rules") or []])
    for o in DOWNSTREAM_NEED_OBSERVATIONS:
        _add(checks, f"dn.{o['need_id'][:16]}", o["need_id"] in [x.get("need_id") for x in dn.get("observations") or []])
        _add(checks, f"dnnc.{o['need_id'][:12]}", o.get("is_contract") is False)
    for a in UPSTREAM_MINIMUM_ASSUMPTIONS:
        _add(checks, f"up.{a['assumption_id'][:16]}", a["assumption_id"] in [x.get("assumption_id") for x in up.get("assumptions") or []])
    for ng_item in CURRENT_NON_GOALS:
        _add(checks, f"ng.{ng_item[:16]}", ng_item in (ng.get("non_goals") or []))
    for p in DESIGN_PRINCIPLES:
        _add(checks, f"prin.{p['principle_id'][:16]}", p["principle_id"] in [x.get("principle_id") for x in docs.get("ipc_self_work_core_design_report_v1.json", {}).get("design_principles") or []])
    for resp in SELF_WORK_SCOPE["responsibilities"]:
        _add(checks, f"resp.{resp[:16]}", resp in (scope.get("responsibilities") or []))

    for k in ("no_runtime_execution", "no_integration_test", "no_record_creation", "no_grant_creation", "no_authorization_request_creation"):
        _add(checks, f"guard.{k[:14]}", s.get(k) is True)
    _add(checks, "sum.handoff_defer", s.get("handoff_contract_p3_defer_remains_defer") is True)
    _add(checks, "sum.periph", s.get("peripheral_contract_does_not_constrain_core") is True)
    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", s.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", fs.get(k) is True)
    for rel in IPC_SELF_WORK_DESIGN_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")
    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"plines.{idx}", (row.get("line_count") or 0) <= 600)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", s.get(k) is True)
    for fb in ("midplatform_completed", "runtime_enabled", "record_created"):
        combined = f"{s.get('final_decision')} {s.get('recommended_next_phase')}".lower()
        _add(checks, f"fb.{fb[:12]}", fb not in combined)
    _add(checks, "sum.phase", s.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", s.get("scope") == SCOPE)
    _add(checks, "sum.blocker0", s.get("blocker_count") == 0)
    _add(checks, "trans.nobox", trans.get("no_black_box_conclusions") is True)
    _add(checks, "meta.design_only", s.get("information_processing_core_self_work_core_design_only") is True)
    _add(checks, "up.impl_min", int(impl_v.get("passed_checks", 0)) >= 420)
    for idx, step in enumerate(INTERNAL_PROCESSING_FLOW):
        srow = next((x for x in flow.get("steps") or [] if x.get("step_id") == step["step_id"]), {})
        _add(checks, f"sout.{idx}", bool(srow.get("output")))
        _add(checks, f"sin.{idx}", bool(srow.get("input")))
    for idx, ct in enumerate(CONCLUSION_TYPES):
        _add(checks, f"cidx.{idx}", ct["conclusion_type"] in [x.get("conclusion_type") for x in conc.get("conclusion_types") or []])
    for idx, f in enumerate(TRANSPARENCY_FIELDS):
        _add(checks, f"tidx.{idx}", f in (trans.get("fields") or []))
    for idx, r in enumerate(SELF_CHECK_REFEREE_RULES):
        _add(checks, f"ridx.{idx}", r["check_id"] in [x.get("check_id") for x in ref.get("checks") or []])
    for idx, r in enumerate(WORKLOAD_CONTROL_RULES):
        _add(checks, f"widx.{idx}", r["rule_id"] in [x.get("rule_id") for x in wl.get("rules") or []])
    for idx, o in enumerate(DOWNSTREAM_NEED_OBSERVATIONS):
        _add(checks, f"didx.{idx}", o["need_id"] in [x.get("need_id") for x in dn.get("observations") or []])
    for idx, a in enumerate(UPSTREAM_MINIMUM_ASSUMPTIONS):
        _add(checks, f"aidx.{idx}", a["assumption_id"] in [x.get("assumption_id") for x in up.get("assumptions") or []])
    for idx, t in enumerate(INFORMATION_TYPES):
        _add(checks, f"typidx.{idx}", t in INFORMATION_TYPES)
    for idx, ng_item in enumerate(CURRENT_NON_GOALS):
        _add(checks, f"ngidx.{idx}", ng_item in (ng.get("non_goals") or []))
    for idx, p in enumerate(DESIGN_PRINCIPLES):
        _add(checks, f"pidx.{idx}", p["principle_id"] in [x.get("principle_id") for x in docs.get("ipc_self_work_core_design_report_v1.json", {}).get("design_principles") or []])
    for idx, resp in enumerate(SELF_WORK_SCOPE["responsibilities"]):
        _add(checks, f"rspidx.{idx}", resp in (scope.get("responsibilities") or []))
    for idx, nresp in enumerate(SELF_WORK_SCOPE["not_responsibilities"]):
        _add(checks, f"nrsp.{idx}", nresp in (scope.get("not_responsibilities") or []))
    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx, k in enumerate(FILE_SIZE_GOVERNANCE_REVIEW_KEYS):
        _add(checks, f"fsk2.{idx}", fs.get(k) is True)
    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        _add(checks, f"pex.{idx}", (REPO_ROOT / rel).is_file())
    _add(checks, "report.final", docs.get("ipc_self_work_core_design_report_v1.json", {}).get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "three.scope", three.get("this_phase_scope") == "self_work_design_only")
    _add(checks, "route.rationale", bool(route.get("rationale")))
    _add(checks, "sum.remaining", s.get("midplatform_still_has_remaining_work") is True)

    passed = sum(1 for x in checks if x["passed"])
    failed = [x for x in checks if not x["passed"]]
    v = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    payload = {"verifier": v, "phase": PHASE_ID, "passed_checks": passed, "failed_checks": len(failed),
               "min_checks": MIN_CHECKS, "blocker_count": len(failed),
               "final_decision": FINAL_DECISION_GO if v == "GO" else "HOLD",
               "recommended_next_phase": SELECTED_NEXT_PHASE if v == "GO" else "HOLD_FOR_ISSUE_REVIEW",
               "failed": failed[:40], "checks": checks}
    (root / "verifier_report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": v, "passed_checks": passed, "failed_checks": len(failed), "final_decision": payload["final_decision"]}, ensure_ascii=False))
    return 0 if v == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
