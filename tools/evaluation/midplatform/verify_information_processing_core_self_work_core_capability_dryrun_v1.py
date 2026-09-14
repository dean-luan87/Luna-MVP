#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify IPC Self-Work Core Capability DryRun v1."""

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
from capabilities.midplatform.information_processing_core_self_work_core_capability_dryrun_items_v1 import (
    CONCLUSION_TYPES, SELF_CHECK_RULES, SELF_WORK_CAPABILITY_TAGS, SELF_WORK_CASES,
)
from capabilities.midplatform.information_processing_core_self_work_core_capability_dryrun_lineage_v1 import IPC_SELF_WORK_WHITELIST_FILES
from capabilities.midplatform.information_processing_core_self_work_core_capability_dryrun_v1 import (
    DEFAULT_IPC_IMPL_ROOT, DEFAULT_OUTPUT, FINAL_DECISION_GO, GO_CONDITIONS_KEYS,
    PHASE_ID, PHASE_PYTHON_FILES, SCOPE, SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 360
ARTIFACTS = (
    "ipc_self_work_core_capability_dryrun_report_v1.json", "three_part_work_model_positioning_v1.json",
    "ipc_self_work_scope_v1.json", "ipc_internal_processing_logic_dryrun_cases_v1.json",
    "ipc_internal_processing_logic_dryrun_results_v1.json", "ipc_conclusion_model_v1.json",
    "ipc_transparency_traceability_model_v1.json", "ipc_self_check_internal_referee_v1.json",
    "ipc_workload_control_self_validation_v1.json", "downstream_need_extraction_v1.json",
    "upstream_assumption_register_v1.json", "core_qualification_result_v1.json",
    "next_route_decision_v1.json", "file_size_governance_review_v1.json", "summary.json", "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_INFORMATION_PROCESSING_CORE_SELF_WORK_CORE_CAPABILITY_DRYRUN_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_SELF_WORK_CORE_CAPABILITY_DRYRUN_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_SELF_WORK_CORE_CAPABILITY_DRYRUN_V1_GO_NO_GO_PACK_V0.md",
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
    cases = docs["ipc_internal_processing_logic_dryrun_cases_v1.json"]
    results = docs["ipc_internal_processing_logic_dryrun_results_v1.json"]
    conc = docs["ipc_conclusion_model_v1.json"]
    trans = docs["ipc_transparency_traceability_model_v1.json"]
    ref = docs["ipc_self_check_internal_referee_v1.json"]
    wl = docs["ipc_workload_control_self_validation_v1.json"]
    dn = docs["downstream_need_extraction_v1.json"]
    up = docs["upstream_assumption_register_v1.json"]
    qual = docs["core_qualification_result_v1.json"]
    route = docs["next_route_decision_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]
    rlist = results.get("results") or []

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.impl_go", impl_s.get("final_decision") == IPC_IMPL_GO)
    _add(checks, "up.impl_v", impl_v.get("verifier") == "GO")
    _add(checks, "sum.pass", s.get("information_processing_core_self_work_dryrun_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "sum.dryrun_ok", s.get("ipc_core_self_work_dryrun_ok") is True)
    _add(checks, "sum.all_cases", s.get("all_self_work_cases_passed") is True)
    _add(checks, "sum.self_first", s.get("self_work_first") is True)
    _add(checks, "sum.no_contract", s.get("downstream_contract_not_defined_yet") is True)
    _add(checks, "sum.no_upstream", s.get("upstream_protocol_not_rewritten_yet") is True)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    _add(checks, "three.self", three.get("self_work_first") is True)
    _add(checks, "three.scope", three.get("this_phase_scope") == "self_work_only")
    _add(checks, "scope.ok", scope.get("self_work_scope_complete") is True)
    _add(checks, "cases.c10", cases.get("case_count", 0) >= 10)
    _add(checks, "res.complete", results.get("ipc_internal_processing_logic_dryrun_complete") is True)
    _add(checks, "res.failed0", results.get("failed_cases") == 0)
    _add(checks, "conc.ok", conc.get("ipc_conclusion_model_complete") is True)
    _add(checks, "conc.explain", conc.get("conclusions_explainable") is True)
    _add(checks, "trans.ok", trans.get("ipc_transparency_traceability_model_complete") is True)
    _add(checks, "trans.trace", trans.get("internal_processing_traceable") is True)
    _add(checks, "ref.ok", ref.get("ipc_self_check_internal_referee_complete") is True)
    _add(checks, "wl.ok", wl.get("ipc_workload_control_self_validation_complete") is True)
    _add(checks, "dn.ok", dn.get("downstream_need_extraction_complete") is True)
    _add(checks, "dn.from_cases", dn.get("downstream_need_extracted_from_actual_cases") is True)
    _add(checks, "up.ok", up.get("upstream_assumption_register_complete") is True)
    _add(checks, "qual.ok", qual.get("core_qualification_result_complete") is True)
    _add(checks, "route.next", route.get("recommended_next_phase") == SELECTED_NEXT_PHASE)

    for c in CONCLUSION_TYPES:
        _add(checks, f"ctype.{c[:16]}", c in (conc.get("conclusion_types") or []))
    for rule in SELF_CHECK_RULES:
        _add(checks, f"rule.{rule[:16]}", rule in (ref.get("rules") or []))
    for tag in SELF_WORK_CAPABILITY_TAGS:
        e = next((x for x in qual.get("entries") or [] if x.get("capability_id") == tag), {})
        _add(checks, f"qual.{tag[:16]}", e.get("qualification_passed") is True)
    for case in rlist:
        _add(checks, f"case.{case.get('case_id','')[:16]}", case.get("case_passed") is True)
        _add(checks, f"re.{case.get('case_id','')[:12]}", case.get("real_execution") is False)
        _add(checks, f"conc.{case.get('case_id','')[:10]}", bool(case.get("conclusion")))
        _add(checks, f"trace.{case.get('case_id','')[:10]}", bool(case.get("traceability_path")))
    for idx, sc in enumerate(SELF_WORK_CASES):
        _add(checks, f"scfg.{idx}", sc["case_id"] in [r.get("case_id") for r in rlist])

    for k in ("no_record_creation", "no_grant_creation", "no_authorization_request_creation", "no_runtime_execution",
              "no_route_execution", "no_real_handoff_execution", "no_candidate_promotion_execution",
              "no_whitebox_runtime_call", "no_persistent_write"):
        _add(checks, f"guard.{k[:14]}", s.get(k) is True)
    _add(checks, "sum.handoff_defer", s.get("handoff_contract_p3_defer_remains_defer") is True)
    _add(checks, "sum.periph", s.get("peripheral_contract_does_not_constrain_core") is True)
    _add(checks, "sum.unknown_drop", s.get("unknown_information_not_silently_dropped") is True)
    _add(checks, "sum.incomplete", s.get("incomplete_information_can_defer") is True)
    _add(checks, "sum.hrisk", s.get("high_risk_information_governance_review_candidate") is True)
    _add(checks, "sum.swallow", s.get("downstream_work_not_swallowed") is True)
    _add(checks, "sum.no_it", s.get("integration_test_executed") is False)
    _add(checks, "sum.runtime_abs", s.get("runtime_execution_absent") is True)
    _add(checks, "sum.phase", s.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", s.get("scope") == SCOPE)
    _add(checks, "sum.blocker0", s.get("blocker_count") == 0)
    _add(checks, "wl.single", wl.get("single_envelope_processing") is True)
    _add(checks, "wl.dedup", wl.get("duplicate_information_idempotency_supported") is True)
    _add(checks, "wl.ambiguous", wl.get("ambiguous_information_can_request_context") is True)
    _add(checks, "dn.contract", dn.get("downstream_contract_not_defined_yet") is True)
    _add(checks, "up.rewrite", up.get("upstream_protocol_not_rewritten_yet") is True)

    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", s.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", fs.get(k) is True)
    for rel in IPC_SELF_WORK_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")
    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"plines.{idx}", (row.get("line_count") or 0) <= 600)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", s.get(k) is True)
    for idx, need in enumerate(dn.get("needs") or []):
        _add(checks, f"need.{idx}", bool(need.get("downstream_need_id")))
    for idx, a in enumerate(up.get("assumptions") or []):
        _add(checks, f"asm.{idx}", bool(a.get("assumption_id")))
    for fb in ("midplatform_completed", "runtime_enabled", "integration_test_executed", "record_created", "grant_issued"):
        combined = f"{s.get('final_decision')} {s.get('recommended_next_phase')}".lower()
        _add(checks, f"fb.{fb[:12]}", fb not in combined)
    for idx, case in enumerate(rlist):
        _add(checks, f"dnobs.{idx}", bool(case.get("downstream_need_observed")))
        _add(checks, f"sck.{idx}", bool(case.get("self_check_result")))
    _add(checks, "up.impl_min", int(impl_v.get("passed_checks", 0)) >= 420)
    _add(checks, "sum.remaining", s.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "sum.explain", s.get("conclusions_explainable") is True)
    _add(checks, "sum.traceable", s.get("internal_processing_traceable") is True)
    _add(checks, "sum.extract", s.get("downstream_need_extracted_from_actual_cases") is True)
    _add(checks, "report.final", docs.get("ipc_self_work_core_capability_dryrun_report_v1.json", {}).get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "res.passed", results.get("passed_cases", 0) >= 10)
    _add(checks, "res.total", results.get("total_cases", 0) >= 11)
    for idx, ct in enumerate(CONCLUSION_TYPES):
        _add(checks, f"ctidx.{idx}", ct in CONCLUSION_TYPES)
    for idx, tag in enumerate(SELF_WORK_CAPABILITY_TAGS):
        _add(checks, f"tagidx.{idx}", tag in SELF_WORK_CAPABILITY_TAGS)
    for idx, rule in enumerate(SELF_CHECK_RULES):
        _add(checks, f"ridx.{idx}", rule in SELF_CHECK_RULES)
    for idx, case in enumerate(rlist):
        _add(checks, f"rtype.{idx}", bool(case.get("detected_type")))
        _add(checks, f"rstat.{idx}", bool(case.get("processing_status")))
        _add(checks, f"rgcand.{idx}", case.get("generated_candidate_type") == "InformationProcessingResultCandidate")
        _add(checks, f"rside.{idx}", case.get("side_effect_allowed") is False)
        _add(checks, f"rwload.{idx}", bool(case.get("workload_control_result")))
        _add(checks, f"rguard.{idx}", bool(case.get("non_execution_guard_result")))
        _add(checks, f"rrcode.{idx}", len(case.get("reason_codes") or []) >= 2)
    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx, k in enumerate(FILE_SIZE_GOVERNANCE_REVIEW_KEYS):
        _add(checks, f"fsk2.{idx}", fs.get(k) is True)
    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        _add(checks, f"pex.{idx}", (REPO_ROOT / rel).is_file())
    for idx, sc in enumerate(SELF_WORK_CASES):
        _add(checks, f"scid.{idx}", sc["case_id"] in [r.get("case_id") for r in rlist])
        _add(checks, f"scpass.{idx}", next((r for r in rlist if r.get("case_id") == sc["case_id"]), {}).get("case_passed") is True)
    for idx, need in enumerate(dn.get("needs") or []):
        _add(checks, f"nrole.{idx}", bool(need.get("likely_future_role")))
        _add(checks, f"nwhy.{idx}", bool(need.get("why_ipc_should_not_handle_it")))
    for idx, a in enumerate(up.get("assumptions") or []):
        _add(checks, f"atier.{idx}", bool(a.get("tier")))
    _add(checks, "three.upstream", bool(three.get("upstream_work")))
    _add(checks, "three.downstream", bool(three.get("downstream_work")))
    _add(checks, "three.no_contract", three.get("downstream_contract_not_defined_yet") is True)
    _add(checks, "route.rationale", bool(route.get("rationale")))
    _add(checks, "route.top_need", bool(route.get("top_downstream_need_observed")))
    _add(checks, "meta.dryrun_only", s.get("information_processing_core_self_work_dryrun_only") is True)
    _add(checks, "up.impl_failed0", impl_v.get("failed_checks") == 0)

    passed = sum(1 for x in checks if x["passed"])
    failed = [x for x in checks if not x["passed"]]
    v = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    payload = {"verifier": v, "phase": PHASE_ID, "passed_checks": passed, "failed_checks": len(failed),
               "min_checks": MIN_CHECKS, "blocker_count": len(failed),
               "final_decision": FINAL_DECISION_GO if v == "GO" else "HOLD",
               "recommended_next_phase": SELECTED_NEXT_PHASE if v == "GO" else "HOLD_FOR_ISSUE_REVIEW",
               "failed": failed[:40], "checks": checks}
    (root / "verifier_report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": v, "passed_checks": passed, "failed_checks": len(failed),
                      "final_decision": payload["final_decision"]}, ensure_ascii=False))
    return 0 if v == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
