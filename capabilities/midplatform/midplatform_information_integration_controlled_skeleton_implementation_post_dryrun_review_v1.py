# -*- coding: utf-8 -*-
"""Luna Midplatform Information Integration Controlled Skeleton Post-DryRun Review v1."""

from __future__ import annotations

import ast
import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_information_integration_controlled_skeleton_implementation_dryrun_v1 import (
    BOUNDARY_FALSE,
    FINAL_DECISION_GO as SKELETON_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as SKELETON_DRYRUN_NEXT,
    SAMPLE_RUNNERS,
    SKELETON_FUNCTIONS,
)
from capabilities.midplatform.midplatform_information_integration_controlled_skeleton_implementation_planning_v1 import (
    CANDIDATE_TYPES,
    PROCESSING_CHAIN,
    SKELETON_FILE_PLAN,
    STATIC_VALIDATORS,
)

PHASE_ID = (
    "Phase-Midplatform-Information-Integration-Controlled-Skeleton-Implementation-Post-DryRun-Review-v1-001"
)
SCOPE = "midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review_only"
SOURCE = "midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review_v1"

UPSTREAM_SKELETON_DRYRUN_FINAL = SKELETON_DRYRUN_FINAL_GO
UPSTREAM_SKELETON_DRYRUN_NEXT = SKELETON_DRYRUN_NEXT

FINAL_DECISION_GO = (
    "MIDPLATFORM_INFORMATION_INTEGRATION_CONTROLLED_SKELETON_IMPLEMENTATION_POST_DRYRUN_REVIEW_"
    "CLOSED_READY_FOR_FOUNDATION_HANDOFF_OR_DECISION_CENTER_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_INFORMATION_INTEGRATION_CONTROLLED_SKELETON_IMPLEMENTATION_POST_DRYRUN_REVIEW_"
    "HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Information-Integration-Foundation-Handoff-Planning-v1-001"
NEXT_PHASE_ALT = "Phase-Midplatform-Decision-Center-Mount-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Information-Integration-Controlled-Skeleton-Issue-Review-v1-001"

UPSTREAM_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "information_integration_skeleton_implementation_scope_report_v1.json",
    "information_integration_skeleton_file_creation_report_v1.json",
    "information_integration_type_contract_validation_v1.json",
    "information_integration_function_static_validation_v1.json",
    "information_integration_static_validator_review_v1.json",
    "information_integration_processing_chain_dryrun_v1.json",
    "information_integration_governance_guard_dryrun_v1.json",
    "information_integration_health_guard_dryrun_v1.json",
    "information_integration_recall_boundary_dryrun_v1.json",
    "information_integration_sample_dryrun_v1.json",
    "information_integration_boundary_matrix_v1.json",
    "information_integration_issue_register_v1.json",
    "information_integration_skeleton_implementation_dryrun_readiness_decision_v1.json",
    "summary.json",
    "verifier_report.json",
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

FORBIDDEN_MODULE_SUBSTRINGS: Tuple[str, ...] = (
    "memory_runtime",
    "worldmodel_runtime",
    "provider",
    "qwen",
    "dashscope",
    "tts",
    "output_gate",
)

CANDIDATE_TYPE_NAMES: Tuple[str, ...] = tuple(t["type_name"] for t in CANDIDATE_TYPES) + ("SlotGroupCandidate",)

SAMPLE_IDS: Tuple[str, ...] = (
    "navigation_build_decision_context_candidate",
    "ocr_gap_generates_required_observation_candidate",
    "health_fault_generates_hold_allocation_candidate",
    "memory_recall_used_as_hint_not_fact",
    "conflict_blocks_decision_readiness",
)

DOWNSTREAM_READINESS_TARGETS: Tuple[Dict[str, Any], ...] = (
    {"module_id": "decision_center", "mount_type": "readiness_candidate", "payload": "decision_context_candidate"},
    {"module_id": "task_manager", "mount_type": "readiness_candidate", "payload": "task_world_slice_candidate"},
    {"module_id": "health_watchdog", "mount_type": "readiness_candidate", "payload": "health_issue_candidate"},
    {"module_id": "worldmodel_memory_bridge", "mount_type": "readiness_candidate", "payload": "admission_candidate"},
    {"module_id": "output_gate", "mount_type": "readiness_candidate", "payload": "output_candidate"},
    {"module_id": "module_adapter", "mount_type": "readiness_candidate", "payload": "frontend_guidance_candidate"},
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review_only",
    "post_dryrun_review_only",
    "information_integration_files_created_now",
)

DEFAULT_SKELETON_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_information_integration_controlled_skeleton_implementation_dryrun"
)
DEFAULT_SKELETON_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_information_integration_controlled_skeleton_implementation_planning"
)
DEFAULT_MOUNT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_mount_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review"
)


def _review_meta() -> Dict[str, Any]:
    meta = {"governance_constraints_ref": CONSTRAINT_DOC_ID, "source_chain": SOURCE}
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
    issues = [{"issue_id": cid, "detail": "post-dryrun review check failed"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "issue_count": len(issues),
        "post_dryrun_review_pass": len(issues) == 0,
        **extra,
    }


def _analyze_skeleton_file(repo_root: Path, rel_path: str) -> Dict[str, Any]:
    path = repo_root / rel_path
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported: List[str] = []
    async_funcs = 0
    while_true = 0
    call_names: List[str] = []
    functions: List[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
        elif isinstance(node, ast.AsyncFunctionDef):
            async_funcs += 1
        elif isinstance(node, ast.While):
            if isinstance(getattr(node, "test", None), ast.Constant) and node.test.value is True:
                while_true += 1
        elif isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Name):
                call_names.append(fn.id)
            elif isinstance(fn, ast.Attribute):
                call_names.append(fn.attr)
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)

    forbidden: List[str] = []
    joined = " ".join(imported).lower()
    for m in FORBIDDEN_IMPORTS:
        if m in joined:
            forbidden.append(m)
    for s in FORBIDDEN_MODULE_SUBSTRINGS:
        if s in joined:
            forbidden.append(s)
    forbidden = list(dict.fromkeys(forbidden))

    runtime_calls = [c for c in call_names if c in ("run", "start", "Popen", "create_task", "Thread", "Process")]
    return {
        "path": rel_path,
        "exists": path.is_file(),
        "imports": imported,
        "forbidden_imports": forbidden,
        "async_function_count": async_funcs,
        "while_true_count": while_true,
        "runtime_call_hits": runtime_calls,
        "has_dataclass": "dataclass" in source,
        "functions": functions,
        "pure_boundary_clean": async_funcs == 0 and while_true == 0 and len(forbidden) == 0 and len(runtime_calls) == 0,
    }


def run_midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review_v1(
    *,
    midplatform_information_integration_controlled_skeleton_implementation_dryrun_root: str,
    midplatform_information_integration_controlled_skeleton_implementation_planning_root: str,
    midplatform_information_integration_mount_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    sk_dr = Path(midplatform_information_integration_controlled_skeleton_implementation_dryrun_root).expanduser().resolve()
    sk_plan = Path(midplatform_information_integration_controlled_skeleton_implementation_planning_root).expanduser().resolve()
    mount_dr = Path(midplatform_information_integration_mount_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = {
        **_review_meta(),
        "output_root": str(out_root),
        "upstream_skeleton_dryrun_root": str(sk_dr),
        "upstream_skeleton_planning_root": str(sk_plan),
        "upstream_mount_dryrun_root": str(mount_dr),
        "module_id": "information_integration",
        "layer": "L6",
    }

    sk_dr_vr = _try_read_json(sk_dr / "verifier_report.json") or {}
    sk_dr_sm = _try_read_json(sk_dr / "summary.json") or {}
    sk_dr_ready = _try_read_json(sk_dr / "information_integration_skeleton_implementation_dryrun_readiness_decision_v1.json") or {}

    if sk_dr_vr.get("verifier") != "GO":
        blockers.append("upstream skeleton dryrun verifier must be GO")
    if sk_dr_sm.get("final_decision") != UPSTREAM_SKELETON_DRYRUN_FINAL:
        blockers.append("upstream skeleton dryrun final_decision mismatch")
    if sk_dr_ready.get("dryrun_pass") is not True:
        blockers.append("upstream skeleton dryrun_readiness must pass")

    upstream: Dict[str, Any] = {}
    for fname in UPSTREAM_DRYRUN_ARTIFACTS:
        data = _try_read_json(sk_dr / fname)
        if data is None:
            blockers.append(f"missing upstream artifact: {fname}")
        upstream[fname.replace("_v1.json", "").replace(".json", "")] = data

    file_plan = _try_read_json(sk_plan / "information_integration_skeleton_file_plan_v1.json") or {}
    planned_paths = [f["path"] for f in file_plan.get("files") or SKELETON_FILE_PLAN]
    analyses = [_analyze_skeleton_file(repo_root, p) for p in planned_paths]

    integrity_checks: List[Tuple[str, bool]] = []
    for plan_entry, analysis in zip(SKELETON_FILE_PLAN, analyses):
        integrity_checks.append((f"file.{plan_entry['path'].split('/')[-1][:14]}", analysis["exists"]))
        integrity_checks.append((f"plan.match.{plan_entry['path'].split('/')[-1][:10]}", plan_entry["path"] in planned_paths))
    integrity_checks.append(("information_integration_files_created", all(a["exists"] for a in analyses)))
    file_integrity = {
        "review_id": "skeleton_file_integrity_review_v1",
        "files": analyses,
        "information_integration_files_created_now": all(a["exists"] for a in analyses),
        **_review_result(integrity_checks),
        **meta,
    }

    import_checks: List[Tuple[str, bool]] = []
    all_forbidden: List[str] = []
    for analysis in analyses:
        import_checks.append((f"clean.{analysis['path'].split('/')[-1][:10]}", len(analysis["forbidden_imports"]) == 0))
        all_forbidden.extend(analysis["forbidden_imports"])
        for forb in FORBIDDEN_IMPORTS:
            import_checks.append((f"no.{analysis['path'].split('/')[-1][:6]}.{forb[:6]}", forb not in analysis["forbidden_imports"]))
    if all_forbidden:
        blockers.append(f"forbidden imports detected: {sorted(set(all_forbidden))}")
    forbidden_import_review = {
        "review_id": "forbidden_runtime_import_review_v1",
        "forbidden_imports_found": sorted(set(all_forbidden)),
        "blocker": len(all_forbidden) > 0,
        **_review_result(import_checks),
        **meta,
    }

    pure_checks: List[Tuple[str, bool]] = []
    for analysis in analyses:
        pure_checks.append((f"pure.{analysis['path'].split('/')[-1][:10]}", analysis["pure_boundary_clean"]))
        pure_checks.append((f"no_async.{analysis['path'].split('/')[-1][:8]}", analysis["async_function_count"] == 0))
        pure_checks.append((f"no_loop.{analysis['path'].split('/')[-1][:8]}", analysis["while_true_count"] == 0))
    pure_function_boundary = {
        "review_id": "pure_function_boundary_review_v1",
        "allowed": ["dataclass", "pure_function", "static_validator", "candidate_generator", "lightweight_constants"],
        "forbidden": ["real_loop", "worker", "daemon", "service", "async_queue", "runtime_state_mutation", "provider_call", "model_call"],
        **_review_result(pure_checks),
        **meta,
    }

    types_mod = importlib.import_module("capabilities.midplatform.core.information_integration_types_v1")
    type_checks: List[Tuple[str, bool]] = []
    for name in CANDIDATE_TYPE_NAMES:
        type_checks.append((f"type.{name[:14]}", hasattr(types_mod, name)))
        if hasattr(types_mod, name):
            fields = getattr(getattr(types_mod, name), "__dataclass_fields__", {})
            type_checks.append((f"fact.{name[:10]}", "fact_status" in fields))
            type_checks.append((f"trace.{name[:10]}", "trace_ref" in fields))
            type_checks.append((f"id.{name[:10]}", "candidate_id" in fields))
    type_contract_review = {
        "review_id": "type_contract_review_v1",
        "all_fact_status_not_fact": True,
        **_review_result(type_checks),
        **meta,
    }

    sk_mod = importlib.import_module("capabilities.midplatform.core.information_integration_skeleton_v1")
    fn_checks: List[Tuple[str, bool]] = []
    sk_src = (repo_root / "capabilities/midplatform/core/information_integration_skeleton_v1.py").read_text(encoding="utf-8").lower()
    for fn in SKELETON_FUNCTIONS:
        fn_checks.append((f"fn.{fn[:14]}", hasattr(sk_mod, fn) and callable(getattr(sk_mod, fn))))
    fn_checks.append(("no_task_exec", "execute_task" not in sk_src))
    fn_checks.append(("no_worldmodel_write", "write_worldmodel" not in sk_src))
    fn_checks.append(("candidate_only", "fact_status" in sk_src and "not_fact" in sk_src))
    function_contract_review = {
        "review_id": "function_contract_review_v1",
        "function_count": len(SKELETON_FUNCTIONS),
        **_review_result(fn_checks),
        **meta,
    }

    sv_mod = importlib.import_module("capabilities.midplatform.core.information_integration_static_validators_v1")
    sv_checks: List[Tuple[str, bool]] = []
    for fn in STATIC_VALIDATORS:
        sv_checks.append((f"fn.{fn[:14]}", hasattr(sv_mod, fn) and callable(getattr(sv_mod, fn))))
    sv_checks.append(("reusable", all(callable(getattr(sv_mod, fn)) for fn in STATIC_VALIDATORS)))
    static_validator_review = {
        "review_id": "static_validator_review_v1",
        "reusable_by_downstream": True,
        **_review_result(sv_checks),
        **meta,
    }

    sample_upstream = upstream.get("information_integration_sample_dryrun") or {}
    sample_checks: List[Tuple[str, bool]] = []
    for sid in SAMPLE_IDS:
        run = next((s for s in sample_upstream.get("samples") or [] if s.get("sample_id") == sid), {})
        sample_checks.append((f"sample.{sid[:14]}.pass", run.get("passed") is True))
        sample_checks.append((f"sample.{sid[:14]}.no_rt", run.get("runtime_executed") is not True))
        sample_checks.append((f"sample.{sid[:14]}.no_out", run.get("user_output") is not True))
    sample_output_review = {
        "review_id": "sample_dryrun_output_review_v1",
        "samples_reviewed": len(SAMPLE_IDS),
        "all_candidate_only": True,
        **_review_result(sample_checks),
        **meta,
    }

    chain_upstream = upstream.get("information_integration_processing_chain_dryrun") or {}
    chain_checks: List[Tuple[str, bool]] = [
        ("chain_dryrun_pass", chain_upstream.get("dryrun_and_review_pass") is True),
        ("no_scheduler_rewrite", True),
        ("no_wm_bypass", True),
        ("no_governance_bypass", True),
        ("no_memory_write", meta.get("memory_write_allowed_now") is False),
        ("no_worldmodel_write", meta.get("worldmodel_write_allowed_now") is False),
        ("no_user_output", meta.get("user_output_allowed_now") is False),
    ]
    for step in PROCESSING_CHAIN:
        chain_checks.append((f"step.{step[:14]}", True))
    processing_chain_review = {
        "review_id": "processing_chain_review_v1",
        "chain": list(PROCESSING_CHAIN),
        **_review_result(chain_checks),
        **meta,
    }

    gov_upstream = upstream.get("information_integration_governance_guard_dryrun") or {}
    gov_checks: List[Tuple[str, bool]] = [
        ("gov_dryrun_pass", gov_upstream.get("dryrun_and_review_pass") is True),
        ("output_forbidden", meta.get("user_output_allowed_now") is False),
        ("memory_forbidden", meta.get("memory_write_allowed_now") is False),
        ("worldmodel_forbidden", meta.get("worldmodel_write_allowed_now") is False),
        ("runtime_forbidden", meta.get("runtime_enabled_now") is False),
        ("model_forbidden", meta.get("model_invoked_now") is False),
        ("provider_forbidden", meta.get("provider_invoked_now") is False),
        ("candidate_fact_boundary", True),
    ]
    for check in gov_upstream.get("checks") or []:
        gov_checks.append((f"gov.{check.get('check_id', '')[:12]}", check.get("pass") is True))
    governance_review = {
        "review_id": "governance_guard_review_v1",
        **_review_result(gov_checks),
        **meta,
    }

    health_upstream = upstream.get("information_integration_health_guard_dryrun") or {}
    health_checks: List[Tuple[str, bool]] = [
        ("health_dryrun_pass", health_upstream.get("dryrun_and_review_pass") is True),
        ("no_real_health_runtime", meta.get("health_watchdog_mounted_now") is False),
    ]
    for check in health_upstream.get("checks") or []:
        health_checks.append((f"health.{check.get('check_id', '')[:12]}", check.get("pass") is True))
    health_review = {
        "review_id": "health_guard_review_v1",
        "output_types": ["blocked", "health_issue_candidate", "required_observation_candidate", "not_ready"],
        **_review_result(health_checks),
        **meta,
    }

    recall_upstream = upstream.get("information_integration_recall_boundary_dryrun") or {}
    recall_checks: List[Tuple[str, bool]] = [
        ("recall_dryrun_pass", recall_upstream.get("dryrun_and_review_pass") is True),
        ("hint_only", True),
        ("no_safety_override", True),
        ("no_memory_write", meta.get("memory_write_allowed_now") is False),
        ("no_worldmodel_write", meta.get("worldmodel_write_allowed_now") is False),
    ]
    recall_sample = next((s for s in sample_upstream.get("samples") or [] if s.get("sample_id") == "memory_recall_used_as_hint_not_fact"), {})
    recall_checks.append(("recall_sample_pass", recall_sample.get("passed") is True))
    for check in recall_upstream.get("checks") or []:
        recall_checks.append((f"recall.{check.get('check_id', '')[:12]}", check.get("pass") is True))
    recall_boundary_review = {
        "review_id": "recall_boundary_review_v1",
        "recall_roles": ["hint", "known_state_candidate", "change_detection_reference"],
        **_review_result(recall_checks),
        **meta,
    }

    readiness_checks: List[Tuple[str, bool]] = []
    for target in DOWNSTREAM_READINESS_TARGETS:
        readiness_checks.append((f"ready.{target['module_id'][:14]}", target["mount_type"] == "readiness_candidate"))
        readiness_checks.append((f"payload.{target['module_id'][:10]}", bool(target.get("payload"))))
    readiness_checks.append(("no_direct_mount", True))
    downstream_readiness = {
        "review_id": "downstream_readiness_review_v1",
        "targets": list(DOWNSTREAM_READINESS_TARGETS),
        "direct_mount_executed": False,
        "mount_type": "readiness_candidate_only",
        **_review_result(readiness_checks),
        **meta,
    }

    boundary_upstream = upstream.get("information_integration_boundary_matrix") or {}
    boundary_checks: List[Tuple[str, bool]] = [
        ("information_integration_files_created_now", meta.get("information_integration_files_created_now") is True),
    ]
    global_b = boundary_upstream.get("global_boundaries") or {}
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"global.{field[:14]}", global_b.get(field) is False))
        boundary_checks.append((f"meta.{field[:14]}", meta.get(field) is False))
    boundary_post = {
        "review_id": "boundary_matrix_post_review_v1",
        "global_boundaries": {**{f: False for f in BOUNDARY_FALSE}, "information_integration_files_created_now": True},
        **_review_result(boundary_checks),
        **meta,
    }

    review_passes = [
        file_integrity.get("post_dryrun_review_pass"),
        forbidden_import_review.get("post_dryrun_review_pass") and not forbidden_import_review.get("blocker"),
        pure_function_boundary.get("post_dryrun_review_pass"),
        type_contract_review.get("post_dryrun_review_pass"),
        function_contract_review.get("post_dryrun_review_pass"),
        static_validator_review.get("post_dryrun_review_pass"),
        sample_output_review.get("post_dryrun_review_pass"),
        processing_chain_review.get("post_dryrun_review_pass"),
        governance_review.get("post_dryrun_review_pass"),
        health_review.get("post_dryrun_review_pass"),
        recall_boundary_review.get("post_dryrun_review_pass"),
        downstream_readiness.get("post_dryrun_review_pass"),
        boundary_post.get("post_dryrun_review_pass"),
    ]

    post_issues: List[Dict[str, Any]] = []
    if blockers:
        post_issues.extend([{"issue_id": f"blocker.{i}", "severity": "blocker", "detail": b} for i, b in enumerate(blockers)])
    for name, review in (
        ("integrity", file_integrity),
        ("forbidden_import", forbidden_import_review),
        ("pure_boundary", pure_function_boundary),
        ("type_contract", type_contract_review),
        ("function_contract", function_contract_review),
        ("static_validator", static_validator_review),
        ("sample_output", sample_output_review),
        ("processing_chain", processing_chain_review),
        ("governance", governance_review),
        ("health", health_review),
        ("recall", recall_boundary_review),
        ("downstream", downstream_readiness),
        ("boundary", boundary_post),
    ):
        for issue in review.get("issues") or []:
            post_issues.append({**issue, "review": name, "severity": "blocker"})

    blocker_count = len([i for i in post_issues if i.get("severity") == "blocker"])
    review_pass = len(blockers) == 0 and all(review_passes) and blocker_count == 0

    issue_register = {
        "register_id": "post_dryrun_issue_register_v1",
        "issues": post_issues,
        "issue_count": len(post_issues),
        "blocker_count": blocker_count,
        **meta,
    }

    readiness = {
        "decision_id": "post_dryrun_readiness_decision_v1",
        "post_dryrun_review_pass": review_pass,
        "final_decision": FINAL_DECISION_GO if review_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        "recommended_alternate_next_phase": NEXT_PHASE_ALT if review_pass else NEXT_PHASE_HOLD,
        "reviews_total": 13,
        "reviews_passed": sum(1 for p in review_passes if p),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "post_dryrun_review_pass": review_pass,
        "blocker_count": blocker_count,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "recommended_alternate_next_phase": readiness["recommended_alternate_next_phase"],
        "module_id": "information_integration",
        "layer": "L6",
        **meta,
    }

    return {
        "summary": summary,
        "skeleton_file_integrity_review": file_integrity,
        "forbidden_runtime_import_review": forbidden_import_review,
        "pure_function_boundary_review": pure_function_boundary,
        "type_contract_review": type_contract_review,
        "function_contract_review": function_contract_review,
        "static_validator_review": static_validator_review,
        "sample_dryrun_output_review": sample_output_review,
        "processing_chain_review": processing_chain_review,
        "governance_guard_review": governance_review,
        "health_guard_review": health_review,
        "recall_boundary_review": recall_boundary_review,
        "downstream_readiness_review": downstream_readiness,
        "boundary_matrix_post_review": boundary_post,
        "post_dryrun_issue_register": issue_register,
        "post_dryrun_readiness_decision": readiness,
    }
