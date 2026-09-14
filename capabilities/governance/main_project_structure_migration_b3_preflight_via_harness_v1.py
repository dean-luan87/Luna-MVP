# -*- coding: utf-8 -*-
"""Main Project Structure Migration B3 Preflight Via Harness v1.

Compressed preflight for Capability modules stable placement.
Includes import path and module naming consistency scans (read-only).
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B3-Preflight-Via-Harness-v1-001"
PREFLIGHT_SCOPE = "main_project_structure_migration_b3_preflight_via_harness_only"
SOURCE_CHAIN = "main_project_structure_migration_b3_preflight_via_harness_v1"

FINAL_DECISION_GO = "MAIN_PROJECT_STRUCTURE_MIGRATION_B3_PREFLIGHT_VIA_HARNESS_READY_FOR_CONTROLLED_EXECUTION"
NEXT_PHASE_GO = "Phase-Main-Project-Structure-Migration-B3-Controlled-Execution-v1-001"
FINAL_DECISION_HOLD = "MAIN_PROJECT_STRUCTURE_MIGRATION_B3_PREFLIGHT_VIA_HARNESS_HOLD_FOR_REVIEW"
NEXT_PHASE_HOLD = "Phase-Main-Project-Structure-Migration-B3-Preflight-Issue-Review-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-B2-Post-Migration-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_B2_POST_MIGRATION_REVIEW_CLOSED_READY_FOR_B3_PREFLIGHT_VIA_HARNESS"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

BATCH_ID = "B3"
BATCH_DOMAIN = "Capability modules stable placement"
CAPABILITIES_ROOT = "capabilities"

EXCLUDE_PATH_PARTS: Tuple[str, ...] = (
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    ".venv",
    "venv",
    "_eval_out",
)

EXCLUDE_GLOBS: Tuple[str, ...] = (
    "**/__pycache__/**",
    "**/*.pyc",
    "_eval_out/**",
    "**/_eval_out/**",
    "**/.pytest_cache/**",
    "**/node_modules/**",
    "**/.venv/**",
    "**/venv/**",
)

REQUIRED_FIXED_CHECKS: Tuple[str, ...] = (
    "scope_check",
    "domain_isolation_check",
    "protected_guard_check",
    "eval_out_readonly_check",
    "file_operation_boundary_check",
    "manifest_requirement_check",
    "rollback_requirement_check",
    "verifier_rerun_requirement_check",
    "post_migration_test_requirement_check",
    "abort_condition_check",
    "workspace_fallback_check",
    "non_claims_check",
    "migration_refactor_opportunity_scan_check",
    "python_import_path_consistency_check",
    "capability_module_naming_consistency_check",
    "readiness_decision",
)

FORBIDDEN_SCOPE_TOKENS: Tuple[str, ...] = (
    "docs/architecture/",
    "tools/",
    "configs/",
    "scripts/",
    "tests/",
    "_eval_out",
    "protected/",
    "/hr/",
    "dnae",
)

VERSION_SUFFIX_RE = re.compile(r"_v\d+\.py$")


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "b3_preflight_via_harness_only": True,
        "selected_batch_id": BATCH_ID,
        "b3_only": True,
        "b0_closed": True,
        "b1_closed": True,
        "b2_closed": True,
        "b4_b7_deferred": True,
        "harness_contract_reused": True,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "arming_chain_reopened_now": False,
        "request_chain_reopened_now": False,
        "b3_preflight_executed_now": True,
        "batch_execution_started_now": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_file_overwrite_executed": False,
        "content_rewrite_executed_now": False,
        "import_rewrite_executed_now": False,
        "module_rename_executed_now": False,
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "runtime_refactor_executed_now": False,
        "old_phase_deleted_now": False,
        "old_phase_deprecated_now": False,
        "verifier_rerun_executed_now": False,
        "rollback_rehearsal_executed_now": False,
        "post_migration_tests_executed_now": False,
        "file_operation_executed_now": False,
        "real_migration_execution_allowed": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _is_workspace_fallback(root: Optional[Path]) -> bool:
    return bool(root) and "Luna-Workspace-Min" in str(root)


def _path_excluded(rel: str) -> bool:
    parts = rel.replace("\\", "/").split("/")
    if any(part in EXCLUDE_PATH_PARTS for part in parts):
        return True
    return rel.endswith(".pyc")


def scan_capability_candidate_paths(repo_root: Path) -> List[str]:
    cap_dir = repo_root / CAPABILITIES_ROOT
    if not cap_dir.is_dir():
        return []
    paths: List[str] = []
    for p in sorted(cap_dir.rglob("*.py")):
        rel = str(p.relative_to(repo_root)).replace("\\", "/")
        if _path_excluded(rel):
            continue
        paths.append(rel)
    return paths


def _module_to_rel_path(repo_root: Path, module: str) -> Optional[str]:
    parts = module.split(".")
    base = repo_root.joinpath(*parts)
    py_file = base.with_suffix(".py")
    if py_file.is_file():
        return str(py_file.relative_to(repo_root)).replace("\\", "/")
    init_file = base / "__init__.py"
    if init_file.is_file():
        return str(init_file.relative_to(repo_root)).replace("\\", "/")
    return None


def _collect_capabilities_imports(tree: ast.AST) -> List[str]:
    modules: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                continue
            if node.module and node.module.startswith("capabilities."):
                modules.append(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("capabilities."):
                    modules.append(alias.name)
    return modules


def _import_resolves(repo_root: Path, module: str) -> bool:
    return _module_to_rel_path(repo_root, module) is not None


def scan_import_path_consistency(repo_root: Path, candidate_paths: List[str]) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    scanned = 0

    for rel in candidate_paths:
        p = repo_root / rel
        if not p.is_file():
            continue
        scanned += 1
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            item = {
                "path": rel,
                "issue_type": "parse_error",
                "severity": "high",
                "detail": str(exc),
            }
            candidates.append(item)
            high_risk.append(item)
            continue

        for mod in _collect_capabilities_imports(tree):
            if not _import_resolves(repo_root, mod):
                item = {
                    "path": rel,
                    "issue_type": "unresolved_capabilities_import",
                    "import_module": mod,
                    "severity": "high",
                    "detail": f"capabilities import does not resolve: {mod}",
                }
                candidates.append(item)
                high_risk.append(item)

    check_pass = len(high_risk) == 0
    return {
        "scan_scope": candidate_paths[:5],
        "scanned_file_count": scanned,
        "import_path_issue_candidates": candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "check_pass": check_pass,
        "import_rewrite_executed_now": False,
        "module_move_executed_now": False,
        "module_rename_executed_now": False,
        "interpretation": "import path consistency pass" if check_pass else "high risk import break detected; hold for review",
    }


def _extract_phase_id(src: str) -> Optional[str]:
    m = re.search(r'PHASE_ID\s*=\s*["\']([^"\']+)["\']', src)
    return m.group(1) if m else None


def _stem_to_phase_token(stem: str) -> str:
    return stem.replace("_", "-").upper()


def scan_capability_module_naming_consistency(repo_root: Path, candidate_paths: List[str]) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    scanned = 0

    for rel in candidate_paths:
        p = repo_root / rel
        if not p.is_file():
            continue
        name = p.name
        if name == "__init__.py":
            continue
        scanned += 1
        stem = p.stem
        is_governance = "/governance/" in rel or rel.startswith("capabilities/governance/")

        if not VERSION_SUFFIX_RE.search(name):
            item = {
                "path": rel,
                "issue_type": "missing_version_suffix",
                "severity": "high" if is_governance else "low",
                "detail": "capability file lacks _vN.py version suffix",
            }
            candidates.append(item)
            if is_governance:
                high_risk.append(item)

        if is_governance and stem.startswith("main_project_structure_migration_"):
            run_path = repo_root / "tools/evaluation/governance" / f"run_{stem}.py"
            verify_path = repo_root / "tools/evaluation/governance" / f"verify_{stem}.py"
            if not run_path.is_file():
                item = {
                    "path": rel,
                    "issue_type": "missing_runner_reference",
                    "severity": "high",
                    "expected_runner": str(run_path.relative_to(repo_root)).replace("\\", "/"),
                    "detail": "governance capability missing matching run script",
                }
                candidates.append(item)
                high_risk.append(item)
            if not verify_path.is_file():
                item = {
                    "path": rel,
                    "issue_type": "missing_verifier_reference",
                    "severity": "high",
                    "expected_verifier": str(verify_path.relative_to(repo_root)).replace("\\", "/"),
                    "detail": "governance capability missing matching verify script",
                }
                candidates.append(item)
                high_risk.append(item)

            try:
                src = p.read_text(encoding="utf-8")
                phase_id = _extract_phase_id(src)
                if phase_id:
                    token = _stem_to_phase_token(stem.replace("main_project_structure_migration_", ""))
                    if token not in phase_id.upper().replace("_", "-"):
                        item = {
                            "path": rel,
                            "issue_type": "phase_id_module_mismatch",
                            "severity": "high",
                            "phase_id": phase_id,
                            "module_stem": stem,
                            "detail": "PHASE_ID does not align with module stem",
                        }
                        candidates.append(item)
                        high_risk.append(item)
            except OSError:
                pass

    check_pass = len(high_risk) == 0
    return {
        "scan_scope": candidate_paths[:5],
        "scanned_file_count": scanned,
        "naming_issue_candidates": candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "low_severity_count": sum(1 for c in candidates if c.get("severity") == "low"),
        "check_pass": check_pass,
        "module_rename_executed_now": False,
        "content_rewrite_executed_now": False,
        "interpretation": "capability module naming consistency pass" if check_pass else "high risk naming inconsistency detected; hold for review",
    }


def _build_batch_config(candidate_paths: List[str]) -> Dict[str, Any]:
    return {
        "batch_id": BATCH_ID,
        "batch_domain": BATCH_DOMAIN,
        "candidate_paths": candidate_paths,
        "exclude_paths": list(EXCLUDE_GLOBS),
        "allowed_operations": ["move", "rename"],
        "blocked_operations": ["delete", "overwrite", "merge", "copy", "content_rewrite"],
        "protected_path_policy": {"mode": "deny", "blocked": ["protected/**", "**/protected/**"]},
        "eval_out_policy": {"mode": "readonly", "write_allowed": False},
        "before_manifest_requirement": {"required": True, "generated_now": False},
        "after_manifest_requirement": {"required": True, "generated_now": False},
        "rollback_route": {"route_id": "B3_CAPABILITY_MODULES_ROLLBACK_ROUTE_V1", "rehearsal_required": True},
        "verifier_rerun_list": ["verify_main_project_structure_migration_b3_preflight_via_harness_v1"],
        "post_migration_test_list": ["capability_module_path_check", "import_path_consistency_check"],
        "abort_conditions": [
            "scope_escape_detected",
            "protected_path_intersection",
            "eval_out_write_attempted",
            "operation_not_allowlisted",
            "high_risk_import_break",
            "high_risk_naming_inconsistency",
        ],
        "workspace_fallback_policy": {"enabled": True},
        "non_claims": [
            "B3 preflight GO ≠ B3 migration executed",
            "B3 preflight GO ≠ import rewrite executed",
            "B3 preflight GO ≠ module rename executed",
            "import/naming scan pass ≠ code modified in preflight",
            "low severity naming candidates ≠ execution blocked",
            "workspace_fallback GO ≠ standard _eval_out already written",
        ],
    }


def run_main_project_structure_migration_b3_preflight_via_harness_v1(
    *,
    b2_post_migration_review_root: str,
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    review_root = Path(b2_post_migration_review_root).expanduser().resolve()
    resolved_repo = Path(repo_root).expanduser().resolve() if repo_root else Path(__file__).resolve().parents[2]

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(review_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
    }

    sm = _try_read_json(review_root / "summary.json") or {}
    vr = _try_read_json(review_root / "verifier_report.json") or {}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("B2 post-migration review verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("upstream phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("upstream final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("upstream recommended_next_phase must be B3 preflight")
    if sm.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok must be true")
    if sm.get("b2_closed_now") is not True:
        blockers.append("b2_closed_now must be true")
    if sm.get("ready_for_b3_preflight_via_harness") is not True:
        blockers.append("ready_for_b3_preflight_via_harness must be true")

    candidate_paths = scan_capability_candidate_paths(resolved_repo)
    if not candidate_paths:
        blockers.append("no capability candidate paths after exclusions")

    for rel in candidate_paths:
        if _path_excluded(rel):
            blockers.append(f"excluded path leaked into candidates: {rel}")
        if not rel.startswith(f"{CAPABILITIES_ROOT}/") or not rel.endswith(".py"):
            blockers.append(f"scope escape: {rel}")
        if any(t in rel.lower() for t in FORBIDDEN_SCOPE_TOKENS if t != "tools/"):
            if any(t in rel for t in ("docs/architecture/", "_eval_out", "protected/")):
                blockers.append(f"forbidden scope token in candidate: {rel}")

    batch_config = _build_batch_config(candidate_paths)

    scope_ok = all(
        p.startswith(f"{CAPABILITIES_ROOT}/") and p.endswith(".py") and not _path_excluded(p)
        for p in candidate_paths
    )
    domain_ok = batch_config["batch_id"] == BATCH_ID and batch_config["batch_domain"] == BATCH_DOMAIN
    protected_ok = batch_config["protected_path_policy"].get("mode") == "deny"
    eval_out_ok = batch_config["eval_out_policy"].get("mode") == "readonly"
    fileop_ok = set(batch_config["allowed_operations"]) == {"move", "rename"} and {
        "delete",
        "overwrite",
        "merge",
        "copy",
        "content_rewrite",
    }.issubset(set(batch_config["blocked_operations"]))
    manifest_ok = batch_config["before_manifest_requirement"]["required"] and batch_config["after_manifest_requirement"]["required"]
    rollback_ok = bool(batch_config["rollback_route"].get("route_id"))
    rerun_ok = bool(batch_config["verifier_rerun_list"])
    post_ok = bool(batch_config["post_migration_test_list"])
    abort_ok = bool(batch_config["abort_conditions"])
    ws_ok = batch_config["workspace_fallback_policy"].get("enabled") is True
    non_claims_ok = len(batch_config["non_claims"]) >= 3

    path_existence = {p: (resolved_repo / p).is_file() for p in candidate_paths}
    exists_ok = all(path_existence.values())
    if not exists_ok:
        blockers.append("some candidate paths missing on disk")

    import_scan = scan_import_path_consistency(resolved_repo, candidate_paths)
    naming_scan = scan_capability_module_naming_consistency(resolved_repo, candidate_paths)
    import_scan.update({k: v for k, v in meta.items() if k not in import_scan})
    naming_scan.update({k: v for k, v in meta.items() if k not in naming_scan})

    refactor_scan = {
        "scan_scope": [CAPABILITIES_ROOT],
        "duplicate_pattern_candidates": [
            {"pattern": "phase boilerplate / boundary guard / summary builder", "location": CAPABILITIES_ROOT},
            {"pattern": "verifier meta inflation loop", "location": "tools/evaluation/governance"},
            {"pattern": "repeated _boundary_meta / _not_fact helpers", "location": CAPABILITIES_ROOT},
        ],
        "extract_now_allowed": False,
        "extract_later_candidates": [
            {"tier": "A", "candidate": "shared_preflight_boundary_meta_helper"},
            {"tier": "B", "candidate": "shared_manifest_fingerprint_helper"},
        ],
        "blocked_from_runtime_refactor_now": True,
        **meta,
    }
    scan_ok = refactor_scan["extract_now_allowed"] is False and refactor_scan["blocked_from_runtime_refactor_now"] is True

    import_ok = import_scan.get("check_pass") is True
    naming_ok = naming_scan.get("check_pass") is True
    hold_for_review = (not import_ok or not naming_ok) and not blockers

    check_results = {
        "scope_check": scope_ok and exists_ok,
        "domain_isolation_check": domain_ok,
        "protected_guard_check": protected_ok,
        "eval_out_readonly_check": eval_out_ok,
        "file_operation_boundary_check": fileop_ok,
        "manifest_requirement_check": manifest_ok,
        "rollback_requirement_check": rollback_ok,
        "verifier_rerun_requirement_check": rerun_ok,
        "post_migration_test_requirement_check": post_ok,
        "abort_condition_check": abort_ok,
        "workspace_fallback_check": ws_ok,
        "non_claims_check": non_claims_ok,
        "migration_refactor_opportunity_scan_check": scan_ok,
        "python_import_path_consistency_check": import_ok,
        "capability_module_naming_consistency_check": naming_ok,
    }
    all_fixed_checks_pass = all(check_results.values()) and not blockers
    if not all_fixed_checks_pass and not blockers and hold_for_review:
        pass  # hold is valid outcome, not a blocker for preflight completion

    if hold_for_review:
        final_decision = FINAL_DECISION_HOLD
        next_phase = NEXT_PHASE_HOLD
        ready_for_execution = False
    elif not blockers and all_fixed_checks_pass:
        final_decision = FINAL_DECISION_GO
        next_phase = NEXT_PHASE_GO
        ready_for_execution = True
    else:
        final_decision = "MAIN_PROJECT_STRUCTURE_MIGRATION_B3_PREFLIGHT_REQUIRES_FIXES"
        next_phase = PHASE_ID
        ready_for_execution = False

    boundary_ok = not blockers and (all_fixed_checks_pass or hold_for_review)

    preflight_result = {
        "batch_id": BATCH_ID,
        "batch_config": batch_config,
        "check_results": check_results,
        "all_checks_pass": all_fixed_checks_pass,
        "hold_for_review": hold_for_review,
        "candidate_path_count": len(candidate_paths),
        "import_high_risk_count": import_scan.get("high_risk_count", 0),
        "naming_high_risk_count": naming_scan.get("high_risk_count", 0),
        "path_existence_sample": dict(list(path_existence.items())[:5]),
        "final_batch_readiness_decision": final_decision,
        **meta,
    }

    readiness = {
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        "ready_for_b3_controlled_execution": ready_for_execution,
        "hold_for_review": hold_for_review,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "preflight_scope": PREFLIGHT_SCOPE,
        "selected_batch_id": BATCH_ID,
        "batch_domain": BATCH_DOMAIN,
        "candidate_path_count": len(candidate_paths),
        "exclude_path_count": len(batch_config["exclude_paths"]),
        "all_fixed_checks_pass": all_fixed_checks_pass,
        "check_results": check_results,
        "hold_for_review": hold_for_review,
        "import_high_risk_count": import_scan.get("high_risk_count", 0),
        "naming_high_risk_count": naming_scan.get("high_risk_count", 0),
        "naming_low_severity_count": naming_scan.get("low_severity_count", 0),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }

    return {
        "summary": summary,
        "b3_batch_config": batch_config,
        "b3_preflight_result": preflight_result,
        "b3_import_path_consistency_scan": import_scan,
        "b3_capability_module_naming_consistency_scan": naming_scan,
        "b3_migration_refactor_opportunity_scan": refactor_scan,
        "b3_preflight_readiness_decision": readiness,
    }
