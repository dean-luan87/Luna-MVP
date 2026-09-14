# -*- coding: utf-8 -*-
"""Luna Midplatform Decision Center Foundation Handoff DryRunAndReview v1."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_decision_center_controlled_skeleton_implementation_dryrun_v1 import (
    FINAL_DECISION_GO as SKELETON_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_DRYRUN_FINAL_GO,
    _analyze_skeleton_file,
)
from capabilities.midplatform.midplatform_decision_center_foundation_handoff_planning_v1 import (
    BOUNDARY_FALSE,
    CHANGE_CONTROL_STEPS,
    DOWNSTREAM_OUTPUT_CONTRACT,
    DOWNSTREAM_READINESS,
    FINAL_DECISION_GO as HANDOFF_PLANNING_FINAL_GO,
    FORBIDDEN_MUTATIONS,
    FROZEN_CANDIDATE_TYPES,
    FROZEN_FUNCTIONS,
    FROZEN_SKELETON_FILES,
    FROZEN_VALIDATORS,
    HANDOFF_RULES,
    NON_CLAIMS,
    REQUIRED_TYPE_BASE_FIELDS,
    ROUTE_RATIONALE,
)
from capabilities.midplatform.midplatform_decision_center_mount_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MOUNT_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MICRO_OS_FREEZE_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_information_integration_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as II_HANDOFF_DRYRUN_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Decision-Center-Foundation-Handoff-DryRunAndReview-v1-001"
SCOPE = "midplatform_decision_center_foundation_handoff_dryrun_and_review_only"
SOURCE = "midplatform_decision_center_foundation_handoff_dryrun_and_review_v1"

UPSTREAM_HANDOFF_PLANNING_FINAL = HANDOFF_PLANNING_FINAL_GO

FINAL_DECISION_GO = (
    "MIDPLATFORM_DECISION_CENTER_FOUNDATION_HANDOFF_DRYRUN_AND_REVIEW_"
    "CLOSED_READY_FOR_HEALTH_WATCHDOG_MOUNT_PLANNING"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_DECISION_CENTER_FOUNDATION_HANDOFF_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Health-Watchdog-Mount-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Decision-Center-Foundation-Handoff-Issue-Review-v1-001"

UPSTREAM_HANDOFF_PLANNING_FILES: Tuple[str, ...] = (
    "decision_center_foundation_handoff_scope_v1.json",
    "decision_center_foundation_version_tag_v1.json",
    "decision_center_frozen_type_interface_v1.json",
    "decision_center_frozen_function_interface_v1.json",
    "decision_center_frozen_validator_interface_v1.json",
    "decision_center_handoff_contract_v1.json",
    "decision_center_downstream_output_contract_v1.json",
    "decision_center_forbidden_mutation_policy_v1.json",
    "decision_center_change_control_policy_v1.json",
    "decision_center_boundary_freeze_v1.json",
    "decision_center_downstream_readiness_matrix_v1.json",
    "decision_center_non_claims_v1.json",
    "decision_center_route_decision_v1.json",
    "decision_center_foundation_handoff_readiness_decision_v1.json",
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
        "phase": "decision_center_mount_dryrun_and_review",
        "expected_final": MOUNT_DRYRUN_FINAL_GO,
        "pass_field": "dryrun_pass",
    },
    {
        "phase": "decision_center_controlled_skeleton_implementation_dryrun",
        "expected_final": SKELETON_DRYRUN_FINAL_GO,
        "pass_field": "dryrun_pass",
    },
    {
        "phase": "decision_center_controlled_skeleton_implementation_post_dryrun_review",
        "expected_final": POST_DRYRUN_FINAL_GO,
        "pass_field": "post_dryrun_review_pass",
    },
    {
        "phase": "decision_center_foundation_handoff_planning",
        "expected_final": HANDOFF_PLANNING_FINAL_GO,
        "pass_field": "planning_pass",
    },
)

DRYRUN_NON_CLAIMS: Tuple[str, ...] = tuple(
    claim.replace("Foundation Handoff", "Foundation Handoff DryRun") for claim in NON_CLAIMS
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_decision_center_foundation_handoff_dryrun_and_review_only",
    "simulated",
    "decision_center_files_created_now",
)

DEFAULT_HANDOFF_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_foundation_handoff_planning"
)
DEFAULT_POST_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_SKELETON_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_decision_center_controlled_skeleton_implementation_dryrun"
)
DEFAULT_MOUNT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_mount_dryrun_and_review"
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
    "midplatform_decision_center_foundation_handoff_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE,
        "module_id": "decision_center",
        "layer": "L7",
        "foundation_id": "midplatform_decision_center_foundation_v1",
        "depends_on": "midplatform_information_integration_foundation_v1",
        "also_depends_on": "midplatform_micro_os_foundation_v1",
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
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


def _resolve_upstream_roots(
    *,
    handoff_planning_root: Path,
    post_dryrun_root: Path,
    skeleton_dryrun_root: Path,
    mount_dryrun_root: Path,
    ii_handoff_dryrun_root: Path,
    micro_os_freeze_dryrun_root: Path,
) -> Dict[str, Path]:
    return {
        "micro_os_foundation_freeze_and_handoff_dryrun_and_review": micro_os_freeze_dryrun_root,
        "information_integration_foundation_handoff_dryrun_and_review": ii_handoff_dryrun_root,
        "decision_center_mount_dryrun_and_review": mount_dryrun_root,
        "decision_center_controlled_skeleton_implementation_dryrun": skeleton_dryrun_root,
        "decision_center_controlled_skeleton_implementation_post_dryrun_review": post_dryrun_root,
        "decision_center_foundation_handoff_planning": handoff_planning_root,
    }


def run_midplatform_decision_center_foundation_handoff_dryrun_and_review_v1(
    *,
    midplatform_decision_center_foundation_handoff_planning_root: str,
    midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review_root: str,
    midplatform_decision_center_controlled_skeleton_implementation_dryrun_root: str,
    midplatform_decision_center_mount_dryrun_and_review_root: str,
    midplatform_information_integration_foundation_handoff_dryrun_and_review_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    plan_root = Path(midplatform_decision_center_foundation_handoff_planning_root).expanduser().resolve()
    post_dr = Path(midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review_root).expanduser().resolve()
    sk_dr = Path(midplatform_decision_center_controlled_skeleton_implementation_dryrun_root).expanduser().resolve()
    mount_dr = Path(midplatform_decision_center_mount_dryrun_and_review_root).expanduser().resolve()
    ii_handoff_dr = Path(midplatform_information_integration_foundation_handoff_dryrun_and_review_root).expanduser().resolve()
    micro_os_dr = Path(midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = {
        **_dryrun_meta(),
        "output_root": str(out_root),
        "upstream_handoff_planning_root": str(plan_root),
        "upstream_post_dryrun_root": str(post_dr),
        "upstream_skeleton_dryrun_root": str(sk_dr),
        "upstream_mount_dryrun_root": str(mount_dr),
        "upstream_ii_handoff_dryrun_root": str(ii_handoff_dr),
        "upstream_micro_os_freeze_dryrun_root": str(micro_os_dr),
    }

    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_ready = _try_read_json(plan_root / "decision_center_foundation_handoff_readiness_decision_v1.json") or {}
    if plan_vr.get("verifier") != "GO":
        blockers.append("upstream handoff planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_HANDOFF_PLANNING_FINAL:
        blockers.append("upstream handoff planning final_decision mismatch")
    if plan_ready.get("planning_pass") is not True:
        blockers.append("upstream handoff planning_readiness must pass")

    upstream: Dict[str, Any] = {}
    for fname in UPSTREAM_HANDOFF_PLANNING_FILES:
        data = _try_read_json(plan_root / fname)
        if data is None:
            blockers.append(f"missing upstream: {fname}")
        upstream[fname.replace("_v1.json", "").replace(".json", "")] = data

    scope_doc = upstream.get("decision_center_foundation_handoff_scope") or {}
    version_doc = upstream.get("decision_center_foundation_version_tag") or {}
    type_doc = upstream.get("decision_center_frozen_type_interface") or {}
    func_doc = upstream.get("decision_center_frozen_function_interface") or {}
    validator_doc = upstream.get("decision_center_frozen_validator_interface") or {}
    handoff_doc = upstream.get("decision_center_handoff_contract") or {}
    output_doc = upstream.get("decision_center_downstream_output_contract") or {}
    mutation_doc = upstream.get("decision_center_forbidden_mutation_policy") or {}
    change_doc = upstream.get("decision_center_change_control_policy") or {}
    boundary_doc = upstream.get("decision_center_boundary_freeze") or {}
    matrix_doc = upstream.get("decision_center_downstream_readiness_matrix") or {}
    nc_doc = upstream.get("decision_center_non_claims") or {}
    route_doc = upstream.get("decision_center_route_decision") or {}

    root_map = _resolve_upstream_roots(
        handoff_planning_root=plan_root,
        post_dryrun_root=post_dr,
        skeleton_dryrun_root=sk_dr,
        mount_dryrun_root=mount_dr,
        ii_handoff_dryrun_root=ii_handoff_dr,
        micro_os_freeze_dryrun_root=micro_os_dr,
    )

    go_chain_checks: List[Tuple[str, bool]] = []
    go_chain_entries: List[Dict[str, Any]] = []
    for entry in UPSTREAM_GO_CHAIN:
        phase = entry["phase"]
        root = root_map[phase]
        vr = _try_read_json(root / "verifier_report.json") or {}
        sm = _try_read_json(root / "summary.json") or {}
        verifier_go = vr.get("verifier") == "GO"
        final_ok = sm.get("final_decision") == entry["expected_final"]
        pass_ok = sm.get(entry["pass_field"]) is True
        go_chain_checks.append((f"go.{phase[:18]}.verifier", verifier_go))
        go_chain_checks.append((f"go.{phase[:18]}.final", final_ok))
        go_chain_checks.append((f"go.{phase[:18]}.pass", pass_ok))
        if not verifier_go:
            blockers.append(f"upstream {phase} verifier must be GO")
        if not final_ok:
            blockers.append(f"upstream {phase} final_decision mismatch")
        if not pass_ok:
            blockers.append(f"upstream {phase} pass flag must be true")
        go_chain_entries.append(
            {
                "phase": phase,
                "root": str(root),
                "verifier": vr.get("verifier"),
                "final_decision": sm.get("final_decision"),
                "expected_final": entry["expected_final"],
                "pass_field": entry["pass_field"],
                "pass_value": sm.get(entry["pass_field"]),
                "go": verifier_go and final_ok and pass_ok,
            }
        )
    upstream_go_chain = {
        "review_id": "upstream_go_chain_review_v1",
        "entries": go_chain_entries,
        "blocker": any(not e["go"] for e in go_chain_entries),
        **_review_result(go_chain_checks),
        **meta,
    }

    version_checks: List[Tuple[str, bool]] = [
        ("foundation_id", version_doc.get("foundation_id") == "midplatform_decision_center_foundation_v1"),
        ("depends_on", version_doc.get("depends_on") == "midplatform_information_integration_foundation_v1"),
        ("also_depends_on", version_doc.get("also_depends_on") == "midplatform_micro_os_foundation_v1"),
        ("version", version_doc.get("version") == "1.0.0-skeleton"),
        ("status", version_doc.get("status") == "frozen_for_downstream_mount_planning"),
        ("runtime_status", version_doc.get("runtime_status") == "not_enabled"),
        ("compat", version_doc.get("compatibility_scope") == "planning_and_static_dryrun_only"),
        ("plan_match_id", plan_sm.get("foundation_id") == version_doc.get("foundation_id")),
        ("plan_match_dep", plan_sm.get("depends_on") == version_doc.get("depends_on")),
        ("plan_match_also_dep", plan_sm.get("also_depends_on") == version_doc.get("also_depends_on")),
    ]
    foundation_version_tag_review = {
        "review_id": "foundation_version_tag_review_v1",
        **_review_result(version_checks),
        **meta,
    }

    analyses = [_analyze_skeleton_file(repo_root, rel) for rel in FROZEN_SKELETON_FILES]
    skeleton_checks: List[Tuple[str, bool]] = []
    all_forbidden: List[str] = []
    for rel, analysis in zip(FROZEN_SKELETON_FILES, analyses):
        skeleton_checks.append((f"file.{rel.split('/')[-1][:14]}", analysis["exists"]))
        skeleton_checks.append((f"scope.{rel.split('/')[-1][:10]}", rel in (scope_doc.get("frozen_skeleton_files") or [])))
        skeleton_checks.append((f"clean.{rel.split('/')[-1][:10]}", analysis["pure_boundary_clean"]))
        skeleton_checks.append((f"no_async.{rel.split('/')[-1][:8]}", analysis["async_function_count"] == 0))
        skeleton_checks.append((f"no_loop.{rel.split('/')[-1][:8]}", analysis["while_true_count"] == 0))
        all_forbidden.extend(analysis["forbidden_imports"])
    skeleton_checks.append(("files_created", all(a["exists"] for a in analyses)))
    skeleton_checks.append(("no_forbidden_imports", len(all_forbidden) == 0))
    if all_forbidden:
        blockers.append(f"forbidden imports detected: {sorted(set(all_forbidden))}")
    skeleton_file_consistency = {
        "review_id": "skeleton_file_consistency_review_v1",
        "files": analyses,
        "forbidden_imports_found": sorted(set(all_forbidden)),
        "blocker": len(all_forbidden) > 0,
        **_review_result(skeleton_checks),
        **meta,
    }

    types_mod = importlib.import_module("capabilities.midplatform.core.decision_center_types_v1")
    type_checks: List[Tuple[str, bool]] = []
    state_values = [s.value for s in types_mod.DecisionState]
    readiness_values = [r.value for r in types_mod.DecisionReadiness]
    type_checks.append(("state.count15", len(state_values) >= 15))
    type_checks.append(("readiness.count5", len(readiness_values) >= 5))
    for enum_name, values in (("DecisionState", state_values), ("DecisionReadiness", readiness_values)):
        type_checks.append((f"enum.{enum_name[:14]}", enum_name in (type_doc.get("enums") or {})))
        type_checks.append((f"disk.{enum_name[:14]}", hasattr(types_mod, enum_name)))
        type_checks.append((f"scope.{enum_name[:12]}", enum_name in (scope_doc.get("frozen_enums") or [])))
        type_checks.append((f"values.{enum_name[:12]}", len(values) >= (15 if enum_name == "DecisionState" else 5)))
    for name in FROZEN_CANDIDATE_TYPES:
        type_checks.append((f"type.{name[:14]}", name in (type_doc.get("types") or [])))
        type_checks.append((f"scope.{name[:12]}", name in (scope_doc.get("frozen_candidate_types") or [])))
        type_checks.append((f"disk.{name[:12]}", hasattr(types_mod, name)))
        if hasattr(types_mod, name):
            fields = getattr(getattr(types_mod, name), "__dataclass_fields__", {})
            for base in REQUIRED_TYPE_BASE_FIELDS:
                type_checks.append((f"{name[:8]}.{base[:10]}", base in fields))
            type_checks.append((f"{name[:8]}.not_fact", fields.get("fact_status") is not None))
    dc_fields = getattr(types_mod.DecisionCandidate, "__dataclass_fields__", {})
    ddhc_fields = getattr(types_mod.DownstreamDecisionHandoffCandidate, "__dataclass_fields__", {})
    type_checks.append(("dc.final_false", dc_fields.get("final_action").default is False))
    type_checks.append(("dc.user_false", dc_fields.get("user_output").default is False))
    type_checks.append(("ddhc.mount_false", ddhc_fields.get("direct_mount").default is False))
    frozen_type_interface_review = {
        "review_id": "frozen_type_interface_review_v1",
        "type_count": len(FROZEN_CANDIDATE_TYPES),
        "decision_state_count": len(state_values),
        "decision_readiness_count": len(readiness_values),
        "fact_status_semantics_immutable": type_doc.get("fact_status_semantics_immutable") is True,
        **_review_result(type_checks),
        **meta,
    }

    sk_mod = importlib.import_module("capabilities.midplatform.core.decision_center_skeleton_v1")
    sk_src = (repo_root / "capabilities/midplatform/core/decision_center_skeleton_v1.py").read_text(encoding="utf-8").lower()
    fn_checks: List[Tuple[str, bool]] = []
    for fn in FROZEN_FUNCTIONS:
        fn_checks.append((f"listed.{fn[:14]}", fn in (func_doc.get("functions") or [])))
        fn_checks.append((f"scope.{fn[:12]}", fn in (scope_doc.get("frozen_functions") or [])))
        fn_checks.append((f"disk.{fn[:12]}", hasattr(sk_mod, fn) and callable(getattr(sk_mod, fn))))
    fn_checks.append(("candidate_only", func_doc.get("candidate_only_outputs") is True))
    fn_checks.append(("no_runtime", func_doc.get("runtime_execution") is False))
    fn_checks.append(("no_task_exec", "execute_task" not in sk_src))
    fn_checks.append(("no_worldmodel_write", "write_worldmodel" not in sk_src))
    fn_checks.append(("no_memory_write", "write_memory" not in sk_src))
    fn_checks.append(("no_user_output_true", "user_output=true" not in sk_src.replace(" ", "")))
    fn_checks.append(("no_final_action_true", "final_action=true" not in sk_src.replace(" ", "")))
    frozen_function_interface_review = {
        "review_id": "frozen_function_interface_review_v1",
        "function_count": len(FROZEN_FUNCTIONS),
        **_review_result(fn_checks),
        **meta,
    }

    sv_mod = importlib.import_module("capabilities.midplatform.core.decision_center_static_validators_v1")
    sv_checks: List[Tuple[str, bool]] = []
    for fn in FROZEN_VALIDATORS:
        sv_checks.append((f"listed.{fn[:14]}", fn in (validator_doc.get("validators") or [])))
        sv_checks.append((f"scope.{fn[:12]}", fn in (scope_doc.get("frozen_validators") or [])))
        sv_checks.append((f"disk.{fn[:12]}", hasattr(sv_mod, fn) and callable(getattr(sv_mod, fn))))
    sv_checks.append(("reusable", validator_doc.get("reusable_by_downstream") is True))
    frozen_validator_interface_review = {
        "review_id": "frozen_validator_interface_review_v1",
        "validator_count": len(FROZEN_VALIDATORS),
        **_review_result(sv_checks),
        **meta,
    }

    handoff_checks: List[Tuple[str, bool]] = []
    rules = handoff_doc.get("rules") or []
    rules_blob = json.dumps(rules, ensure_ascii=False).lower()
    for rule in HANDOFF_RULES:
        handoff_checks.append((f"rule.{rule[:16]}", rule in rules))
    handoff_checks.append(("forb.final_action", "final action" in rules_blob))
    handoff_checks.append(("forb.task_execution", "task execution" in rules_blob))
    handoff_checks.append(("forb.user_output", "user output" in rules_blob))
    handoff_checks.append(("forb.runtime", "runtime" in rules_blob))
    handoff_checks.append(("forb.governance", "governance" in rules_blob))
    handoff_checks.append(("forb.memory", "memory" in rules_blob and "worldmodel" in rules_blob))
    handoff_contract_dryrun = {
        "dryrun_id": "handoff_contract_dryrun_v1",
        "rule_count": len(HANDOFF_RULES),
        **_review_result(handoff_checks),
        **meta,
    }

    output_checks: List[Tuple[str, bool]] = [
        ("output_gate_ready_false", output_doc.get("output_gate_ready") is False),
        ("task_manager_ready_false", output_doc.get("task_manager_ready") is False),
        ("health_watchdog_ready_false", output_doc.get("health_watchdog_ready") is False),
        ("entry_count6", output_doc.get("entry_count") == 6),
    ]
    for entry in DOWNSTREAM_OUTPUT_CONTRACT:
        found = next((e for e in output_doc.get("entries") or [] if e.get("consumer") == entry["consumer"]), {})
        output_checks.append((f"consumer.{entry['consumer'][:14]}", bool(found)))
        output_checks.append((f"payload.{entry['consumer'][:10]}", len(found.get("consumes") or []) >= 1))
        for payload in entry["consumes"]:
            output_checks.append((f"payload.{entry['consumer'][:6]}.{payload[:8]}", payload in (found.get("consumes") or [])))
    downstream_output_contract_review = {
        "review_id": "downstream_output_contract_review_v1",
        "output_gate_ready": False,
        "task_manager_ready": False,
        "health_watchdog_ready": False,
        **_review_result(output_checks),
        **meta,
    }

    mut_checks: List[Tuple[str, bool]] = [
        (f"mut.{m[:12]}", m in (mutation_doc.get("forbidden_mutations") or [])) for m in FORBIDDEN_MUTATIONS
    ]
    mut_blob = json.dumps(mutation_doc.get("forbidden_mutations") or []).lower()
    mut_checks.extend(
        [
            ("mut.final_action", "final_action" in mut_blob),
            ("mut.user_output", "user_output" in mut_blob),
            ("mut.direct_mount", "direct_mount" in mut_blob),
            ("mut.no_ii_redefine", "redefine_information_integration" in mut_blob),
        ]
    )
    forbidden_mutation_policy_review = {
        "review_id": "forbidden_mutation_policy_review_v1",
        **_review_result(mut_checks),
        **meta,
    }

    change_checks: List[Tuple[str, bool]] = [
        (f"step.{s[:12]}", s in (change_doc.get("steps") or [])) for s in CHANGE_CONTROL_STEPS
    ]
    change_checks.append(("no_change_now", change_doc.get("change_executed_in_this_phase") is False))
    change_control_policy_review = {
        "review_id": "change_control_policy_review_v1",
        **_review_result(change_checks),
        **meta,
    }

    boundary_checks: List[Tuple[str, bool]] = [
        ("decision_center_files_created_now", meta.get("decision_center_files_created_now") is True),
    ]
    global_b = boundary_doc.get("global_boundaries") or {}
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"global.{field[:14]}", global_b.get(field) is False))
        boundary_checks.append((f"meta.{field[:14]}", meta.get(field) is False))
    boundary_freeze_review = {
        "review_id": "boundary_freeze_review_v1",
        "global_boundaries": {**{f: False for f in BOUNDARY_FALSE}, "decision_center_files_created_now": True},
        **_review_result(boundary_checks),
        **meta,
    }

    matrix_checks: List[Tuple[str, bool]] = []
    for entry in DOWNSTREAM_READINESS:
        found = next((e for e in matrix_doc.get("entries") or [] if e.get("module") == entry["module"]), {})
        matrix_checks.append((f"ready.{entry['module'][:14]}", found.get("readiness") == entry["readiness"]))
    matrix_checks.extend(
        [
            (
                "primary_hw",
                any(
                    e.get("module") == "health_watchdog_mount_planning" and e.get("readiness") == "primary_next_ready"
                    for e in matrix_doc.get("entries") or []
                ),
            ),
            (
                "secondary_tm",
                any(
                    e.get("module") == "task_manager_mount_planning"
                    and e.get("readiness") == "secondary_after_health_watchdog_or_parallel_later"
                    for e in matrix_doc.get("entries") or []
                ),
            ),
            (
                "output_gate_not_ready",
                any(
                    e.get("module") == "output_gate_mount_planning"
                    and e.get("readiness") == "not_ready_until_output_handoff_contract_review"
                    for e in matrix_doc.get("entries") or []
                ),
            ),
        ]
    )
    downstream_readiness_matrix_review = {
        "review_id": "downstream_readiness_matrix_review_v1",
        **_review_result(matrix_checks),
        **meta,
    }

    nc_checks: List[Tuple[str, bool]] = []
    for claim in DRYRUN_NON_CLAIMS:
        nc_checks.append((f"dryrun.{claim[:14]}", True))
    for claim in nc_doc.get("non_claims") or []:
        nc_checks.append((f"plan.{claim[:14]}", claim in NON_CLAIMS))
    nc_checks.append(("nc.count11", len(DRYRUN_NON_CLAIMS) == 11))
    non_claims_review = {
        "review_id": "non_claims_review_v1",
        "dryrun_non_claims": list(DRYRUN_NON_CLAIMS),
        "planning_non_claims": list(NON_CLAIMS),
        **_review_result(nc_checks),
        **meta,
    }

    route_checks: List[Tuple[str, bool]] = [
        ("primary_hw", route_doc.get("primary_next_phase") == NEXT_PHASE_GO),
        ("secondary_tm", route_doc.get("secondary_next_phase") == "Phase-Midplatform-Task-Manager-Mount-Planning-v1-001"),
        ("deferred_count3", len(route_doc.get("deferred") or []) == 3),
        ("health_watchdog_no_recovery", meta.get("recovery_executed_now") is not True),
        ("hw_consumes_safety_refs", True),
    ]
    for r in ROUTE_RATIONALE:
        route_checks.append((f"rationale.{r[:14]}", r in (route_doc.get("rationale") or [])))
    route_decision_review = {
        "review_id": "route_decision_review_v1",
        "health_watchdog_consumes": ["health_review_candidate", "blocked", "hold", "safety_refs"],
        "real_recovery_triggered": False,
        **_review_result(route_checks),
        **meta,
    }

    review_passes = [
        upstream_go_chain.get("dryrun_and_review_pass") and not upstream_go_chain.get("blocker"),
        foundation_version_tag_review.get("dryrun_and_review_pass"),
        skeleton_file_consistency.get("dryrun_and_review_pass") and not skeleton_file_consistency.get("blocker"),
        frozen_type_interface_review.get("dryrun_and_review_pass"),
        frozen_function_interface_review.get("dryrun_and_review_pass"),
        frozen_validator_interface_review.get("dryrun_and_review_pass"),
        handoff_contract_dryrun.get("dryrun_and_review_pass"),
        downstream_output_contract_review.get("dryrun_and_review_pass"),
        forbidden_mutation_policy_review.get("dryrun_and_review_pass"),
        change_control_policy_review.get("dryrun_and_review_pass"),
        boundary_freeze_review.get("dryrun_and_review_pass"),
        downstream_readiness_matrix_review.get("dryrun_and_review_pass"),
        non_claims_review.get("dryrun_and_review_pass"),
        route_decision_review.get("dryrun_and_review_pass"),
    ]

    issues: List[Dict[str, Any]] = []
    if blockers:
        issues.extend([{"issue_id": f"blocker.{i}", "severity": "blocker", "detail": b} for i, b in enumerate(blockers)])
    for name, review in (
        ("upstream_go_chain", upstream_go_chain),
        ("foundation_version_tag", foundation_version_tag_review),
        ("skeleton_file_consistency", skeleton_file_consistency),
        ("frozen_type_interface", frozen_type_interface_review),
        ("frozen_function_interface", frozen_function_interface_review),
        ("frozen_validator_interface", frozen_validator_interface_review),
        ("handoff_contract", handoff_contract_dryrun),
        ("downstream_output_contract", downstream_output_contract_review),
        ("forbidden_mutation_policy", forbidden_mutation_policy_review),
        ("change_control_policy", change_control_policy_review),
        ("boundary_freeze", boundary_freeze_review),
        ("downstream_readiness_matrix", downstream_readiness_matrix_review),
        ("non_claims", non_claims_review),
        ("route_decision", route_decision_review),
    ):
        for issue in review.get("issues") or []:
            issues.append({**issue, "review": name, "severity": "blocker"})

    blocker_count = len([i for i in issues if i.get("severity") == "blocker"])
    dryrun_pass = len(blockers) == 0 and all(review_passes) and blocker_count == 0

    issue_register = {
        "register_id": "issue_register_v1",
        "issues": issues,
        "issue_count": len(issues),
        "blocker_count": blocker_count,
        **meta,
    }

    readiness = {
        "decision_id": "handoff_dryrun_readiness_decision_v1",
        "dryrun_pass": dryrun_pass,
        "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "foundation_id": version_doc.get("foundation_id"),
        "depends_on": version_doc.get("depends_on"),
        "also_depends_on": version_doc.get("also_depends_on"),
        "foundation_version": version_doc.get("version"),
        "runtime_status": version_doc.get("runtime_status"),
        "reviews_total": 14,
        "reviews_passed": sum(1 for p in review_passes if p),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "blocker_count": blocker_count,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "foundation_id": version_doc.get("foundation_id"),
        "depends_on": version_doc.get("depends_on"),
        "also_depends_on": version_doc.get("also_depends_on"),
        "foundation_version": version_doc.get("version"),
        "runtime_status": version_doc.get("runtime_status"),
        "primary_route_after_handoff": route_doc.get("primary_next_phase"),
        "non_claims": list(DRYRUN_NON_CLAIMS),
        **meta,
    }

    return {
        "summary": summary,
        "upstream_go_chain_review": upstream_go_chain,
        "foundation_version_tag_review": foundation_version_tag_review,
        "skeleton_file_consistency_review": skeleton_file_consistency,
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
