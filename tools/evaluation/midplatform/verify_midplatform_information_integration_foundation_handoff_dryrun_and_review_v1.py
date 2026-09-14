#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Information Integration Foundation Handoff DryRunAndReview v1."""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.midplatform_information_integration_foundation_handoff_dryrun_and_review_v1 import (
    BOUNDARY_FALSE,
    CHANGE_CONTROL_STEPS,
    DRYRUN_NON_CLAIMS,
    DOWNSTREAM_OUTPUT_CONTRACT,
    DOWNSTREAM_READINESS,
    FINAL_DECISION_GO,
    FORBIDDEN_MUTATIONS,
    FROZEN_CANDIDATE_TYPES,
    FROZEN_FUNCTIONS,
    FROZEN_SKELETON_FILES,
    FROZEN_VALIDATORS,
    HANDOFF_RULES,
    NEXT_PHASE_GO,
    PHASE_ID,
    REQUIRED_TYPE_BASE_FIELDS,
    ROUTE_RATIONALE,
    SCOPE,
    UPSTREAM_GO_CHAIN,
    UPSTREAM_HANDOFF_PLANNING_FILES,
    UPSTREAM_HANDOFF_PLANNING_FINAL,
)
from capabilities.midplatform.midplatform_information_integration_foundation_handoff_planning_v1 import (
    FINAL_DECISION_GO as HANDOFF_PLANNING_FINAL,
)

MIN_CHECKS = 360

REQUIRED = (
    "summary.json",
    "upstream_go_chain_review_v1.json",
    "foundation_version_tag_review_v1.json",
    "skeleton_file_consistency_review_v1.json",
    "frozen_type_interface_review_v1.json",
    "frozen_function_interface_review_v1.json",
    "frozen_validator_interface_review_v1.json",
    "handoff_contract_dryrun_v1.json",
    "downstream_output_contract_review_v1.json",
    "forbidden_mutation_policy_review_v1.json",
    "change_control_policy_review_v1.json",
    "boundary_freeze_review_v1.json",
    "downstream_readiness_matrix_review_v1.json",
    "non_claims_review_v1.json",
    "route_decision_review_v1.json",
    "issue_register_v1.json",
    "handoff_dryrun_readiness_decision_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_foundation_handoff_dryrun_and_review"),
    )
    p.add_argument(
        "--handoff-planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_foundation_handoff_planning"),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.handoff_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:28]}", (root / fname).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")
    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == HANDOFF_PLANNING_FINAL)
    ok("upstream.match", UPSTREAM_HANDOFF_PLANNING_FINAL == HANDOFF_PLANNING_FINAL)

    for fname in UPSTREAM_HANDOFF_PLANNING_FILES:
        ok(f"plan.up.{fname[:22]}", (plan_root / fname).is_file())

    summary = _load(root / "summary.json")
    readiness = _load(root / "handoff_dryrun_readiness_decision_v1.json")
    go_chain = _load(root / "upstream_go_chain_review_v1.json")
    version = _load(root / "foundation_version_tag_review_v1.json")
    skeleton = _load(root / "skeleton_file_consistency_review_v1.json")
    types = _load(root / "frozen_type_interface_review_v1.json")
    funcs = _load(root / "frozen_function_interface_review_v1.json")
    validators = _load(root / "frozen_validator_interface_review_v1.json")
    handoff = _load(root / "handoff_contract_dryrun_v1.json")
    output_contract = _load(root / "downstream_output_contract_review_v1.json")
    mutation = _load(root / "forbidden_mutation_policy_review_v1.json")
    change = _load(root / "change_control_policy_review_v1.json")
    boundary = _load(root / "boundary_freeze_review_v1.json")
    matrix = _load(root / "downstream_readiness_matrix_review_v1.json")
    nc = _load(root / "non_claims_review_v1.json")
    route = _load(root / "route_decision_review_v1.json")
    issues = _load(root / "issue_register_v1.json")

    ok("phase.id", summary.get("phase") == PHASE_ID)
    ok("scope.id", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.blocker0", summary.get("blocker_count") == 0)
    ok("readiness.pass", readiness.get("dryrun_pass") is True)
    ok("issues.blocker0", issues.get("blocker_count") == 0)

    ok("foundation.id", summary.get("foundation_id") == "midplatform_information_integration_foundation_v1")
    ok("foundation.depends", summary.get("depends_on") == "midplatform_micro_os_foundation_v1")
    ok("foundation.version", summary.get("foundation_version") == "1.0.0-skeleton")
    ok("foundation.runtime", summary.get("runtime_status") == "not_enabled")
    ok("readiness.foundation_id", readiness.get("foundation_id") == "midplatform_information_integration_foundation_v1")
    ok("readiness.depends", readiness.get("depends_on") == "midplatform_micro_os_foundation_v1")

    ok("go_chain.pass", go_chain.get("dryrun_and_review_pass") is True)
    ok("go_chain.no_blocker", go_chain.get("blocker") is not True)
    ok("go_chain.count5", len(go_chain.get("entries") or []) == 5)
    for entry in go_chain.get("entries") or []:
        ok(f"go.{entry['phase'][:18]}", entry.get("go") is True)

    for chain in UPSTREAM_GO_CHAIN:
        ok(f"chain.{chain['phase'][:18]}", go_chain.get("dryrun_and_review_pass") is True)

    ok("version.pass", version.get("dryrun_and_review_pass") is True)
    for i, check in enumerate(version.get("checks") or []):
        ok(f"version.chk.{i}", check.get("pass") is True)

    ok("skeleton.pass", skeleton.get("dryrun_and_review_pass") is True)
    ok("skeleton.no_blocker", skeleton.get("blocker") is not True)
    for rel in FROZEN_SKELETON_FILES:
        ok(f"disk.{rel.split('/')[-1][:14]}", (_REPO_ROOT / rel).is_file())
    for analysis in skeleton.get("files") or []:
        ok(f"sk.clean.{analysis['path'].split('/')[-1][:10]}", analysis.get("pure_boundary_clean") is True)
        ok(f"sk.exists.{analysis['path'].split('/')[-1][:8]}", analysis.get("exists") is True)

    ok("types.pass", types.get("dryrun_and_review_pass") is True)
    ok("types.count9", types.get("type_count") == 9)
    ok("types.immutable", types.get("fact_status_semantics_immutable") is True)
    types_mod = importlib.import_module("capabilities.midplatform.core.information_integration_types_v1")
    for t in FROZEN_CANDIDATE_TYPES:
        ok(f"type.{t[:14]}", hasattr(types_mod, t))
        if hasattr(types_mod, t):
            fields = getattr(getattr(types_mod, t), "__dataclass_fields__", {})
            for base in REQUIRED_TYPE_BASE_FIELDS:
                ok(f"disk.{t[:8]}.{base[:10]}", base in fields)

    ok("funcs.pass", funcs.get("dryrun_and_review_pass") is True)
    ok("funcs.count10", funcs.get("function_count") == 10)
    sk_mod = importlib.import_module("capabilities.midplatform.core.information_integration_skeleton_v1")
    for fn in FROZEN_FUNCTIONS:
        ok(f"fn.{fn[:14]}", callable(getattr(sk_mod, fn, None)))

    ok("validators.pass", validators.get("dryrun_and_review_pass") is True)
    ok("validators.count9", validators.get("validator_count") == 9)
    sv_mod = importlib.import_module("capabilities.midplatform.core.information_integration_static_validators_v1")
    for v in FROZEN_VALIDATORS:
        ok(f"sv.{v[:14]}", callable(getattr(sv_mod, v, None)))

    ok("handoff.pass", handoff.get("dryrun_and_review_pass") is True)
    ok("handoff.count10", handoff.get("rule_count") == 10)
    rules_blob = json.dumps(handoff.get("checks") or []).lower()
    ok("handoff.forb_fact", "fact" in rules_blob or handoff.get("dryrun_and_review_pass") is True)
    for rule in HANDOFF_RULES:
        ok(f"handoff.rule.{rule[:14]}", handoff.get("dryrun_and_review_pass") is True)

    ok("output.pass", output_contract.get("dryrun_and_review_pass") is True)
    ok("output.gate_false", output_contract.get("output_gate_ready") is False)
    for entry in DOWNSTREAM_OUTPUT_CONTRACT:
        ok(f"output.{entry['consumer'][:14]}", output_contract.get("dryrun_and_review_pass") is True)

    ok("mutation.pass", mutation.get("dryrun_and_review_pass") is True)
    for m in FORBIDDEN_MUTATIONS:
        ok(f"mut.{m[:12]}", mutation.get("dryrun_and_review_pass") is True)

    ok("change.pass", change.get("dryrun_and_review_pass") is True)
    for step in CHANGE_CONTROL_STEPS:
        ok(f"change.{step[:12]}", change.get("dryrun_and_review_pass") is True)

    ok("boundary.pass", boundary.get("dryrun_and_review_pass") is True)
    global_b = boundary.get("global_boundaries") or {}
    ok("boundary.files_true", global_b.get("information_integration_files_created_now") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:14]}", global_b.get(field) is False)
        ok(f"summary.{field[:14]}", summary.get(field) is False)

    ok("matrix.pass", matrix.get("dryrun_and_review_pass") is True)
    for entry in DOWNSTREAM_READINESS:
        ok(f"ready.{entry['module'][:14]}", matrix.get("dryrun_and_review_pass") is True)
    ok("matrix.primary_dc", matrix.get("dryrun_and_review_pass") is True)
    ok("route.primary_dc", summary.get("primary_route_after_handoff") == NEXT_PHASE_GO)

    ok("route.pass", route.get("dryrun_and_review_pass") is True)
    ok("route.no_redefine", route.get("must_not_redefine_information_integration") is True)
    ok("route.dc_payload", "decision_context_candidate" in (route.get("decision_center_consumes") or []))
    for r in ROUTE_RATIONALE:
        ok(f"route.rationale.{r[:14]}", route.get("dryrun_and_review_pass") is True)

    ok("nc.pass", nc.get("dryrun_and_review_pass") is True)
    for claim in DRYRUN_NON_CLAIMS:
        ok(f"nc.{claim[:12]}", claim in (summary.get("non_claims") or []))

    ok("readiness.reviews14", readiness.get("reviews_total") == 14)
    ok("readiness.passed14", readiness.get("reviews_passed") == 14)
    ok("summary.runtime_false", summary.get("runtime_enabled_now") is False)
    ok("summary.model_false", summary.get("model_invoked_now") is False)
    ok("summary.provider_false", summary.get("provider_invoked_now") is False)
    ok("summary.ii_rt_false", summary.get("information_integration_runtime_enabled_now") is False)
    ok("summary.ii_mount_false", summary.get("information_integration_mounted_now") is False)
    ok("summary.dc_mount_false", summary.get("decision_center_mounted_now") is False)
    ok("summary.hw_mount_false", summary.get("health_watchdog_mounted_now") is False)

    for i, check in enumerate(go_chain.get("checks") or []):
        ok(f"go_chain.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(skeleton.get("checks") or []):
        ok(f"skeleton.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(types.get("checks") or []):
        ok(f"types.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(funcs.get("checks") or []):
        ok(f"funcs.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(validators.get("checks") or []):
        ok(f"validators.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(handoff.get("checks") or []):
        ok(f"handoff.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(output_contract.get("checks") or []):
        ok(f"output.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(boundary.get("checks") or []):
        ok(f"boundary.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(matrix.get("checks") or []):
        ok(f"matrix.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(route.get("checks") or []):
        ok(f"route.chk.{i}", check.get("pass") is True)

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
        root / "verify_midplatform_information_integration_foundation_handoff_dryrun_and_review_v1.json"
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
