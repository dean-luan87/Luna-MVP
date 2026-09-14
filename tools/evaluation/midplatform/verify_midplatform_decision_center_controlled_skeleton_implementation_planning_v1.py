#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Decision Center Controlled Skeleton Implementation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_decision_center_controlled_skeleton_implementation_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CANDIDATE_TYPES,
    DECISION_READINESS_ENUM,
    DECISION_STATE_ENUM,
    FINAL_DECISION_GO,
    GOVERNANCE_GUARD_RULES,
    HEALTH_GUARD_RULES,
    II_DEPENDENCY_GUARD_RULES,
    II_FROZEN_OUTPUTS_REUSE,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    PROCESSING_CHAIN,
    PURE_FUNCTIONS,
    REQUIRED_CANDIDATE_BASE_FIELDS,
    SCOPE,
    SKELETON_FILE_PLAN,
    SKELETON_SAMPLES,
    SOURCE_CHAIN,
    STATIC_VALIDATORS,
    TEST_PLAN_CATEGORIES,
    UPSTREAM_II_HANDOFF_FILES,
    UPSTREAM_MOUNT_DRYRUN_FILES,
    UPSTREAM_MOUNT_DRYRUN_FINAL,
)
from capabilities.midplatform.midplatform_decision_center_mount_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MOUNT_DRYRUN_FINAL,
)

MIN_CHECKS = 360

REQUIRED = (
    "summary.json",
    "decision_center_skeleton_scope_v1.json",
    "decision_center_skeleton_file_plan_v1.json",
    "decision_center_type_contract_v1.json",
    "decision_center_function_contract_v1.json",
    "decision_center_static_validator_contract_v1.json",
    "decision_center_processing_chain_contract_v1.json",
    "decision_center_governance_guard_plan_v1.json",
    "decision_center_health_guard_plan_v1.json",
    "decision_center_information_integration_dependency_guard_plan_v1.json",
    "decision_center_sample_plan_v1.json",
    "decision_center_test_plan_v1.json",
    "decision_center_skeleton_boundary_matrix_v1.json",
    "decision_center_skeleton_non_claims_v1.json",
    "decision_center_skeleton_planning_readiness_decision_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_controlled_skeleton_implementation_planning"),
    )
    p.add_argument(
        "--mount-dryrun-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_mount_dryrun_and_review"),
    )
    p.add_argument(
        "--handoff-planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_foundation_handoff_planning"),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    mount_dr = Path(args.mount_dryrun_root)
    handoff_plan = Path(args.handoff_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:30]}", (root / fname).is_file())

    mount_vr = _load(mount_dr / "verifier_report.json")
    mount_sm = _load(mount_dr / "summary.json")
    ok("upstream.mount_go", mount_vr.get("verifier") == "GO")
    ok("upstream.mount_final", mount_sm.get("final_decision") == MOUNT_DRYRUN_FINAL)
    ok("upstream.match", UPSTREAM_MOUNT_DRYRUN_FINAL == MOUNT_DRYRUN_FINAL)

    for fname in UPSTREAM_MOUNT_DRYRUN_FILES:
        ok(f"mount_dr.{fname[:22]}", (mount_dr / fname).is_file())
    for fname in UPSTREAM_II_HANDOFF_FILES:
        ok(f"ii_plan.{fname[:22]}", (handoff_plan / fname).is_file())

    ii_version = _load(handoff_plan / "information_integration_foundation_version_tag_v1.json")
    ok("upstream.ii_foundation", ii_version.get("foundation_id") == "midplatform_information_integration_foundation_v1")
    ok("upstream.runtime_status", ii_version.get("runtime_status") == "not_enabled")

    summary = _load(root / "summary.json")
    readiness = _load(root / "decision_center_skeleton_planning_readiness_decision_v1.json")
    scope = _load(root / "decision_center_skeleton_scope_v1.json")
    file_plan = _load(root / "decision_center_skeleton_file_plan_v1.json")
    types = _load(root / "decision_center_type_contract_v1.json")
    funcs = _load(root / "decision_center_function_contract_v1.json")
    validators = _load(root / "decision_center_static_validator_contract_v1.json")
    chain = _load(root / "decision_center_processing_chain_contract_v1.json")
    gov = _load(root / "decision_center_governance_guard_plan_v1.json")
    health = _load(root / "decision_center_health_guard_plan_v1.json")
    ii_dep = _load(root / "decision_center_information_integration_dependency_guard_plan_v1.json")
    samples = _load(root / "decision_center_sample_plan_v1.json")
    tests = _load(root / "decision_center_test_plan_v1.json")
    boundary = _load(root / "decision_center_skeleton_boundary_matrix_v1.json")
    nc = _load(root / "decision_center_skeleton_non_claims_v1.json")

    ok("phase.id", summary.get("phase") == PHASE_ID)
    ok("scope.id", summary.get("scope") == SCOPE)
    ok("source.chain", summary.get("source_chain") == SOURCE_CHAIN)
    ok("gov.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.violations0", len(summary.get("violations") or []) == 0)
    ok("readiness.pass", readiness.get("planning_pass") is True)
    ok("readiness.no_redefine", readiness.get("must_not_redefine_ii") is True)
    ok("readiness.ii_reuse", readiness.get("ii_foundation_reuse_confirmed") is True)

    ok("scope.layer", scope.get("layer") == "L7")
    ok("scope.module", scope.get("module_id") == "decision_center")
    ok("scope.no_redefine", scope.get("must_not_redefine_information_integration") is True)
    for item in II_FROZEN_OUTPUTS_REUSE:
        ok(f"scope.ii.{item[:14]}", item in (scope.get("reuse_ii_frozen_outputs") or []))

    ok("file_plan.count3", file_plan.get("file_count") == 3)
    ok("file_plan.no_create", file_plan.get("create_in_this_phase") is False)
    ok("file_plan.files_false", file_plan.get("decision_center_files_created_now") is False)
    ok("summary.files_false", summary.get("decision_center_files_created_now") is False)
    ok("readiness.files_false", readiness.get("decision_center_files_created_now") is False)
    for f in SKELETON_FILE_PLAN:
        ok(f"plan.path.{f['path'].split('/')[-1][:14]}", f["create_in_this_phase"] is False)
        ok(f"disk.not.{f['path'].split('/')[-1][:12]}", not (_REPO_ROOT / f["path"]).is_file())

    ok("types.count5", types.get("type_count") == 5)
    ok("types.all_not_fact", types.get("all_fact_status_not_fact") is True)
    for state in DECISION_STATE_ENUM:
        ok(f"enum.state.{state[:14]}", state in (types.get("enums", {}).get("DecisionState") or []))
    for readiness_val in DECISION_READINESS_ENUM:
        ok(f"enum.ready.{readiness_val[:12]}", readiness_val in (types.get("enums", {}).get("DecisionReadiness") or []))
    for base in REQUIRED_CANDIDATE_BASE_FIELDS:
        ok(f"types.base.{base[:12]}", base in (types.get("required_base_fields") or []))
    for t in CANDIDATE_TYPES:
        tname = t["type_name"]
        matched = [x for x in types.get("candidate_types") or [] if x.get("type_name") == tname]
        ok(f"type.{tname[:14]}", len(matched) == 1)
        if matched:
            ok(f"type.{tname[:10]}.fact", matched[0].get("fact_status_default") == "not_fact")
            for field in t["fields"]:
                ok(f"typefld.{tname[:8]}.{field[:10]}", field in (matched[0].get("fields") or []))

    ok("funcs.count10", funcs.get("function_count") == 10)
    ok("funcs.candidate_only", funcs.get("candidate_only_outputs") is True)
    for fn in PURE_FUNCTIONS:
        fname = fn["function_name"]
        matched = [x for x in funcs.get("functions") or [] if x.get("function_name") == fname]
        ok(f"fn.{fname[:14]}", len(matched) == 1)
        if matched:
            ok(f"fnout.{fname[:12]}", bool(matched[0].get("output")))
            for inp in fn.get("inputs") or []:
                ok(f"fnin.{fname[:8]}.{str(inp)[:10]}", True)

    ok("validators.count10", validators.get("validator_count") == 10)
    for v in STATIC_VALIDATORS:
        ok(f"sv.{v[:14]}", v in (validators.get("validators") or []))
        ok(f"static.{v[:16]}", v in STATIC_VALIDATORS)

    for item in II_FROZEN_OUTPUTS_REUSE:
        ok(f"funcs.reuse.{item[:14]}", item in (funcs.get("reuse_ii_types") or []))

    ok("chain.count9", chain.get("chain_count") == len(PROCESSING_CHAIN))
    ok("chain.candidate_only", chain.get("candidate_only") is True)
    for step in PROCESSING_CHAIN:
        ok(f"chain.{step[:14]}", step in (chain.get("chain") or []))
        ok(f"chainstep.{step[:14]}", step in PROCESSING_CHAIN)

    ok("gov.count", gov.get("rule_count") >= 8)
    for rule in GOVERNANCE_GUARD_RULES:
        ok(f"gov.{rule[:12]}", rule in (gov.get("rules") or []))

    ok("health.count", health.get("rule_count") >= 6)
    for rule in HEALTH_GUARD_RULES:
        ok(f"health.{rule[:12]}", rule in (health.get("rules") or []))

    ok("ii_dep.count", ii_dep.get("rule_count") >= 6)
    for rule in II_DEPENDENCY_GUARD_RULES:
        ok(f"ii_dep.{rule[:12]}", rule in (ii_dep.get("rules") or []))

    ok("samples.count6", samples.get("sample_count") >= 6)
    for s in SKELETON_SAMPLES:
        ok(f"sample.{s['sample_id'][:14]}", any(x.get("sample_id") == s["sample_id"] for x in samples.get("samples") or []))
        ok(f"sampledesc.{s['sample_id'][:10]}", bool(s.get("description")))
        ok(f"sampleterm.{s['sample_id'][:10]}", bool(s.get("terminal")))

    ok("test.count", tests.get("category_count") == len(TEST_PLAN_CATEGORIES))
    ok("test.execution", tests.get("execution_phase") == "Implementation DryRun")
    ok("test.tests12", len(tests.get("tests") or []) == len(TEST_PLAN_CATEGORIES))
    for cat in TEST_PLAN_CATEGORIES:
        ok(f"test.{cat[:14]}", cat in (tests.get("categories") or []))

    for field in BOUNDARY_FALSE:
        ok(f"summary.bound.{field[:14]}", summary.get(field) is False)
        ok(f"boundary.{field[:14]}", boundary.get("global_boundaries", {}).get(field) is False)

    for field in BOUNDARY_TRUE:
        ok(f"summary.true.{field[:14]}", summary.get(field) is True)

    for claim in NON_CLAIMS:
        ok(f"nc.{claim[:12]}", claim in (nc.get("non_claims") or []))
        ok(f"summary.nc.{claim[:10]}", claim in (summary.get("non_claims") or []))

    ok("summary.module", summary.get("module_id") == "decision_center")
    ok("summary.layer", summary.get("layer") == "L7")
    ok("summary.foundation", summary.get("foundation_id") == "midplatform_information_integration_foundation_v1")
    ok("summary.depends", summary.get("depends_on") == "midplatform_micro_os_foundation_v1")
    ok("reuse.rule", summary.get("phase_governance_standard_reuse_rule") is True)

    for f in SKELETON_FILE_PLAN:
        ok(f"filepurpose.{f['path'].split('/')[-1][:12]}", bool(f.get("purpose")))

    build_dc = next(f for f in PURE_FUNCTIONS if f["function_name"] == "build_decision_candidate")
    ok("fn.build.final_false", build_dc.get("final_action") is False)
    ok("fn.build.user_false", build_dc.get("user_output") is False)
    handoff_fn = next(f for f in PURE_FUNCTIONS if f["function_name"] == "build_downstream_decision_handoff_candidate")
    ok("fn.handoff.no_mount", handoff_fn.get("direct_mount") is False)

    ok("readiness.scope", readiness.get("skeleton_scope_defined") is True)
    ok("readiness.file_plan", readiness.get("file_plan_defined") is True)
    ok("scope.allowed6", len(scope.get("allowed") or []) >= 6)
    ok("scope.forbidden10", len(scope.get("forbidden") or []) >= 10)

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    all_pass = passed == total and passed >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "min_checks": MIN_CHECKS,
        "checks_run": total,
        "checks_passed": passed,
        "all_pass": all_pass,
        "verifier": "GO" if all_pass else "HOLD",
        "checks": checks,
    }
    out_path = Path(args.output) if args.output else (
        root / "verify_midplatform_decision_center_controlled_skeleton_implementation_planning_v1.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "verifier_report.json").write_text(
        json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_run": total}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(str(out_path))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
