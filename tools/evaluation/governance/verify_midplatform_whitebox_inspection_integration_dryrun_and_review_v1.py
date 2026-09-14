#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Whitebox Inspection Integration DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_whitebox_inspection_integration_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CHV_MAPPING,
    EVIDENCE_TRACE_MAPPING,
    FACTORY_AUTH_MAPPING,
    FINAL_DECISION_GO,
    GLOBAL_TO_LOCAL_PRINCIPLES,
    INSPECTION_LAYERS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_PLANNING_FINAL,
    VALIDATION_ABSORPTION,
    WHITEBOX_VISIBILITY_DOMAINS,
)

MIN_CHECKS = 161

REQUIRED = (
    "whitebox_inspection_integration_dryrun_review_policy_v1.json",
    "whitebox_integration_planning_input_review_v1.json",
    "whitebox_inspection_model_candidate_v1.json",
    "whitebox_visibility_domain_review_v1.json",
    "validation_engineering_absorption_review_v1.json",
    "constitution_health_validation_mapping_review_v1.json",
    "factory_authorization_mapping_review_v1.json",
    "evidence_boundary_traceback_mapping_review_v1.json",
    "global_to_local_principle_review_v1.json",
    "whitebox_layer_model_review_v1.json",
    "whitebox_drilldown_policy_review_v1.json",
    "ocr_real_dep_local_evidence_review_v1.json",
    "no_parallel_whitebox_review_v1.json",
    "whitebox_boundary_audit_v1.json",
    "whitebox_blocked_path_result_v1.json",
    "whitebox_integration_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_whitebox_inspection_integration_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_whitebox_inspection_integration_planning"
        ),
    )
    p.add_argument(
        "--ocr-execution-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_real_minimal_controlled_execution"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.planning_root)
    ocr_root = Path(args.ocr_execution_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")
    ocr_vr = _load(ocr_root / "verifier_report.json")
    ocr_sm = _load(ocr_root / "summary.json")

    summary = _load(root / "summary.json")
    model = _load(root / "whitebox_inspection_model_candidate_v1.json")
    visibility = _load(root / "whitebox_visibility_domain_review_v1.json")
    val_abs = _load(root / "validation_engineering_absorption_review_v1.json")
    chv = _load(root / "constitution_health_validation_mapping_review_v1.json")
    factory = _load(root / "factory_authorization_mapping_review_v1.json")
    evidence = _load(root / "evidence_boundary_traceback_mapping_review_v1.json")
    global_local = _load(root / "global_to_local_principle_review_v1.json")
    layers = _load(root / "whitebox_layer_model_review_v1.json")
    drilldown = _load(root / "whitebox_drilldown_policy_review_v1.json")
    ocr_local = _load(root / "ocr_real_dep_local_evidence_review_v1.json")
    no_parallel = _load(root / "no_parallel_whitebox_review_v1.json")
    boundary = _load(root / "whitebox_boundary_audit_v1.json")
    blocked = _load(root / "whitebox_blocked_path_result_v1.json")
    closure = _load(root / "whitebox_integration_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    planning_input = _load(root / "whitebox_integration_planning_input_review_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_no_parallel", plan_sm.get("new_parallel_whitebox_system_created_now") is False)
    ok("upstream.ocr_go", ocr_vr.get("verifier") == "GO")
    ok("upstream.ocr_boundary", ocr_sm.get("boundary_ok") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("whitebox_inspection_integration_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.model_gen", summary.get("whitebox_inspection_model_candidate_generated_now") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("model.id", model.get("model_id") == "whitebox_inspection_model_v1")
    ok("model.role", model.get("role") == "transparent_inspection_and_explainable_supervision")
    ok("model.no_rulemaking", model.get("rulemaking_allowed") is False)
    ok("model.no_val_replace", model.get("validation_engineering_replacement_allowed") is False)
    ok("model.no_auth_redef", model.get("authorization_standard_redefinition_allowed") is False)
    ok("model.no_provider", model.get("provider_execution_allowed") is False)
    ok("model.no_runtime", model.get("runtime_enabled_now") is False)
    ok("model.absorbs", model.get("absorbs_existing_detection_chain") is True)
    ok("model.no_parallel", model.get("creates_parallel_system") is False)
    ok("model.default_system", model.get("default_entry_layer") == "system")

    ok("visibility.all10", visibility.get("all_domains_pass") is True)
    for domain in WHITEBOX_VISIBILITY_DOMAINS:
        ok(f"domain.{domain[:15]}", any(
            d.get("domain") == domain and d.get("pass") is True
            for d in (visibility.get("visibility_domains") or [])
        ))

    ok("val_abs.pass", val_abs.get("dryrun_and_review_pass") is True)
    ok("val_abs.executor", val_abs.get("validation_engineering_remains_executor_gatekeeper") is True)
    ok("val_abs.visibility", val_abs.get("whitebox_only_visibility_explainability_auditability") is True)
    for m in VALIDATION_ABSORPTION:
        ok(f"absorb.{m['component'][:12]}", any(
            x.get("component") == m["component"] and x.get("absorbed") is True
            for x in (val_abs.get("mappings") or [])
        ))

    ok("chv.pass", chv.get("dryrun_and_review_pass") is True)
    ok("chv.replaces_none", chv.get("whitebox_replaces_none") is True)
    for m in CHV_MAPPING:
        ok(f"chv.{m['layer'][:15]}", any(
            x.get("layer") == m["layer"] for x in (chv.get("mappings") or [])
        ))

    ok("factory.pass", factory.get("dryrun_and_review_pass") is True)
    for m in FACTORY_AUTH_MAPPING:
        ok(f"factory.{m['artifact'][:12]}", any(
            x.get("artifact") == m["artifact"] for x in (factory.get("mappings") or [])
        ))

    ok("evidence.pass", evidence.get("dryrun_and_review_pass") is True)
    for m in EVIDENCE_TRACE_MAPPING:
        ok(f"evidence.{m['artifact'][:12]}", any(
            x.get("artifact") == m["artifact"] for x in (evidence.get("mappings") or [])
        ))

    ok("global.pass", global_local.get("dryrun_and_review_pass") is True)
    ok("global.system_first", global_local.get("inspect_system_before_module") is True)
    ok("global.chain_first", global_local.get("inspect_chain_before_node") is True)
    ok("global.resp_first", global_local.get("inspect_responsibility_before_implementation") is True)
    ok("global.midplatform_first", global_local.get("inspect_midplatform_decision_before_provider_detail") is True)
    ok("global.upstream_signal", global_local.get("local_check_requires_upstream_signal") is True)
    for principle in GLOBAL_TO_LOCAL_PRINCIPLES:
        ok(f"principle.{principle[:18]}", principle in (global_local.get("hard_principles") or []))

    ok("layers.pass", layers.get("dryrun_and_review_pass") is True)
    ok("layers.default_system", layers.get("default_entry_layer") == "system")
    ok("layers.node_upstream", layers.get("node_level_requires_upstream_trigger") is True)
    ok("layers.node_not_global", layers.get("node_level_checks_do_not_define_global_health") is True)
    for layer in INSPECTION_LAYERS:
        ok(f"layer.{layer['layer_id'][:12]}", any(
            l.get("layer_id") == layer["layer_id"] for l in (layers.get("layers") or [])
        ))

    ok("drilldown.pass", drilldown.get("dryrun_and_review_pass") is True)
    ok("drilldown.node_only", drilldown.get("node_level_drilldown_only") is True)

    ok("ocr.pass", ocr_local.get("dryrun_and_review_pass") is True)
    ok("ocr.node_level", ocr_local.get("package_cache_hash_import_read_only") is True)
    ok("ocr.no_auto_fix", ocr_local.get("failures_do_not_trigger_install_download_repair") is True)
    ok("ocr.no_finalize", ocr_local.get("does_not_finalize_provider") is True)
    ok("ocr.no_runtime", ocr_local.get("does_not_enable_runtime") is True)
    ok("ocr.no_smoke", ocr_local.get("does_not_authorize_smoke_sample_ocr") is True)

    ok("no_parallel.pass", no_parallel.get("dryrun_and_review_pass") is True)
    ok("no_parallel.true", no_parallel.get("no_new_parallel_whitebox_system") is True)
    ok("no_parallel.preserved", no_parallel.get("historical_detection_artifacts_preserved") is True)
    ok("no_parallel.not_invalid", no_parallel.get("previous_work_not_invalidated") is True)

    ok("boundary.pass", boundary.get("dryrun_and_review_pass") is True)
    ok("boundary.forbidden_absent", boundary.get("forbidden_actions_absent") is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count12", blocked.get("blocked_count") == len(BLOCKED_PATHS))
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp[:20]}", any(
            x.get("blocked_path") == bp and x.get("blocked") is True
            for x in (blocked.get("blocked_paths") or [])
        ))

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("closure.model_valid", closure.get("whitebox_model_candidate_valid") is True)
    ok("closure.domains10", closure.get("ten_visibility_domains_pass") is True)

    ok("next_route.resume", next_route.get("ready_for_midplatform_core_architecture_resume") is True)
    ok("next_route.no_runtime", next_route.get("whitebox_runtime_enabled") is False)
    ok("next_route.ocr_blocked", next_route.get("ocr_local_inspection_expansion_blocked") is True)

    ok("planning_input.pass", planning_input.get("review_pass") is True)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("dryrun_and_review_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "dryrun_and_review_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "whitebox_model_candidate_generated": True,
        "no_parallel_whitebox": True,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
