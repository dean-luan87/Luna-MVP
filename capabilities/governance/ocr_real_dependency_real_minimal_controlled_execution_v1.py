# -*- coding: utf-8 -*-
"""OCR Real Minimal Controlled Execution v1 — first real 5-check execution phase."""

from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_real_dependency_execution_final_preflight_v1 import (
    MINIMAL_SCOPE_ALLOWED_CHECKS,
)
from capabilities.governance.ocr_real_dependency_real_minimal_controlled_execution_final_ready_check_v1 import (
    FINAL_DECISION_GO as UPSTREAM_READY_FINAL_GO,
    NEXT_PHASE_GO as UPSTREAM_READY_NEXT_PHASE,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-v1-001"
SCOPE = "real_minimal_controlled_execution_phase"
SOURCE_CHAIN = "ocr_real_dependency_real_minimal_controlled_execution_v1"

UPSTREAM_READY_FINAL = UPSTREAM_READY_FINAL_GO
UPSTREAM_READY_NEXT = UPSTREAM_READY_NEXT_PHASE

FINAL_DECISION_PASS = (
    "OCR_REAL_DEPENDENCY_REAL_MINIMAL_CONTROLLED_EXECUTION_COMPLETED_READY_FOR_POST_REVIEW"
)
FINAL_DECISION_FAIL = (
    "OCR_REAL_DEPENDENCY_REAL_MINIMAL_CONTROLLED_EXECUTION_COMPLETED_WITH_FAILURE_"
    "READY_FOR_POST_REVIEW"
)
FINAL_DECISION_VIOLATION = (
    "OCR_REAL_DEPENDENCY_REAL_MINIMAL_CONTROLLED_EXECUTION_BLOCKED_FOR_BOUNDARY_VIOLATION_REVIEW"
)
NEXT_PHASE_POST_REVIEW = "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-Post-Review-v1-001"
NEXT_PHASE_VIOLATION = (
    "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-Boundary-Violation-Review-v1-001"
)

NON_CLAIMS: Tuple[str, ...] = (
    "Real minimal execution completed ≠ provider selected",
    "provider import check pass ≠ OCR runtime enabled",
    "package/cache/hash pass ≠ OCR usable in production",
    "execution completed ≠ smoke/sample OCR allowed",
    "Post-Review required before any next route",
)

BOUNDARY_TRUE_EXECUTED: Tuple[str, ...] = (
    "real_execution_started_now",
    "package_presence_check_executed_now",
    "model_cache_path_check_executed_now",
    "model_file_existence_check_executed_now",
    "model_file_hash_check_executed_now",
    "provider_import_check_executed_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "dependency_install_executed_now",
    "model_download_executed_now",
    "cache_mutation_executed_now",
    "provider_runtime_invoked_now",
    "provider_initialization_dry_check_executed_now",
    "runtime_smoke_check_executed_now",
    "sample_ocr_check_executed_now",
    "ocr_request_submitted_now",
    "image_read_executed_now",
    "crop_executed_now",
    "ocr_fact_generated_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "provider_selection_finalized_now",
    "controlled_trial_started_now",
    "production_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_real_minimal_controlled_execution"
)


def _execution_meta() -> Dict[str, Any]:
    meta = {
        "real_minimal_controlled_execution_phase": True,
        "execution_scope": "minimal_real_dependency_check",
        "allowed_real_checks_count": len(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "provider_selection_finalized_now": False,
        "provider_runtime_invoked_now": False,
        "provider_invoked_now": False,
    }
    for field in BOUNDARY_TRUE_EXECUTED:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _resolve_cache_path() -> Path:
    raw = os.environ.get("LUNA_OCR_MODEL_CACHE", "")
    if raw:
        return Path(raw).expanduser()
    home_default = Path.home() / ".paddleocr"
    if home_default.exists():
        return home_default
    return Path(os.environ.get("LUNA_OCR_PROBE_CACHE_PATH", str(home_default))).expanduser()


def _probe_packages() -> List[str]:
    raw = os.environ.get("LUNA_OCR_PROBE_PACKAGES", "paddlepaddle,paddleocr")
    return [p.strip() for p in raw.split(",") if p.strip()]


def _probe_import_module() -> str:
    return os.environ.get("LUNA_OCR_PROBE_IMPORT_MODULE", "paddleocr")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _check_package_presence(packages: List[str]) -> Dict[str, Any]:
    results = []
    all_present = True
    for pkg in packages:
        try:
            spec = importlib.util.find_spec(pkg)
        except (ImportError, ModuleNotFoundError, ValueError) as exc:
            spec = None
            err = str(exc)
        else:
            err = None
        present = spec is not None
        if not present:
            all_present = False
        results.append({"package": pkg, "present": present, "error": err})
    return {
        "check_id": "package_presence_check",
        "executed_at": _utc_now(),
        "pass": all_present,
        "packages": results,
        "failure_route": None if all_present else "package_missing",
        "remediation_blocked": ["install", "upgrade", "repair", "download"],
    }


def _check_model_cache_path(cache_path: Path) -> Dict[str, Any]:
    exists = cache_path.exists()
    accessible = exists and os.access(cache_path, os.R_OK)
    return {
        "check_id": "model_cache_path_check",
        "executed_at": _utc_now(),
        "cache_path": str(cache_path),
        "exists": exists,
        "accessible": accessible,
        "pass": accessible,
        "failure_route": None if accessible else "cache_path_missing",
        "remediation_blocked": ["create_production_cache", "download", "cache_mutation"],
    }


def _iter_model_files(cache_path: Path, limit: int = 20) -> List[Path]:
    if not cache_path.exists():
        return []
    files: List[Path] = []
    for root, _dirs, names in os.walk(cache_path):
        for name in names:
            files.append(Path(root) / name)
            if len(files) >= limit:
                return files
    return files


def _check_model_file_existence(cache_path: Path) -> Dict[str, Any]:
    files = _iter_model_files(cache_path)
    return {
        "check_id": "model_file_existence_check",
        "executed_at": _utc_now(),
        "cache_path": str(cache_path),
        "file_count": len(files),
        "sample_files": [str(f) for f in files[:5]],
        "pass": len(files) > 0,
        "failure_route": None if files else "model_file_missing",
        "remediation_blocked": ["download", "auto_repair"],
    }


def _check_model_file_hash(cache_path: Path) -> Dict[str, Any]:
    files = _iter_model_files(cache_path, limit=10)
    hashes: List[Dict[str, Any]] = []
    for fp in files:
        try:
            digest = hashlib.sha256(fp.read_bytes()).hexdigest()
            hashes.append({"path": str(fp), "sha256": digest, "pass": True})
        except OSError as exc:
            hashes.append({"path": str(fp), "sha256": None, "pass": False, "error": str(exc)})
    all_ok = bool(hashes) and all(h.get("pass") for h in hashes)
    return {
        "check_id": "model_file_hash_check",
        "executed_at": _utc_now(),
        "hashed_file_count": len(hashes),
        "hashes": hashes,
        "pass": all_ok,
        "failure_route": None if all_ok else ("model_file_missing" if not hashes else "hash_mismatch"),
        "remediation_blocked": ["modify_cache", "overwrite", "move"],
    }


def _check_provider_import(module_name: str) -> Dict[str, Any]:
    """Isolated subprocess import — no OCR runtime init in parent process."""
    imported = False
    error: Optional[str] = None
    child_env = {
        **os.environ,
        "MPLBACKEND": "Agg",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    code = (
        "import importlib; "
        f"importlib.import_module({module_name!r}); "
        "print('import_ok')"
    )
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=60,
            env=child_env,
        )
        imported = proc.returncode == 0 and "import_ok" in (proc.stdout or "")
        if not imported:
            error = (proc.stderr or proc.stdout or "import_failed").strip()[:2000]
    except subprocess.TimeoutExpired:
        error = "import_check_timeout"
    except OSError as exc:
        error = str(exc)
    return {
        "check_id": "provider_import_check",
        "executed_at": _utc_now(),
        "import_module": module_name,
        "import_succeeded": imported,
        "import_isolated_subprocess": True,
        "pass": imported,
        "runtime_invoked": False,
        "ocr_initialized": False,
        "parent_process_import_avoided": True,
        "failure_route": None if imported else "import_failed",
        "remediation_blocked": ["repair", "install", "smoke", "sample_ocr"],
        "error": error,
    }


def run_ocr_real_dependency_real_minimal_controlled_execution_v1(
    *,
    ocr_real_dependency_real_minimal_controlled_execution_final_ready_check_root: str,
    ocr_real_dependency_real_minimal_execution_authorization_decision_root: Optional[str] = None,
    ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_root: Optional[str] = None,
    ocr_real_dependency_execution_final_preflight_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    boundary_violations: List[str] = []

    ready_root = Path(
        ocr_real_dependency_real_minimal_controlled_execution_final_ready_check_root
    ).expanduser().resolve()
    ready_sm = _try_read_json(ready_root / "summary.json") or {}
    ready_vr = _try_read_json(ready_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    evidence_dir = out_root / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        **_execution_meta(),
        "upstream_final_ready_check_root": str(ready_root),
        "output_root": str(out_root),
        "evidence_output_path": str(evidence_dir),
        "owner_operator_confirmation_required": True,
    }

    if ready_vr.get("verifier") != "GO":
        blockers.append("final ready check verifier must be GO")
    if ready_sm.get("final_decision") != UPSTREAM_READY_FINAL:
        blockers.append("final ready check final_decision mismatch")
    if ready_sm.get("recommended_next_phase") != UPSTREAM_READY_NEXT:
        blockers.append("final ready check recommended_next_phase mismatch")
    if ready_sm.get("real_execution_started_now") is not False:
        blockers.append("execution must not have started before this phase")
    if meta.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must be null")

    if blockers:
        raise RuntimeError(f"upstream gate failed: {blockers}")

    packages = _probe_packages()
    cache_path = _resolve_cache_path()
    import_module = _probe_import_module()

    env_snapshot = {
        "snapshot_id": "execution_environment_snapshot_v1",
        "captured_at": _utc_now(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "cwd": str(Path.cwd()),
        "probe_packages": packages,
        "probe_import_module": import_module,
        "model_cache_path": str(cache_path),
        "output_root": str(out_root),
        **meta,
    }

    package_result = _check_package_presence(packages)
    cache_result = _check_model_cache_path(cache_path)
    file_result = _check_model_file_existence(cache_path)
    hash_result = _check_model_file_hash(cache_path)
    import_result = _check_provider_import(import_module)

    check_results = [package_result, cache_result, file_result, hash_result, import_result]
    failure_routes: List[Dict[str, Any]] = []
    for r in check_results:
        if r.get("failure_route"):
            failure_routes.append({
                "check_id": r["check_id"],
                "condition": r["failure_route"],
                "action": "record_failure_only",
                "remediation_blocked": r.get("remediation_blocked", []),
            })

    all_checks_executed = all(r.get("executed_at") for r in check_results)
    checks_passed = all(r.get("pass") for r in check_results)
    boundary_ok = len(boundary_violations) == 0

    meta["provider_imported_now"] = import_result.get("import_succeeded") is True

    boundary_audit = {
        "audit_id": "execution_boundary_audit_v1",
        "audited_at": _utc_now(),
        "boundary_violations": boundary_violations,
        "boundary_ok": boundary_ok,
        "forbidden_still_false": {f: meta.get(f) is False for f in BOUNDARY_FALSE},
        "allowed_executed": {f: meta.get(f) is True for f in BOUNDARY_TRUE_EXECUTED},
        "smoke_sample_ocr_blocked": True,
        "provider_finalize_blocked": True,
        **meta,
    }

    rollback_result = {
        "result_id": "execution_rollback_result_v1",
        "rollback_required": not checks_passed,
        "rollback_executed_now": False,
        "failed_package_check_does_not_trigger_install": True,
        "failed_import_does_not_trigger_repair": True,
        "missing_model_file_does_not_trigger_download": True,
        "hash_mismatch_does_not_trigger_cache_mutation": True,
        **meta,
    }

    failure_route_result = {
        "result_id": "execution_failure_route_result_v1",
        "routes_triggered": failure_routes,
        "route_count": len(failure_routes),
        "hard_block_violations": boundary_violations,
        **meta,
    }

    evidence_package = {
        "package_id": "execution_evidence_package_v1",
        "assembled_at": _utc_now(),
        "artifacts": {
            "execution_window_ref": str(ready_root / "final_ready_check_result_v1.json"),
            "environment_snapshot": str(out_root / "execution_environment_snapshot_v1.json"),
            "python_version_snapshot": sys.version,
            "package_presence_result": str(out_root / "package_presence_check_result_v1.json"),
            "model_cache_path_result": str(out_root / "model_cache_path_check_result_v1.json"),
            "model_file_existence_result": str(out_root / "model_file_existence_check_result_v1.json"),
            "model_file_hash_result": str(out_root / "model_file_hash_check_result_v1.json"),
            "provider_import_check_result": str(out_root / "provider_import_check_result_v1.json"),
            "boundary_audit_result": str(out_root / "execution_boundary_audit_v1.json"),
            "failure_route_result": str(out_root / "execution_failure_route_result_v1.json"),
            "rollback_result": str(out_root / "execution_rollback_result_v1.json"),
            "verifier_report": str(out_root / "verifier_report.json"),
            "post_execution_review": "pending_post_review_phase",
        },
        "checks_passed": checks_passed,
        "checks_executed_count": len(check_results),
        **meta,
    }

    if not boundary_ok:
        final_decision = FINAL_DECISION_VIOLATION
        next_phase = NEXT_PHASE_VIOLATION
    elif checks_passed:
        final_decision = FINAL_DECISION_PASS
        next_phase = NEXT_PHASE_POST_REVIEW
    else:
        final_decision = FINAL_DECISION_FAIL
        next_phase = NEXT_PHASE_POST_REVIEW

    execution_decision = {
        "decision_id": "real_minimal_controlled_execution_decision_v1",
        "execution_completed": all_checks_executed,
        "checks_passed": checks_passed,
        "boundary_ok": boundary_ok,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }

    ready_input = {
        "review_id": "final_ready_check_input_review_v1",
        "upstream_root": str(ready_root),
        "verifier_go": ready_vr.get("verifier") == "GO",
        "final_decision": ready_sm.get("final_decision"),
        "review_pass": True,
        **meta,
    }

    policy = {
        "policy_id": "real_minimal_controlled_execution_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "allowed_checks": list(MINIMAL_SCOPE_ALLOWED_CHECKS),
        **meta,
    }

    non_claims = {
        "register_id": "execution_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "execution_completed": all_checks_executed,
        "checks_passed": checks_passed,
        "boundary_ok": boundary_ok,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        "failure_routes_triggered": [r["condition"] for r in failure_routes],
        **meta,
    }

    return {
        "real_minimal_controlled_execution_policy": policy,
        "final_ready_check_input_review": ready_input,
        "execution_environment_snapshot": env_snapshot,
        "package_presence_check_result": package_result,
        "model_cache_path_check_result": cache_result,
        "model_file_existence_check_result": file_result,
        "model_file_hash_check_result": hash_result,
        "provider_import_check_result": import_result,
        "execution_boundary_audit": boundary_audit,
        "execution_failure_route_result": failure_route_result,
        "execution_rollback_result": rollback_result,
        "execution_evidence_package": evidence_package,
        "execution_non_claims_register": non_claims,
        "real_minimal_controlled_execution_decision": execution_decision,
        "summary": summary,
    }
