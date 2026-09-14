#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Information Processing Core Work Manual Definition v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.information_processing_core_work_manual_definition_v1 import (
    DEFAULT_OUTPUT,
    DEFAULT_WORK_MANUAL_MAPPING_ROOT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.information_processing_core_work_manual_items_v1 import (
    CORE_WORK_DEFINITION,
    EXTERNAL_WORKFLOW,
    FUTURE_EXPANSION,
    GOVERNANCE_SERVICE_RULES,
    INFORMATION_TYPES,
    INTERNAL_WORKFLOW_STEPS,
    JUDGE_REFEREE_RULES,
    ORGANIZATION_CONTEXT,
    QUALIFICATION_STANDARD,
    ROLE_JOB_DEFINITION,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    WORK_DETAIL_ITEMS,
    WORKLOAD_CONTROL,
)
from capabilities.midplatform.information_processing_core_work_manual_lineage_v1 import IPC_WORK_MANUAL_WHITELIST_FILES
from capabilities.midplatform.luna_project_organization_work_manual_and_existing_work_mapping_v1 import (
    FINAL_DECISION_GO as WM_FINAL_GO,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 340
ARTIFACTS = (
    "organization_context_v1.json",
    "core_work_definition_v1.json",
    "role_job_definition_v1.json",
    "work_detail_v1.json",
    "internal_workflow_v1.json",
    "external_workflow_v1.json",
    "judge_referee_rules_v1.json",
    "governance_protocol_boundary_service_rules_v1.json",
    "workload_control_v1.json",
    "qualification_standard_v1.json",
    "future_expansion_v1.json",
    "implementation_readiness_review_v1.json",
    "next_route_decision_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_INFORMATION_PROCESSING_CORE_WORK_MANUAL_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_WORK_MANUAL_DEFINITION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_WORK_MANUAL_DEFINITION_V1_GO_NO_GO_PACK_V0.md",
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
    parser.add_argument("--work-manual-mapping-root", default=DEFAULT_WORK_MANUAL_MAPPING_ROOT)
    args = parser.parse_args()
    root, upstream = Path(args.output_root), Path(args.work_manual_mapping_root)
    checks: List[Dict[str, Any]] = []
    wm_s, wm_v = _read(upstream / "summary.json"), _read(upstream / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    org = docs["organization_context_v1.json"]
    core = docs["core_work_definition_v1.json"]
    role = docs["role_job_definition_v1.json"]
    detail = docs["work_detail_v1.json"]
    internal = docs["internal_workflow_v1.json"]
    external = docs["external_workflow_v1.json"]
    judge = docs["judge_referee_rules_v1.json"]
    gov = docs["governance_protocol_boundary_service_rules_v1.json"]
    workload = docs["workload_control_v1.json"]
    qual = docs["qualification_standard_v1.json"]
    future = docs["future_expansion_v1.json"]
    impl = docs["implementation_readiness_review_v1.json"]
    route = docs["next_route_decision_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    for name in ARTIFACTS:
        if name == "verifier_report.json":
            continue
        _add(checks, f"art.{name.split('.')[0][:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.wm_go", wm_s.get("final_decision") == WM_FINAL_GO)
    _add(checks, "up.wm_v", wm_v.get("verifier") == "GO")
    _add(checks, "up.wm_min", int(wm_v.get("passed_checks", 0)) >= 340)
    _add(checks, "sum.pass", summary.get("information_processing_core_work_manual_definition_pass") is True)
    _add(checks, "sum.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", summary.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "sum.blocker0", summary.get("blocker_count") == 0)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", summary.get(k) is True)
    _add(checks, "sum.ipc_primary", summary.get("information_processing_core_identified_as_primary_core") is True)
    _add(checks, "sum.wf_before_proto", summary.get("workflow_before_protocol") is True)
    _add(checks, "sum.handoff_not_req", summary.get("module_handoff_contract_not_required_for_information_classification") is True)
    _add(checks, "sum.integ_not_req", summary.get("integration_contract_not_required_for_information_classification") is True)
    _add(checks, "sum.unknown_ok", summary.get("unknown_information_allowed") is True)
    _add(checks, "sum.non_exec", summary.get("non_execution_boundary_preserved") is True)
    _add(checks, "sum.no_impl", summary.get("no_controlled_implementation_created") is True)
    _add(checks, "sum.no_runtime", summary.get("no_runtime_execution") is True)
    _add(checks, "sum.no_it", summary.get("no_integration_test") is True)
    _add(checks, "sum.no_rec", summary.get("no_record_creation") is True)
    _add(checks, "sum.no_grant", summary.get("no_grant_creation") is True)
    _add(checks, "sum.no_auth", summary.get("no_authorization_request_creation") is True)
    _add(checks, "sum.prior_go", summary.get("prior_go_results_not_invalidated") is True)
    _add(checks, "sum.type_reg", summary.get("information_type_registry_defined") is True)

    _add(checks, "org.complete", org.get("organization_context_complete") is True)
    _add(checks, "org.midplatform", org.get("organization") == "Midplatform")
    _add(checks, "core.complete", core.get("core_work_definition_complete") is True)
    _add(checks, "core.primary", core.get("primary_core_function") == "Information Processing Core")
    _add(checks, "role.complete", role.get("role_job_definition_complete") is True)
    _add(checks, "role.primary", role.get("information_processing_core_identified_as_primary_core") is True)
    _add(checks, "detail.complete", detail.get("work_detail_complete") is True)
    _add(checks, "internal.complete", internal.get("internal_workflow_complete") is True)
    _add(checks, "external.complete", external.get("external_workflow_complete") is True)
    _add(checks, "judge.complete", judge.get("judge_referee_rules_complete") is True)
    _add(checks, "gov.periph", gov.get("peripheral_rules_serve_core") is True)
    _add(checks, "workload.complete", workload.get("workload_control_complete") is True)
    _add(checks, "qual.complete", qual.get("qualification_standard_complete") is True)
    _add(checks, "future.complete", future.get("future_expansion_complete") is True)
    _add(checks, "impl.ok", impl.get("implementation_readiness_ok") is True)
    _add(checks, "route.next", route.get("recommended_next_phase") == SELECTED_NEXT_PHASE)

    _add(checks, "gov.handoff", gov.get("module_handoff_contract_not_required_for_information_classification") is True)
    _add(checks, "gov.integ", gov.get("integration_contract_not_required_for_information_classification") is True)
    _add(checks, "gov.periph_core", gov.get("peripheral_contract_does_not_constrain_core") is True)
    _add(checks, "gov.proto_forbid", gov.get("protocol_before_workflow_forbidden") is True)
    _add(checks, "impl.no_impl", impl.get("no_controlled_implementation_created") is True)
    _add(checks, "impl.manual_ready", impl.get("manual_ready_for_controlled_implementation") is True)

    for t in INFORMATION_TYPES:
        _add(checks, f"type.{t[:16]}", t in (detail.get("information_types") or []))
    for item in CORE_WORK_DEFINITION["core_work_items"]:
        _add(checks, f"core.{item[:16]}", item in (core.get("core_work_items") or []))
    for item in CORE_WORK_DEFINITION["not_core_work"]:
        _add(checks, f"not.{item[:16]}", item in (core.get("not_core_work") or []))
    for tag in QUALIFICATION_STANDARD["minimum_capability_tags"]:
        _add(checks, f"tag.{tag[:16]}", tag in (qual.get("minimum_capability_tags") or []))
    for step in INTERNAL_WORKFLOW_STEPS:
        _add(checks, f"step.{step['step_id'][:16]}", step["step_id"] in [s.get("step_id") for s in internal.get("steps") or []])
    for work in WORK_DETAIL_ITEMS:
        _add(checks, f"work.{work['work_id'][:16]}", work["work_id"] in [w.get("work_id") for w in detail.get("items") or []])
    for exp in FUTURE_EXPANSION["reserved"]:
        _add(checks, f"exp.{exp[:16]}", exp in (future.get("reserved") or []))

    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", summary.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", file_size.get(k) is True)
    for rel in IPC_WORK_MANUAL_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")

    _add(checks, "sum.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", summary.get("scope") == SCOPE)
    _add(checks, "sum.issues_empty", summary.get("issues") == [])
    _add(checks, "sum.selected", summary.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "sum.construction", summary.get("midplatform_overall_status") == "construction_consolidation")
    _add(checks, "sum.remaining", summary.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "sum.not_final", summary.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "sum.template", summary.get("template_lineage_ok") is True)
    _add(checks, "sum.no_fragment", summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "sum.integration_false", summary.get("integration_test_executed") is False)
    _add(checks, "sum.runtime_absent", summary.get("runtime_execution_absent") is True)
    _add(checks, "sum.real_auth_false", summary.get("real_request_issuance_authorized") is False)
    _add(checks, "role.title", bool(role.get("job_title")))
    _add(checks, "role.mission", bool(role.get("job_mission")))
    _add(checks, "role.forbidden", "record_creation" in (role.get("forbidden") or []))
    _add(checks, "judge.judges", len(judge.get("judges") or []) >= 3)
    _add(checks, "judge.resp", bool(judge.get("responsibility")))
    _add(checks, "workload.scope", bool(workload.get("single_processing_scope")))
    _add(checks, "workload.no_absorb", workload.get("no_downstream_work_absorption") is True)
    _add(checks, "ext.lifecycle", bool(external.get("to_lifecycle_manager_when")))
    _add(checks, "ext.orchestration", bool(external.get("to_core_orchestration_when")))
    _add(checks, "ext.must_not", bool(external.get("must_not_continue_downstream_when")))
    _add(checks, "internal.wf_proto", internal.get("workflow_before_protocol") is True)
    _add(checks, "detail.types11", len(detail.get("information_types") or []) >= 11)
    _add(checks, "core.items10", len(core.get("core_work_items") or []) >= 10)
    _add(checks, "qual.tags12", len(qual.get("minimum_capability_tags") or []) >= 12)
    _add(checks, "future.res10", len(future.get("reserved") or []) >= 10)
    _add(checks, "steps12", len(internal.get("steps") or []) >= 12)
    _add(checks, "work11", len(detail.get("items") or []) >= 11)

    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"plines.{idx}", (row.get("line_count") or 0) <= 600)
        _add(checks, f"pex.{idx}", row.get("exists") is True)
    for fb in ("midplatform_completed", "runtime_enabled", "integration_test_executed", "grant_issued", "record_created"):
        combined = f"{summary.get('final_decision')} {summary.get('recommended_next_phase')}".lower()
        _add(checks, f"fb.{fb[:12]}", fb not in combined)
    for idx, t in enumerate(INFORMATION_TYPES):
        _add(checks, f"tidx.{idx}", t in INFORMATION_TYPES)
    for idx, tag in enumerate(QUALIFICATION_STANDARD["minimum_capability_tags"]):
        _add(checks, f"tqual.{idx}", tag in (qual.get("minimum_capability_tags") or []))
    for idx, step in enumerate(INTERNAL_WORKFLOW_STEPS):
        s = next((x for x in internal.get("steps") or [] if x.get("step_id") == step["step_id"]), {})
        _add(checks, f"sout.{idx}", bool(s.get("output")))
        _add(checks, f"sin.{idx}", bool(s.get("input")))
    for idx, w in enumerate(WORK_DETAIL_ITEMS):
        e = next((x for x in detail.get("items") or [] if x.get("work_id") == w["work_id"]), {})
        _add(checks, f"wact.{idx}", bool(e.get("action")))
    for idx, exp in enumerate(FUTURE_EXPANSION["reserved"]):
        _add(checks, f"eidx.{idx}", exp in (future.get("reserved") or []))
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", summary.get(k) is True)
    for pos in ORGANIZATION_CONTEXT["role_positioning"]:
        _add(checks, f"pos.{pos[:14]}", pos in (org.get("role_positioning") or []))
    for src in ROLE_JOB_DEFINITION["upstream_sources"]:
        _add(checks, f"upsrc.{src[:12]}", src in (role.get("upstream_sources") or []))
    for tgt in ROLE_JOB_DEFINITION["downstream_targets"]:
        _add(checks, f"dntgt.{tgt[:12]}", tgt in (role.get("downstream_targets") or []))
    for crit in JUDGE_REFEREE_RULES["correctness_criteria"]:
        _add(checks, f"crit.{crit[:14]}", crit in (judge.get("correctness_criteria") or []))
    for resp_k in JUDGE_REFEREE_RULES["responsibility"]:
        _add(checks, f"resp.{resp_k[:12]}", resp_k in (judge.get("responsibility") or {}))
    _add(checks, "gov.constitution", bool(gov.get("constitution_hard_constraint_only")))
    _add(checks, "workload.unknown", bool(workload.get("unknown_handling")))
    _add(checks, "workload.defer", bool(workload.get("queue_defer_rules")))
    _add(checks, "workload.reject", bool(workload.get("reject_rules")))
    _add(checks, "workload.overload", bool(workload.get("overload_marker")))
    _add(checks, "org.stage", org.get("stage_positioning") == "candidate_level_non_runtime_controlled")
    _add(checks, "up.wm_failed0", wm_v.get("failed_checks") == 0)
    _add(checks, "sum.no_promo", summary.get("no_candidate_promotion") is True)
    _add(checks, "sum.no_adapter", summary.get("no_adapter_whitebox") is True)
    _add(checks, "sum.no_route", summary.get("no_runtime_route") is True)
    _add(checks, "impl.no_record", impl.get("no_record_creation") is True)
    _add(checks, "impl.no_grant", impl.get("no_grant_creation") is True)
    _add(checks, "impl.no_auth", impl.get("no_authorization_request_creation") is True)
    _add(checks, "route.readiness", route.get("next_phase_readiness_ok") is True)
    _add(checks, "route.selected", route.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "meta.definition_only", summary.get("information_processing_core_work_manual_definition_only") is True)
    _add(checks, "meta.scope_only", summary.get("scope") == "information_processing_core_work_manual_definition_only")
    for key, val in GOVERNANCE_SERVICE_RULES.items():
        if isinstance(val, bool):
            _add(checks, f"govk.{key[:14]}", gov.get(key) == val)
    _add(checks, "role.metaphors4", len(role.get("job_metaphors") or []) >= 4)
    _add(checks, "org.framework", bool(org.get("parent_framework")))
    _add(checks, "org.luna_rel", bool(org.get("luna_relationship")))
    _add(checks, "qual.go_criteria", len(qual.get("go_criteria") or []) >= 5)
    _add(checks, "ext.upstream", len(external.get("upstream_sources") or []) >= 5)
    _add(checks, "ext.downstream", len(external.get("downstream_targets") or []) >= 3)
    _add(checks, "judge.overreach", len(judge.get("overreach_signals") or []) >= 3)
    _add(checks, "judge.omission", len(judge.get("omission_signals") or []) >= 3)
    _add(checks, "core.not7", len(core.get("not_core_work") or []) >= 7)
    _add(checks, "workload.no_expand", workload.get("no_unbounded_classification_expansion") is True)

    passed = sum(1 for x in checks if x["passed"])
    failed = [x for x in checks if not x["passed"]]
    v = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    payload = {
        "verifier": v,
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        "final_decision": FINAL_DECISION_GO if v == "GO" else "HOLD",
        "recommended_next_phase": SELECTED_NEXT_PHASE if v == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "verifier": v,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "final_decision": payload["final_decision"],
        "recommended_next_phase": payload["recommended_next_phase"],
    }, ensure_ascii=False))
    return 0 if v == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
