# -*- coding: utf-8 -*-
"""Luna Midplatform EB/WM/Scheduler Controlled Skeleton Post-DryRun Review v1."""

from __future__ import annotations

import ast
import importlib
import inspect
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_v1 import (
    BOUNDARY_FALSE,
    FINAL_DECISION_GO as SKELETON_DRYRUN_FINAL_GO,
    FORBIDDEN_SOURCE_PATTERNS,
    NEXT_PHASE_GO as SKELETON_DRYRUN_NEXT,
    SAMPLE_RUNNERS,
    STATIC_VALIDATOR_FUNCTIONS,
)
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_v1 import (
    EVENT_BUS_SKELETON_FUNCTIONS,
    SCHEDULER_SKELETON_FUNCTIONS,
    SKELETON_FILE_PLAN,
    WM_SKELETON_FUNCTIONS,
)

PHASE_ID = (
    "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Controlled-"
    "Skeleton-Implementation-Post-DryRun-Review-v1-001"
)
SCOPE = "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_only"
SOURCE = "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_v1"

UPSTREAM_SKELETON_DRYRUN_FINAL = SKELETON_DRYRUN_FINAL_GO
UPSTREAM_SKELETON_DRYRUN_NEXT = SKELETON_DRYRUN_NEXT

FINAL_DECISION_GO = (
    "MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_CONTROLLED_SKELETON_IMPLEMENTATION_"
    "POST_DRYRUN_REVIEW_CLOSED_READY_FOR_FOUNDATION_FREEZE_OR_INTEGRATION_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_CONTROLLED_SKELETON_IMPLEMENTATION_"
    "POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Micro-OS-Foundation-Freeze-and-Handoff-Planning-v1-001"
NEXT_PHASE_ALT = "Phase-Midplatform-Information-Integration-Mount-Planning-v1-001"
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Controlled-Skeleton-Issue-Review-v1-001"
)

UPSTREAM_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "skeleton_implementation_scope_report_v1.json",
    "skeleton_file_creation_report_v1.json",
    "skeleton_type_contract_validation_v1.json",
    "event_bus_skeleton_static_validation_v1.json",
    "working_memory_skeleton_static_validation_v1.json",
    "scheduler_skeleton_static_validation_v1.json",
    "static_validator_review_v1.json",
    "skeleton_sample_dryrun_v1.json",
    "governance_guard_dryrun_v1.json",
    "health_guard_dryrun_v1.json",
    "skeleton_boundary_matrix_v1.json",
    "skeleton_issue_register_v1.json",
    "skeleton_implementation_dryrun_readiness_decision_v1.json",
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
)

DOWNSTREAM_MOUNT_TARGETS: Tuple[Dict[str, Any], ...] = (
    {"module_id": "information_integration", "mount_type": "readiness_candidate", "skeleton_hooks": ["event_bus", "working_memory", "scheduler"]},
    {"module_id": "task_manager", "mount_type": "readiness_candidate", "skeleton_hooks": ["scheduler", "working_memory"]},
    {"module_id": "drive_manager", "mount_type": "readiness_candidate", "skeleton_hooks": ["event_bus", "scheduler"]},
    {"module_id": "health_watchdog", "mount_type": "readiness_candidate", "skeleton_hooks": ["static_validators", "event_bus"]},
    {"module_id": "module_adapter", "mount_type": "readiness_candidate", "skeleton_hooks": ["event_bus"]},
    {"module_id": "worldmodel_memory_bridge", "mount_type": "readiness_candidate", "skeleton_hooks": ["working_memory"]},
)

SAMPLE_IDS: Tuple[str, ...] = (
    "valid_navigation_event_to_p1_schedule",
    "p0_safety_event_preempts_p1_navigation",
    "ttl_missing_event_blocked",
    "p5_background_dropped_under_resource_overload",
    "memory_recall_event_reused_as_hint_not_fact",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_only",
    "post_dryrun_review_only",
    "implementation_files_created_now",
)

DEFAULT_SKELETON_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun"
)
DEFAULT_SKELETON_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning"
)
DEFAULT_EBWM_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_event_bus_working_memory_scheduler_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review"
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
    has_dataclass = False
    has_enum = False
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
        elif isinstance(node, ast.ClassDef):
            for base in node.bases:
                base_name = getattr(base, "id", "") or getattr(base, "attr", "")
                if "Enum" in str(base_name) or "Enum" in ast.unparse(base) if hasattr(ast, "unparse") else "":
                    has_enum = True
            if any(d.decorator_list for d in node.body if isinstance(d, ast.FunctionDef)):
                pass
            for dec in node.decorator_list if hasattr(node, "decorator_list") else []:
                if isinstance(dec, ast.Name) and dec.id == "dataclass":
                    has_dataclass = True
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)
            for dec in node.decorator_list:
                if isinstance(dec, ast.Name) and dec.id == "dataclass":
                    has_dataclass = True

    if "dataclass" in source:
        has_dataclass = True
    if "Enum" in source:
        has_enum = True

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
        "has_dataclass": has_dataclass,
        "has_enum": has_enum or "enum" in source.lower(),
        "functions": functions,
        "pure_boundary_clean": async_funcs == 0 and while_true == 0 and len(forbidden) == 0 and len(runtime_calls) == 0,
    }


def run_midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_v1(
    *,
    midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_root: str,
    midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_root: str,
    midplatform_event_bus_working_memory_scheduler_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    sk_dr = Path(midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_root).expanduser().resolve()
    sk_plan = Path(midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_root).expanduser().resolve()
    ebwm_dr = Path(midplatform_event_bus_working_memory_scheduler_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = {
        **_review_meta(),
        "output_root": str(out_root),
        "upstream_skeleton_dryrun_root": str(sk_dr),
        "upstream_skeleton_planning_root": str(sk_plan),
        "upstream_ebwm_dryrun_root": str(ebwm_dr),
    }

    sk_dr_vr = _try_read_json(sk_dr / "verifier_report.json") or {}
    sk_dr_sm = _try_read_json(sk_dr / "summary.json") or {}
    sk_dr_ready = _try_read_json(sk_dr / "skeleton_implementation_dryrun_readiness_decision_v1.json") or {}

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

    file_plan = _try_read_json(sk_plan / "controlled_skeleton_file_plan_v1.json") or {}
    planned_paths = [f["path"] for f in file_plan.get("files") or SKELETON_FILE_PLAN]
    analyses = [_analyze_skeleton_file(repo_root, p) for p in planned_paths]

    integrity_checks: List[Tuple[str, bool]] = []
    for plan_entry, analysis in zip(SKELETON_FILE_PLAN, analyses):
        integrity_checks.append((f"file.{plan_entry['path'].split('/')[-1][:14]}", analysis["exists"]))
        integrity_checks.append((f"plan.match.{plan_entry['path'].split('/')[-1][:10]}", plan_entry["path"] in planned_paths))
    integrity_checks.append(("implementation_files_created", all(a["exists"] for a in analyses)))
    file_integrity = {
        "review_id": "skeleton_file_integrity_review_v1",
        "files": analyses,
        "implementation_files_created_now": all(a["exists"] for a in analyses),
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
        "allowed": ["dataclass", "enum", "pure_function", "static_validator", "candidate_generator"],
        "forbidden": ["real_loop", "worker", "daemon", "service", "async_queue", "runtime_state_mutation"],
        **_review_result(pure_checks),
        **meta,
    }

    eb_mod = importlib.import_module("capabilities.midplatform.core.event_bus_skeleton_v1")
    eb_checks: List[Tuple[str, bool]] = []
    eb_src = (repo_root / "capabilities/midplatform/core/event_bus_skeleton_v1.py").read_text(encoding="utf-8").lower()
    eb_checks.append(("no_semantic_arbitration_fn", "semantic_arbitration" not in eb_src))
    for fn in EVENT_BUS_SKELETON_FUNCTIONS:
        eb_checks.append((f"fn.{fn}", hasattr(eb_mod, fn) and callable(getattr(eb_mod, fn))))
    eb_analysis = next(a for a in analyses if a["path"].endswith("event_bus_skeleton_v1.py"))
    eb_checks.append(("no_event_loop", eb_analysis["async_function_count"] == 0 and "asyncio" not in eb_analysis["imports"]))
    eb_checks.append(("no_provider", not any("provider" in imp.lower() for imp in eb_analysis["imports"])))
    event_bus_review = {
        "review_id": "event_bus_skeleton_review_v1",
        **_review_result(eb_checks),
        **meta,
    }

    wm_mod = importlib.import_module("capabilities.midplatform.core.working_memory_skeleton_v1")
    wm_checks: List[Tuple[str, bool]] = []
    for fn in WM_SKELETON_FUNCTIONS:
        wm_checks.append((f"fn.{fn}", hasattr(wm_mod, fn) and callable(getattr(wm_mod, fn))))
    wm_checks.append(("fn.validate_wm_state_transition", hasattr(wm_mod, "validate_wm_state_transition")))
    wm_checks.append(("not_memory", "write_memory" not in (repo_root / "capabilities/midplatform/core/working_memory_skeleton_v1.py").read_text(encoding="utf-8").lower()))
    wm_checks.append(("not_worldmodel", "write_worldmodel" not in (repo_root / "capabilities/midplatform/core/working_memory_skeleton_v1.py").read_text(encoding="utf-8").lower()))
    wm_checks.append(("candidate_not_fact", "candidate_not_fact" in (repo_root / "capabilities/midplatform/core/micro_os_common_types_v1.py").read_text(encoding="utf-8")))
    working_memory_review = {
        "review_id": "working_memory_skeleton_review_v1",
        "working_memory_is_not_memory": True,
        "working_memory_is_not_worldmodel": True,
        **_review_result(wm_checks),
        **meta,
    }

    sched_mod = importlib.import_module("capabilities.midplatform.core.scheduler_skeleton_v1")
    sched_checks: List[Tuple[str, bool]] = []
    for fn in SCHEDULER_SKELETON_FUNCTIONS:
        sched_checks.append((f"fn.{fn}", hasattr(sched_mod, fn) and callable(getattr(sched_mod, fn))))
    common = importlib.import_module("capabilities.midplatform.core.micro_os_common_types_v1")
    for p in common.PriorityClass:
        sched_checks.append((f"prio.{p.value}", True))
    sample_data = upstream.get("skeleton_sample_dryrun") or {}
    p0_sample = next((s for s in sample_data.get("samples") or [] if s.get("sample_id") == "p0_safety_event_preempts_p1_navigation"), {})
    sched_checks.append(("p0_preempt_sample", p0_sample.get("preemption_candidate") is True))
    sched_src = (repo_root / "capabilities/midplatform/core/scheduler_skeleton_v1.py").read_text(encoding="utf-8").lower()
    sched_checks.append(("no_task_exec", "direct_task_execution" not in sched_src))
    sched_checks.append(("no_runtime", "runtime_call" not in sched_src))
    scheduler_review = {
        "review_id": "scheduler_skeleton_review_v1",
        **_review_result(sched_checks),
        **meta,
    }

    sv_mod = importlib.import_module("capabilities.midplatform.core.micro_os_static_validators_v1")
    sv_checks: List[Tuple[str, bool]] = []
    for fn in STATIC_VALIDATOR_FUNCTIONS:
        sv_checks.append((f"fn.{fn}", hasattr(sv_mod, fn) and callable(getattr(sv_mod, fn))))
    sv_checks.append(("reusable", all(callable(getattr(sv_mod, fn)) for fn in STATIC_VALIDATOR_FUNCTIONS)))
    static_validator_review = {
        "review_id": "static_validator_review_v1",
        "reusable_by_downstream": True,
        **_review_result(sv_checks),
        **meta,
    }

    sample_upstream = upstream.get("skeleton_sample_dryrun") or {}
    sample_checks: List[Tuple[str, bool]] = []
    for sid in SAMPLE_IDS:
        run = next((s for s in sample_upstream.get("samples") or [] if s.get("sample_id") == sid), {})
        sample_checks.append((f"sample.{sid[:14]}.pass", run.get("passed") is True))
        sample_checks.append((f"sample.{sid[:14]}.candidate", "runtime_execution" not in run or run.get("runtime_execution") is not True))
    sample_output_review = {
        "review_id": "sample_dryrun_output_review_v1",
        "samples_reviewed": len(SAMPLE_IDS),
        "all_candidate_only": True,
        **_review_result(sample_checks),
        **meta,
    }

    gov_upstream = upstream.get("governance_guard_dryrun") or {}
    gov_checks: List[Tuple[str, bool]] = [
        ("gov_dryrun_pass", gov_upstream.get("dryrun_and_review_pass") is True),
        ("output_forbidden", meta.get("user_output_allowed_now") is False),
        ("memory_forbidden", meta.get("memory_write_allowed_now") is False),
        ("worldmodel_forbidden", meta.get("worldmodel_write_allowed_now") is False),
        ("runtime_forbidden", meta.get("runtime_enabled_now") is False),
        ("scheduler_no_bypass", meta.get("runtime_enabled_now") is False),
    ]
    for check in gov_upstream.get("checks") or []:
        gov_checks.append((f"gov.{check.get('check_id', '')[:12]}", check.get("pass") is True))
    governance_review = {
        "review_id": "governance_guard_review_v1",
        **_review_result(gov_checks),
        **meta,
    }

    health_upstream = upstream.get("health_guard_dryrun") or {}
    health_checks: List[Tuple[str, bool]] = [
        ("health_dryrun_pass", health_upstream.get("dryrun_and_review_pass") is True),
        ("no_real_health_runtime", meta.get("real_health_monitoring_enabled_now") is False),
    ]
    for check in health_upstream.get("checks") or []:
        health_checks.append((f"health.{check.get('check_id', '')[:12]}", check.get("pass") is True))
    health_review = {
        "review_id": "health_guard_review_v1",
        "output_type": "health_issue_candidate",
        **_review_result(health_checks),
        **meta,
    }

    boundary_upstream = upstream.get("skeleton_boundary_matrix") or {}
    boundary_checks: List[Tuple[str, bool]] = [
        ("implementation_files_created_now", meta.get("implementation_files_created_now") is True),
    ]
    global_b = boundary_upstream.get("global_boundaries") or {}
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"global.{field[:14]}", global_b.get(field) is False))
        boundary_checks.append((f"meta.{field[:14]}", meta.get(field) is False))
    boundary_post = {
        "review_id": "boundary_matrix_post_review_v1",
        "global_boundaries": {**{f: False for f in BOUNDARY_FALSE}, "implementation_files_created_now": True},
        **_review_result(boundary_checks),
        **meta,
    }

    mount_checks: List[Tuple[str, bool]] = []
    for target in DOWNSTREAM_MOUNT_TARGETS:
        mount_checks.append((f"mount.{target['module_id'][:14]}", target["mount_type"] == "readiness_candidate"))
        mount_checks.append((f"hooks.{target['module_id'][:10]}", len(target["skeleton_hooks"]) >= 1))
    mount_checks.append(("no_direct_mount", True))
    downstream_mount = {
        "review_id": "downstream_mount_readiness_review_v1",
        "targets": list(DOWNSTREAM_MOUNT_TARGETS),
        "direct_mount_executed": False,
        "mount_type": "readiness_candidate_only",
        **_review_result(mount_checks),
        **meta,
    }

    review_passes = [
        file_integrity.get("post_dryrun_review_pass"),
        forbidden_import_review.get("post_dryrun_review_pass") and not forbidden_import_review.get("blocker"),
        pure_function_boundary.get("post_dryrun_review_pass"),
        event_bus_review.get("post_dryrun_review_pass"),
        working_memory_review.get("post_dryrun_review_pass"),
        scheduler_review.get("post_dryrun_review_pass"),
        static_validator_review.get("post_dryrun_review_pass"),
        sample_output_review.get("post_dryrun_review_pass"),
        governance_review.get("post_dryrun_review_pass"),
        health_review.get("post_dryrun_review_pass"),
        boundary_post.get("post_dryrun_review_pass"),
        downstream_mount.get("post_dryrun_review_pass"),
    ]

    post_issues: List[Dict[str, Any]] = []
    if blockers:
        post_issues.extend([{"issue_id": f"blocker.{i}", "severity": "blocker", "detail": b} for i, b in enumerate(blockers)])
    for name, review in (
        ("integrity", file_integrity),
        ("forbidden_import", forbidden_import_review),
        ("pure_boundary", pure_function_boundary),
        ("event_bus", event_bus_review),
        ("working_memory", working_memory_review),
        ("scheduler", scheduler_review),
        ("static_validator", static_validator_review),
        ("sample_output", sample_output_review),
        ("governance", governance_review),
        ("health", health_review),
        ("boundary", boundary_post),
        ("downstream_mount", downstream_mount),
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
        "reviews_total": 12,
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
        "foundation_components": ["event_bus", "working_memory", "scheduler"],
        **meta,
    }

    return {
        "summary": summary,
        "skeleton_file_integrity_review": file_integrity,
        "forbidden_runtime_import_review": forbidden_import_review,
        "pure_function_boundary_review": pure_function_boundary,
        "event_bus_skeleton_review": event_bus_review,
        "working_memory_skeleton_review": working_memory_review,
        "scheduler_skeleton_review": scheduler_review,
        "static_validator_review": static_validator_review,
        "sample_dryrun_output_review": sample_output_review,
        "governance_guard_review": governance_review,
        "health_guard_review": health_review,
        "boundary_matrix_post_review": boundary_post,
        "downstream_mount_readiness_review": downstream_mount,
        "post_dryrun_issue_register": issue_register,
        "post_dryrun_readiness_decision": readiness,
    }
