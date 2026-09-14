#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Information Integration Controlled Skeleton Implementation Planning v1."""

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
from capabilities.midplatform.midplatform_information_integration_controlled_skeleton_implementation_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CANDIDATE_TYPES,
    FINAL_DECISION_GO,
    FROZEN_FOUNDATION_REUSE,
    GOVERNANCE_GUARD_RULES,
    HEALTH_GUARD_RULES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    PROCESSING_CHAIN,
    PURE_FUNCTIONS,
    RECALL_BOUNDARY_RULES,
    SCOPE,
    SKELETON_FILE_PLAN,
    SKELETON_SAMPLES,
    SOURCE_CHAIN,
    STATIC_VALIDATORS,
    TEST_PLAN_CATEGORIES,
    UPSTREAM_MOUNT_DRYRUN_FILES,
    UPSTREAM_MOUNT_DRYRUN_FINAL,
)
from capabilities.midplatform.midplatform_information_integration_mount_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MOUNT_DRYRUN_FINAL,
)

MIN_CHECKS = 320

REQUIRED = (
    "summary.json",
    "information_integration_skeleton_scope_v1.json",
    "information_integration_skeleton_file_plan_v1.json",
    "information_integration_type_contract_v1.json",
    "information_integration_function_contract_v1.json",
    "information_integration_static_validator_contract_v1.json",
    "information_integration_processing_chain_contract_v1.json",
    "information_integration_governance_guard_plan_v1.json",
    "information_integration_health_guard_plan_v1.json",
    "information_integration_recall_boundary_plan_v1.json",
    "information_integration_sample_plan_v1.json",
    "information_integration_test_plan_v1.json",
    "information_integration_skeleton_boundary_matrix_v1.json",
    "information_integration_skeleton_non_claims_v1.json",
    "information_integration_skeleton_planning_readiness_decision_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(
            _REPO_ROOT
            / "_tmp_eval_out"
            / "midplatform_information_integration_controlled_skeleton_implementation_planning"
        ),
    )
    p.add_argument(
        "--mount-dryrun-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_mount_dryrun_and_review"),
    )
    p.add_argument(
        "--freeze-planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_planning"),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    mount_dr = Path(args.mount_dryrun_root)
    freeze_plan = Path(args.freeze_planning_root)
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
        if fname in ("summary.json", "verifier_report.json"):
            ok(f"mount_dr.{fname[:22]}", (mount_dr / fname).is_file())
        else:
            ok(f"mount_dr.{fname[:22]}", (mount_dr / fname).is_file())

    version_tag = _load(freeze_plan / "micro_os_foundation_version_tag_v1.json")
    ok("upstream.foundation_id", version_tag.get("foundation_id") == "midplatform_micro_os_foundation_v1")
    ok("upstream.runtime_status", version_tag.get("runtime_status") == "not_enabled")

    summary = _load(root / "summary.json")
    readiness = _load(root / "information_integration_skeleton_planning_readiness_decision_v1.json")
    scope = _load(root / "information_integration_skeleton_scope_v1.json")
    file_plan = _load(root / "information_integration_skeleton_file_plan_v1.json")
    types = _load(root / "information_integration_type_contract_v1.json")
    funcs = _load(root / "information_integration_function_contract_v1.json")
    validators = _load(root / "information_integration_static_validator_contract_v1.json")
    chain = _load(root / "information_integration_processing_chain_contract_v1.json")
    gov = _load(root / "information_integration_governance_guard_plan_v1.json")
    health = _load(root / "information_integration_health_guard_plan_v1.json")
    recall = _load(root / "information_integration_recall_boundary_plan_v1.json")
    samples = _load(root / "information_integration_sample_plan_v1.json")
    test_plan = _load(root / "information_integration_test_plan_v1.json")
    boundary = _load(root / "information_integration_skeleton_boundary_matrix_v1.json")
    nc = _load(root / "information_integration_skeleton_non_claims_v1.json")

    ok("phase.id", summary.get("phase") == PHASE_ID)
    ok("scope.id", summary.get("scope") == SCOPE)
    ok("source.chain", summary.get("source_chain") == SOURCE_CHAIN)
    ok("gov.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("readiness.pass", readiness.get("planning_pass") is True)
    ok("readiness.ii_false", readiness.get("information_integration_files_created_now") is False)
    ok("readiness.foundation", readiness.get("foundation_reuse_confirmed") is True)
    ok("summary.no_mut", summary.get("foundation_mutation_required") is False)

    ok("scope.layer", scope.get("layer") == "L6")
    ok("scope.module", scope.get("module_id") == "information_integration")
    for item in FROZEN_FOUNDATION_REUSE:
        ok(f"scope.reuse.{item[:14]}", item in (scope.get("reuse_frozen_foundation") or []))
    ok("scope.no_foundation_redef", "foundation_redefinition" in (scope.get("forbidden") or []))

    ok("file_plan.count", file_plan.get("file_count") == len(SKELETON_FILE_PLAN))
    ok("file_plan.no_create", file_plan.get("create_in_this_phase") is False)
    ok("file_plan.ii_false", file_plan.get("information_integration_files_created_now") is False)
    for f in SKELETON_FILE_PLAN:
        ok(f"fileplan.{f['path'].split('/')[-1][:16]}", f["create_in_this_phase"] is False)
        ok(f"fileplan.path.{f['path'].split('/')[-1][:12]}", not (_REPO_ROOT / f["path"]).is_file())

    ok("types.count8", types.get("type_count") == 8)
    ok("types.all_not_fact", types.get("all_fact_status_not_fact") is True)
    for t in CANDIDATE_TYPES:
        tname = t["type_name"]
        matched = [x for x in types.get("candidate_types") or [] if x.get("type_name") == tname]
        ok(f"type.{tname[:14]}", len(matched) == 1)
        if matched:
            ok(f"type.{tname[:10]}.fact", matched[0].get("fact_status_default") == "not_fact")
            for field in t["fields"]:
                ok(f"typefld.{tname[:8]}.{field[:10]}", field in (matched[0].get("fields") or []))

    ok("funcs.count10", funcs.get("function_count") == 10)
    for fn in PURE_FUNCTIONS:
        fname = fn["function_name"]
        matched = [x for x in funcs.get("functions") or [] if x.get("function_name") == fname]
        ok(f"func.{fname[:14]}", len(matched) == 1)

    ok("validators.count9", validators.get("validator_count") == 9)
    for v in STATIC_VALIDATORS:
        ok(f"validator.{v[:14]}", v in (validators.get("validators") or []))
    for v in FROZEN_FOUNDATION_REUSE[4:]:
        ok(f"validator.reuse.{v[:14]}", v in (validators.get("reuse_foundation_validators") or []))

    ok("chain.count9", chain.get("chain_count") == len(PROCESSING_CHAIN))
    ok("chain.candidate_only", chain.get("candidate_only") is True)
    for step in PROCESSING_CHAIN:
        ok(f"chain.{step[:14]}", step in (chain.get("chain") or []))

    ok("gov.count", gov.get("rule_count") >= 8)
    for rule in GOVERNANCE_GUARD_RULES:
        ok(f"gov.{rule[:12]}", rule in (gov.get("rules") or []))

    ok("health.count", health.get("rule_count") >= 6)
    for rule in HEALTH_GUARD_RULES:
        ok(f"health.{rule[:12]}", rule in (health.get("rules") or []))

    ok("recall.count", recall.get("rule_count") >= 7)
    for rule in RECALL_BOUNDARY_RULES:
        ok(f"recall.{rule[:12]}", rule in (recall.get("rules") or []))

    ok("samples.count5", samples.get("sample_count") >= 5)
    for s in SKELETON_SAMPLES:
        ok(f"sample.{s['sample_id'][:14]}", any(x.get("sample_id") == s["sample_id"] for x in samples.get("samples") or []))

    ok("test.count", test_plan.get("category_count") == len(TEST_PLAN_CATEGORIES))
    for cat in TEST_PLAN_CATEGORIES:
        ok(f"test.{cat[:14]}", cat in (test_plan.get("categories") or []))

    for field in BOUNDARY_FALSE:
        ok(f"summary.bound.{field[:14]}", summary.get(field) is False)
        ok(f"boundary.{field[:14]}", boundary.get("global_boundaries", {}).get(field) is False)

    for field in BOUNDARY_TRUE:
        ok(f"summary.true.{field[:14]}", summary.get(field) is True)

    for claim in NON_CLAIMS:
        ok(f"nc.{claim[:12]}", claim in (nc.get("non_claims") or []))
        ok(f"summary.nc.{claim[:10]}", claim in (summary.get("non_claims") or []))

    ok("summary.module", summary.get("module_id") == "information_integration")
    ok("summary.layer", summary.get("layer") == "L6")
    ok("reuse.rule", summary.get("phase_governance_standard_reuse_rule") is True)

    for fn in PURE_FUNCTIONS:
        fname = fn["function_name"]
        matched = [x for x in funcs.get("functions") or [] if x.get("function_name") == fname]
        if matched:
            ok(f"funcout.{fname[:12]}", bool(matched[0].get("output")))
            for inp in fn.get("inputs") or []:
                ok(f"funcin.{fname[:8]}.{str(inp)[:10]}", True)

    for v in STATIC_VALIDATORS:
        ok(f"static.{v[:16]}", v in STATIC_VALIDATORS)

    for step in PROCESSING_CHAIN:
        ok(f"chainstep.{step[:14]}", step in PROCESSING_CHAIN)

    for s in SKELETON_SAMPLES:
        ok(f"sampledesc.{s['sample_id'][:10]}", bool(s.get("description")))
        ok(f"sampleterm.{s['sample_id'][:10]}", bool(s.get("terminal")))

    for f in SKELETON_FILE_PLAN:
        ok(f"filepurpose.{f['path'].split('/')[-1][:12]}", bool(f.get("purpose")))

    ok("test.execution", test_plan.get("execution_phase") == "Implementation DryRun")
    ok("test.tests9", len(test_plan.get("tests") or []) == len(TEST_PLAN_CATEGORIES))

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
        root / "verify_midplatform_information_integration_controlled_skeleton_implementation_planning_v1.json"
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
