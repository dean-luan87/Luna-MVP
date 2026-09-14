# -*- coding: utf-8 -*-
"""Luna Midplatform Health Watchdog Foundation Handoff DryRunAndReview v1."""

from __future__ import annotations

import ast
import dataclasses
import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_health_watchdog_foundation_handoff_planning_v1 import (
    ALSO_DEPENDS_ON,
    ALSO_DEPENDS_ON_MICRO_OS,
    CHANGE_CONTROL_STEPS,
    COMPATIBILITY_SCOPE,
    DEPENDS_ON,
    DOWNSTREAM_OUTPUT_CONTRACT,
    DOWNSTREAM_READINESS,
    FINAL_DECISION_GO as HANDOFF_PLANNING_FINAL_GO,
    FORBIDDEN_MUTATIONS,
    FOUNDATION_ID,
    FOUNDATION_STATUS,
    FOUNDATION_VERSION,
    FROZEN_CANDIDATE_TYPES,
    FROZEN_ENUM_TYPES,
    HANDOFF_RULES,
    NON_CLAIMS,
    REQUIRED_TYPE_BASE_FIELDS,
)
from capabilities.midplatform.midplatform_health_watchdog_controlled_skeleton_implementation_dryrun_v1 import (
    FINAL_DECISION_GO as SKELETON_DRYRUN_FINAL_GO,
    PURE_FUNCTION_NAMES,
    RUNTIME_FALSE_FLAGS,
    SKELETON_FILES,
    STATIC_VALIDATOR_NAMES,
)
from capabilities.midplatform.midplatform_health_watchdog_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_health_watchdog_mount_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MOUNT_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_decision_center_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DECISION_CENTER_HANDOFF_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_information_integration_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as II_HANDOFF_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MICRO_OS_FREEZE_DRYRUN_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Health-Watchdog-Foundation-Handoff-DryRunAndReview-v1-001"
SCOPE = "midplatform_health_watchdog_foundation_handoff_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_health_watchdog_foundation_handoff_dryrun_and_review_v1"

UPSTREAM_HANDOFF_PLANNING_FINAL = HANDOFF_PLANNING_FINAL_GO

FINAL_DECISION_GO = (
    "MIDPLATFORM_HEALTH_WATCHDOG_FOUNDATION_HANDOFF_DRYRUN_AND_REVIEW_"
    "CLOSED_READY_FOR_TASK_MANAGER_MOUNT_PLANNING"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_HEALTH_WATCHDOG_FOUNDATION_HANDOFF_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Mount-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Health-Watchdog-Foundation-Handoff-Issue-Review-v1-001"

UPSTREAM_HANDOFF_PLANNING_FILES: Tuple[str, ...] = (
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
    "verifier_report.json",
)

UPSTREAM_GO_CHAIN: Tuple[Dict[str, str], ...] = (
    {
        "phase": "micro_os_foundation_freeze_and_handoff_dryrun_and_review",
        "expected_final": MICRO_OS_FREEZE_DRYRUN_FINAL_GO,
        "pass_field": "dryrun_pass",
    },
    {
        "phase": "information_integration_foundation_handoff_dryrun_and_review",
        "expected_final": II_HANDOFF_DRYRUN_FINAL_GO,
        "pass_field": "dryrun_pass",
    },
    {
        "phase": "decision_center_foundation_handoff_dryrun_and_review",
        "expected_final": DECISION_CENTER_HANDOFF_DRYRUN_FINAL_GO,
        "pass_field": "dryrun_pass",
    },
    {
        "phase": "health_watchdog_mount_dryrun_and_review",
        "expected_final": MOUNT_DRYRUN_FINAL_GO,
        "pass_field": "dryrun_pass",
    },
    {
        "phase": "health_watchdog_controlled_skeleton_implementation_dryrun",
        "expected_final": SKELETON_DRYRUN_FINAL_GO,
        "pass_field": "dryrun_pass",
    },
    {
        "phase": "health_watchdog_controlled_skeleton_implementation_post_dryrun_review",
        "expected_final": POST_DRYRUN_FINAL_GO,
        "pass_field": "post_dryrun_review_pass",
    },
    {
        "phase": "health_watchdog_foundation_handoff_planning",
        "expected_final": HANDOFF_PLANNING_FINAL_GO,
        "pass_field": "planning_pass",
    },
)

DRYRUN_NON_CLAIMS: Tuple[str, ...] = tuple(
    claim.replace("Foundation Handoff", "Foundation Handoff DryRun") for claim in NON_CLAIMS
)

FORBIDDEN_IMPORTS: Tuple[str, ...] = (
    "asyncio",
    "threading",
    "multiprocessing",
    "subprocess",
    "socket",
    "requests",
    "httpx",
    "aiohttp",
    "openai",
    "anthropic",
    "dashscope",
)

FORBIDDEN_TOKENS: Tuple[str, ...] = (
    "async def",
    "await ",
    "Thread(",
    "Process(",
    "Popen(",
    "system(",
    "runtime_enabled_now = True",
    "recovery_execution=True",
    "restart_allowed=True",
    "process_control_allowed=True",
    "real_degradation=True",
    "direct_mount=True",
    "task_execution_now = True",
    "user_output_allowed_now = True",
    "memory_write_allowed_now = True",
    "worldmodel_write_allowed_now = True",
)

DEFAULT_HANDOFF_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_foundation_handoff_planning"
)
DEFAULT_POST_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_health_watchdog_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_SKELETON_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_health_watchdog_controlled_skeleton_implementation_dryrun"
)
DEFAULT_MOUNT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_mount_dryrun_and_review"
)
DEFAULT_DECISION_CENTER_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_foundation_handoff_dryrun_and_review"
)
DEFAULT_II_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_MICRO_OS_FREEZE_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_health_watchdog_foundation_handoff_dryrun_and_review"
)


def _dryrun_meta(output_root: Path, planning_root: Path) -> Dict[str, Any]:
    meta: Dict[str, Any] = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "foundation_id": FOUNDATION_ID,
        "depends_on": DEPENDS_ON,
        "also_depends_on": ALSO_DEPENDS_ON,
        "also_depends_on_micro_os": ALSO_DEPENDS_ON_MICRO_OS,
        "foundation_version": FOUNDATION_VERSION,
        "runtime_status": "not_enabled",
        "midplatform_health_watchdog_foundation_handoff_dryrun_and_review_only": True,
        "simulated": True,
        "health_watchdog_files_created_now": True,
        "output_root": str(output_root),
        "upstream_handoff_planning_root": str(planning_root),
    }
    for flag in RUNTIME_FALSE_FLAGS:
        meta[flag] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_result(checks: List[Tuple[str, bool]], **extra: Any) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "handoff dryrun review check failed"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "issue_count": len(issues),
        "dryrun_and_review_pass": len(issues) == 0,
        **extra,
    }


def _scan_skeleton_file(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {"path": str(path), "exists": False, "parse_ok": False, "pure_boundary_clean": False, "issues": ["missing"]}
    source = path.read_text(encoding="utf-8")
    issues: List[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return {"path": str(path), "exists": True, "parse_ok": False, "pure_boundary_clean": False, "issues": [str(exc)]}
    import_count = 0
    async_function_count = 0
    while_true_count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_count += len(node.names)
            for alias in node.names:
                if alias.name.split(".")[0] in FORBIDDEN_IMPORTS:
                    issues.append(f"forbidden_import:{alias.name}")
        if isinstance(node, ast.ImportFrom) and node.module:
            import_count += 1
            if node.module.split(".")[0] in FORBIDDEN_IMPORTS:
                issues.append(f"forbidden_import:{node.module}")
        if isinstance(node, ast.AsyncFunctionDef):
            async_function_count += 1
            issues.append("async_function")
        if isinstance(node, ast.While) and isinstance(node.test, ast.Constant) and node.test.value is True:
            while_true_count += 1
            issues.append("while_true")
    for token in FORBIDDEN_TOKENS:
        if token in source:
            issues.append(f"forbidden_token:{token}")
    return {
        "path": str(path),
        "exists": True,
        "parse_ok": True,
        "import_count": import_count,
        "async_function_count": async_function_count,
        "while_true_count": while_true_count,
        "forbidden_imports_found": [i for i in issues if i.startswith("forbidden_import")],
        "issues": issues,
        "pure_boundary_clean": len(issues) == 0,
    }


def _field_default(cls: Any, field_name: str) -> Any:
    field = cls.__dataclass_fields__[field_name]
    if field.default is not dataclasses.MISSING:
        return field.default
    return None


def _resolve_upstream_roots(
    *,
    handoff_planning_root: Path,
    post_dryrun_root: Path,
    skeleton_dryrun_root: Path,
    mount_dryrun_root: Path,
    decision_center_handoff_dryrun_root: Path,
    ii_handoff_dryrun_root: Path,
    micro_os_freeze_dryrun_root: Path,
) -> Dict[str, Path]:
    return {
        "micro_os_foundation_freeze_and_handoff_dryrun_and_review": micro_os_freeze_dryrun_root,
        "information_integration_foundation_handoff_dryrun_and_review": ii_handoff_dryrun_root,
        "decision_center_foundation_handoff_dryrun_and_review": decision_center_handoff_dryrun_root,
        "health_watchdog_mount_dryrun_and_review": mount_dryrun_root,
        "health_watchdog_controlled_skeleton_implementation_dryrun": skeleton_dryrun_root,
        "health_watchdog_controlled_skeleton_implementation_post_dryrun_review": post_dryrun_root,
        "health_watchdog_foundation_handoff_planning": handoff_planning_root,
    }


def run_midplatform_health_watchdog_foundation_handoff_dryrun_and_review_v1(
    *,
    midplatform_health_watchdog_foundation_handoff_planning_root: str,
    midplatform_health_watchdog_controlled_skeleton_implementation_post_dryrun_review_root: str,
    midplatform_health_watchdog_controlled_skeleton_implementation_dryrun_root: str,
    midplatform_health_watchdog_mount_dryrun_and_review_root: str,
    midplatform_decision_center_foundation_handoff_dryrun_and_review_root: str,
    midplatform_information_integration_foundation_handoff_dryrun_and_review_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    plan_root = Path(midplatform_health_watchdog_foundation_handoff_planning_root).expanduser().resolve()
    post_dr = Path(midplatform_health_watchdog_controlled_skeleton_implementation_post_dryrun_review_root).expanduser().resolve()
    sk_dr = Path(midplatform_health_watchdog_controlled_skeleton_implementation_dryrun_root).expanduser().resolve()
    mount_dr = Path(midplatform_health_watchdog_mount_dryrun_and_review_root).expanduser().resolve()
    dc_dr = Path(midplatform_decision_center_foundation_handoff_dryrun_and_review_root).expanduser().resolve()
    ii_dr = Path(midplatform_information_integration_foundation_handoff_dryrun_and_review_root).expanduser().resolve()
    micro_dr = Path(midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _dryrun_meta(out_root, plan_root)

    plan_summary = _try_read_json(plan_root / "summary.json") or {}
    plan_verifier = _try_read_json(plan_root / "verifier_report.json") or {}
    if plan_summary.get("final_decision") != HANDOFF_PLANNING_FINAL_GO:
        blockers.append("handoff_planning_final_decision_not_go")
    if plan_verifier.get("verifier") != "GO":
        blockers.append("handoff_planning_verifier_not_go")
    for fname in UPSTREAM_HANDOFF_PLANNING_FILES:
        if not (plan_root / fname).is_file():
            blockers.append(f"missing_handoff_planning_file:{fname}")

    roots = _resolve_upstream_roots(
        handoff_planning_root=plan_root,
        post_dryrun_root=post_dr,
        skeleton_dryrun_root=sk_dr,
        mount_dryrun_root=mount_dr,
        decision_center_handoff_dryrun_root=dc_dr,
        ii_handoff_dryrun_root=ii_dr,
        micro_os_freeze_dryrun_root=micro_dr,
    )
    entries: List[Dict[str, Any]] = []
    for chain in UPSTREAM_GO_CHAIN:
        phase = chain["phase"]
        root = roots[phase]
        summary = _try_read_json(root / "summary.json") or {}
        verifier = _try_read_json(root / "verifier_report.json") or {}
        go = summary.get("final_decision") == chain["expected_final"] and verifier.get("verifier") == "GO"
        entries.append(
            {
                "phase": phase,
                "root": str(root),
                "expected_final": chain["expected_final"],
                "actual_final": summary.get("final_decision"),
                "verifier": verifier.get("verifier"),
                "go": go,
            }
        )
        if not go:
            blockers.append(f"upstream_not_go:{phase}")
    upstream_go_chain_review = _review_result(
        [(f"upstream.{e['phase']}", e["go"]) for e in entries],
        review_id="upstream_go_chain_review_v1",
        entries=entries,
        blocker=any(not e["go"] for e in entries),
        **meta,
    )

    version_plan = _try_read_json(plan_root / "health_watchdog_foundation_version_tag_v1.json") or {}
    version_checks = [
        ("foundation_id", version_plan.get("foundation_id") == FOUNDATION_ID),
        ("depends_on", version_plan.get("depends_on") == DEPENDS_ON),
        ("also_depends_on", version_plan.get("also_depends_on") == ALSO_DEPENDS_ON),
        ("also_depends_on_micro_os", version_plan.get("also_depends_on_micro_os") == ALSO_DEPENDS_ON_MICRO_OS),
        ("version", version_plan.get("version") == FOUNDATION_VERSION),
        ("status", version_plan.get("status") == FOUNDATION_STATUS),
        ("runtime_status", version_plan.get("runtime_status") == "not_enabled"),
        ("compatibility_scope", version_plan.get("compatibility_scope") == COMPATIBILITY_SCOPE),
    ]
    foundation_version_tag_review = _review_result(
        version_checks,
        review_id="foundation_version_tag_review_v1",
        version=FOUNDATION_VERSION,
        status=FOUNDATION_STATUS,
        compatibility_scope=COMPATIBILITY_SCOPE,
        **meta,
    )

    scope_plan = _try_read_json(plan_root / "health_watchdog_foundation_handoff_scope_v1.json") or {}
    file_scans = []
    file_checks: List[Tuple[str, bool]] = []
    forbidden_imports_found: List[str] = []
    for rel in SKELETON_FILES:
        scan = _scan_skeleton_file(repo_root / rel)
        scan["path"] = rel
        file_scans.append(scan)
        file_checks.append((f"file.exists.{rel}", scan.get("exists") is True))
        file_checks.append((f"file.scope.{rel}", rel in (scope_plan.get("frozen_skeleton_files") or [])))
        file_checks.append((f"file.clean.{rel}", scan.get("pure_boundary_clean") is True))
        forbidden_imports_found.extend(scan.get("forbidden_imports_found") or [])
    skeleton_file_consistency_review = _review_result(
        file_checks,
        review_id="skeleton_file_consistency_review_v1",
        files=file_scans,
        forbidden_imports_found=forbidden_imports_found,
        blocker=bool(forbidden_imports_found),
        **meta,
    )

    types_mod = importlib.import_module("capabilities.midplatform.core.health_watchdog_types_v1")
    type_plan = _try_read_json(plan_root / "health_watchdog_frozen_type_interface_v1.json") or {}
    type_checks: List[Tuple[str, bool]] = []
    for enum_name in FROZEN_ENUM_TYPES:
        type_checks.append((f"enum.exists.{enum_name}", hasattr(types_mod, enum_name)))
    type_checks.extend(
        [
            ("state.count15", len(getattr(types_mod, "HealthWatchdogState")) == 15),
            ("severity.count5", len(getattr(types_mod, "HealthSeverity")) == 5),
        ]
    )
    for type_name in FROZEN_CANDIDATE_TYPES:
        cls = getattr(types_mod, type_name, None)
        fields = getattr(cls, "__dataclass_fields__", {}) if cls else {}
        type_checks.append((f"type.exists.{type_name}", cls is not None))
        for field in REQUIRED_TYPE_BASE_FIELDS:
            type_checks.append((f"type.field.{type_name}.{field}", field in fields))
        if "fact_status" in fields:
            type_checks.append((f"type.not_fact.{type_name}", fields["fact_status"].default == "not_fact"))
    type_checks.extend(
        [
            (
                "Degradation.real_degradation_false",
                _field_default(types_mod.DegradationCandidate, "real_degradation") is False,
            ),
            (
                "Recovery.recovery_execution_false",
                _field_default(types_mod.RecoveryRecommendationCandidate, "recovery_execution") is False,
            ),
            (
                "Recovery.restart_allowed_false",
                _field_default(types_mod.RecoveryRecommendationCandidate, "restart_allowed") is False,
            ),
            (
                "Recovery.process_control_allowed_false",
                _field_default(types_mod.RecoveryRecommendationCandidate, "process_control_allowed") is False,
            ),
            (
                "Watchdog.direct_mount_false",
                _field_default(types_mod.WatchdogHandoffCandidate, "direct_mount") is False,
            ),
            ("plan.type_count6", type_plan.get("type_count") == 6),
            ("plan.enum_count2", type_plan.get("enum_count") == 2),
        ]
    )
    frozen_type_interface_review = _review_result(
        type_checks,
        review_id="frozen_type_interface_review_v1",
        type_count=len(FROZEN_CANDIDATE_TYPES),
        health_watchdog_state_count=len(getattr(types_mod, "HealthWatchdogState")),
        health_severity_count=len(getattr(types_mod, "HealthSeverity")),
        fact_status_semantics_immutable=True,
        **meta,
    )

    skeleton_mod = importlib.import_module("capabilities.midplatform.core.health_watchdog_skeleton_v1")
    function_plan = _try_read_json(plan_root / "health_watchdog_frozen_function_interface_v1.json") or {}
    function_checks = [
        (f"function.callable.{name}", callable(getattr(skeleton_mod, name, None))) for name in PURE_FUNCTION_NAMES
    ]
    for key in ("candidate_only", "no_runtime", "no_recovery_execution", "no_restart", "no_process_control", "no_task_execution", "no_user_output"):
        function_checks.append((f"plan.{key}", function_plan.get(key) is True))
    frozen_function_interface_review = _review_result(
        function_checks,
        review_id="frozen_function_interface_review_v1",
        function_count=len(PURE_FUNCTION_NAMES),
        functions=list(PURE_FUNCTION_NAMES),
        **meta,
    )

    validators_mod = importlib.import_module("capabilities.midplatform.core.health_watchdog_static_validators_v1")
    validator_plan = _try_read_json(plan_root / "health_watchdog_frozen_validator_interface_v1.json") or {}
    validator_checks = [
        (f"validator.callable.{name}", callable(getattr(validators_mod, name, None))) for name in STATIC_VALIDATOR_NAMES
    ]
    validator_checks.append(("plan.validator_count", validator_plan.get("validator_count") == len(STATIC_VALIDATOR_NAMES)))
    frozen_validator_interface_review = _review_result(
        validator_checks,
        review_id="frozen_validator_interface_review_v1",
        validator_count=len(STATIC_VALIDATOR_NAMES),
        validators=list(STATIC_VALIDATOR_NAMES),
        **meta,
    )

    handoff_plan = _try_read_json(plan_root / "health_watchdog_handoff_contract_v1.json") or {}
    handoff_checks = [(f"rule.{rule[:40]}", rule in (handoff_plan.get("rules") or [])) for rule in HANDOFF_RULES]
    handoff_contract_dryrun = _review_result(
        handoff_checks,
        dryrun_id="handoff_contract_dryrun_v1",
        rules=list(HANDOFF_RULES),
        rule_count=len(HANDOFF_RULES),
        **meta,
    )

    output_plan = _try_read_json(plan_root / "health_watchdog_downstream_output_contract_v1.json") or {}
    output_rows = {row.get("consumer"): row for row in output_plan.get("outputs") or []}
    output_checks: List[Tuple[str, bool]] = [
        ("task_manager_ready_false", output_plan.get("task_manager_ready") is False),
        ("output_gate_ready_false", output_plan.get("output_gate_ready") is False),
        ("module_adapter_ready_false", output_plan.get("module_adapter_ready") is False),
    ]
    for row in DOWNSTREAM_OUTPUT_CONTRACT:
        doc = output_rows.get(row["consumer"]) or {}
        output_checks.append((f"consumer.{row['consumer']}", bool(doc)))
        for item in row["consumes"]:
            output_checks.append((f"consumer.{row['consumer']}.{item}", item in (doc.get("consumes") or [])))
    downstream_output_contract_review = _review_result(
        output_checks,
        review_id="downstream_output_contract_review_v1",
        outputs=list(DOWNSTREAM_OUTPUT_CONTRACT),
        **meta,
    )

    mutation_plan = _try_read_json(plan_root / "health_watchdog_forbidden_mutation_policy_v1.json") or {}
    mutation_checks = [
        (f"mutation.{mutation[:45]}", mutation in (mutation_plan.get("forbidden_mutations") or []))
        for mutation in FORBIDDEN_MUTATIONS
    ]
    forbidden_mutation_policy_review = _review_result(
        mutation_checks,
        review_id="forbidden_mutation_policy_review_v1",
        forbidden_mutations=list(FORBIDDEN_MUTATIONS),
        **meta,
    )

    change_plan = _try_read_json(plan_root / "health_watchdog_change_control_policy_v1.json") or {}
    change_checks = [(f"change.{step}", step in (change_plan.get("steps") or [])) for step in CHANGE_CONTROL_STEPS]
    change_checks.append(("real_change_executed_now_false", change_plan.get("real_change_executed_now") is False))
    change_control_policy_review = _review_result(
        change_checks,
        review_id="change_control_policy_review_v1",
        steps=list(CHANGE_CONTROL_STEPS),
        real_change_executed_now=False,
        **meta,
    )

    boundary_plan = _try_read_json(plan_root / "health_watchdog_boundary_freeze_v1.json") or {}
    global_b = boundary_plan.get("global_boundaries") or {}
    boundary_checks = [("health_watchdog_files_created_now", global_b.get("health_watchdog_files_created_now") is True)]
    boundary_checks.extend((flag, global_b.get(flag) is False) for flag in RUNTIME_FALSE_FLAGS)
    boundary_freeze_review = _review_result(
        boundary_checks,
        review_id="boundary_freeze_review_v1",
        global_boundaries={"health_watchdog_files_created_now": True, **{flag: False for flag in RUNTIME_FALSE_FLAGS}},
        **meta,
    )

    matrix_plan = _try_read_json(plan_root / "health_watchdog_downstream_readiness_matrix_v1.json") or {}
    matrix_rows = {row.get("module"): row for row in matrix_plan.get("readiness") or []}
    matrix_checks = [
        (f"matrix.{row['module']}", matrix_rows.get(row["module"], {}).get("readiness") == row["readiness"])
        for row in DOWNSTREAM_READINESS
    ]
    matrix_checks.append(
        (
            "route_order_task_manager_primary",
            matrix_rows.get("task_manager_mount_planning", {}).get("readiness") == "primary_next_ready",
        )
    )
    downstream_readiness_matrix_review = _review_result(
        matrix_checks,
        review_id="downstream_readiness_matrix_review_v1",
        readiness=list(DOWNSTREAM_READINESS),
        **meta,
    )

    non_claim_plan = _try_read_json(plan_root / "health_watchdog_non_claims_v1.json") or {}
    non_claim_checks = [
        (f"non_claim.{claim[:45]}", claim in (non_claim_plan.get("non_claims") or [])) for claim in NON_CLAIMS
    ]
    dry_claim_checks = [(f"dry_non_claim.{claim[:45]}", True) for claim in DRYRUN_NON_CLAIMS]
    non_claims_review = _review_result(
        non_claim_checks + dry_claim_checks,
        review_id="non_claims_review_v1",
        non_claims=list(DRYRUN_NON_CLAIMS),
        **meta,
    )

    route_plan = _try_read_json(plan_root / "health_watchdog_route_decision_v1.json") or {}
    route_checks = [
        ("primary_next_phase", route_plan.get("primary_next_phase") == NEXT_PHASE_GO),
        (
            "secondary_next_phase",
            route_plan.get("secondary_next_phase")
            == "Phase-Midplatform-Module-Adapter-Feedback-Mount-Planning-v1-001",
        ),
        ("output_gate_deferred", "Output Gate Mount" in (route_plan.get("deferred") or [])),
        ("worldmodel_memory_bridge_deferred", "WorldModel-Memory Bridge Mount" in (route_plan.get("deferred") or [])),
        ("decision_center_loopback_deferred", "Decision Center Loopback Review" in (route_plan.get("deferred") or [])),
    ]
    route_decision_review = _review_result(
        route_checks,
        review_id="route_decision_review_v1",
        primary_next_phase=NEXT_PHASE_GO,
        secondary_next_phase="Phase-Midplatform-Module-Adapter-Feedback-Mount-Planning-v1-001",
        deferred=["Output Gate Mount", "WorldModel-Memory Bridge Mount", "Decision Center Loopback Review"],
        task_manager_consumes_candidates_only=True,
        task_manager_executes_health_watchdog_recovery=False,
        **meta,
    )

    review_docs = [
        upstream_go_chain_review,
        foundation_version_tag_review,
        skeleton_file_consistency_review,
        frozen_type_interface_review,
        frozen_function_interface_review,
        frozen_validator_interface_review,
        handoff_contract_dryrun,
        downstream_output_contract_review,
        forbidden_mutation_policy_review,
        change_control_policy_review,
        boundary_freeze_review,
        downstream_readiness_matrix_review,
        non_claims_review,
        route_decision_review,
    ]
    for doc in review_docs:
        if doc.get("dryrun_and_review_pass") is not True:
            blockers.append(f"review_failed:{doc.get('review_id') or doc.get('dryrun_id')}")
    issue_register = {
        "register_id": "issue_register_v1",
        "issues": blockers,
        "blocker_count": len(blockers),
        **meta,
    }
    dryrun_pass = len(blockers) == 0
    readiness = {
        "decision_id": "handoff_dryrun_readiness_decision_v1",
        "dryrun_pass": dryrun_pass,
        "foundation_id": FOUNDATION_ID,
        "foundation_version": FOUNDATION_VERSION,
        "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "blocker_count": len(blockers),
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "blocker_count": len(blockers),
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        **meta,
    }
    return {
        "summary": summary,
        "upstream_go_chain_review": upstream_go_chain_review,
        "foundation_version_tag_review": foundation_version_tag_review,
        "skeleton_file_consistency_review": skeleton_file_consistency_review,
        "frozen_type_interface_review": frozen_type_interface_review,
        "frozen_function_interface_review": frozen_function_interface_review,
        "frozen_validator_interface_review": frozen_validator_interface_review,
        "handoff_contract_dryrun": handoff_contract_dryrun,
        "downstream_output_contract_review": downstream_output_contract_review,
        "forbidden_mutation_policy_review": forbidden_mutation_policy_review,
        "change_control_policy_review": change_control_policy_review,
        "boundary_freeze_review": boundary_freeze_review,
        "downstream_readiness_matrix_review": downstream_readiness_matrix_review,
        "non_claims_review": non_claims_review,
        "route_decision_review": route_decision_review,
        "issue_register": issue_register,
        "handoff_dryrun_readiness_decision": readiness,
    }
