# -*- coding: utf-8 -*-
"""Main Project Structure Migration B4 Preflight Via Harness v1.

Compressed preflight for Runner / verifier stable placement.
Includes pairing, phase reference, and import consistency scans (read-only).
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B4-Preflight-Via-Harness-v1-001"
PREFLIGHT_SCOPE = "main_project_structure_migration_b4_preflight_via_harness_only"
SOURCE_CHAIN = "main_project_structure_migration_b4_preflight_via_harness_v1"

FINAL_DECISION_GO = "MAIN_PROJECT_STRUCTURE_MIGRATION_B4_PREFLIGHT_VIA_HARNESS_READY_FOR_CONTROLLED_EXECUTION"
NEXT_PHASE_GO = "Phase-Main-Project-Structure-Migration-B4-Controlled-Execution-v1-001"
FINAL_DECISION_HOLD = "MAIN_PROJECT_STRUCTURE_MIGRATION_B4_PREFLIGHT_VIA_HARNESS_HOLD_FOR_REVIEW"
NEXT_PHASE_HOLD = "Phase-Main-Project-Structure-Migration-B4-Preflight-Issue-Review-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-B3-Post-Migration-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_B3_POST_MIGRATION_REVIEW_CLOSED_READY_FOR_B4_PREFLIGHT_VIA_HARNESS"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

BATCH_ID = "B4"
BATCH_DOMAIN = "Runner / verifier stable placement"
GOVERNANCE_TOOLS_ROOT = "tools/evaluation/governance"

EXCLUDE_PATH_PARTS: Tuple[str, ...] = (
    "__pycache__",
    ".pytest_cache",
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
    "runner_verifier_pairing_consistency_check",
    "phase_reference_consistency_check",
    "runner_module_import_consistency_check",
    "readiness_decision",
)

FORBIDDEN_SCOPE_TOKENS: Tuple[str, ...] = (
    "capabilities/",
    "docs/architecture/",
    "configs/",
    "scripts/",
    "tests/",
    "_eval_out",
    "protected/",
    "/hr/",
    "dnae",
)

ALLOWLIST_SHARED_CAPABILITY_IMPORTS: Set[str] = {
    "migration_governance_development_constraints_v1",
}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "b4_preflight_via_harness_only": True,
        "selected_batch_id": BATCH_ID,
        "b4_only": True,
        "b0_closed": True,
        "b1_closed": True,
        "b2_closed": True,
        "b3_closed": True,
        "b5_b7_deferred": True,
        "harness_contract_reused": True,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "arming_chain_reopened_now": False,
        "request_chain_reopened_now": False,
        "b4_preflight_executed_now": True,
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


def scan_runner_verifier_candidate_paths(repo_root: Path) -> List[str]:
    gov_dir = repo_root / GOVERNANCE_TOOLS_ROOT
    if not gov_dir.is_dir():
        return []
    paths: List[str] = []
    for p in sorted(gov_dir.rglob("*.py")):
        rel = str(p.relative_to(repo_root)).replace("\\", "/")
        if _path_excluded(rel):
            continue
        paths.append(rel)
    return paths


def _script_stem(rel: str) -> Optional[str]:
    name = Path(rel).name
    if name.startswith("run_") and name.endswith(".py"):
        return name[len("run_") : -3]
    if name.startswith("verify_") and name.endswith(".py"):
        return name[len("verify_") : -3]
    return None


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


def _import_resolves(repo_root: Path, module: str) -> bool:
    return _module_to_rel_path(repo_root, module) is not None


def _collect_imports(tree: ast.AST) -> List[str]:
    modules: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                continue
            if node.module:
                modules.append(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                modules.append(alias.name)
    return modules


def _extract_capability_imports(src: str) -> List[str]:
    return CAPABILITY_IMPORT_RE.findall(src)


CAPABILITY_IMPORT_RE = re.compile(
    r"from\s+capabilities\.governance\.([a-z0-9_]+)\s+import",
)


def _extract_local_phase_id(src: str) -> Optional[str]:
    m = re.search(
        r'PHASE_ID\s*=\s*(?:\(\s*)?["\']([^"\']+)["\']',
        src,
        re.DOTALL,
    )
    return m.group(1).strip() if m else None


def scan_runner_verifier_pairing_consistency(repo_root: Path, candidate_paths: List[str]) -> Dict[str, Any]:
    run_stems: Dict[str, str] = {}
    verify_stems: Dict[str, str] = {}
    missing_pair_candidates: List[Dict[str, Any]] = []
    naming_mismatch_candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []

    for rel in candidate_paths:
        stem = _script_stem(rel)
        if stem is None:
            continue
        if rel.endswith(f"run_{stem}.py"):
            run_stems[stem] = rel
        elif rel.endswith(f"verify_{stem}.py"):
            verify_stems[stem] = rel

    for stem, run_path in run_stems.items():
        if stem not in verify_stems:
            item = {
                "issue_type": "missing_verify_pair",
                "run_path": run_path,
                "stem": stem,
                "severity": "high",
                "detail": f"run_{stem}.py has no matching verify_{stem}.py",
            }
            missing_pair_candidates.append(item)
            high_risk.append(item)

    for stem, verify_path in verify_stems.items():
        if stem not in run_stems:
            item = {
                "issue_type": "missing_run_pair",
                "verify_path": verify_path,
                "stem": stem,
                "severity": "high",
                "detail": f"verify_{stem}.py has no matching run_{stem}.py",
            }
            missing_pair_candidates.append(item)
            high_risk.append(item)

    for stem in sorted(set(run_stems) & set(verify_stems)):
        if not stem.endswith("_v1") and not stem.endswith("_v0"):
            item = {
                "issue_type": "missing_version_suffix_in_stem",
                "stem": stem,
                "severity": "low",
                "detail": "run/verify stem lacks _vN suffix",
            }
            naming_mismatch_candidates.append(item)

    check_pass = len(high_risk) == 0
    return {
        "run_script_count": len(run_stems),
        "verify_script_count": len(verify_stems),
        "paired_count": len(set(run_stems) & set(verify_stems)),
        "missing_pair_candidates": missing_pair_candidates,
        "naming_mismatch_candidates": naming_mismatch_candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "low_severity_count": len(naming_mismatch_candidates),
        "check_pass": check_pass,
        "module_rename_executed_now": False,
        "interpretation": "runner/verifier pairing pass" if check_pass else "missing run/verify pair detected; hold for review",
    }


def scan_phase_reference_consistency(repo_root: Path, candidate_paths: List[str]) -> Dict[str, Any]:
    phase_reference_issue_candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []

    for rel in candidate_paths:
        stem = _script_stem(rel)
        if stem is None:
            continue
        p = repo_root / rel
        try:
            src = p.read_text(encoding="utf-8")
        except OSError as exc:
            item = {"path": rel, "issue_type": "read_error", "severity": "high", "detail": str(exc)}
            phase_reference_issue_candidates.append(item)
            high_risk.append(item)
            continue

        all_cap_imports = _extract_capability_imports(src)
        primary_cap_imports = [m for m in all_cap_imports if m not in ALLOWLIST_SHARED_CAPABILITY_IMPORTS]
        stem_import_present = stem in all_cap_imports
        local_phase_id = _extract_local_phase_id(src)
        is_run = rel.endswith(f"run_{stem}.py")
        is_verify = rel.endswith(f"verify_{stem}.py")

        if is_run and not stem_import_present:
            item = {
                "path": rel,
                "issue_type": "missing_primary_capability_import",
                "expected_module": stem,
                "severity": "high",
                "detail": f"run_{stem}.py must import capabilities.governance.{stem}",
            }
            phase_reference_issue_candidates.append(item)
            high_risk.append(item)

        if is_verify and not stem_import_present and not local_phase_id:
            item = {
                "path": rel,
                "issue_type": "missing_phase_reference",
                "expected_module": stem,
                "severity": "high",
                "detail": f"verify_{stem}.py lacks capability import and local PHASE_ID",
            }
            phase_reference_issue_candidates.append(item)
            high_risk.append(item)

        for cap_mod in primary_cap_imports:
            if cap_mod != stem:
                item = {
                    "path": rel,
                    "issue_type": "auxiliary_capability_import",
                    "imported_module": cap_mod,
                    "script_stem": stem,
                    "severity": "low",
                    "detail": f"auxiliary capabilities.governance.{cap_mod} import alongside primary stem {stem}",
                }
                phase_reference_issue_candidates.append(item)

        if stem_import_present and local_phase_id:
            cap_path = repo_root / "capabilities" / "governance" / f"{stem}.py"
            if cap_path.is_file():
                try:
                    cap_phase = _extract_local_phase_id(cap_path.read_text(encoding="utf-8"))
                    if cap_phase and cap_phase != local_phase_id:
                        item = {
                            "path": rel,
                            "issue_type": "local_vs_capability_phase_id_drift",
                            "local_phase_id": local_phase_id,
                            "capability_phase_id": cap_phase,
                            "severity": "low",
                            "detail": "local PHASE_ID differs from imported capability PHASE_ID",
                        }
                        phase_reference_issue_candidates.append(item)
                except OSError:
                    pass
        elif local_phase_id:
            token = stem.replace("_", "-").upper()
            if token not in local_phase_id.upper().replace("_", "-"):
                item = {
                    "path": rel,
                    "issue_type": "local_phase_id_stem_drift",
                    "phase_id": local_phase_id,
                    "script_stem": stem,
                    "severity": "low",
                    "detail": "local PHASE_ID token drift from script stem",
                }
                phase_reference_issue_candidates.append(item)
        elif stem_import_present:
            cap_path = repo_root / "capabilities" / "governance" / f"{stem}.py"
            if cap_path.is_file():
                try:
                    cap_phase = _extract_local_phase_id(cap_path.read_text(encoding="utf-8"))
                    if cap_phase:
                        token = stem.replace("_", "-").upper()
                        if token not in cap_phase.upper().replace("_", "-"):
                            item = {
                                "path": rel,
                                "issue_type": "capability_phase_id_stem_drift",
                                "capability_phase_id": cap_phase,
                                "script_stem": stem,
                                "severity": "low",
                                "detail": "imported capability PHASE_ID token drift from script stem",
                            }
                            phase_reference_issue_candidates.append(item)
                except OSError:
                    pass

    check_pass = len(high_risk) == 0
    return {
        "scanned_script_count": sum(1 for p in candidate_paths if _script_stem(p)),
        "phase_reference_issue_candidates": phase_reference_issue_candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "low_severity_count": sum(1 for c in phase_reference_issue_candidates if c.get("severity") == "low"),
        "check_pass": check_pass,
        "content_rewrite_executed_now": False,
        "interpretation": "phase reference consistency pass" if check_pass else "high risk phase reference issue detected; hold for review",
    }


def scan_runner_module_import_consistency(repo_root: Path, candidate_paths: List[str]) -> Dict[str, Any]:
    import_path_issue_candidates: List[Dict[str, Any]] = []
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
            item = {"path": rel, "issue_type": "parse_error", "severity": "high", "detail": str(exc)}
            import_path_issue_candidates.append(item)
            high_risk.append(item)
            continue

        for mod in _collect_imports(tree):
            if mod.startswith(("capabilities.", "tools.")):
                if not _import_resolves(repo_root, mod):
                    item = {
                        "path": rel,
                        "issue_type": "unresolved_import",
                        "import_module": mod,
                        "severity": "high",
                        "detail": f"import does not resolve: {mod}",
                    }
                    import_path_issue_candidates.append(item)
                    high_risk.append(item)

    check_pass = len(high_risk) == 0
    return {
        "scanned_file_count": scanned,
        "import_path_issue_candidates": import_path_issue_candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "check_pass": check_pass,
        "import_rewrite_executed_now": False,
        "module_move_executed_now": False,
        "interpretation": "runner module import consistency pass" if check_pass else "high risk unresolved import detected; hold for review",
    }


def _build_batch_config(candidate_paths: List[str]) -> Dict[str, Any]:
    return {
        "batch_id": BATCH_ID,
        "batch_domain": BATCH_DOMAIN,
        "candidate_paths": candidate_paths,
        "exclude_paths": list(EXCLUDE_GLOBS),
        "allowed_operations": ["move", "rename"],
        "blocked_operations": ["delete", "overwrite", "merge", "copy", "content_rewrite", "import_rewrite"],
        "protected_path_policy": {"mode": "deny", "blocked": ["protected/**", "**/protected/**"]},
        "eval_out_policy": {"mode": "readonly", "write_allowed": False},
        "before_manifest_requirement": {"required": True, "generated_now": False},
        "after_manifest_requirement": {"required": True, "generated_now": False},
        "rollback_route": {"route_id": "B4_RUNNER_VERIFIER_ROLLBACK_ROUTE_V1", "rehearsal_required": True},
        "verifier_rerun_list": ["verify_main_project_structure_migration_b4_preflight_via_harness_v1"],
        "post_migration_test_list": ["runner_verifier_path_check", "runner_verifier_pairing_check"],
        "abort_conditions": [
            "scope_escape_detected",
            "protected_path_intersection",
            "eval_out_write_attempted",
            "operation_not_allowlisted",
            "high_risk_pairing_break",
            "high_risk_phase_reference_break",
            "high_risk_unresolved_import",
        ],
        "workspace_fallback_policy": {"enabled": True},
        "non_claims": [
            "B4 preflight GO ≠ B4 migration executed",
            "B4 preflight GO ≠ import rewrite executed",
            "pairing/naming scan pass ≠ files renamed in preflight",
            "low severity phase reference candidates ≠ execution blocked",
            "workspace_fallback GO ≠ standard _eval_out already written",
        ],
    }


def run_main_project_structure_migration_b4_preflight_via_harness_v1(
    *,
    b3_post_migration_review_root: str,
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    review_root = Path(b3_post_migration_review_root).expanduser().resolve()
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
        blockers.append("B3 post-migration review verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("upstream phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("upstream final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("upstream recommended_next_phase must be B4 preflight")
    if sm.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok must be true")
    if sm.get("b3_closed_now") is not True:
        blockers.append("b3_closed_now must be true")
    if sm.get("ready_for_b4_preflight_via_harness") is not True:
        blockers.append("ready_for_b4_preflight_via_harness must be true")

    candidate_paths = scan_runner_verifier_candidate_paths(resolved_repo)
    if not candidate_paths:
        blockers.append("no runner/verifier candidate paths after exclusions")

    for rel in candidate_paths:
        if _path_excluded(rel):
            blockers.append(f"excluded path leaked into candidates: {rel}")
        if not rel.startswith(f"{GOVERNANCE_TOOLS_ROOT}/") or not rel.endswith(".py"):
            blockers.append(f"scope escape: {rel}")

    batch_config = _build_batch_config(candidate_paths)

    scope_ok = all(
        p.startswith(f"{GOVERNANCE_TOOLS_ROOT}/") and p.endswith(".py") and not _path_excluded(p)
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

    pairing_scan = scan_runner_verifier_pairing_consistency(resolved_repo, candidate_paths)
    phase_scan = scan_phase_reference_consistency(resolved_repo, candidate_paths)
    import_scan = scan_runner_module_import_consistency(resolved_repo, candidate_paths)

    for scan in (pairing_scan, phase_scan, import_scan):
        scan.update({k: v for k, v in meta.items() if k not in scan})

    refactor_scan = {
        "scan_scope": [GOVERNANCE_TOOLS_ROOT],
        "duplicate_pattern_candidates": [
            {"pattern": "run/verify argparse + OUTPUT_FILES boilerplate", "location": GOVERNANCE_TOOLS_ROOT},
            {"pattern": "verifier meta inflation loop", "location": GOVERNANCE_TOOLS_ROOT},
            {"pattern": "phase table update helper", "location": "docs/architecture/evaluation"},
        ],
        "extract_now_allowed": False,
        "extract_later_candidates": [
            {"tier": "A", "candidate": "shared_run_verify_output_writer"},
            {"tier": "B", "candidate": "shared_verifier_meta_inflation_helper"},
        ],
        "blocked_from_runtime_refactor_now": True,
        **meta,
    }
    scan_ok = refactor_scan["extract_now_allowed"] is False and refactor_scan["blocked_from_runtime_refactor_now"] is True

    pairing_ok = pairing_scan.get("check_pass") is True
    phase_ok = phase_scan.get("check_pass") is True
    import_ok = import_scan.get("check_pass") is True
    hold_for_review = (not pairing_ok or not phase_ok or not import_ok) and not blockers

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
        "runner_verifier_pairing_consistency_check": pairing_ok,
        "phase_reference_consistency_check": phase_ok,
        "runner_module_import_consistency_check": import_ok,
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
        final_decision = "MAIN_PROJECT_STRUCTURE_MIGRATION_B4_PREFLIGHT_REQUIRES_FIXES"
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
        "pairing_high_risk_count": pairing_scan.get("high_risk_count", 0),
        "phase_reference_high_risk_count": phase_scan.get("high_risk_count", 0),
        "import_high_risk_count": import_scan.get("high_risk_count", 0),
        "path_existence_sample": dict(list(path_existence.items())[:5]),
        "final_batch_readiness_decision": final_decision,
        **meta,
    }

    readiness = {
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        "ready_for_b4_controlled_execution": ready_for_execution,
        "hold_for_review": hold_for_review,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "preflight_scope": PREFLIGHT_SCOPE,
        "selected_batch_id": BATCH_ID,
        "batch_domain": BATCH_DOMAIN,
        "candidate_path_count": len(candidate_paths),
        "run_script_count": pairing_scan.get("run_script_count", 0),
        "verify_script_count": pairing_scan.get("verify_script_count", 0),
        "paired_count": pairing_scan.get("paired_count", 0),
        "exclude_path_count": len(batch_config["exclude_paths"]),
        "all_fixed_checks_pass": all_fixed_checks_pass,
        "check_results": check_results,
        "hold_for_review": hold_for_review,
        "pairing_high_risk_count": pairing_scan.get("high_risk_count", 0),
        "phase_reference_high_risk_count": phase_scan.get("high_risk_count", 0),
        "import_high_risk_count": import_scan.get("high_risk_count", 0),
        "pairing_low_severity_count": pairing_scan.get("low_severity_count", 0),
        "phase_reference_low_severity_count": phase_scan.get("low_severity_count", 0),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }

    return {
        "summary": summary,
        "b4_batch_config": batch_config,
        "b4_preflight_result": preflight_result,
        "b4_runner_verifier_pairing_consistency_scan": pairing_scan,
        "b4_phase_reference_consistency_scan": phase_scan,
        "b4_runner_module_import_consistency_scan": import_scan,
        "b4_migration_refactor_opportunity_scan": refactor_scan,
        "b4_preflight_readiness_decision": readiness,
    }
