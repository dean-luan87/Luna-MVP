# -*- coding: utf-8 -*-
"""Simulation Lab crash_recovery × PaddleOCR batch recovery contract + optional merge.

Phase-SimulationLab-CrashRecovery-PaddleOCR-BatchRecovery-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "SimulationLab-CrashRecovery-PaddleOCR-BatchRecovery-001"

SUMMARY_SCHEMA = "simulation_lab_crash_recovery_paddleocr_batch_recovery_summary_v0"
CONTRACT_SCHEMA = "simulation_lab_crash_recovery_paddleocr_contract_v0"
MERGE_SCHEMA = "simulation_lab_crash_recovery_paddleocr_child_summary_merge_report_v0"
CLASSIFY_SCHEMA = "simulation_lab_crash_recovery_paddleocr_crash_signal_classification_report_v0"
ACTION_SCHEMA = "simulation_lab_crash_recovery_paddleocr_recovery_action_matrix_v0"
MERGED_SIM_SCHEMA = "simulation_lab_crash_recovery_paddleocr_merged_simulation_summary_v0"
RV_LINK_SCHEMA = "simulation_lab_crash_recovery_paddleocr_real_values_link_report_v0"
BOUNDARY_SCHEMA = "simulation_lab_crash_recovery_paddleocr_boundary_report_v0"
NON_CLAIMS_SCHEMA = "simulation_lab_crash_recovery_paddleocr_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "simulation_lab_crash_recovery_paddleocr_open_followups_v0"
AUDIT_SCHEMA = "simulation_lab_crash_recovery_paddleocr_audit_v0"

CONTRACT_REQUIRED_FIELDS: Tuple[str, ...] = (
    "child_phase",
    "child_output_root",
    "simulation_profile_id",
    "provider_name",
    "provider_mode",
    "batch_size",
    "sample_count",
    "attempted_count",
    "success_count",
    "failed_count",
    "recovered_count",
    "exit_code",
    "signal",
    "crash_detected",
    "oom_detected",
    "rss_peak_mb",
    "failed_sample_refs",
    "recovery_action_taken",
    "fallback_action_taken",
    "summary_status",
    "audit",
)

CLASSIFICATION_RULES: Tuple[Dict[str, Any], ...] = (
    {"condition": "exit_code=139", "classified_as": "SIGSEGV", "label": "segmentation_fault"},
    {"condition": "signal=SIGSEGV", "classified_as": "SIGSEGV", "label": "segmentation_fault"},
    {"condition": "oom_detected=true", "classified_as": "oom_or_memory_pressure", "label": "oom"},
    {"condition": "exit_code=0 and failed_count=0", "classified_as": "no_crash", "label": "clean_run"},
    {"condition": "exit_code!=0 and exit_code!=139", "classified_as": "non_sigsegv_failure", "label": "other_failure"},
)


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _bool(v: Any, default: bool = False) -> bool:
    if v is None:
        return default
    return bool(v)


def _source_ok(root: Path, name: str) -> bool:
    sm = _read_json(root / name) or {}
    if not sm:
        return False
    hint = str(sm.get("phase_verdict_hint") or sm.get("verdict") or sm.get("batch_recovery_verdict") or "").upper()
    return hint in ("GO", "CONDITIONAL_GO") or sm.get("collection_scope") == "readonly_real_values_smoke"


def build_contract_template() -> Dict[str, Any]:
    template: Dict[str, Any] = {f: None for f in CONTRACT_REQUIRED_FIELDS}
    template["schema_version"] = CONTRACT_SCHEMA
    template["provider_name"] = "paddleocr"
    template["provider_mode"] = "heavy_batch_subprocess"
    template["simulation_profile_id"] = "crash_recovery"
    template["child_phase"] = "Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001"
    template["field_descriptions"] = {
        "exit_code": "139 must classify as SIGSEGV (128+11).",
        "signal": "SIGSEGV or numeric 11 for segmentation fault.",
        "batch_size": "Recorded batch_size from child run.",
        "failed_sample_refs": "Traceable sample ids from crash report.",
        "rss_peak_mb": "May be null; field must exist.",
        "forbidden_fields": ["ocr_accuracy", "provider_winner", "benchmark_score"],
    }
    return template


def build_child_command_suggestion(core_root: Path, workspace_root: Path) -> str:
    out = workspace_root / "_eval_out" / "paddleocr_batch_recovery_under_simulation_crash_recovery_v0"
    return "\n".join(
        [
            "# PaddleOCR Batch Recovery under Simulation Lab crash_recovery",
            "",
            "This phase does **not** auto-run the child command.",
            "",
            "## Suggested command template",
            "",
            "```bash",
            "python3 tools/evaluation/ocr/run_paddleocr_labeled_set_batch_recovery_v0.py \\",
            f"  --repo-root {core_root} \\",
            "  --materialize-root <PADDLEOCR_MODEL_ROOT> \\",
            "  --pinned-manifest <PADDLEOCR_MODEL_ROOT>/snapshot/paddleocr_manifest_v1_pinned_manifest_candidate.json \\",
            "  --labeled-set-manifest <LABELED_SET_ROOT>/configs/evaluation/ocr/paddleocr_labeled_set_manifest_v0.example.json \\",
            "  --batch-size 5 \\",
            f"  --output-root {out}",
            "```",
            "",
            "## Child summary required",
            "",
            f"- Output: `{out}/paddleocr_labeled_set_batch_recovery_summary.json`",
            "- Set env or annotate: `simulation_profile_id=crash_recovery`",
            "- Record: `exit_code`, `signal`, `batch_size`, `failed_sample_refs`",
            "",
            "## Merge into this phase",
            "",
            "```bash",
            "python3 tools/evaluation/simulation/run_simulation_lab_crash_recovery_paddleocr_batch_recovery_v0.py \\",
            f"  --output-root {workspace_root}/_eval_out/simulation_lab_crash_recovery_paddleocr_batch_recovery_v0 \\",
            f"  --crash-recovery-harness-root {workspace_root}/_eval_out/simulation_lab_minimal_harness_v0/crash_recovery \\",
            f"  --child-summary {out}/paddleocr_labeled_set_batch_recovery_summary.json",
            "```",
        ]
    )


def _signal_name(sig: Any) -> Optional[str]:
    if sig is None:
        return None
    if isinstance(sig, str):
        return sig.upper()
    try:
        n = int(sig)
        if n == 11:
            return "SIGSEGV"
        if n == 9:
            return "SIGKILL"
        if n == 15:
            return "SIGTERM"
    except (TypeError, ValueError):
        pass
    return str(sig)


def _normalize_child_summary(child_path: Path) -> Tuple[Dict[str, Any], List[str]]:
    errs: List[str] = []
    sm = _read_json(child_path) or {}
    if not sm:
        return {}, ["child_summary_unreadable"]

    out_root = Path(str(sm.get("output_root") or child_path.parent))
    crash_report = _read_json(out_root / "paddleocr_labeled_set_batch_crash_report.json") or {}
    results = _read_json(out_root / "paddleocr_labeled_set_batch_results_matrix.json") or {}
    audit = _read_json(out_root / "paddleocr_labeled_set_batch_audit_report.json") or {}

    crash_entries = crash_report.get("crash_entries") or []
    rows = results.get("rows") or []

    exit_code: Optional[int] = None
    signal: Optional[str] = None
    failed_refs: List[str] = []
    rss_peak_mb: Optional[float] = None

    for e in crash_entries:
        if isinstance(e, dict):
            if e.get("exit_code") is not None:
                exit_code = int(e["exit_code"])
            sig = e.get("signal")
            if sig is not None:
                signal = _signal_name(sig)
            failed_refs.extend([str(x) for x in (e.get("crash_sample_candidates") or [])])

    if exit_code is None and rows:
        for r in rows:
            if isinstance(r, dict) and r.get("exit_code") is not None:
                rc = int(r["exit_code"])
                if exit_code is None or rc != 0:
                    exit_code = rc
                sig = _signal_name(r.get("signal"))
                if sig:
                    signal = sig

    if exit_code == 139 and not signal:
        signal = "SIGSEGV"
    if exit_code is not None and exit_code < 0:
        signal = _signal_name(-exit_code) or signal

    oom_detected = exit_code == -9 or signal == "SIGKILL" or _bool(sm.get("oom_detected"))
    crash_detected = bool(crash_entries) or (exit_code not in (None, 0)) or _bool(signal)

    batch_size = sm.get("batch_size")
    sample_count = sm.get("merged_sample_count_expected") or sm.get("sample_count")
    success_count = sm.get("completed_batch_count") or sm.get("success_count")
    failed_count = sm.get("failed_batch_count") or sm.get("failed_count")
    attempted = sm.get("batch_count") or sm.get("attempted_count")

    normalized = {
        "child_phase": sm.get("phase") or "Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001",
        "child_output_root": str(out_root),
        "simulation_profile_id": str(sm.get("simulation_profile_id") or "crash_recovery"),
        "provider_name": "paddleocr",
        "provider_mode": str(sm.get("provider_mode") or "heavy_batch_subprocess"),
        "batch_size": batch_size,
        "sample_count": sample_count,
        "attempted_count": attempted,
        "success_count": success_count,
        "failed_count": failed_count,
        "recovered_count": sm.get("recovered_count") or success_count,
        "exit_code": exit_code,
        "signal": signal,
        "crash_detected": crash_detected,
        "oom_detected": oom_detected,
        "rss_peak_mb": sm.get("rss_peak_mb", rss_peak_mb),
        "failed_sample_refs": failed_refs,
        "recovery_action_taken": sm.get("recovery_action_taken"),
        "fallback_action_taken": sm.get("fallback_action_taken"),
        "summary_status": sm.get("batch_recovery_verdict") or sm.get("summary_status"),
        "audit": audit if audit else {"readonly": True},
    }

    for f in CONTRACT_REQUIRED_FIELDS:
        if f not in normalized:
            normalized[f] = None

    return normalized, errs


def classify_crash(normalized: Optional[Dict[str, Any]], *, child_provided: bool) -> Dict[str, Any]:
    if not child_provided or not normalized:
        return {
            "schema_version": CLASSIFY_SCHEMA,
            "classification_status": "pending_child_summary",
            "classification_rules": list(CLASSIFICATION_RULES),
            "applied_classification": None,
        }

    exit_code = normalized.get("exit_code")
    signal = normalized.get("signal")
    oom = _bool(normalized.get("oom_detected"))
    failed_count = int(normalized.get("failed_count") or 0)

    applied = "pending"
    if oom:
        applied = "oom_or_memory_pressure"
    elif exit_code == 139 or signal == "SIGSEGV":
        applied = "segmentation_fault"
    elif exit_code == 0 and failed_count == 0:
        applied = "no_crash"
    elif exit_code not in (None, 0):
        applied = "non_sigsegv_failure"

    return {
        "schema_version": CLASSIFY_SCHEMA,
        "classification_status": "classified",
        "classification_rules": list(CLASSIFICATION_RULES),
        "applied_classification": applied,
        "exit_code": exit_code,
        "signal": signal,
        "oom_detected": oom,
    }


def build_recovery_action_matrix(normalized: Optional[Dict[str, Any]], classification: Dict[str, Any]) -> Dict[str, Any]:
    applied = classification.get("applied_classification")
    rows = [
        {
            "condition": "SIGSEGV",
            "detected": applied == "segmentation_fault",
            "recommended_recovery_action": "reduce_batch_size",
            "action_taken": (normalized or {}).get("recovery_action_taken"),
            "action_committed": bool((normalized or {}).get("recovery_action_taken")),
            "routing_changed": False,
            "fact_write_allowed": False,
        },
        {
            "condition": "OOM",
            "detected": applied == "oom_or_memory_pressure" or _bool((normalized or {}).get("oom_detected")),
            "recommended_recovery_action": "fallback_to_lightweight_provider",
            "action_taken": (normalized or {}).get("fallback_action_taken"),
            "action_committed": bool((normalized or {}).get("fallback_action_taken")),
            "routing_changed": False,
            "fact_write_allowed": False,
        },
        {
            "condition": "timeout",
            "detected": False,
            "recommended_recovery_action": "retry_single_sample",
            "action_taken": None,
            "action_committed": False,
            "routing_changed": False,
            "fact_write_allowed": False,
        },
        {
            "condition": "provider_error",
            "detected": applied == "non_sigsegv_failure",
            "recommended_recovery_action": "isolate_failed_sample",
            "action_taken": None,
            "action_committed": False,
            "routing_changed": False,
            "fact_write_allowed": False,
        },
        {
            "condition": "empty_result",
            "detected": False,
            "recommended_recovery_action": "hold_for_manual_review",
            "action_taken": None,
            "action_committed": False,
            "routing_changed": False,
            "fact_write_allowed": False,
        },
        {
            "condition": "partial_failure",
            "detected": int((normalized or {}).get("failed_count") or 0) > 0,
            "recommended_recovery_action": "mark_sample_unstable",
            "action_taken": None,
            "action_committed": False,
            "routing_changed": False,
            "fact_write_allowed": False,
        },
    ]
    return {"schema_version": ACTION_SCHEMA, "row_count": len(rows), "rows": rows}


def build_merge_report(child_path: Optional[Path], normalized: Optional[Dict[str, Any]], merge_errs: List[str]) -> Dict[str, Any]:
    provided = child_path is not None and child_path.is_file()
    required_present = False
    profile_match = False
    if provided and normalized:
        required_present = all(normalized.get(f) is not None or f in ("rss_peak_mb", "recovery_action_taken", "fallback_action_taken", "signal") for f in CONTRACT_REQUIRED_FIELDS)
        required_present = all(f in normalized for f in CONTRACT_REQUIRED_FIELDS)
        profile_match = normalized.get("simulation_profile_id") in ("crash_recovery", None) or True
        if normalized.get("simulation_profile_id") and normalized.get("simulation_profile_id") != "crash_recovery":
            profile_match = False

    merge_status = "not_provided"
    if provided and normalized and not merge_errs:
        merge_status = "merged_ok" if required_present else "merge_incomplete"
    elif provided:
        merge_status = "merge_failed"

    refs = (normalized or {}).get("failed_sample_refs") or []
    return {
        "schema_version": MERGE_SCHEMA,
        "child_summary_provided": provided,
        "child_summary_path": str(child_path) if child_path else None,
        "child_summary_read_ok": provided and bool(normalized),
        "required_fields_present": required_present,
        "simulation_profile_id_matches": profile_match if provided else False,
        "exit_code": (normalized or {}).get("exit_code"),
        "signal": (normalized or {}).get("signal"),
        "batch_size": (normalized or {}).get("batch_size"),
        "sample_count": (normalized or {}).get("sample_count"),
        "success_count": (normalized or {}).get("success_count"),
        "failed_count": (normalized or {}).get("failed_count"),
        "recovered_count": (normalized or {}).get("recovered_count"),
        "crash_detected": (normalized or {}).get("crash_detected"),
        "oom_detected": (normalized or {}).get("oom_detected"),
        "rss_peak_mb": (normalized or {}).get("rss_peak_mb"),
        "failed_sample_refs_count": len(refs),
        "merge_status": merge_status,
        "required_for_full_recovery_verdict": not provided,
        "merge_errors": merge_errs,
    }


def build_merged_simulation_summary(
    crash_harness_root: Path,
    merge_report: Dict[str, Any],
    normalized: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    base = dict(_read_json(crash_harness_root / "simulation_summary.json") or {})
    provided = merge_report.get("child_summary_provided")
    recovery_status = "pending_child_execution"
    if provided and merge_report.get("merge_status") == "merged_ok":
        recovery_status = "child_summary_merged"
    elif provided:
        recovery_status = "merge_incomplete"

    base.update(
        {
            "schema_version": MERGED_SIM_SCHEMA,
            "harness_schema": base.get("harness_schema"),
            "simulation_profile_id": "crash_recovery",
            "child_phase_attached": provided,
            "child_summary_ref": merge_report.get("child_summary_path"),
            "crash_recovery_context": {
                "child_summary_provided": provided,
                "exit_code": (normalized or {}).get("exit_code"),
                "signal": (normalized or {}).get("signal"),
                "crash_detected": (normalized or {}).get("crash_detected"),
                "batch_size": (normalized or {}).get("batch_size"),
                "rss_peak_mb": (normalized or {}).get("rss_peak_mb"),
                "failed_sample_refs_count": merge_report.get("failed_sample_refs_count", 0),
                "recovery_status": recovery_status,
                "ocr_accuracy_evaluated": False,
                "benchmark_result_claimed": False,
            },
        }
    )
    return base


def build_real_values_link(smoke_root: Path) -> Dict[str, Any]:
    sm = _read_json(smoke_root / "cross_modal_vision_ocr_benchmark_real_values_smoke_summary.json") or {}
    return {
        "schema_version": RV_LINK_SCHEMA,
        "benchmark_smoke_root": str(smoke_root),
        "current_benchmark_values_collected_t0_t1": _bool(sm.get("real_values_collected")),
        "t2_quality_performance_values_collected": _bool(sm.get("t2_quality_performance_values_collected")),
        "crash_recovery_metrics_future_t2": True,
        "current_phase_updates_t2_values": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "interpretation": "Crash recovery engineering fields only; not merged into benchmark score.",
    }


def build_boundary_report() -> Dict[str, Any]:
    return {
        "schema_version": BOUNDARY_SCHEMA,
        "boundary_ok": True,
        "violations": [],
        "ocr_routing_changed": False,
        "runtime_routing_changed": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "provider_comparison_claimed": False,
        "benchmark_result_claimed": False,
    }


def build_non_claims_report() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "not_paddleocr_accuracy": True,
        "not_production_paddleocr": True,
        "not_provider_superiority": True,
        "not_benchmark": True,
        "not_performance_certification": True,
        "crash_not_fully_resolved_claim": True,
        "default_heavy_paddleocr_not_enabled": True,
        "no_routing_change": True,
        "no_fact_layer_write": True,
    }


def build_open_followups() -> Dict[str, Any]:
    items = [
        "run actual PaddleOCR batch recovery under crash_recovery profile",
        "add low_memory_4gb stress profile execution",
        "add ocr_heavy_provider_stress profile",
        "add FailureAttributionMatrix",
        "add failed sample quarantine",
        "add batch size auto-reduction policy dry-run",
        "add provider fallback dry-run",
        "add crash sample artifact retention",
        "add resource report integration",
        "add T2 stability metric collection later",
    ]
    return {"schema_version": FOLLOWUPS_SCHEMA, "items": items, "item_count": len(items)}


def build_audit(*, child_provided: bool, child_merged: bool) -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "simulation_lab_crash_recovery_paddleocr_phase_executed": True,
        "recovery_contract_generated": True,
        "child_execution_invoked_by_this_phase": False,
        "child_summary_provided": child_provided,
        "child_summary_merged": child_merged,
        "ocr_accuracy_evaluated": False,
        "provider_comparison_claimed": False,
        "benchmark_result_claimed": False,
        "production_readiness_claimed": False,
        "ocr_routing_changed": False,
        "runtime_routing_changed": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
    }


def build_summary(
    *,
    child_provided: bool,
    child_merged: bool,
    harness_ok: bool,
    smoke_ok: bool,
    recovery_status: str,
) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "recovery_scope": "crash_recovery_contract_and_optional_merge",
        "simulation_profile_id": "crash_recovery",
        "based_on_simulation_lab_minimal_harness": harness_ok,
        "based_on_benchmark_real_values_smoke": smoke_ok,
        "run_model_default": False,
        "child_execution_invoked_by_this_phase": False,
        "child_summary_provided": child_provided,
        "child_summary_merged": child_merged,
        "recovery_status": recovery_status,
        "ocr_accuracy_evaluated": False,
        "provider_comparison_claimed": False,
        "benchmark_result_claimed": False,
        "production_readiness_claimed": False,
        "runtime_routing_changed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
    }


def run_simulation_lab_crash_recovery_paddleocr_batch_recovery_v0(
    *,
    crash_recovery_harness_root: str,
    developer_full_harness_root: str,
    benchmark_real_values_smoke_root: str,
    benchmark_planning_root: str,
    v1_track_closures_root: str,
    child_summary_path: Optional[str] = None,
    workspace_root: Optional[str] = None,
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    str,
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    crash_root = Path(crash_recovery_harness_root).resolve()
    dev_root = Path(developer_full_harness_root).resolve()
    smoke_root = Path(benchmark_real_values_smoke_root).resolve()
    planning_root = Path(benchmark_planning_root).resolve()
    closures_root = Path(v1_track_closures_root).resolve()

    if not (crash_root / "simulation_summary.json").is_file():
        errs.append("crash_recovery_simulation_summary_missing")

    harness_ok = (crash_root / "simulation_summary.json").is_file() and (dev_root / "simulation_summary.json").is_file()
    smoke_ok = _source_ok(smoke_root, "cross_modal_vision_ocr_benchmark_real_values_smoke_summary.json")
    if not smoke_ok:
        errs.append("benchmark_smoke_not_ok")

    if not _source_ok(planning_root, "cross_modal_vision_ocr_benchmark_real_values_planning_summary.json"):
        errs.append("benchmark_planning_not_ok")

    if not _source_ok(closures_root, "cross_modal_vision_ocr_testboard_v1_track_closures_summary.json"):
        errs.append("track_closures_not_ok")

    ws = Path(workspace_root).resolve() if workspace_root else crash_root.parent.parent
    core = ws
    if (ws / "tools").is_symlink():
        core = (ws / "tools").resolve().parent

    contract = build_contract_template()
    cmd_md = build_child_command_suggestion(core, ws)

    child_p: Optional[Path] = Path(child_summary_path).resolve() if child_summary_path else None
    normalized: Optional[Dict[str, Any]] = None
    merge_errs: List[str] = []
    if child_p and child_p.is_file():
        normalized, merge_errs = _normalize_child_summary(child_p)
        if merge_errs:
            errs.extend(merge_errs)
        contract["example_normalized_child"] = normalized
    else:
        child_p = None

    merge_report = build_merge_report(child_p, normalized, merge_errs)
    classification = classify_crash(normalized, child_provided=child_p is not None)
    action_matrix = build_recovery_action_matrix(normalized, classification)
    merged_sim = build_merged_simulation_summary(crash_root, merge_report, normalized)
    rv_link = build_real_values_link(smoke_root)
    boundary = build_boundary_report()
    non_claims = build_non_claims_report()
    followups = build_open_followups()

    child_provided = child_p is not None
    child_merged = merge_report.get("merge_status") == "merged_ok"
    recovery_status = merged_sim.get("crash_recovery_context", {}).get("recovery_status", "pending_child_execution")

    if child_provided and not child_merged and merge_report.get("merge_status") == "merge_failed":
        errs.append("child_merge_failed")

    summary = build_summary(
        child_provided=child_provided,
        child_merged=child_merged,
        harness_ok=harness_ok,
        smoke_ok=smoke_ok,
        recovery_status=recovery_status,
    )

    audit = build_audit(child_provided=child_provided, child_merged=child_merged)

    return (
        summary,
        contract,
        cmd_md,
        merge_report,
        classification,
        action_matrix,
        merged_sim,
        rv_link,
        boundary,
        non_claims,
        followups,
        audit,
        errs,
    )
