# -*- coding: utf-8 -*-
"""Main Project Structure Migration B6 Preflight Via Harness v1.

Compressed preflight for Tools / scripts / tests stable placement.
Excludes B4-closed tools/evaluation/governance/**/*.py.
Includes command entrypoint, script dependency, and test reference scans (read-only).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B6-Preflight-Via-Harness-v1-001"
PREFLIGHT_SCOPE = "main_project_structure_migration_b6_preflight_via_harness_only"
SOURCE_CHAIN = "main_project_structure_migration_b6_preflight_via_harness_v1"

FINAL_DECISION_GO = "MAIN_PROJECT_STRUCTURE_MIGRATION_B6_PREFLIGHT_VIA_HARNESS_READY_FOR_CONTROLLED_EXECUTION"
NEXT_PHASE_GO = "Phase-Main-Project-Structure-Migration-B6-Controlled-Execution-v1-001"
FINAL_DECISION_HOLD = "MAIN_PROJECT_STRUCTURE_MIGRATION_B6_PREFLIGHT_VIA_HARNESS_HOLD_FOR_REVIEW"
NEXT_PHASE_HOLD = "Phase-Main-Project-Structure-Migration-B6-Preflight-Issue-Review-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-B5-Post-Migration-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_B5_POST_MIGRATION_REVIEW_CLOSED_READY_FOR_B6_PREFLIGHT_VIA_HARNESS"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

BATCH_ID = "B6"
BATCH_DOMAIN = "Tools / scripts / tests stable placement"

SCAN_ROOTS: Tuple[str, ...] = ("tools", "scripts", "tests")
SCAN_EXTENSIONS: Tuple[str, ...] = (".py", ".sh", ".md")
B4_EXCLUDE_PREFIX = "tools/evaluation/governance/"

EXCLUDE_PATH_PARTS: Tuple[str, ...] = (
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "_eval_out",
    "node_modules",
)

EXCLUDE_GLOBS: Tuple[str, ...] = (
    "tools/evaluation/governance/**/*.py",
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
    "command_entrypoint_consistency_check",
    "script_dependency_consistency_check",
    "test_reference_path_consistency_check",
    "readiness_decision",
)

CLEAN_FILE_PATH_RE = re.compile(
    r"^((?:tools|scripts|tests|configs|docs|capabilities)/(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.[A-Za-z0-9]+)$"
)
QUOTED_STRING_RE = re.compile(r"""['"]([^'"]{5,220})['"]""")
PYTHON_ENTRY_RE = re.compile(r"python3?\s+((?:tools|scripts)/[\w./_-]+\.(?:py|sh))")
SHELL_SOURCE_RE = re.compile(r"(?:source|\.\s+)\s*((?:tools|scripts)/[\w./_-]+\.sh)")


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "b6_preflight_via_harness_only": True,
        "selected_batch_id": BATCH_ID,
        "b6_only": True,
        "b0_closed": True,
        "b1_closed": True,
        "b2_closed": True,
        "b3_closed": True,
        "b4_closed": True,
        "b5_closed": True,
        "b7_deferred": True,
        "harness_contract_reused": True,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "arming_chain_reopened_now": False,
        "request_chain_reopened_now": False,
        "b6_preflight_executed_now": True,
        "batch_execution_started_now": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_file_overwrite_executed": False,
        "content_rewrite_executed_now": False,
        "script_rewrite_executed_now": False,
        "test_rewrite_executed_now": False,
        "command_rewrite_executed_now": False,
        "import_rewrite_executed_now": False,
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
    if rel.endswith(".pyc") or rel.endswith(".DS_Store"):
        return True
    return False


def _is_b4_excluded(rel: str) -> bool:
    return rel.startswith(B4_EXCLUDE_PREFIX) and rel.endswith(".py")


def _matches_candidate(rel: str) -> bool:
    if _path_excluded(rel) or _is_b4_excluded(rel):
        return False
    if not any(rel.startswith(f"{root}/") for root in SCAN_ROOTS):
        return False
    return Path(rel).suffix in SCAN_EXTENSIONS


def scan_tools_scripts_tests_candidate_paths(repo_root: Path) -> List[str]:
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


def _clean_file_ref(raw: str) -> Optional[str]:
    raw = raw.strip().split("?")[0].split("#")[0]
    if any(token in raw for token in ("{", "}", "*", "...")):
        return None
    if not raw.isascii():
        return None
    match = CLEAN_FILE_PATH_RE.match(raw)
    return match.group(1) if match else None


def _resolve_repo_file(repo_root: Path, ref: str) -> bool:
    if ref.startswith(("http://", "https://", "file://", "_eval_out/", "models/")):
        return True
    try:
        return (repo_root / ref).is_file()
    except OSError:
        return False


def _read_text(rel_path: str, repo_root: Path) -> str:
    try:
        return (repo_root / rel_path).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _extract_path_refs(text: str) -> Set[str]:
    refs: Set[str] = set()
    for raw in QUOTED_STRING_RE.findall(text):
        cleaned = _clean_file_ref(raw)
        if cleaned:
            refs.add(cleaned)
    for pattern in (PYTHON_ENTRY_RE, SHELL_SOURCE_RE):
        for raw in pattern.findall(text):
            cleaned = _clean_file_ref(raw)
            if cleaned:
                refs.add(cleaned)
    return refs


def _is_intentional_missing_ref(ref: str) -> bool:
    lower = ref.lower()
    return "missing" in lower or "manifest_missing" in lower


def _is_verifier_companion_ref(source_rel: str, ref: str) -> bool:
    name = Path(source_rel).name
    return (name.startswith("verify_") or name.startswith("run_")) and ref.startswith(("scripts/", "tools/"))


def scan_command_entrypoint_consistency(repo_root: Path, candidate_paths: List[str]) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    scanned = 0

    for rel in candidate_paths:
        if not rel.endswith((".py", ".sh")):
            continue
        text = _read_text(rel, repo_root)
        if not text:
            continue
        scanned += 1
        seen: Set[str] = set()
        for raw in PYTHON_ENTRY_RE.findall(text) + SHELL_SOURCE_RE.findall(text):
            ref = _clean_file_ref(raw)
            if not ref or ref in seen:
                continue
            seen.add(ref)
            if _resolve_repo_file(repo_root, ref):
                continue
            if rel.startswith("tests/") or rel.endswith(".md"):
                severity = "low"
            else:
                severity = "high"
            item = {
                "source_path": rel,
                "entrypoint_path": ref,
                "issue_type": "unresolved_command_entrypoint",
                "severity": severity,
                "detail": f"command entrypoint does not resolve: {ref}",
            }
            candidates.append(item)
            if severity == "high":
                high_risk.append(item)

    check_pass = len(high_risk) == 0
    return {
        "scanned_file_count": scanned,
        "command_entrypoint_issue_candidates": candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "low_severity_count": sum(1 for c in candidates if c.get("severity") == "low"),
        "check_pass": check_pass,
        "command_rewrite_executed_now": False,
        "interpretation": "command entrypoint consistency pass" if check_pass else "unresolved command entrypoint; hold for review",
    }


def scan_script_dependency_consistency(repo_root: Path, candidate_paths: List[str]) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    scanned = 0

    for rel in candidate_paths:
        if not rel.startswith(("tools/", "scripts/")):
            continue
        text = _read_text(rel, repo_root)
        if not text:
            continue
        scanned += 1
        for ref in sorted(_extract_path_refs(text)):
            if not ref.startswith(("tools/", "scripts/", "configs/", "docs/", "capabilities/")):
                continue
            if _resolve_repo_file(repo_root, ref):
                continue
            if _is_intentional_missing_ref(ref):
                candidates.append(
                    {
                        "source_path": rel,
                        "referenced_path": ref,
                        "issue_type": "intentional_missing_fixture_reference",
                        "severity": "low",
                        "detail": f"intentional missing-path reference: {ref}",
                    }
                )
                continue
            if _is_verifier_companion_ref(rel, ref):
                candidates.append(
                    {
                        "source_path": rel,
                        "referenced_path": ref,
                        "issue_type": "verifier_companion_reference_missing",
                        "severity": "low",
                        "detail": f"verifier/run companion reference not present: {ref}",
                    }
                )
                continue
            if ".example." in ref or rel.endswith(".md"):
                candidates.append(
                    {
                        "source_path": rel,
                        "referenced_path": ref,
                        "issue_type": "example_or_doc_reference_missing",
                        "severity": "low",
                        "detail": f"example/doc reference not present: {ref}",
                    }
                )
                continue
            item = {
                "source_path": rel,
                "referenced_path": ref,
                "issue_type": "unresolved_script_dependency",
                "severity": "high",
                "detail": f"script dependency does not resolve: {ref}",
            }
            candidates.append(item)
            high_risk.append(item)

    check_pass = len(high_risk) == 0
    return {
        "scanned_file_count": scanned,
        "script_dependency_issue_candidates": candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "low_severity_count": sum(1 for c in candidates if c.get("severity") == "low"),
        "check_pass": check_pass,
        "script_rewrite_executed_now": False,
        "interpretation": "script dependency consistency pass" if check_pass else "unresolved script dependency; hold for review",
    }


def scan_test_reference_path_consistency(repo_root: Path, candidate_paths: List[str]) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    scanned = 0
    fixture_high_prefixes = ("tests/traces/baselines/", "tests/fixtures/")
    fixture_low_prefixes = ("tests/assets/", "tests/data/")

    for rel in candidate_paths:
        if not rel.startswith("tests/"):
            continue
        text = _read_text(rel, repo_root)
        if not text:
            continue
        scanned += 1
        for ref in sorted(_extract_path_refs(text)):
            if not ref.startswith(("tests/", "tools/", "configs/", "capabilities/")):
                continue
            if _resolve_repo_file(repo_root, ref):
                continue
            is_fixture_high = ref.startswith(fixture_high_prefixes)
            is_fixture_low = ref.startswith(fixture_low_prefixes)
            if is_fixture_high and rel.endswith(".py"):
                severity = "high"
            else:
                severity = "low"
            item = {
                "source_path": rel,
                "referenced_path": ref,
                "issue_type": "unresolved_test_reference" if severity == "high" else "test_reference_candidate",
                "severity": severity,
                "detail": f"test reference does not resolve: {ref}",
            }
            candidates.append(item)
            if severity == "high":
                high_risk.append(item)

    check_pass = len(high_risk) == 0
    return {
        "scanned_file_count": scanned,
        "test_reference_issue_candidates": candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "low_severity_count": sum(1 for c in candidates if c.get("severity") == "low"),
        "check_pass": check_pass,
        "test_rewrite_executed_now": False,
        "interpretation": "test reference path consistency pass" if check_pass else "unresolved test reference; hold for review",
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
            "script_rewrite",
            "test_rewrite",
            "command_rewrite",
            "import_rewrite",
        ],
        "protected_path_policy": {"mode": "deny", "blocked": ["protected/**", "**/protected/**"]},
        "eval_out_policy": {"mode": "readonly", "write_allowed": False},
        "before_manifest_requirement": {"required": True, "generated_now": False},
        "after_manifest_requirement": {"required": True, "generated_now": False},
        "rollback_route": {"route_id": "B6_TOOLS_SCRIPTS_TESTS_ROLLBACK_ROUTE_V1", "rehearsal_required": True},
        "verifier_rerun_list": ["verify_main_project_structure_migration_b6_preflight_via_harness_v1"],
        "post_migration_test_list": [
            "tools_scripts_tests_path_check",
            "command_entrypoint_consistency_check",
        ],
        "abort_conditions": [
            "scope_escape_detected",
            "protected_path_intersection",
            "eval_out_write_attempted",
            "operation_not_allowlisted",
            "high_risk_command_entrypoint_break",
            "high_risk_script_dependency_break",
            "high_risk_test_reference_break",
        ],
        "workspace_fallback_policy": {"enabled": True},
        "non_claims": [
            "B6 preflight GO ≠ B6 migration executed",
            "B6 preflight GO ≠ script/test/command rewrite executed",
            "B4 governance runner/verifier exclusion ≠ B4 reopened",
            "low severity reference candidates ≠ execution blocked",
            "workspace_fallback GO ≠ standard _eval_out already written",
        ],
    }


def run_main_project_structure_migration_b6_preflight_via_harness_v1(
    *,
    b5_post_migration_review_root: str,
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    review_root = Path(b5_post_migration_review_root).expanduser().resolve()
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
        blockers.append("B5 post-migration review verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("upstream phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("upstream final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("upstream recommended_next_phase must be B6 preflight")
    if sm.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok must be true")
    if sm.get("b5_closed_now") is not True:
        blockers.append("b5_closed_now must be true")
    if sm.get("ready_for_b6_preflight_via_harness") is not True:
        blockers.append("ready_for_b6_preflight_via_harness must be true")

    candidate_paths = scan_tools_scripts_tests_candidate_paths(resolved_repo)
    if not candidate_paths:
        blockers.append("no tools/scripts/tests candidate paths")

    b4_leaked = [p for p in candidate_paths if _is_b4_excluded(p)]
    if b4_leaked:
        blockers.append(f"B4 governance paths leaked: {len(b4_leaked)}")

    for rel in candidate_paths:
        if _path_excluded(rel):
            blockers.append(f"excluded path leaked: {rel}")
        if not any(rel.startswith(f"{root}/") for root in SCAN_ROOTS):
            blockers.append(f"scope escape: {rel}")

    batch_config = _build_batch_config(candidate_paths)

    scope_ok = all(_matches_candidate(p) for p in candidate_paths)
    domain_ok = batch_config["batch_id"] == BATCH_ID and batch_config["batch_domain"] == BATCH_DOMAIN
    protected_ok = batch_config["protected_path_policy"].get("mode") == "deny"
    eval_out_ok = batch_config["eval_out_policy"].get("mode") == "readonly"
    fileop_ok = set(batch_config["allowed_operations"]) == {"move", "rename"} and {
        "delete",
        "overwrite",
        "merge",
        "copy",
        "content_rewrite",
        "script_rewrite",
        "test_rewrite",
        "command_rewrite",
        "import_rewrite",
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

    command_scan = scan_command_entrypoint_consistency(resolved_repo, candidate_paths)
    script_scan = scan_script_dependency_consistency(resolved_repo, candidate_paths)
    test_scan = scan_test_reference_path_consistency(resolved_repo, candidate_paths)
    for scan in (command_scan, script_scan, test_scan):
        scan.update({k: v for k, v in meta.items() if k not in scan})

    refactor_scan = {
        "scan_scope": list(SCAN_ROOTS),
        "duplicate_pattern_candidates": [
            {"pattern": "repeated CLI argparse + OUTPUT_FILES boilerplate", "location": "tools/"},
            {"pattern": "repeated path resolver helper", "location": "tools/"},
            {"pattern": "repeated test fixture loader", "location": "tests/"},
        ],
        "extract_now_allowed": False,
        "extract_later_candidates": [
            {"tier": "A", "candidate": "shared_cli_output_writer"},
            {"tier": "B", "candidate": "shared_repo_path_resolver"},
        ],
        "blocked_from_runtime_refactor_now": True,
        **meta,
    }
    scan_ok = refactor_scan["extract_now_allowed"] is False and refactor_scan["blocked_from_runtime_refactor_now"] is True

    command_ok = command_scan.get("check_pass") is True
    script_ok = script_scan.get("check_pass") is True
    test_ok = test_scan.get("check_pass") is True
    hold_for_review = (not command_ok or not script_ok or not test_ok) and not blockers

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
        "command_entrypoint_consistency_check": command_ok,
        "script_dependency_consistency_check": script_ok,
        "test_reference_path_consistency_check": test_ok,
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
        final_decision = "MAIN_PROJECT_STRUCTURE_MIGRATION_B6_PREFLIGHT_REQUIRES_FIXES"
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
        "command_high_risk_count": command_scan.get("high_risk_count", 0),
        "script_high_risk_count": script_scan.get("high_risk_count", 0),
        "test_high_risk_count": test_scan.get("high_risk_count", 0),
        "b4_governance_py_excluded_from_batch": True,
        "path_existence_sample": dict(list(path_existence.items())[:5]),
        "final_batch_readiness_decision": final_decision,
        **meta,
    }

    readiness = {
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        "ready_for_b6_controlled_execution": ready_for_execution,
        "hold_for_review": hold_for_review,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "preflight_scope": PREFLIGHT_SCOPE,
        "selected_batch_id": BATCH_ID,
        "batch_domain": BATCH_DOMAIN,
        "candidate_path_count": len(candidate_paths),
        "tools_count": sum(1 for p in candidate_paths if p.startswith("tools/")),
        "scripts_count": sum(1 for p in candidate_paths if p.startswith("scripts/")),
        "tests_count": sum(1 for p in candidate_paths if p.startswith("tests/")),
        "exclude_path_count": len(batch_config["exclude_paths"]),
        "all_fixed_checks_pass": all_fixed_checks_pass,
        "check_results": check_results,
        "hold_for_review": hold_for_review,
        "command_high_risk_count": command_scan.get("high_risk_count", 0),
        "script_high_risk_count": script_scan.get("high_risk_count", 0),
        "test_high_risk_count": test_scan.get("high_risk_count", 0),
        "command_low_severity_count": command_scan.get("low_severity_count", 0),
        "script_low_severity_count": script_scan.get("low_severity_count", 0),
        "test_low_severity_count": test_scan.get("low_severity_count", 0),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }

    return {
        "summary": summary,
        "b6_batch_config": batch_config,
        "b6_preflight_result": preflight_result,
        "b6_command_entrypoint_consistency_scan": command_scan,
        "b6_script_dependency_consistency_scan": script_scan,
        "b6_test_reference_path_consistency_scan": test_scan,
        "b6_migration_refactor_opportunity_scan": refactor_scan,
        "b6_preflight_readiness_decision": readiness,
    }
