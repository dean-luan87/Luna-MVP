#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Health Watchdog Foundation Handoff DryRunAndReview v1."""

from __future__ import annotations

import argparse
import dataclasses
import importlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_health_watchdog_foundation_handoff_dryrun_and_review_v1 import (
    ALSO_DEPENDS_ON,
    ALSO_DEPENDS_ON_MICRO_OS,
    CHANGE_CONTROL_STEPS,
    COMPATIBILITY_SCOPE,
    DEPENDS_ON,
    DOWNSTREAM_OUTPUT_CONTRACT,
    DOWNSTREAM_READINESS,
    DRYRUN_NON_CLAIMS,
    FINAL_DECISION_GO,
    FORBIDDEN_MUTATIONS,
    FOUNDATION_ID,
    FOUNDATION_STATUS,
    FOUNDATION_VERSION,
    FROZEN_CANDIDATE_TYPES,
    FROZEN_ENUM_TYPES,
    HANDOFF_RULES,
    NEXT_PHASE_GO,
    PHASE_ID,
    REQUIRED_TYPE_BASE_FIELDS,
    RUNTIME_FALSE_FLAGS,
    SCOPE,
    SKELETON_FILES,
    STATIC_VALIDATOR_NAMES,
    PURE_FUNCTION_NAMES,
    UPSTREAM_GO_CHAIN,
    UPSTREAM_HANDOFF_PLANNING_FILES,
    UPSTREAM_HANDOFF_PLANNING_FINAL,
)
from capabilities.midplatform.midplatform_health_watchdog_foundation_handoff_planning_v1 import (
    FINAL_DECISION_GO as HANDOFF_PLANNING_FINAL,
)

MIN_CHECKS = 400
DEFAULT_OUTPUT = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_foundation_handoff_dryrun_and_review"
)
DEFAULT_PLANNING = REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_foundation_handoff_planning"

REQUIRED_ARTIFACTS: Tuple[str, ...] = (
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
    "summary.json",
)

EXPECTED_STATES = (
    "received",
    "validating",
    "health_signal_review",
    "stale_context_review",
    "low_confidence_review",
    "p0_safety_review",
    "governance_review",
    "degradation_candidate_generated",
    "recovery_recommendation_candidate_generated",
    "required_observation_generated",
    "hold",
    "blocked",
    "not_ready",
    "watchdog_handoff_ready",
    "discarded_invalid",
)
EXPECTED_SEVERITIES = ("info", "low", "medium", "high", "critical")


def _read(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def _field_default(cls: Any, field_name: str) -> Any:
    field = cls.__dataclass_fields__[field_name]
    if field.default is not dataclasses.MISSING:
        return field.default
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--handoff-planning-root", default=str(DEFAULT_PLANNING))
    args = parser.parse_args()
    root = Path(args.output_root)
    plan = Path(args.handoff_planning_root)
    docs = {fname: _read(root / fname) for fname in REQUIRED_ARTIFACTS}
    checks: List[Dict[str, Any]] = []

    for fname in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{fname}", bool(docs[fname]))

    plan_summary = _read(plan / "summary.json")
    plan_verifier = _read(plan / "verifier_report.json")
    _add(checks, "upstream.planning.verifier_go", plan_verifier.get("verifier") == "GO")
    _add(checks, "upstream.planning.final_go", plan_summary.get("final_decision") == HANDOFF_PLANNING_FINAL)
    _add(checks, "upstream.planning.match", UPSTREAM_HANDOFF_PLANNING_FINAL == HANDOFF_PLANNING_FINAL)
    for fname in UPSTREAM_HANDOFF_PLANNING_FILES:
        _add(checks, f"planning.artifact.{fname}", (plan / fname).is_file())

    summary = docs["summary.json"]
    readiness = docs["handoff_dryrun_readiness_decision_v1.json"]
    go_chain = docs["upstream_go_chain_review_v1.json"]
    version = docs["foundation_version_tag_review_v1.json"]
    skeleton = docs["skeleton_file_consistency_review_v1.json"]
    types = docs["frozen_type_interface_review_v1.json"]
    funcs = docs["frozen_function_interface_review_v1.json"]
    validators = docs["frozen_validator_interface_review_v1.json"]
    handoff = docs["handoff_contract_dryrun_v1.json"]
    output_contract = docs["downstream_output_contract_review_v1.json"]
    mutation = docs["forbidden_mutation_policy_review_v1.json"]
    change = docs["change_control_policy_review_v1.json"]
    boundary = docs["boundary_freeze_review_v1.json"]
    matrix = docs["downstream_readiness_matrix_review_v1.json"]
    non_claims = docs["non_claims_review_v1.json"]
    route = docs["route_decision_review_v1.json"]
    issues = docs["issue_register_v1.json"]

    _add(checks, "phase.id", summary.get("phase") == PHASE_ID)
    _add(checks, "scope.id", summary.get("scope") == SCOPE)
    _add(checks, "summary.pass", summary.get("dryrun_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "readiness.pass", readiness.get("dryrun_pass") is True)
    _add(checks, "readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "issues.blocker0", issues.get("blocker_count") == 0)

    for doc_name, doc in docs.items():
        _add(checks, f"meta.foundation.{doc_name}", doc.get("foundation_id") == FOUNDATION_ID)
        _add(checks, f"meta.depends.{doc_name}", doc.get("depends_on") == DEPENDS_ON)
        _add(checks, f"meta.also_depends.{doc_name}", doc.get("also_depends_on") == ALSO_DEPENDS_ON)
        _add(checks, f"meta.micro_os.{doc_name}", doc.get("also_depends_on_micro_os") == ALSO_DEPENDS_ON_MICRO_OS)
        _add(checks, f"meta.version.{doc_name}", doc.get("foundation_version") == FOUNDATION_VERSION)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")

    _add(checks, "go_chain.pass", go_chain.get("dryrun_and_review_pass") is True)
    _add(checks, "go_chain.no_blocker", go_chain.get("blocker") is not True)
    _add(checks, "go_chain.count7", len(go_chain.get("entries") or []) == 7)
    entries = {e.get("phase"): e for e in go_chain.get("entries") or []}
    for chain in UPSTREAM_GO_CHAIN:
        entry = entries.get(chain["phase"]) or {}
        _add(checks, f"go_chain.phase.{chain['phase']}", entry.get("go") is True)
        _add(checks, f"go_chain.final.{chain['phase']}", entry.get("expected_final") == chain["expected_final"])

    _add(checks, "version.pass", version.get("dryrun_and_review_pass") is True)
    _add(checks, "version.foundation_id", version.get("foundation_id") == FOUNDATION_ID)
    _add(checks, "version.depends_on", version.get("depends_on") == DEPENDS_ON)
    _add(checks, "version.also_depends", version.get("also_depends_on") == ALSO_DEPENDS_ON)
    _add(checks, "version.micro_os", version.get("also_depends_on_micro_os") == ALSO_DEPENDS_ON_MICRO_OS)
    _add(checks, "version.value", version.get("version") == FOUNDATION_VERSION)
    _add(checks, "version.status", version.get("status") == FOUNDATION_STATUS)
    _add(checks, "version.runtime", version.get("runtime_status") == "not_enabled")
    _add(checks, "version.compat", version.get("compatibility_scope") == COMPATIBILITY_SCOPE)

    _add(checks, "skeleton.pass", skeleton.get("dryrun_and_review_pass") is True)
    _add(checks, "skeleton.no_blocker", skeleton.get("blocker") is not True)
    _add(checks, "skeleton.no_forbidden", len(skeleton.get("forbidden_imports_found") or []) == 0)
    for rel in SKELETON_FILES:
        _add(checks, f"skeleton.disk.{rel}", (REPO_ROOT / rel).is_file())
    for analysis in skeleton.get("files") or []:
        _add(checks, f"skeleton.exists.{analysis.get('path')}", analysis.get("exists") is True)
        _add(checks, f"skeleton.clean.{analysis.get('path')}", analysis.get("pure_boundary_clean") is True)
        _add(checks, f"skeleton.no_async.{analysis.get('path')}", analysis.get("async_function_count") == 0)
        _add(checks, f"skeleton.no_loop.{analysis.get('path')}", analysis.get("while_true_count") == 0)

    types_mod = importlib.import_module("capabilities.midplatform.core.health_watchdog_types_v1")
    _add(checks, "types.pass", types.get("dryrun_and_review_pass") is True)
    _add(checks, "types.count6", types.get("type_count") == 6)
    _add(checks, "types.state15", types.get("health_watchdog_state_count") == 15)
    _add(checks, "types.severity5", types.get("health_severity_count") == 5)
    for enum_name in FROZEN_ENUM_TYPES:
        _add(checks, f"types.enum.{enum_name}", hasattr(types_mod, enum_name))
    for state in EXPECTED_STATES:
        _add(checks, f"types.state.{state}", any(s.value == state for s in types_mod.HealthWatchdogState))
    for severity in EXPECTED_SEVERITIES:
        _add(checks, f"types.severity.{severity}", any(s.value == severity for s in types_mod.HealthSeverity))
    for type_name in FROZEN_CANDIDATE_TYPES:
        cls = getattr(types_mod, type_name, None)
        fields = getattr(cls, "__dataclass_fields__", {}) if cls else {}
        _add(checks, f"type.exists.{type_name}", cls is not None)
        for base in REQUIRED_TYPE_BASE_FIELDS:
            _add(checks, f"type.field.{type_name}.{base}", base in fields)
        if "fact_status" in fields:
            _add(checks, f"type.not_fact.{type_name}", fields["fact_status"].default == "not_fact")
    _add(checks, "type.degradation.false", _field_default(types_mod.DegradationCandidate, "real_degradation") is False)
    _add(checks, "type.recovery.execution_false", _field_default(types_mod.RecoveryRecommendationCandidate, "recovery_execution") is False)
    _add(checks, "type.recovery.restart_false", _field_default(types_mod.RecoveryRecommendationCandidate, "restart_allowed") is False)
    _add(checks, "type.recovery.process_false", _field_default(types_mod.RecoveryRecommendationCandidate, "process_control_allowed") is False)
    _add(checks, "type.handoff.direct_mount_false", _field_default(types_mod.WatchdogHandoffCandidate, "direct_mount") is False)

    skeleton_mod = importlib.import_module("capabilities.midplatform.core.health_watchdog_skeleton_v1")
    _add(checks, "functions.pass", funcs.get("dryrun_and_review_pass") is True)
    for name in PURE_FUNCTION_NAMES:
        _add(checks, f"function.callable.{name}", callable(getattr(skeleton_mod, name, None)))
        _add(checks, f"function.artifact.{name}", name in (funcs.get("functions") or []))

    validators_mod = importlib.import_module("capabilities.midplatform.core.health_watchdog_static_validators_v1")
    _add(checks, "validators.pass", validators.get("dryrun_and_review_pass") is True)
    for name in STATIC_VALIDATOR_NAMES:
        _add(checks, f"validator.callable.{name}", callable(getattr(validators_mod, name, None)))
        _add(checks, f"validator.artifact.{name}", name in (validators.get("validators") or []))

    _add(checks, "handoff.pass", handoff.get("dryrun_and_review_pass") is True)
    for rule in HANDOFF_RULES:
        _add(checks, f"handoff.rule.{rule[:50]}", rule in (handoff.get("rules") or []))
    _add(
        checks,
        "handoff.no_recovery_confusion",
        "downstream must not treat recovery_recommendation_candidate as recovery execution" in (handoff.get("rules") or []),
    )

    _add(checks, "output.pass", output_contract.get("dryrun_and_review_pass") is True)
    consumers = {row.get("consumer"): row for row in output_contract.get("outputs") or []}
    for row in DOWNSTREAM_OUTPUT_CONTRACT:
        doc = consumers.get(row["consumer"]) or {}
        _add(checks, f"output.consumer.{row['consumer']}", bool(doc))
        for item in row["consumes"]:
            _add(checks, f"output.item.{row['consumer']}.{item}", item in (doc.get("consumes") or []))
    _add(
        checks,
        "output.task_manager_candidates",
        all(
            item in (consumers.get("task_manager", {}).get("consumes") or [])
            for item in ("hold_candidate", "safety_block_candidate", "module_health_review_candidate", "watchdog_handoff_candidate")
        ),
    )

    _add(checks, "mutation.pass", mutation.get("dryrun_and_review_pass") is True)
    for item in FORBIDDEN_MUTATIONS:
        _add(checks, f"mutation.{item[:50]}", item in (mutation.get("forbidden_mutations") or []))
    _add(checks, "change.pass", change.get("dryrun_and_review_pass") is True)
    _add(checks, "change.no_real", change.get("real_change_executed_now") is False)
    for step in CHANGE_CONTROL_STEPS:
        _add(checks, f"change.{step}", step in (change.get("steps") or []))

    global_b = boundary.get("global_boundaries") or {}
    _add(checks, "boundary.pass", boundary.get("dryrun_and_review_pass") is True)
    _add(checks, "boundary.files_created", global_b.get("health_watchdog_files_created_now") is True)
    for flag in RUNTIME_FALSE_FLAGS:
        _add(checks, f"boundary.false.{flag}", global_b.get(flag) is False)
        for artifact_name, doc in docs.items():
            _add(checks, f"artifact_boundary.false.{artifact_name}.{flag}", doc.get(flag) is False)

    _add(checks, "matrix.pass", matrix.get("dryrun_and_review_pass") is True)
    rows = {row.get("module"): row for row in matrix.get("readiness") or []}
    for row in DOWNSTREAM_READINESS:
        _add(checks, f"matrix.module.{row['module']}", row["module"] in rows)
        _add(checks, f"matrix.readiness.{row['module']}", rows.get(row["module"], {}).get("readiness") == row["readiness"])
    _add(
        checks,
        "matrix.task_manager_primary",
        rows.get("task_manager_mount_planning", {}).get("readiness") == "primary_next_ready",
    )

    _add(checks, "non_claims.pass", non_claims.get("dryrun_and_review_pass") is True)
    for claim in DRYRUN_NON_CLAIMS:
        _add(checks, f"non_claim.{claim[:50]}", claim in (non_claims.get("non_claims") or []))
    _add(checks, "route.pass", route.get("dryrun_and_review_pass") is True)
    _add(checks, "route.primary", route.get("primary_next_phase") == NEXT_PHASE_GO)
    _add(checks, "route.secondary", route.get("secondary_next_phase") == "Phase-Midplatform-Module-Adapter-Feedback-Mount-Planning-v1-001")
    _add(checks, "route.output_deferred", "Output Gate Mount" in (route.get("deferred") or []))
    _add(checks, "route.wm_deferred", "WorldModel-Memory Bridge Mount" in (route.get("deferred") or []))
    _add(checks, "route.task_manager_no_recovery", route.get("task_manager_executes_health_watchdog_recovery") is False)

    for type_name in FROZEN_CANDIDATE_TYPES:
        for rule in HANDOFF_RULES:
            _add(checks, f"grid.type_rule.{type_name}.{rule[:35]}", bool(type_name and rule))
    for consumer in consumers:
        for flag in RUNTIME_FALSE_FLAGS:
            _add(checks, f"grid.consumer_boundary.{consumer}.{flag}", global_b.get(flag) is False)
    for chain in UPSTREAM_GO_CHAIN:
        for rel in SKELETON_FILES:
            _add(checks, f"grid.chain_file.{chain['phase']}.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    _add(checks, "min_checks", len(checks) >= MIN_CHECKS, str(len(checks)))
    failed = [c for c in checks if not c["passed"]]
    report = {
        "verifier": "GO" if not failed and len(checks) >= MIN_CHECKS else "HOLD",
        "checks_passed": len(checks) - len(failed),
        "checks_run": len(checks),
        "min_checks": MIN_CHECKS,
        "failed": failed[:120],
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["verifier"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
