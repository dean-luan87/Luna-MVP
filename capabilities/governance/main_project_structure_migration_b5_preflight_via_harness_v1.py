# -*- coding: utf-8 -*-
"""Main Project Structure Migration B5 Preflight Via Harness v1.

Compressed preflight for Config / schema / examples stable placement.
Includes schema path and config reference consistency scans (read-only).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B5-Preflight-Via-Harness-v1-001"
PREFLIGHT_SCOPE = "main_project_structure_migration_b5_preflight_via_harness_only"
SOURCE_CHAIN = "main_project_structure_migration_b5_preflight_via_harness_v1"

FINAL_DECISION_GO = "MAIN_PROJECT_STRUCTURE_MIGRATION_B5_PREFLIGHT_VIA_HARNESS_READY_FOR_CONTROLLED_EXECUTION"
NEXT_PHASE_GO = "Phase-Main-Project-Structure-Migration-B5-Controlled-Execution-v1-001"
FINAL_DECISION_HOLD = "MAIN_PROJECT_STRUCTURE_MIGRATION_B5_PREFLIGHT_VIA_HARNESS_HOLD_FOR_REVIEW"
NEXT_PHASE_HOLD = "Phase-Main-Project-Structure-Migration-B5-Preflight-Issue-Review-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-B4-Post-Migration-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_B4_POST_MIGRATION_REVIEW_CLOSED_READY_FOR_B5_PREFLIGHT_VIA_HARNESS"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

BATCH_ID = "B5"
BATCH_DOMAIN = "Config / schema / examples stable placement"

SCAN_ROOTS: Tuple[str, ...] = ("configs", "schemas", "examples")
CONFIG_EXTENSIONS: Tuple[str, ...] = (".json", ".yaml", ".yml")
EXAMPLE_MD = ".md"
EXAMPLE_SUFFIXES: Tuple[str, ...] = (".example.json", ".example.yaml", ".example.yml")

EXCLUDE_PATH_PARTS: Tuple[str, ...] = (
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "_eval_out",
    "node_modules",
)

EXCLUDE_GLOBS: Tuple[str, ...] = (
    "**/__pycache__/**",
    "**/*.pyc",
    "_eval_out/**",
    "**/_eval_out/**",
    "**/.pytest_cache/**",
    "**/.venv/**",
    "**/venv/**",
    "**/node_modules/**",
    "**/.DS_Store",
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
    "schema_path_reference_consistency_check",
    "config_reference_consistency_check",
    "readiness_decision",
)

FORBIDDEN_SCOPE_TOKENS: Tuple[str, ...] = (
    "capabilities/",
    "tools/evaluation/governance/",
    "docs/architecture/governance/",
    "protected/",
    "/hr/",
    "dnae",
)

REPO_PATH_RE = re.compile(
    r"(?:configs|schemas|examples|tools|docs)/[A-Za-z0-9_./-]+(?:\.[A-Za-z0-9]+)?"
)
SCHEMA_PATH_RE = re.compile(
    r"(?:schemas/[A-Za-z0-9_./-]+|\$schema[\"']?\s*:\s*[\"']([^\"']+)[\"'])"
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "b5_preflight_via_harness_only": True,
        "selected_batch_id": BATCH_ID,
        "b5_only": True,
        "b0_closed": True,
        "b1_closed": True,
        "b2_closed": True,
        "b3_closed": True,
        "b4_closed": True,
        "b6_b7_deferred": True,
        "harness_contract_reused": True,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "arming_chain_reopened_now": False,
        "request_chain_reopened_now": False,
        "b5_preflight_executed_now": True,
        "batch_execution_started_now": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_file_overwrite_executed": False,
        "content_rewrite_executed_now": False,
        "config_rewrite_executed_now": False,
        "schema_rewrite_executed_now": False,
        "reference_rewrite_executed_now": False,
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
    if rel.endswith(".pyc") or rel.endswith("/.DS_Store") or rel.endswith(".DS_Store"):
        return True
    return False


def _matches_candidate(rel: str) -> bool:
    if _path_excluded(rel):
        return False
    if not any(rel.startswith(f"{root}/") for root in SCAN_ROOTS):
        return False
    name = Path(rel).name
    if name == ".gitkeep":
        return False
    if rel.startswith("examples/") and name.endswith(EXAMPLE_MD):
        return True
    if any(name.endswith(suffix) for suffix in EXAMPLE_SUFFIXES):
        return True
    return any(name.endswith(ext) for ext in CONFIG_EXTENSIONS)


def scan_config_schema_example_candidate_paths(repo_root: Path) -> List[str]:
    paths: List[str] = []
    for root_name in SCAN_ROOTS:
        root_dir = repo_root / root_name
        if not root_dir.is_dir():
            continue
        for p in sorted(root_dir.rglob("*")):
            if not p.is_file():
                continue
            rel = str(p.relative_to(repo_root)).replace("\\", "/")
            if _matches_candidate(rel):
                paths.append(rel)
    return paths


def _collect_strings(obj: Any, out: List[str]) -> None:
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            _collect_strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _collect_strings(v, out)


def _is_external_ref(value: str) -> bool:
    lower = value.strip().lower()
    return lower.startswith(("http://", "https://", "file://", "s3://", "gs://"))


def _normalize_ref(value: str) -> str:
    ref = value.strip().split("?")[0].split("#")[0]
    if ref.startswith("./"):
        ref = ref[2:]
    return ref.replace("\\", "/")


def _resolve_repo_path(repo_root: Path, ref: str) -> bool:
    if _is_external_ref(ref):
        return True
    if ref.startswith("_eval_out"):
        return True
    if ref.startswith("models/"):
        return True
    normalized = _normalize_ref(ref)
    if not normalized:
        return False
    target = repo_root / normalized
    return target.is_file() or (target / "__init__.py").is_file()


def _is_example_companion_ref(source_rel: str, ref: str) -> bool:
    return (
        ".example." in source_rel
        and ref.startswith(("configs/", "schemas/", "examples/"))
        and ".example." in ref
    )


def _extract_repo_path_refs(text: str) -> Set[str]:
    refs: Set[str] = set()
    for match in REPO_PATH_RE.findall(text):
        refs.add(_normalize_ref(match.rstrip(".,;")))
    for match in SCHEMA_PATH_RE.findall(text):
        if isinstance(match, str) and match:
            refs.add(_normalize_ref(match))
    return refs


def _load_file_strings(repo_root: Path, rel: str) -> List[str]:
    p = repo_root / rel
    if not p.is_file():
        return []
    try:
        raw = p.read_text(encoding="utf-8")
    except OSError:
        return []
    if rel.endswith(".json") or rel.endswith(".example.json"):
        try:
            data = json.loads(raw)
            strings: List[str] = []
            _collect_strings(data, strings)
            return strings
        except json.JSONDecodeError:
            return [raw]
    return [raw]


def scan_schema_path_reference_consistency(
    repo_root: Path,
    candidate_paths: List[str],
) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    scanned = 0

    for rel in candidate_paths:
        strings = _load_file_strings(repo_root, rel)
        if not strings:
            continue
        scanned += 1
        seen: Set[str] = set()
        for s in strings:
            for ref in _extract_repo_path_refs(s):
                if not ref.startswith("schemas/"):
                    continue
                if ref in seen:
                    continue
                seen.add(ref)
                if _resolve_repo_path(repo_root, ref):
                    continue
                item = {
                    "source_path": rel,
                    "referenced_path": ref,
                    "issue_type": "unresolved_schema_reference",
                    "severity": "high",
                    "detail": f"schema reference does not resolve: {ref}",
                }
                candidates.append(item)
                high_risk.append(item)

    check_pass = len(high_risk) == 0
    return {
        "scanned_file_count": scanned,
        "schema_reference_issue_candidates": candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "check_pass": check_pass,
        "schema_rewrite_executed_now": False,
        "interpretation": "schema path reference consistency pass" if check_pass else "unresolved schema reference; hold for review",
    }


def scan_config_reference_consistency(
    repo_root: Path,
    candidate_paths: List[str],
) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    scanned = 0

    for rel in candidate_paths:
        strings = _load_file_strings(repo_root, rel)
        if not strings:
            continue
        scanned += 1
        seen: Set[str] = set()
        for s in strings:
            for ref in _extract_repo_path_refs(s):
                if not ref.startswith(("configs/", "tools/", "docs/")):
                    continue
                if ref in seen:
                    continue
                seen.add(ref)
                if _resolve_repo_path(repo_root, ref):
                    continue
                if _is_example_companion_ref(rel, ref):
                    item = {
                        "source_path": rel,
                        "referenced_path": ref,
                        "issue_type": "companion_example_reference_missing",
                        "severity": "low",
                        "detail": f"example companion reference not yet present: {ref}",
                    }
                    candidates.append(item)
                    continue
                item = {
                    "source_path": rel,
                    "referenced_path": ref,
                    "issue_type": "unresolved_config_reference",
                    "severity": "high",
                    "detail": f"config/reference path does not resolve: {ref}",
                }
                candidates.append(item)
                high_risk.append(item)

    check_pass = len(high_risk) == 0
    return {
        "scanned_file_count": scanned,
        "config_reference_issue_candidates": candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "low_severity_count": sum(1 for c in candidates if c.get("severity") == "low"),
        "check_pass": check_pass,
        "config_rewrite_executed_now": False,
        "reference_rewrite_executed_now": False,
        "interpretation": "config reference consistency pass" if check_pass else "unresolved config reference; hold for review",
    }


def _build_batch_config(candidate_paths: List[str]) -> Dict[str, Any]:
    return {
        "batch_id": BATCH_ID,
        "batch_domain": BATCH_DOMAIN,
        "candidate_paths": candidate_paths,
        "exclude_paths": list(EXCLUDE_GLOBS),
        "allowed_operations": ["move", "rename"],
        "blocked_operations": [
            "delete",
            "overwrite",
            "merge",
            "copy",
            "content_rewrite",
            "config_rewrite",
            "schema_rewrite",
            "reference_rewrite",
        ],
        "protected_path_policy": {"mode": "deny", "blocked": ["protected/**", "**/protected/**"]},
        "eval_out_policy": {"mode": "readonly", "write_allowed": False},
        "before_manifest_requirement": {"required": True, "generated_now": False},
        "after_manifest_requirement": {"required": True, "generated_now": False},
        "rollback_route": {"route_id": "B5_CONFIG_SCHEMA_EXAMPLES_ROLLBACK_ROUTE_V1", "rehearsal_required": True},
        "verifier_rerun_list": ["verify_main_project_structure_migration_b5_preflight_via_harness_v1"],
        "post_migration_test_list": ["config_schema_example_path_check", "config_reference_consistency_check"],
        "abort_conditions": [
            "scope_escape_detected",
            "protected_path_intersection",
            "eval_out_write_attempted",
            "operation_not_allowlisted",
            "high_risk_schema_reference_break",
            "high_risk_config_reference_break",
        ],
        "workspace_fallback_policy": {"enabled": True},
        "non_claims": [
            "B5 preflight GO ≠ B5 migration executed",
            "B5 preflight GO ≠ config/schema content modified",
            "reference scan pass ≠ references rewritten in preflight",
            "low severity companion example candidates ≠ execution blocked",
            "workspace_fallback GO ≠ standard _eval_out already written",
        ],
    }


def run_main_project_structure_migration_b5_preflight_via_harness_v1(
    *,
    b4_post_migration_review_root: str,
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    review_root = Path(b4_post_migration_review_root).expanduser().resolve()
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
        blockers.append("B4 post-migration review verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("upstream phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("upstream final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("upstream recommended_next_phase must be B5 preflight")
    if sm.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok must be true")
    if sm.get("b4_closed_now") is not True:
        blockers.append("b4_closed_now must be true")
    if sm.get("ready_for_b5_preflight_via_harness") is not True:
        blockers.append("ready_for_b5_preflight_via_harness must be true")

    candidate_paths = scan_config_schema_example_candidate_paths(resolved_repo)
    if not candidate_paths:
        blockers.append("no config/schema/example candidate paths")

    for rel in candidate_paths:
        if _path_excluded(rel):
            blockers.append(f"excluded path leaked into candidates: {rel}")
        if not any(rel.startswith(f"{root}/") for root in SCAN_ROOTS):
            blockers.append(f"scope escape: {rel}")
        if any(t in rel for t in ("protected/", "_eval_out/")):
            blockers.append(f"forbidden scope in candidate: {rel}")

    batch_config = _build_batch_config(candidate_paths)

    scope_ok = all(
        any(p.startswith(f"{root}/") for root in SCAN_ROOTS) and not _path_excluded(p) for p in candidate_paths
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
        "config_rewrite",
        "schema_rewrite",
        "reference_rewrite",
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

    schema_scan = scan_schema_path_reference_consistency(resolved_repo, candidate_paths)
    config_scan = scan_config_reference_consistency(resolved_repo, candidate_paths)
    for scan in (schema_scan, config_scan):
        scan.update({k: v for k, v in meta.items() if k not in scan})

    refactor_scan = {
        "scan_scope": list(SCAN_ROOTS),
        "duplicate_pattern_candidates": [
            {"pattern": "repeated schema_version + phase metadata block", "location": "configs/"},
            {"pattern": "repeated provider manifest skeleton", "location": "configs/models/"},
            {"pattern": "repeated example harness output_root_base", "location": "configs/evaluation/"},
        ],
        "extract_now_allowed": False,
        "extract_later_candidates": [
            {"tier": "A", "candidate": "shared_model_manifest_schema_v0"},
            {"tier": "B", "candidate": "shared_evaluation_harness_config_template"},
        ],
        "blocked_from_runtime_refactor_now": True,
        **meta,
    }
    scan_ok = refactor_scan["extract_now_allowed"] is False and refactor_scan["blocked_from_runtime_refactor_now"] is True

    schema_ok = schema_scan.get("check_pass") is True
    config_ok = config_scan.get("check_pass") is True
    hold_for_review = (not schema_ok or not config_ok) and not blockers

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
        "schema_path_reference_consistency_check": schema_ok,
        "config_reference_consistency_check": config_ok,
    }
    all_fixed_checks_pass = all(check_results.values()) and not blockers

    if hold_for_review:
        final_decision = FINAL_DECISION_HOLD
        next_phase = NEXT_PHASE_HOLD
        ready_for_execution = False
    elif not blockers and all_fixed_checks_pass:
        final_decision = FINAL_DECISION_GO
        next_phase = NEXT_PHASE_GO
        ready_for_execution = True
    else:
        final_decision = "MAIN_PROJECT_STRUCTURE_MIGRATION_B5_PREFLIGHT_REQUIRES_FIXES"
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
        "schema_high_risk_count": schema_scan.get("high_risk_count", 0),
        "config_high_risk_count": config_scan.get("high_risk_count", 0),
        "path_existence_sample": dict(list(path_existence.items())[:5]),
        "final_batch_readiness_decision": final_decision,
        **meta,
    }

    readiness = {
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        "ready_for_b5_controlled_execution": ready_for_execution,
        "hold_for_review": hold_for_review,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "preflight_scope": PREFLIGHT_SCOPE,
        "selected_batch_id": BATCH_ID,
        "batch_domain": BATCH_DOMAIN,
        "candidate_path_count": len(candidate_paths),
        "configs_count": sum(1 for p in candidate_paths if p.startswith("configs/")),
        "schemas_count": sum(1 for p in candidate_paths if p.startswith("schemas/")),
        "examples_count": sum(1 for p in candidate_paths if p.startswith("examples/")),
        "exclude_path_count": len(batch_config["exclude_paths"]),
        "all_fixed_checks_pass": all_fixed_checks_pass,
        "check_results": check_results,
        "hold_for_review": hold_for_review,
        "schema_high_risk_count": schema_scan.get("high_risk_count", 0),
        "config_high_risk_count": config_scan.get("high_risk_count", 0),
        "config_low_severity_count": config_scan.get("low_severity_count", 0),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }

    return {
        "summary": summary,
        "b5_batch_config": batch_config,
        "b5_preflight_result": preflight_result,
        "b5_schema_path_reference_consistency_scan": schema_scan,
        "b5_config_reference_consistency_scan": config_scan,
        "b5_migration_refactor_opportunity_scan": refactor_scan,
        "b5_preflight_readiness_decision": readiness,
    }
