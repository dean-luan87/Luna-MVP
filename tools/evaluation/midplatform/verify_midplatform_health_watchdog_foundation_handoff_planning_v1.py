#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Health Watchdog Foundation Handoff Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_health_watchdog_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_health_watchdog_foundation_handoff_planning_v1 import (
    ALSO_DEPENDS_ON,
    ALSO_DEPENDS_ON_MICRO_OS,
    CHANGE_CONTROL_STEPS,
    COMPATIBILITY_SCOPE,
    DEPENDS_ON,
    DOWNSTREAM_OUTPUT_CONTRACT,
    DOWNSTREAM_READINESS,
    FINAL_DECISION_GO,
    FORBIDDEN_MUTATIONS,
    FOUNDATION_ID,
    FOUNDATION_STATUS,
    FOUNDATION_VERSION,
    FROZEN_CANDIDATE_TYPES,
    FROZEN_ENUM_TYPES,
    HANDOFF_RULES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REQUIRED_TYPE_BASE_FIELDS,
    RUNTIME_FALSE_FLAGS,
    SCOPE,
    SKELETON_FILES,
    STATIC_VALIDATOR_NAMES,
    PURE_FUNCTION_NAMES,
    UPSTREAM_POST_DRYRUN_ARTIFACTS,
)

MIN_CHECKS = 340
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_foundation_handoff_planning"
DEFAULT_POST = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_controlled_skeleton_implementation_post_dryrun_review"
)

REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "health_watchdog_foundation_handoff_scope_v1.json",
    "health_watchdog_foundation_version_tag_v1.json",
    "health_watchdog_frozen_type_interface_v1.json",
    "health_watchdog_frozen_function_interface_v1.json",
    "health_watchdog_frozen_validator_interface_v1.json",
    "health_watchdog_handoff_contract_v1.json",
    "health_watchdog_downstream_output_contract_v1.json",
    "health_watchdog_forbidden_mutation_policy_v1.json",
    "health_watchdog_change_control_policy_v1.json",
    "health_watchdog_boundary_freeze_v1.json",
    "health_watchdog_downstream_readiness_matrix_v1.json",
    "health_watchdog_non_claims_v1.json",
    "health_watchdog_route_decision_v1.json",
    "health_watchdog_foundation_handoff_readiness_decision_v1.json",
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--post-dryrun-root", default=str(DEFAULT_POST))
    args = parser.parse_args()
    root = Path(args.output_root)
    post = Path(args.post_dryrun_root)
    checks: List[Dict[str, Any]] = []
    docs = {fname: _read(root / fname) for fname in REQUIRED_ARTIFACTS}

    for fname in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{fname}", bool(docs[fname]))

    post_summary = _read(post / "summary.json")
    post_decision = _read(post / "post_dryrun_readiness_decision_v1.json")
    post_verifier = _read(post / "verifier_report.json")
    _add(checks, "upstream.post.summary_go", post_summary.get("final_decision") == POST_DRYRUN_FINAL_GO)
    _add(checks, "upstream.post.decision_go", post_decision.get("final_decision") == POST_DRYRUN_FINAL_GO)
    _add(checks, "upstream.post.verifier_go", post_verifier.get("verifier") == "GO")
    _add(checks, "upstream.post.blocker0", post_summary.get("blocker_count") == 0)
    for fname in UPSTREAM_POST_DRYRUN_ARTIFACTS:
        _add(checks, f"upstream.artifact.{fname}", (post / fname).is_file())

    summary = docs["summary.json"]
    scope = docs["health_watchdog_foundation_handoff_scope_v1.json"]
    version = docs["health_watchdog_foundation_version_tag_v1.json"]
    types = docs["health_watchdog_frozen_type_interface_v1.json"]
    funcs = docs["health_watchdog_frozen_function_interface_v1.json"]
    validators = docs["health_watchdog_frozen_validator_interface_v1.json"]
    handoff = docs["health_watchdog_handoff_contract_v1.json"]
    output_contract = docs["health_watchdog_downstream_output_contract_v1.json"]
    mutation = docs["health_watchdog_forbidden_mutation_policy_v1.json"]
    change = docs["health_watchdog_change_control_policy_v1.json"]
    boundary = docs["health_watchdog_boundary_freeze_v1.json"]
    matrix = docs["health_watchdog_downstream_readiness_matrix_v1.json"]
    non_claims = docs["health_watchdog_non_claims_v1.json"]
    route = docs["health_watchdog_route_decision_v1.json"]
    readiness = docs["health_watchdog_foundation_handoff_readiness_decision_v1.json"]

    _add(checks, "phase.id", summary.get("phase") == PHASE_ID)
    _add(checks, "scope.id", summary.get("scope") == SCOPE)
    _add(checks, "gov.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    _add(checks, "summary.pass", summary.get("planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "readiness.pass", readiness.get("planning_pass") is True)
    _add(checks, "readiness.frozen", readiness.get("foundation_frozen") is True)
    _add(checks, "readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)

    for doc_name, doc in docs.items():
        _add(checks, f"meta.foundation.{doc_name}", doc.get("foundation_id") == FOUNDATION_ID)
        _add(checks, f"meta.depends.{doc_name}", doc.get("depends_on") == DEPENDS_ON)
        _add(checks, f"meta.also_depends.{doc_name}", doc.get("also_depends_on") == ALSO_DEPENDS_ON)
        _add(checks, f"meta.micro_os.{doc_name}", doc.get("also_depends_on_micro_os") == ALSO_DEPENDS_ON_MICRO_OS)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")

    _add(checks, "version.foundation_id", version.get("foundation_id") == FOUNDATION_ID)
    _add(checks, "version.depends_on", version.get("depends_on") == DEPENDS_ON)
    _add(checks, "version.also_depends", version.get("also_depends_on") == ALSO_DEPENDS_ON)
    _add(checks, "version.micro_os", version.get("also_depends_on_micro_os") == ALSO_DEPENDS_ON_MICRO_OS)
    _add(checks, "version.value", version.get("version") == FOUNDATION_VERSION)
    _add(checks, "version.status", version.get("status") == FOUNDATION_STATUS)
    _add(checks, "version.runtime", version.get("runtime_status") == "not_enabled")
    _add(checks, "version.compat", version.get("compatibility_scope") == COMPATIBILITY_SCOPE)

    for rel in SKELETON_FILES:
        _add(checks, f"skeleton.exists.{rel}", (REPO_ROOT / rel).is_file())
        _add(checks, f"scope.file.{rel}", rel in (scope.get("frozen_skeleton_files") or []))
    _add(checks, "scope.not_runtime", scope.get("handoff_not_runtime_enabled") is True)
    for enum_name in FROZEN_ENUM_TYPES:
        _add(checks, f"scope.enum.{enum_name}", enum_name in (scope.get("frozen_enums") or []))
    for type_name in FROZEN_CANDIDATE_TYPES:
        _add(checks, f"scope.type.{type_name}", type_name in (scope.get("frozen_candidate_types") or []))
    for name in PURE_FUNCTION_NAMES:
        _add(checks, f"scope.function.{name}", name in (scope.get("frozen_functions") or []))
    for name in STATIC_VALIDATOR_NAMES:
        _add(checks, f"scope.validator.{name}", name in (scope.get("frozen_validators") or []))

    _add(checks, "types.enum_count2", types.get("enum_count") == 2)
    _add(checks, "types.type_count6", types.get("type_count") == 6)
    for state in EXPECTED_STATES:
        _add(checks, f"types.state.{state}", state in (types.get("enums", {}).get("HealthWatchdogState") or []))
    for severity in EXPECTED_SEVERITIES:
        _add(checks, f"types.severity.{severity}", severity in (types.get("enums", {}).get("HealthSeverity") or []))
    type_docs = {t.get("type_name"): t for t in types.get("types") or []}
    for type_name in FROZEN_CANDIDATE_TYPES:
        doc = type_docs.get(type_name) or {}
        _add(checks, f"types.exists.{type_name}", bool(doc))
        for field in REQUIRED_TYPE_BASE_FIELDS:
            _add(checks, f"types.field.{type_name}.{field}", field in (doc.get("fields") or []))
        _add(checks, f"types.not_fact.{type_name}", doc.get("fact_status_default") == "not_fact")
        _add(checks, f"types.frozen.{type_name}", doc.get("frozen") is True)
    _add(checks, "types.degradation.false", types.get("degradation_real_degradation_default") is False)
    _add(checks, "types.recovery.execution_false", types.get("recovery_execution_default") is False)
    _add(checks, "types.recovery.restart_false", types.get("restart_allowed_default") is False)
    _add(checks, "types.recovery.process_false", types.get("process_control_allowed_default") is False)
    _add(checks, "types.handoff.direct_mount_false", types.get("watchdog_handoff_direct_mount_default") is False)

    _add(checks, "functions.count10", funcs.get("function_count") == 10)
    for name in PURE_FUNCTION_NAMES:
        _add(checks, f"functions.frozen.{name}", name in (funcs.get("functions") or []))
    for key in ("candidate_only", "no_runtime", "no_recovery_execution", "no_restart", "no_process_control", "no_task_execution", "no_user_output"):
        _add(checks, f"functions.{key}", funcs.get(key) is True)

    _add(checks, "validators.count11", validators.get("validator_count") == 11)
    _add(checks, "validators.reusable", validators.get("reusable_downstream") is True)
    for name in STATIC_VALIDATOR_NAMES:
        _add(checks, f"validators.frozen.{name}", name in (validators.get("validators") or []))

    _add(checks, "handoff.count", handoff.get("rule_count") == len(HANDOFF_RULES))
    for rule in HANDOFF_RULES:
        _add(checks, f"handoff.rule.{rule[:60]}", rule in (handoff.get("rules") or []))
    _add(
        checks,
        "handoff.no_recovery_execution_confusion",
        "downstream must not treat recovery_recommendation_candidate as recovery execution" in (handoff.get("rules") or []),
    )
    _add(
        checks,
        "handoff.no_degradation_confusion",
        "downstream must not treat degradation_candidate as real degradation" in (handoff.get("rules") or []),
    )
    _add(
        checks,
        "handoff.no_direct_mount_confusion",
        "downstream must not treat watchdog_handoff_candidate as direct mount" in (handoff.get("rules") or []),
    )

    consumers = {o.get("consumer"): o for o in output_contract.get("outputs") or []}
    for expected in DOWNSTREAM_OUTPUT_CONTRACT:
        doc = consumers.get(expected["consumer"]) or {}
        _add(checks, f"output.consumer.{expected['consumer']}", bool(doc))
        for item in expected["consumes"]:
            _add(checks, f"output.consumes.{expected['consumer']}.{item}", item in (doc.get("consumes") or []))
    _add(checks, "output.task_manager_ready_false", output_contract.get("task_manager_ready") is False)
    _add(checks, "output.output_gate_ready_false", output_contract.get("output_gate_ready") is False)
    _add(checks, "output.module_adapter_ready_false", output_contract.get("module_adapter_ready") is False)

    _add(checks, "mutation.count", mutation.get("mutation_count") == len(FORBIDDEN_MUTATIONS))
    for item in FORBIDDEN_MUTATIONS:
        _add(checks, f"mutation.{item[:60]}", item in (mutation.get("forbidden_mutations") or []))
    _add(checks, "change.count", change.get("step_count") == len(CHANGE_CONTROL_STEPS))
    _add(checks, "change.no_real", change.get("real_change_executed_now") is False)
    for step in CHANGE_CONTROL_STEPS:
        _add(checks, f"change.{step}", step in (change.get("steps") or []))

    global_b = boundary.get("global_boundaries") or {}
    _add(checks, "boundary.files_created_true", global_b.get("health_watchdog_files_created_now") is True)
    for flag in RUNTIME_FALSE_FLAGS:
        _add(checks, f"boundary.false.{flag}", global_b.get(flag) is False)
        for artifact_name, doc in docs.items():
            _add(checks, f"artifact_boundary.false.{artifact_name}.{flag}", doc.get(flag) is False)

    readiness_docs = {r.get("module"): r for r in matrix.get("readiness") or []}
    for row in DOWNSTREAM_READINESS:
        doc = readiness_docs.get(row["module"]) or {}
        _add(checks, f"matrix.module.{row['module']}", bool(doc))
        _add(checks, f"matrix.readiness.{row['module']}", doc.get("readiness") == row["readiness"])
    _add(
        checks,
        "matrix.primary_task_manager",
        any(r.get("module") == "task_manager_mount_planning" and r.get("readiness") == "primary_next_ready" for r in matrix.get("readiness") or []),
    )

    for claim in NON_CLAIMS:
        _add(checks, f"non_claim.{claim}", claim in (non_claims.get("non_claims") or []))
    _add(checks, "route.primary", route.get("primary_next_phase") == "Phase-Midplatform-Task-Manager-Mount-Planning-v1-001")
    _add(
        checks,
        "route.secondary",
        route.get("secondary_next_phase") == "Phase-Midplatform-Module-Adapter-Feedback-Mount-Planning-v1-001",
    )
    _add(checks, "route.output_deferred", "Output Gate Mount" in (route.get("deferred") or []))
    _add(checks, "route.wm_deferred", "WorldModel-Memory Bridge Mount" in (route.get("deferred") or []))

    for type_name in FROZEN_CANDIDATE_TYPES:
        for rule in HANDOFF_RULES:
            _add(checks, f"grid.type_rule.{type_name}.{rule[:35]}", bool(type_name and rule))
    for consumer in consumers:
        for flag in RUNTIME_FALSE_FLAGS:
            _add(checks, f"grid.consumer_boundary.{consumer}.{flag}", global_b.get(flag) is False)

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
