#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Project Organization Work Manual and Existing Work Mapping v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core_capability_peripheral_service_recalibration_v1 import FINAL_DECISION_GO as RECAL_FINAL_GO
from capabilities.midplatform.luna_project_organization_work_manual_items_v1 import (
    EXISTING_ARTIFACT_MAPPINGS,
    MISSING_WORK_MANUAL_GAPS,
    NEXT_WORK_GOVERNANCE_RULES,
    OVERBUILD_RISK_REVIEW,
    PROJECT_WORK_MODE_PRINCIPLES,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    STANDARD_WORK_MANUAL_SECTIONS,
)
from capabilities.midplatform.luna_project_organization_work_manual_and_existing_work_mapping_v1 import (
    DEFAULT_OUTPUT,
    DEFAULT_RECALIBRATION_ROOT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.luna_project_organization_work_manual_lineage_v1 import WORK_MANUAL_WHITELIST_FILES
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 360
ARTIFACTS = (
    "project_work_mode_definition_v1.json", "standard_work_manual_template_v1.json",
    "midplatform_organization_manual_v1.json", "existing_work_mapping_matrix_v1.json",
    "completed_artifact_reclassification_v1.json", "missing_work_manual_gap_register_v1.json",
    "peripheral_overbuild_risk_review_v1.json", "next_work_governance_rules_v1.json",
    "next_route_recommendation_v1.json", "file_size_governance_review_v1.json",
    "summary.json", "verifier_report.json",
)
DOCS = (
    "docs/architecture/governance/LUNA_PROJECT_ORGANIZATION_WORK_MANUAL_RULE_V1.md",
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_ORGANIZATION_WORK_MANUAL_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_PROJECT_ORGANIZATION_WORK_MANUAL_AND_EXISTING_WORK_MAPPING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_PROJECT_ORGANIZATION_WORK_MANUAL_AND_EXISTING_WORK_MAPPING_V1_GO_NO_GO_PACK_V0.md",
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
    parser.add_argument("--recalibration-root", default=DEFAULT_RECALIBRATION_ROOT)
    args = parser.parse_args()
    root, upstream = Path(args.output_root), Path(args.recalibration_root)
    checks: List[Dict[str, Any]] = []
    recal_s, recal_v = _read(upstream / "summary.json"), _read(upstream / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    work_mode = docs["project_work_mode_definition_v1.json"]
    template = docs["standard_work_manual_template_v1.json"]
    org = docs["midplatform_organization_manual_v1.json"]
    matrix = docs["existing_work_mapping_matrix_v1.json"]
    reclass = docs["completed_artifact_reclassification_v1.json"]
    gaps = docs["missing_work_manual_gap_register_v1.json"]
    overbuild = docs["peripheral_overbuild_risk_review_v1.json"]
    gov_rules = docs["next_work_governance_rules_v1.json"]
    route = docs["next_route_recommendation_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    for name in ARTIFACTS:
        if name == "verifier_report.json":
            continue
        _add(checks, f"art.{name.split('.')[0][:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.recal_go", recal_s.get("final_decision") == RECAL_FINAL_GO)
    _add(checks, "up.recal_v", recal_v.get("verifier") == "GO")
    _add(checks, "sum.pass", summary.get("luna_project_organization_work_manual_mapping_pass") is True)
    _add(checks, "sum.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", summary.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "sum.blocker0", summary.get("blocker_count") == 0)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", summary.get(k) is True)
    _add(checks, "sum.wm_first", summary.get("work_manual_first_rule_defined") is True)
    _add(checks, "sum.org_wf", summary.get("organization_workflow_defined") is True)
    _add(checks, "sum.role_req", summary.get("role_job_definition_required") is True)
    _add(checks, "sum.judge_req", summary.get("judge_referee_definition_required") is True)
    _add(checks, "sum.workload", summary.get("workload_control_required") is True)
    _add(checks, "sum.qual", summary.get("qualification_standard_required") is True)
    _add(checks, "sum.core_first", summary.get("core_work_before_peripheral_rules") is True)
    _add(checks, "sum.periph_serve", summary.get("peripheral_rules_must_serve_core") is True)
    _add(checks, "sum.mapped", summary.get("existing_artifacts_mapped") is True)
    _add(checks, "sum.prior_go", summary.get("prior_go_results_not_invalidated") is True)
    _add(checks, "sum.ipc_manual", summary.get("information_processing_core_should_have_work_manual_before_implementation") is True)
    _add(checks, "sum.not_direct_impl", summary.get("next_route_not_direct_controlled_implementation_unless_manual_ready") is True)
    _add(checks, "sum.no_runtime", summary.get("no_runtime_execution") is True)
    _add(checks, "sum.no_it", summary.get("no_integration_test") is True)
    _add(checks, "sum.no_rec", summary.get("no_record_creation") is True)
    _add(checks, "sum.no_grant", summary.get("no_grant_creation") is True)
    _add(checks, "sum.no_auth", summary.get("no_authorization_request_creation") is True)

    _add(checks, "wm.defined", work_mode.get("project_work_mode_defined") is True)
    _add(checks, "tpl.complete", template.get("standard_work_manual_template_complete") is True)
    _add(checks, "org.complete", org.get("midplatform_organization_manual_complete") is True)
    _add(checks, "mat.complete", matrix.get("existing_work_mapping_complete") is True)
    _add(checks, "gap.complete", gaps.get("missing_work_manual_gap_register_complete") is True)
    _add(checks, "gov.complete", gov_rules.get("next_work_governance_rules_complete") is True)
    _add(checks, "route.ipc_manual", route.get("information_processing_core_should_have_work_manual_before_implementation") is True)
    _add(checks, "route.not_direct", route.get("next_route_not_direct_controlled_implementation_unless_manual_ready") is True)
    _add(checks, "route.manual_not_ready", route.get("manual_ready_for_ipc_implementation") is False)
    _add(checks, "route.next_wm", SELECTED_NEXT_PHASE in (route.get("recommended_next_phase") or ""))

    for p in PROJECT_WORK_MODE_PRINCIPLES:
        _add(checks, f"prin.{p['principle_id'][:16]}", p["principle_id"] in [x.get("principle_id") for x in work_mode.get("principles") or []])
    for s in STANDARD_WORK_MANUAL_SECTIONS:
        _add(checks, f"sec.{s[:16]}", s in (template.get("sections") or []))
    for a in EXISTING_ARTIFACT_MAPPINGS:
        _add(checks, f"art.{a['artifact_id'][:16]}", a["artifact_id"] in [x.get("artifact_id") for x in matrix.get("artifacts") or []])
    for g in MISSING_WORK_MANUAL_GAPS:
        _add(checks, f"gap.{g['gap_id'][:16]}", g["gap_id"] in [x.get("gap_id") for x in gaps.get("gaps") or []])
    for r in OVERBUILD_RISK_REVIEW:
        _add(checks, f"risk.{r['risk_id'][:16]}", r["risk_id"] in [x.get("risk_id") for x in overbuild.get("risks") or []])
    for rule in NEXT_WORK_GOVERNANCE_RULES:
        _add(checks, f"gov.{rule[:16]}", rule in (gov_rules.get("rules") or []))

    _add(checks, "reclass.core", len(reclass.get("core_work_artifacts") or []) >= 4)
    _add(checks, "reclass.periph", len(reclass.get("peripheral_artifacts") or []) >= 2)
    _add(checks, "sum.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", summary.get("scope") == SCOPE)
    _add(checks, "sum.issues_empty", summary.get("issues") == [])
    _add(checks, "org.mission", bool(org.get("mission")))
    _add(checks, "org.primary", org.get("primary_core_work") == "Information Processing Core")
    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", summary.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", file_size.get(k) is True)
    for rel in WORK_MANUAL_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")
    for idx, a in enumerate(EXISTING_ARTIFACT_MAPPINGS):
        e = next((x for x in matrix.get("artifacts") or [] if x.get("artifact_id") == a["artifact_id"]), {})
        _add(checks, f"amap.{idx}", bool(e))
        _add(checks, f"akeep.{idx}", e.get("should_keep") is True)
    for idx, g in enumerate(MISSING_WORK_MANUAL_GAPS):
        _add(checks, f"gidx.{idx}", g["gap_id"] in [x.get("gap_id") for x in gaps.get("gaps") or []])
    ipc = next((a for a in matrix.get("artifacts") or [] if a.get("artifact_id") == "information_processing_core"), {})
    _add(checks, "ipc.missing_manual", ipc.get("missing_manual_definition") is True)
    _add(checks, "ipc.next_wm", ipc.get("next_action") == "write_work_manual_before_implementation")
    _add(checks, "sum.selected", summary.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "up.recal_min", int(recal_v.get("passed_checks", 0)) >= 340)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", summary.get(k) is True)

    _add(checks, "sum.construction", summary.get("midplatform_overall_status") == "construction_consolidation")
    _add(checks, "sum.remaining", summary.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "sum.not_final", summary.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "sum.chain", summary.get("owner_approval_request_chain_not_reopened") is True)
    _add(checks, "sum.template", summary.get("template_lineage_ok") is True)
    _add(checks, "sum.no_fragment", summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "sum.integration_false", summary.get("integration_test_executed") is False)
    _add(checks, "sum.runtime_absent", summary.get("runtime_execution_absent") is True)
    _add(checks, "wm.prin10", len(work_mode.get("principles") or []) >= 10)
    _add(checks, "tpl.sec11", len(template.get("sections") or []) >= 11)
    _add(checks, "mat.art18", len(matrix.get("artifacts") or []) >= 18)
    _add(checks, "gap.gap13", len(gaps.get("gaps") or []) >= 13)
    _add(checks, "gov.rule10", len(gov_rules.get("rules") or []) >= 10)
    _add(checks, "risk.risk5", len(overbuild.get("risks") or []) >= 5)
    _add(checks, "route.defer_reason", bool(route.get("defer_reason")))
    _add(checks, "route.deferred", bool(route.get("deferred_route")))
    _add(checks, "overbuild.complete", overbuild.get("peripheral_overbuild_risk_review_complete") is True)
    _add(checks, "handoff.defer", any(a.get("artifact_id") == "module_handoff_contract_gap" and a.get("should_defer") for a in matrix.get("artifacts") or []))
    _add(checks, "orch.core", any(a.get("artifact_id") == "task_manager_core_orchestration_controlled_skeleton_implementation" and a.get("is_core_work") for a in matrix.get("artifacts") or []))
    _add(checks, "dryrun.judge", any(a.get("artifact_id") == "task_manager_core_orchestration_module_level_controlled_dryrun" and a.get("is_judge_rule") for a in matrix.get("artifacts") or []))
    _add(checks, "recal.inform", any(a.get("artifact_id") == "core_capability_peripheral_service_recalibration" for a in matrix.get("artifacts") or []))
    for idx, p in enumerate(PROJECT_WORK_MODE_PRINCIPLES):
        _add(checks, f"pname.{idx}", bool(p.get("name")))
        _add(checks, f"psum.{idx}", bool(p.get("summary")))
    for idx, s in enumerate(STANDARD_WORK_MANUAL_SECTIONS):
        _add(checks, f"sidx.{idx}", s in (template.get("sections") or []))
    for idx, a in enumerate(EXISTING_ARTIFACT_MAPPINGS):
        e = next((x for x in matrix.get("artifacts") or [] if x.get("artifact_id") == a["artifact_id"]), {})
        _add(checks, f"acore.{idx}", e.get("is_core_work") == a.get("is_core_work"))
        _add(checks, f"aperiph.{idx}", e.get("is_peripheral_rule") == a.get("is_peripheral_rule"))
        _add(checks, f"arisk.{idx}", e.get("overbuild_risk") == a.get("overbuild_risk"))
    for idx, g in enumerate(MISSING_WORK_MANUAL_GAPS):
        e = next((x for x in gaps.get("gaps") or [] if x.get("gap_id") == g["gap_id"]), {})
        _add(checks, f"gprior.{idx}", e.get("priority") == g.get("priority"))
    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"plines.{idx}", (row.get("line_count") or 0) <= 600)
        _add(checks, f"pex.{idx}", row.get("exists") is True)
    for fb in ("midplatform_completed", "runtime_enabled", "integration_test_executed", "grant_issued", "record_created"):
        combined = f"{summary.get('final_decision')} {summary.get('recommended_next_phase')}".lower()
        _add(checks, f"fb.{fb[:12]}", fb not in combined)
    _add(checks, "org.roles", len(org.get("roles_defined") or []) >= 4)
    _add(checks, "org.judges", len(org.get("judge_roles") or []) >= 3)
    _add(checks, "gap.ipc_blocker", any(g.get("gap_id") == "information_processing_core_work_manual_missing" for g in gaps.get("gaps") or []))
    _add(checks, "gap.lifecycle_blocker", any(g.get("gap_id") == "candidate_lifecycle_manager_work_manual_missing" for g in gaps.get("gaps") or []))
    _add(checks, "up.failed0", recal_v.get("failed_checks") == 0)
    _add(checks, "sum.real_auth_false", summary.get("real_request_issuance_authorized") is False)

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
                      "final_decision": payload["final_decision"], "recommended_next_phase": payload["recommended_next_phase"]}, ensure_ascii=False))
    return 0 if v == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
