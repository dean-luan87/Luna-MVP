#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Information Integration Foundation Handoff Planning v1."""

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

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_DRYRUN_FINAL,
)
from capabilities.midplatform.midplatform_information_integration_foundation_handoff_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CHANGE_CONTROL_STEPS,
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
    NON_CLAIMS,
    PHASE_ID,
    REQUIRED_TYPE_BASE_FIELDS,
    ROUTE_RATIONALE,
    SCOPE,
    SOURCE_CHAIN,
    UPSTREAM_POST_DRYRUN_ARTIFACTS,
    UPSTREAM_POST_DRYRUN_FINAL,
)

MIN_CHECKS = 300

REQUIRED = (
    "summary.json",
    "information_integration_foundation_handoff_scope_v1.json",
    "information_integration_foundation_version_tag_v1.json",
    "information_integration_frozen_type_interface_v1.json",
    "information_integration_frozen_function_interface_v1.json",
    "information_integration_frozen_validator_interface_v1.json",
    "information_integration_handoff_contract_v1.json",
    "information_integration_downstream_output_contract_v1.json",
    "information_integration_forbidden_mutation_policy_v1.json",
    "information_integration_change_control_policy_v1.json",
    "information_integration_boundary_freeze_v1.json",
    "information_integration_downstream_readiness_matrix_v1.json",
    "information_integration_non_claims_v1.json",
    "information_integration_route_decision_v1.json",
    "information_integration_foundation_handoff_readiness_decision_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_foundation_handoff_planning"),
    )
    p.add_argument(
        "--post-dryrun-root",
        default=str(
            _REPO_ROOT
            / "_tmp_eval_out"
            / "midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review"
        ),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    post_dr = Path(args.post_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:30]}", (root / fname).is_file())

    post_vr = _load(post_dr / "verifier_report.json")
    post_sm = _load(post_dr / "summary.json")
    ok("upstream.post_go", post_vr.get("verifier") == "GO")
    ok("upstream.post_final", post_sm.get("final_decision") == POST_DRYRUN_FINAL)
    ok("upstream.match", UPSTREAM_POST_DRYRUN_FINAL == POST_DRYRUN_FINAL)

    for fname in UPSTREAM_POST_DRYRUN_ARTIFACTS:
        ok(f"post.up.{fname[:24]}", (post_dr / fname).is_file())

    summary = _load(root / "summary.json")
    readiness = _load(root / "information_integration_foundation_handoff_readiness_decision_v1.json")
    scope = _load(root / "information_integration_foundation_handoff_scope_v1.json")
    version = _load(root / "information_integration_foundation_version_tag_v1.json")
    types = _load(root / "information_integration_frozen_type_interface_v1.json")
    funcs = _load(root / "information_integration_frozen_function_interface_v1.json")
    validators = _load(root / "information_integration_frozen_validator_interface_v1.json")
    handoff = _load(root / "information_integration_handoff_contract_v1.json")
    output_contract = _load(root / "information_integration_downstream_output_contract_v1.json")
    mutation = _load(root / "information_integration_forbidden_mutation_policy_v1.json")
    change = _load(root / "information_integration_change_control_policy_v1.json")
    boundary = _load(root / "information_integration_boundary_freeze_v1.json")
    matrix = _load(root / "information_integration_downstream_readiness_matrix_v1.json")
    nc = _load(root / "information_integration_non_claims_v1.json")
    route = _load(root / "information_integration_route_decision_v1.json")

    ok("phase.id", summary.get("phase") == PHASE_ID)
    ok("scope.id", summary.get("scope") == SCOPE)
    ok("source.chain", summary.get("source_chain") == SOURCE_CHAIN)
    ok("gov.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.violations0", len(summary.get("violations") or []) == 0)
    ok("readiness.pass", readiness.get("planning_pass") is True)
    ok("readiness.frozen", readiness.get("foundation_frozen") is True)

    ok("version.foundation_id", version.get("foundation_id") == "midplatform_information_integration_foundation_v1")
    ok("version.depends_on", version.get("depends_on") == "midplatform_micro_os_foundation_v1")
    ok("version.version", version.get("version") == "1.0.0-skeleton")
    ok("version.status", version.get("status") == "frozen_for_downstream_mount_planning")
    ok("version.runtime_status", version.get("runtime_status") == "not_enabled")
    ok("version.compat", version.get("compatibility_scope") == "planning_and_static_dryrun_only")
    ok("summary.foundation_id", summary.get("foundation_id") == "midplatform_information_integration_foundation_v1")
    ok("summary.depends_on", summary.get("depends_on") == "midplatform_micro_os_foundation_v1")

    for consumer in ("decision_center", "task_manager", "health_watchdog", "worldmodel_memory_bridge", "module_adapter", "output_gate"):
        ok(f"version.consumer.{consumer[:12]}", consumer in (version.get("allowed_consumers") or []))

    for rel in FROZEN_SKELETON_FILES:
        ok(f"skfile.{rel.split('/')[-1][:16]}", (_REPO_ROOT / rel).is_file())
        ok(f"scope.file.{rel.split('/')[-1][:12]}", rel in (scope.get("frozen_skeleton_files") or []))

    ok("scope.handoff_not_rt", scope.get("handoff_not_runtime_enabled") is True)

    ok("types.count9", types.get("type_count") == 9)
    ok("types.immutable", types.get("fact_status_semantics_immutable") is True)
    ok("types.not_fact", types.get("fact_status_default") == "not_fact")
    for t in FROZEN_CANDIDATE_TYPES:
        ok(f"type.{t[:14]}", t in (types.get("types") or []))
        ok(f"scope.type.{t[:12]}", t in (scope.get("frozen_candidate_types") or []))
    for field in REQUIRED_TYPE_BASE_FIELDS:
        ok(f"type.base.{field[:12]}", field in (types.get("required_base_fields") or []))

    types_mod = importlib.import_module("capabilities.midplatform.core.information_integration_types_v1")
    for t in FROZEN_CANDIDATE_TYPES:
        cls = getattr(types_mod, t, None)
        ok(f"disk.type.{t[:14]}", cls is not None)
        if cls:
            fields = getattr(cls, "__dataclass_fields__", {})
            for base in REQUIRED_TYPE_BASE_FIELDS:
                ok(f"disk.{t[:8]}.{base[:10]}", base in fields)

    ok("funcs.count10", funcs.get("function_count") == 10)
    ok("funcs.candidate_only", funcs.get("candidate_only_outputs") is True)
    ok("funcs.no_runtime", funcs.get("runtime_execution") is False)
    sk_mod = importlib.import_module("capabilities.midplatform.core.information_integration_skeleton_v1")
    for fn in FROZEN_FUNCTIONS:
        ok(f"fn.{fn[:14]}", fn in (funcs.get("functions") or []))
        ok(f"disk.fn.{fn[:14]}", callable(getattr(sk_mod, fn, None)))
        ok(f"scope.fn.{fn[:12]}", fn in (scope.get("frozen_functions") or []))

    ok("validators.count9", validators.get("validator_count") == 9)
    ok("validators.reusable", validators.get("reusable_by_downstream") is True)
    sv_mod = importlib.import_module("capabilities.midplatform.core.information_integration_static_validators_v1")
    for v in FROZEN_VALIDATORS:
        ok(f"sv.{v[:14]}", v in (validators.get("validators") or []))
        ok(f"disk.sv.{v[:14]}", callable(getattr(sv_mod, v, None)))
        ok(f"scope.sv.{v[:12]}", v in (scope.get("frozen_validators") or []))

    ok("handoff.count", handoff.get("rule_count") == len(HANDOFF_RULES))
    for rule in HANDOFF_RULES:
        ok(f"handoff.{rule[:18]}", rule in (handoff.get("rules") or []))
    rules_blob = json.dumps(handoff.get("rules") or []).lower()
    ok("handoff.not_fact", "fact" in rules_blob)
    ok("handoff.not_decision", "final decision" in rules_blob)
    ok("handoff.not_output", "user output" in rules_blob)

    ok("output.count", output_contract.get("entry_count") == len(DOWNSTREAM_OUTPUT_CONTRACT))
    ok("output.gate_false", output_contract.get("output_gate_ready") is False)
    for entry in DOWNSTREAM_OUTPUT_CONTRACT:
        matched = [e for e in output_contract.get("entries") or [] if e.get("consumer") == entry["consumer"]]
        ok(f"output.{entry['consumer'][:14]}", len(matched) == 1)
        if matched:
            ok(f"output.{entry['consumer'][:10]}.payload", len(matched[0].get("consumes") or []) >= 1)

    ok("mutation.count", mutation.get("mutation_count") == len(FORBIDDEN_MUTATIONS))
    for m in FORBIDDEN_MUTATIONS:
        ok(f"mut.{m[:18]}", m in (mutation.get("forbidden_mutations") or []))

    ok("change.count", change.get("step_count") == len(CHANGE_CONTROL_STEPS))
    ok("change.no_exec", change.get("change_executed_in_this_phase") is False)
    for s in CHANGE_CONTROL_STEPS:
        ok(f"change.{s[:16]}", s in (change.get("steps") or []))

    global_b = boundary.get("global_boundaries") or {}
    ok("boundary.files_true", global_b.get("information_integration_files_created_now") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:16]}", global_b.get(field) is False)
        ok(f"summary.bound.{field[:16]}", summary.get(field) is False)
    for field in BOUNDARY_TRUE:
        ok(f"summary.true.{field[:16]}", summary.get(field) is True)

    ok("matrix.count", matrix.get("entry_count") == len(DOWNSTREAM_READINESS))
    for entry in DOWNSTREAM_READINESS:
        matched = [e for e in matrix.get("entries") or [] if e.get("module") == entry["module"]]
        ok(f"matrix.{entry['module'][:18]}", len(matched) == 1 and matched[0].get("readiness") == entry["readiness"])

    for claim in NON_CLAIMS:
        ok(f"nc.{claim[:16]}", claim in (nc.get("non_claims") or []))
        ok(f"summary.nc.{claim[:14]}", claim in (summary.get("non_claims") or []))

    ok("route.primary", route.get("primary_next_phase") == "Phase-Midplatform-Decision-Center-Mount-Planning-v1-001")
    ok("route.secondary", route.get("secondary_next_phase") == "Phase-Midplatform-Health-Watchdog-Mount-Planning-v1-001")
    ok("route.deferred4", len(route.get("deferred") or []) == 4)
    for r in ROUTE_RATIONALE:
        ok(f"route.rationale.{r[:14]}", r in (route.get("rationale") or []))
    ok("summary.primary", summary.get("primary_route_after_handoff") == route.get("primary_next_phase"))

    ok("summary.module", summary.get("module_id") == "information_integration")
    ok("summary.layer", summary.get("layer") == "L6")
    ok("reuse.rule", summary.get("phase_governance_standard_reuse_rule") is True)
    ok("reuse.no_new_gov", summary.get("new_governance_need_proven") is False)

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
        root / "verify_midplatform_information_integration_foundation_handoff_planning_v1.json"
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
